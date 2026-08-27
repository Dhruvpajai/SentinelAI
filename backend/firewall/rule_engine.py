"""
Rule-based prompt evaluation engine.

Matches normalized prompts against defined security rules.
"""

from backend.firewall.interfaces import IRuleEngine
from backend.firewall.models import RuleMatch


class RuleEngine(IRuleEngine):
    """Evaluates normalized prompts against security rules."""

    def evaluate(self, normalized_prompt: str) -> list[RuleMatch]:
        """
        Run rule checks against a normalized prompt.

        Args:
            normalized_prompt: Preprocessed prompt text.

        Returns:
            List of rules that matched the prompt.
        """
        # TODO: Implement rule evaluation logic
        ...
