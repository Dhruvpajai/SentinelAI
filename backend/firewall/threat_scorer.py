"""
Threat scoring for matched security rules.

Computes risk scores and severity levels from rule match results.
"""

from backend.firewall.interfaces import IThreatScorer
from backend.firewall.models import RuleMatch, Severity


class ThreatScorer(IThreatScorer):
    """Computes risk scores and severity from rule match results."""

    def score(
        self,
        normalized_prompt: str,
        matched_rules: list[RuleMatch],
    ) -> tuple[float, Severity]:
        """
        Compute a risk score and severity from rule match results.

        Args:
            normalized_prompt: Preprocessed prompt text.
            matched_rules: Rules that matched during evaluation.

        Returns:
            Tuple of (risk_score, severity).
        """
        # TODO: Implement threat scoring logic
        ...
