"""
Abstract interfaces for the prompt analysis engine.

Defines contracts that concrete implementations must fulfill, enabling
dependency inversion and swap-friendly components.
"""

from abc import ABC, abstractmethod

from backend.firewall.models import (
    PromptAnalysisRequest,
    PromptAnalysisResult,
    RuleMatch,
    Severity,
)


class IPromptNormalizer(ABC):
    """Contract for normalizing raw prompt text before analysis."""

    @abstractmethod
    def normalize(self, prompt: str) -> str:
        """
        Normalize a raw prompt for consistent downstream evaluation.

        Args:
            prompt: The original user prompt.

        Returns:
            Normalized prompt string.
        """
        ...


class IRuleEngine(ABC):
    """Contract for evaluating prompts against security rules."""

    @abstractmethod
    def evaluate(self, normalized_prompt: str) -> list[RuleMatch]:
        """
        Run rule checks against a normalized prompt.

        Args:
            normalized_prompt: Preprocessed prompt text.

        Returns:
            List of rules that matched the prompt.
        """
        ...


class IThreatScorer(ABC):
    """Contract for computing risk scores and severity from rule matches."""

    @abstractmethod
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
        ...


class IPromptAnalyzer(ABC):
    """Contract for the top-level prompt analysis orchestrator."""

    @abstractmethod
    def analyze(self, request: PromptAnalysisRequest) -> PromptAnalysisResult:
        """
        Run the full prompt analysis pipeline.

        Args:
            request: Analysis input containing the raw prompt.

        Returns:
            Complete analysis result with decision metadata.
        """
        ...
