"""
Domain models for the prompt analysis engine.

Defines request/result data structures and shared value types used across
the firewall pipeline.
"""

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    """Threat severity level derived from analysis."""

    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(str, Enum):
    """Final action taken on a prompt after analysis."""

    ALLOW = "allow"
    BLOCK = "block"
    REVIEW = "review"


@dataclass(frozen=True)
class PromptAnalysisRequest:
    """Input payload for prompt analysis."""

    prompt: str


@dataclass(frozen=True)
class RuleMatch:
    """A single rule that matched during evaluation."""

    rule_id: str
    rule_name: str
    description: str


@dataclass(frozen=True)
class PromptAnalysisResult:
    """Complete outcome of analyzing a prompt through the firewall pipeline."""

    original_prompt: str
    normalized_prompt: str
    matched_rules: list[RuleMatch] = field(default_factory=list)
    severity: Severity = Severity.NONE
    risk_score: float = 0.0
    decision: Decision = Decision.ALLOW
