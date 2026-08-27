"""
Prompt analysis orchestrator.

Coordinates normalization, rule evaluation, and threat scoring into a
single analysis pipeline.
"""

from backend.firewall.interfaces import (
    IPromptAnalyzer,
    IPromptNormalizer,
    IRuleEngine,
    IThreatScorer,
)
from backend.firewall.models import PromptAnalysisRequest, PromptAnalysisResult


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
    ) -> None:
        """
        Initialize the analyzer with its pipeline dependencies.

        Args:
            normalizer: Component for prompt text normalization.
            rule_engine: Component for rule-based evaluation.
            threat_scorer: Component for risk scoring and severity.
        """
        self._normalizer = normalizer
        self._rule_engine = rule_engine
        self._threat_scorer = threat_scorer

    def analyze(self, request: PromptAnalysisRequest) -> PromptAnalysisResult:
        """
        Run the full prompt analysis pipeline.

        Args:
            request: Analysis input containing the raw prompt.

        Returns:
            Complete analysis result with decision metadata.
        """
        # TODO: Orchestrate normalize → evaluate → score → decide
        ...
