"""
Prompt text normalization for the analysis pipeline.

Prepares raw user input for consistent rule evaluation.
"""

from backend.firewall.interfaces import IPromptNormalizer


class PromptNormalizer(IPromptNormalizer):
    """Normalizes raw prompt text before rule evaluation."""

    def normalize(self, prompt: str) -> str:
        """
        Normalize a raw prompt for consistent downstream evaluation.

        Args:
            prompt: The original user prompt.

        Returns:
            Normalized prompt string.
        """
        # TODO: Implement prompt normalization (whitespace, encoding, etc.)
        ...
