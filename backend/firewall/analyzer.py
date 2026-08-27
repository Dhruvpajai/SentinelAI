"""
Prompt analysis orchestrator.

Coordinates normalization, rule evaluation, and threat scoring into a
single analysis pipeline.
"""

from dataclasses import dataclass, field
from typing import Mapping

from backend.firewall.interfaces import (
    IPromptAnalyzer,
    IPromptNormalizer,
    IRuleEngine,
    IThreatScorer,
)
from backend.firewall.models import (
    Decision,
    PromptAnalysisRequest,
    PromptAnalysisResult,
    Severity,
)

DEFAULT_DECISIONS_BY_SEVERITY: dict[Severity, Decision] = {
    Severity.NONE: Decision.ALLOW,
    Severity.LOW: Decision.ALLOW,
    Severity.MEDIUM: Decision.REVIEW,
    Severity.HIGH: Decision.BLOCK,
    Severity.CRITICAL: Decision.BLOCK,
}


@dataclass(frozen=True)
class DecisionPolicy:
    """
    Configurable mapping from derived severity to a firewall decision.

    Default policy:
        LOW → allow
        MEDIUM → review
        HIGH → block
        CRITICAL → block
    """

    decisions_by_severity: Mapping[Severity, Decision] = field(
        default_factory=lambda: dict(DEFAULT_DECISIONS_BY_SEVERITY)
    )


class PromptAnalyzer(IPromptAnalyzer):
    """
    Orchestrates the prompt analysis pipeline.

    Depends on abstractions for each pipeline stage, enabling dependency
    injection and independent testing of components.
    """

    def __init__(
        self,
        normalizer: IPromptNormalizer,
        rule_engine: IRuleEngine,
        threat_scorer: IThreatScorer,
        decision_policy: DecisionPolicy | None = None,
    ) -> None:
        """
        Initialize the analyzer with its pipeline dependencies.

        Args:
            normalizer: Component for prompt text normalization.
            rule_engine: Component for rule-based evaluation.
            threat_scorer: Component for risk scoring and severity.
            decision_policy: Mapping from severity to allow/review/block.
        """
        self._normalizer = normalizer
        self._rule_engine = rule_engine
        self._threat_scorer = threat_scorer
        self._decision_policy = decision_policy or DecisionPolicy()

    def analyze(self, request: PromptAnalysisRequest) -> PromptAnalysisResult:
        """
        Run the full prompt analysis pipeline.

        Args:
            request: Analysis input containing the raw prompt.

        Returns:
            Complete analysis result with decision metadata.
        """
        original_prompt = request.prompt
        normalized_prompt = self._normalizer.normalize(original_prompt)
        matched_rules = self._rule_engine.evaluate(normalized_prompt)
        risk_score, severity = self._threat_scorer.score(
            normalized_prompt,
            matched_rules,
        )
        decision = self._decision_policy.decisions_by_severity.get(
            severity,
            Decision.REVIEW,
        )
        return PromptAnalysisResult(
            original_prompt=original_prompt,
            normalized_prompt=normalized_prompt,
            matched_rules=matched_rules,
            severity=severity,
            risk_score=risk_score,
            decision=decision,
        )
