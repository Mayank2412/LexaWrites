import json
import os
import shutil
import subprocess
import time
import markdown
import pydyf
from google import genai
from google.genai.errors import APIError

# Compatibility shim in case pip cache retains WeasyPrint 62.x with pydyf >= 0.11.0
if not hasattr(pydyf.Stream, "transform") and hasattr(pydyf.Stream, "set_matrix"):
    pydyf.Stream.transform = pydyf.Stream.set_matrix
if not hasattr(pydyf.Stream, "text_matrix") and hasattr(pydyf.Stream, "set_text_matrix"):
    pydyf.Stream.text_matrix = pydyf.Stream.set_text_matrix

from weasyprint import HTML
from verifier import DeterministicVerifier


class ProgrammaticBookPipeline:
    def __init__(self, state_file):
        # 1. Setup isolated 'temp_generations' transient cache directory
        self.run_dir = "temp_generations"
        os.makedirs(self.run_dir, exist_ok=True)

        with open(state_file, "r", encoding="utf-8") as f:
            incoming_state = json.load(f)

        # Determine local state path inside run directory
        self.local_state_path = os.path.join(self.run_dir, "volume_state.json")

        if os.path.exists(self.local_state_path):
            with open(self.local_state_path, "r", encoding="utf-8") as f:
                cached_state = json.load(f)
            if cached_state.get("metadata", {}).get("volume_id") != incoming_state.get("metadata", {}).get("volume_id"):
                print("New volume_id detected. Clearing stale temp_generations/ cache...")
                shutil.rmtree(self.run_dir, ignore_errors=True)
                os.makedirs(self.run_dir, exist_ok=True)

        if not os.path.exists(self.local_state_path):
            self.state = incoming_state
            self._write_state_to_cache()
            print(f"Initialized fresh run directory in {self.run_dir}/ with {state_file}")
            self._sync_cache_to_git(f"Initialize volume_state.json in {self.run_dir}/")
        else:
            print(f"Resuming run from existing state inside {self.run_dir}/")
            with open(self.local_state_path, "r", encoding="utf-8") as f:
                self.state = json.load(f)

        self.volume_id = self.state["metadata"]["volume_id"]
        self.verifier = DeterministicVerifier(self.state)
        self.client = genai.Client(api_key=os.environ["LEXAWRITES"])

        # Deduplicated model pool for 503/429/404 auto-switching fallback order
        default_pool = [
            os.getenv("MODEL_NAME", "gemini-3.8-flash"),
            "gemini-3.6-flash",
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
            "gemini-3-flash",
            "gemini-2.5-flash",
        ]
        self.model_pool = list(dict.fromkeys(default_pool))

        self.raw_chapters = {}

    def _write_file_atomic(self, path, content):
        """Writes and immediately flushes content to disk inside temp_generations."""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

    def _write_state_to_cache(self):
        """Persists the current volume_state.json into temp_generations immediately."""
        state_json = json.dumps(self.state, indent=2)
        self._write_file_atomic(self.local_state_path, state_json)

    def _sync_cache_to_git(self, commit_message, extra_path=None):
        """Commits and pushes specified paths incrementally in CI."""
        if os.getenv("GITHUB_ACTIONS") != "true":
            return
        try:
            subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=False)
            subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=False)

            paths_to_add = [self.run_dir]
            if extra_path:
                paths_to_add.append(extra_path)

            subprocess.run(["git", "add"] + paths_to_add, check=False)
            diff = subprocess.run(["git", "diff", "--staged", "--quiet"], check=False)
            if diff.returncode != 0:
                subprocess.run(["git", "commit", "-m", commit_message], check=False)
                subprocess.run(["git", "pull", "--rebase"], check=False)
                subprocess.run(["git", "push"], check=False)
                print(f"Synced paths {paths_to_add} to repository: {commit_message}")
        except Exception as e:
            print(f"Incremental git sync warning (non-fatal): {e}")

    def generate_chapter(self, chapter_spec):
        ch_num = chapter_spec["chapter_num"]
        chapter_filename = f"ch_{ch_num}.md"
        cache_path = os.path.join(self.run_dir, chapter_filename)

        # 2. Check if chapter is already generated in temp_generations (Smart Resume)
        if os.path.exists(cache_path):
            print(f"Resuming: Loading already generated Chapter {ch_num} from {self.run_dir}/...")
            with open(cache_path, "r", encoding="utf-8") as f:
                cached_draft = f.read()
            if chapter_spec.get("status") != "verified":
                chapter_spec["status"] = "verified"
                chapter_spec["cache_file"] = chapter_filename
                self._write_state_to_cache()
            return cached_draft

        print(f"Executing Generation for Chapter {ch_num}: {chapter_spec['title']}...")
        error_feedback = ""

        # Auto-switch logic across model pool on capacity/availability errors
        for current_model in self.model_pool:
            print(f"Attempting generation with model tier: {current_model}")

            for attempt in range(1, 4):
                try:
                    prompt = f"""
                    You are a senior systems architect and subject-matter author writing a concise, high-signal technical explainer chapter.
                    Use the reference dataset below as your factual anchor:
                    <reference_data>
                    {json.dumps(self.state, indent=2)}
                    </reference_data>

                    CHAPTER BRIEF:
                    - Chapter {ch_num}: {chapter_spec['title']}
                    - Core Topic: {chapter_spec['focus']}

                    WRITING & FORMATTING RULES:
                    1. HEADING: Begin immediately with: ### Chapter {ch_num}: {chapter_spec['title']}
                    2. VOICE & CLARITY: Write 350 to 500 words of sharp, natural, human-grade non-fiction prose. Explain *why* the mechanics work in the real world, including engineering trade-offs, physical bottlenecks, and failure modes.
                    3. NO AI SLOP OR JARGON STUFFING:
                       - NEVER print JSON variable keys in prose (e.g., write "daily grain ration", NEVER write "C_daily" or "pack_mule_capacity_kg").
                       - NEVER mention the Volume ID or state object in the text.
                       - NEVER spell out decimal numbers in words (write "0.84 kg", NEVER "zero point eight four kilograms").
                       - NEVER narrate elementary arithmetic (do not write "Multiplying X by Y yields Z"). State the operational insight directly.
                    4. STRICT BAN ON LATEX: Do NOT use `$`, `$$`, `\\text`, `\\times`, or any LaTeX syntax. Use standard plain-text symbols and HTML/Unicode units (e.g., km/h, m², °C, kW).
                    5. CLEAN COMPACT TABLE: Include exactly one Markdown table (maximum 4 columns, concise headers) that summarizes the key benchmarks for this chapter.
                    6. BANNED WORDS: Do not use any of these words: {self.state['thematic_guardrails']['banned_adjectives']}.
                    {error_feedback}
                    """

                    response = self.client.models.generate_content(
                        model=current_model,
                        contents=prompt,
                    )
                    draft = (response.text or "").strip()
                    if draft.startswith("```"):
                        draft = draft.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

                    is_valid, errors = self.verifier.verify_segment(draft)
                    if is_valid:
                        self._write_file_atomic(cache_path, draft)
                        chapter_spec["status"] = "verified"
                        chapter_spec["verified_model"] = current_model
                        chapter_spec["cache_file"] = chapter_filename
                        self._write_state_to_cache()

                        print(f"Chapter {ch_num} passed verification using {current_model}. Saved to {cache_path}.")
                        self._sync_cache_to_git(
                            f"Cache verified Chapter {ch_num} ({self.volume_id}) in {self.run_dir}/"
                        )
                        time.sleep(8)
                        return draft
                    else:
                        print(f"Chapter {ch_num} failed verification attempt {attempt}: {errors}")
                        error_feedback = "\nPREVIOUS ATTEMPT FAILED VERIFICATION. FIX THESE EXACT ERRORS:\n" + "\n".join(errors)

                except APIError as e:
                    print(f"API Error ({e.code if hasattr(e, 'code') else 'Unknown'}) on {current_model}: {e}")
                    if any(code in str(e) for code in ("503", "429", "404", "UNAVAILABLE", "NOT_FOUND")):
                        print(f"Capacity/availability block encountered on {current_model}. Triggering auto-switch to next model in pool...")
                        break

                    if attempt == 3:
                        raise e
                    time.sleep(10 * attempt)

        raise RuntimeError(f"Chapter {ch_num} failed generation across all models in pool due to capacity limits.")

    def run_pipeline(self):
        ordered_keys = []
        for ch_spec in self.state["chapters"]:
            key = f"ch{ch_spec['chapter_num']}"
            self.raw_chapters[key] = self.generate_chapter(ch_spec)
            ordered_keys.append(key)

        full_markdown = "\n\n".join([self.raw_chapters[k] for k in ordered_keys])
        self.compile_typesetting(full_markdown)

    def compile_typesetting(self, full_markdown):
        """Converts raw Markdown into an Amazon KDP print-compliant 6x9 PDF and commits it to output/."""
        print("Initializing WeasyPrint Typesetting Engine...")
        html_content = markdown.markdown(full_markdown, extensions=["tables", "fenced_code"])
        meta = self.state["metadata"]

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        pdf_filename = os.path.join(output_dir, f"output_v{self.volume_id}.pdf")

        styled_html = f"""
        <html>
        <head>
            <style>
                @page {{
                    size: 6in 9in;
                    margin-top: 0.75in;
                    margin-bottom: 0.75in;
                }}
                @page :left {{
                    margin-left: 0.5in;
                    margin-right: 0.75in;
                    @bottom-left {{ content: counter(page); font-family: 'Georgia', serif; font-size: 9pt; }}
                }}
                @page :right {{
                    margin-left: 0.75in;
                    margin-right: 0.5in;
                    @bottom-right {{ content: counter(page); font-family: 'Georgia', serif; font-size: 9pt; }}
                }}
                @page :first {{
                    @bottom-left {{ content: none; }}
                    @bottom-right {{ content: none; }}
                }}
                body {{ font-family: 'Georgia', serif; font-size: 10.5pt; line-height: 1.55; color: #111111; text-align: left; }}
                .front-matter {{ page-break-after: always; text-align: center; padding-top: 2.5in; }}
                .copyright-page {{ page-break-after: always; padding-top: 5in; font-size: 8.5pt; text-align: left; }}
                h3 {{ font-family: 'Arial', sans-serif; font-size: 13pt; border-bottom: 1px solid #333; padding-bottom: 4px; break-before: page; text-align: left; }}
                table {{ width: 100%; table-layout: fixed; border-collapse: collapse; margin: 16px 0; font-size: 8.5pt; break-inside: avoid; word-wrap: break-word; }}
                th, td {{ border: 1px solid #444; padding: 6px; text-align: left; vertical-align: top; }}
                th {{ background-color: #f0f0f0; font-family: 'Arial', sans-serif; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="front-matter">
                <h1 style="font-family: 'Arial', sans-serif; font-size: 20pt; margin-bottom: 8px;">{meta['title']}</h1>
                <p style="font-size: 12pt; color: #444;">{meta['subtitle']}</p>
                <p style="margin-top: 2in; font-size: 11pt;"><strong>{meta['author']}</strong></p>
            </div>
            <div class="copyright-page">
                <p><strong>{meta['title']}</strong></p>
                <p>Volume ID: {meta['volume_id']} | Pillar: {meta['pillar']}</p>
                <p>All rights reserved. Deterministic compilation minted via LexaWrites Pipeline.</p>
            </div>
            {html_content}
        </body>
        </html>
        """
        HTML(string=styled_html).write_pdf(pdf_filename)
        print(f"Print-Ready PDF compiled successfully as {pdf_filename}.")
        self._sync_cache_to_git(f"Add compiled PDF {pdf_filename}", extra_path=output_dir)


if __name__ == "__main__":
    state_path = os.getenv("STATE_FILE", "volume_state.json")
    pipeline = ProgrammaticBookPipeline(state_path)
    pipeline.run_pipeline()
