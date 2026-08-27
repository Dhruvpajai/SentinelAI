"""
Threat scoring for matched security rules.

Computes risk scores and severity levels from rule match results.
"""

from dataclasses import dataclass, field
from typing import Mapping

from backend.firewall.interfaces import IThreatScorer
from backend.firewall.models import RuleMatch, Severity

DEFAULT_SEVERITY_POINTS: dict[Severity, float] = {
    Severity.NONE: 0.0,
    Severity.LOW: 15.0,
    Severity.MEDIUM: 30.0,
    Severity.HIGH: 50.0,
    Severity.CRITICAL: 80.0,
}


@dataclass(frozen=True)
class ScoringPolicy:
    """
    Configurable mapping from rule matches to a capped risk score.

    Default severity points:
        NONE: 0, LOW: 15, MEDIUM: 30, HIGH: 50, CRITICAL: 80

    Default derived-severity bands (inclusive of the lower bound):
        0–24: LOW, 25–49: MEDIUM, 50–74: HIGH, 75–100: CRITICAL
    """

    points_by_severity: Mapping[Severity, float] = field(
        default_factory=lambda: dict(DEFAULT_SEVERITY_POINTS)
    )
    medium_threshold: float = 25.0
    high_threshold: float = 50.0
    critical_threshold: float = 75.0
    max_score: float = 100.0

    def __post_init__(self) -> None:
        if self.max_score <= 0:
            raise ValueError("max_score must be greater than 0.")
        if not (
            0
            <= self.medium_threshold
            <= self.high_threshold
            <= self.critical_threshold
            <= self.max_score
        ):
            raise ValueError(
                "Thresholds must satisfy "
                "0 <= medium <= high <= critical <= max_score."
            )
        for severity, points in self.points_by_severity.items():
            if points < 0:
                raise ValueError(f"Points for {severity} must be non-negative.")


class ThreatScorer(IThreatScorer):
    """Computes a deterministic risk score and severity from rule matches."""

    def __init__(self, policy: ScoringPolicy | None = None) -> None:
        """
        Initialize the scorer with an optional scoring policy.

        Args:
            policy: Point values and severity thresholds. Defaults to the
                built-in scoring policy.
        """
        self._policy = policy or ScoringPolicy()

    def score(
        self,
        normalized_prompt: str,
        matched_rules: list[RuleMatch],
    ) -> tuple[float, Severity]:
        """
        Compute a risk score and severity from rule match results.

        Scoring is based only on matched-rule severities. The prompt text is
        accepted to satisfy the analyzer pipeline contract and is not used
        in the score calculation. No allow/review/block decision is made.

        Args:
            normalized_prompt: Preprocessed prompt text.
            matched_rules: Rules that matched during evaluation.

        Returns:
            Tuple of (risk_score, severity). Empty matches yield (0.0, LOW).
        """
        del normalized_prompt
        policy = self._policy

        if not matched_rules:
            return 0.0, Severity.LOW

        total = sum(
            policy.points_by_severity.get(match.severity, 0.0)
            for match in matched_rules
        )
        risk_score = min(total, policy.max_score)
        return risk_score, self._severity_for_score(risk_score)

    def _severity_for_score(self, risk_score: float) -> Severity:
        policy = self._policy
        if risk_score >= policy.critical_threshold:
            return Severity.CRITICAL
        if risk_score >= policy.high_threshold:
            return Severity.HIGH
        if risk_score >= policy.medium_threshold:
            return Severity.MEDIUM
        return Severity.LOW
