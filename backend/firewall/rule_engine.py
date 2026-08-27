"""
Rule-based prompt evaluation engine.

Matches normalized prompts against defined security rules.
"""

from collections.abc import Sequence

from backend.firewall.interfaces import IRuleEngine
from backend.firewall.models import RuleMatch
from backend.firewall.rules import SecurityRule, get_default_security_rules


class RuleEngine(IRuleEngine):
    """Evaluates normalized prompts against configurable security rules."""

    def __init__(self, rules: Sequence[SecurityRule] | None = None) -> None:
        """
        Initialize the engine with an optional custom rule set.

        Args:
            rules: Security rules to evaluate. Defaults to the built-in catalog.
        """
        self._rules: tuple[SecurityRule, ...] = (
            tuple(rules) if rules is not None else get_default_security_rules()
        )

    def evaluate(self, normalized_prompt: str) -> list[RuleMatch]:
        """
        Run rule checks against a normalized prompt.

        Performs case-insensitive phrase matching and returns one structured
        match per triggered rule. Scoring and final decisions are handled
        elsewhere in the pipeline.

        Args:
            normalized_prompt: Preprocessed prompt text.

        Returns:
            List of rules that matched the prompt.
        """
        if not normalized_prompt:
            return []

        text = normalized_prompt.casefold()
        matches: list[RuleMatch] = []

        for rule in self._rules:
            if any(pattern.search(text) for pattern in rule.patterns):
                matches.append(
                    RuleMatch(
                        rule_id=rule.rule_id,
                        rule_name=rule.rule_name,
                        description=rule.description,
                        category=rule.category,
                        severity=rule.severity,
                    )
                )

        return matches
