"""
Prompt text normalization for the analysis pipeline.

Prepares raw user input for consistent rule evaluation.
"""

import re

from backend.firewall.interfaces import IPromptNormalizer

_WHITESPACE_RUN = re.compile(r"\s+")


class PromptNormalizer(IPromptNormalizer):
    """Normalizes raw prompt text before rule evaluation."""

    def normalize(self, prompt: str) -> str:
        """
        Normalize a raw prompt for consistent downstream evaluation.

        Strips outer whitespace, collapses internal whitespace runs to a
        single space, and lowercases the text. Punctuation and word content
        are preserved unchanged aside from case normalization.

        Args:
            prompt: The original user prompt.

        Returns:
            Normalized prompt string, or an empty string for blank input.
        """
        text = prompt.strip()
        text = _WHITESPACE_RUN.sub(" ", text)
        return text.lower()
