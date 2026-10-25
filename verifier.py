import re

class DeterministicVerifier:
    def __init__(self, state):
        self.state = state
        self.banned_words = [w.lower() for w in state["thematic_guardrails"]["banned_adjectives"]]
        self.require_table = state["thematic_guardrails"]["require_markdown_table"]
        self.allowed_numbers = self._extract_allowed_numbers(state)

    def _extract_allowed_numbers(self, obj):
        """Recursively extracts all valid numeric literals from the state JSON."""
        allowed = set()
        if isinstance(obj, dict):
            for v in obj.values():
                allowed.update(self._extract_allowed_numbers(v))
        elif isinstance(obj, list):
            for item in obj:
                allowed.update(self._extract_allowed_numbers(item))
        elif isinstance(obj, (int, float)):
            allowed.add(float(obj))
        return allowed

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

        # 3. Numeric Ground-Truth Audit
        found_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', markdown_text)
        for num_str in found_numbers:
            val = float(num_str)
            if val not in self.allowed_numbers:
                errors.append(f"Unverified numeric value '{num_str}' not present in volume_state.json.")

        return (len(errors) == 0), errors
