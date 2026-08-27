"""FastAPI dependency providers for request-scoped services."""

from fastapi import Request

from backend.firewall.analyzer import PromptAnalyzer
from backend.firewall.interfaces import IPromptAnalyzer
from backend.firewall.normalizer import PromptNormalizer
from backend.firewall.rule_engine import RuleEngine
from backend.firewall.threat_scorer import ThreatScorer


def build_prompt_analyzer() -> PromptAnalyzer:
    """Compose the default prompt analysis pipeline."""
    return PromptAnalyzer(
        normalizer=PromptNormalizer(),
        rule_engine=RuleEngine(),
        threat_scorer=ThreatScorer(),
    )


def get_prompt_analyzer(request: Request) -> IPromptAnalyzer:
    """
    Return the application-scoped prompt analyzer.

    The instance is stored on app.state by the application factory so routes
    do not construct or cache pipeline components themselves.
    """
    analyzer = getattr(request.app.state, "prompt_analyzer", None)
    if analyzer is None:
        analyzer = build_prompt_analyzer()
        request.app.state.prompt_analyzer = analyzer
    return analyzer
