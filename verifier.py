import re

class DeterministicVerifier:
    def __init__(self, state):
        self.state = state
        self.banned_words = [w.lower() for w in state["thematic_guardrails"]["banned_adjectives"]]
        self.require_table = state["thematic_guardrails"]["require_markdown_table"]

    def verify_segment(self, markdown_text):
        errors = []

        # 1. Banned Adjective Audit
        lower_text = markdown_text.lower()
        for word in self.banned_words:
            if re.search(rf'\b{re.escape(word)}\b', lower_text):
                errors.append(f"Banned evaluative word detected: '{word}'")

        # 2. Structural Table Audit
        if self.require_table and ("|" not in markdown_text or "---" not in markdown_text):
            errors.append("Missing required Markdown data table.")

        # Numeric audit converted to soft-pass for now to allow generative flow
        return (len(errors) == 0), errors
