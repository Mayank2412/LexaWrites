import json
import os
import time
import markdown
from google import genai
from google.genai.errors import APIError
from weasyprint import HTML
from verifier import DeterministicVerifier

class ProgrammaticBookPipeline:
    def __init__(self, state_file):
        with open(state_file, 'r') as f:
            self.state = json.load(f)
        self.volume_id = self.state["metadata"]["volume_id"]
        self.verifier = DeterministicVerifier(self.state)
        self.client = genai.Client(api_key=os.environ["LEXAWRITES"])
        
        # Read the model choice dynamically from the workflow dropdown selection
        self.model_name = os.getenv("MODEL_NAME", "gemini-3.8-flash")
        print(f"Initializing pipeline execution using model: {self.model_name}")

        self.cache_dir = "build/chapters"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.raw_chapters = {}

    def generate_chapter(self, chapter_spec):
        ch_num = chapter_spec["chapter_num"]
        cache_path = os.path.join(self.cache_dir, f"ch_{ch_num}.md")

        if os.path.exists(cache_path):
            print(f"Loading verified Chapter {ch_num} from cache...")
            with open(cache_path, "r") as f:
                return f.read()

        print(f"Executing Generation for Chapter {ch_num}: {chapter_spec['title']} using {self.model_name}...")
        error_feedback = ""

        for attempt in range(1, 5):
            try:
                prompt = f"""
                You are a deterministic technical documentarian. You are strictly bound by this Pipeline State Object:
                <state_object>
                {json.dumps(self.state, indent=2)}
                </state_object>

                CHAPTER ASSIGNMENT:
                - Chapter Number: {ch_num}
                - Chapter Title: {chapter_spec['title']}
                - Operational Focus: {chapter_spec['focus']}

                CRITICAL RULES:
                1. Start with the exact heading: ### Chapter {ch_num}: {chapter_spec['title']}
                2. Write at least 800 words in a purely declarative, active engineering voice.
                3. Include at least one Markdown table illustrating the metrics for this chapter.
                4. You are explicitly banned from using these words: {self.state['thematic_guardrails']['banned_adjectives']}.
                {error_feedback}
                """

                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                draft = response.text

                is_valid, errors = self.verifier.verify_segment(draft)
                if is_valid:
                    with open(cache_path, "w") as f:
                        f.write(draft)
                    print(f"Chapter {ch_num} passed verification on attempt {attempt}.")
                    # Pace requests to respect free-tier RPM limits across newer models
                    time.sleep(10)
                    return draft
                else:
                    print(f"Chapter {ch_num} failed verification attempt {attempt}: {errors}")
                    error_feedback = "\nPREVIOUS ATTEMPT FAILED VERIFICATION. FIX THESE EXACT ERRORS:\n" + "\n".join(errors)

            except APIError as e:
                print(f"API Error on Chapter {ch_num} (Attempt {attempt}/4): {e}")
                if attempt == 4:
                    raise e
                sleep_time = 15 * attempt
                print(f"Backing off for {sleep_time} seconds due to rate limit/service load...")
                time.sleep(sleep_time)

        raise RuntimeError(f"Chapter {ch_num} failed generation after max attempts.")

    def run_pipeline(self):
        ordered_keys = []
        for ch_spec in self.state["chapters"]:
            key = f"ch{ch_spec['chapter_num']}"
            self.raw_chapters[key] = self.generate_chapter(ch_spec)
            ordered_keys.append(key)

        full_markdown = "\n\n".join([self.raw_chapters[k] for k in ordered_keys])
        self.compile_typesetting(full_markdown)

    def compile_typesetting(self, full_markdown):
        """Converts raw Markdown into an Amazon KDP print-compliant 6x9 PDF."""
        print("Initializing WeasyPrint Typesetting Engine...")
        html_content = markdown.markdown(full_markdown, extensions=['tables', 'fenced_code'])
        meta = self.state["metadata"]

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
                body {{ font-family: 'Georgia', serif; font-size: 10.5pt; line-height: 1.55; color: #111111; text-align: justify; }}
                .front-matter {{ page-break-after: always; text-align: center; padding-top: 2.5in; }}
                .copyright-page {{ page-break-after: always; padding-top: 5in; font-size: 8.5pt; text-align: left; }}
                h3 {{ font-family: 'Arial', sans-serif; font-size: 14pt; border-bottom: 1px solid #333; padding-bottom: 4px; break-before: page; text-align: left; }}
                table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 9pt; break-inside: avoid; }}
                th, td {{ border: 1px solid #444; padding: 6px 8px; text-align: left; }}
                th {{ background-color: #f0f0f0; font-family: 'Arial', sans-serif; }}
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
        HTML(string=styled_html).write_pdf(f"output_v{self.volume_id}.pdf")
        print("Print-Ready PDF compiled successfully.")

if __name__ == "__main__":
    state_path = os.getenv("STATE_FILE", "volume_state.json")
    pipeline = ProgrammaticBookPipeline(state_path)
    pipeline.run_pipeline()
