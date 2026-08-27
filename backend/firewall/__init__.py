"""
Prompt and response firewall module.

Provides the prompt analysis engine foundation for detecting malicious
input before it reaches an LLM.
"""

from backend.firewall.analyzer import DecisionPolicy, PromptAnalyzer
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
    RuleMatch,
    Severity,
)
from backend.firewall.normalizer import PromptNormalizer
from backend.firewall.rule_engine import RuleEngine
from backend.firewall.threat_scorer import ThreatScorer

__all__ = [
    "Decision",
    "DecisionPolicy",
    "IPromptAnalyzer",
    "IPromptNormalizer",
    "IRuleEngine",
    "IThreatScorer",
    "PromptAnalysisRequest",
    "PromptAnalysisResult",
    "PromptAnalyzer",
    "PromptNormalizer",
    "RuleEngine",
    "RuleMatch",
    "Severity",
    "ThreatScorer",
]
