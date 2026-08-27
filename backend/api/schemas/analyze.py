"""Prompt analysis request and response schemas."""

from pydantic import BaseModel, Field

from backend.firewall.models import Decision, Severity


class AnalyzeRequest(BaseModel):
    """Incoming prompt to analyze."""

    prompt: str = Field(..., description="Raw prompt text to evaluate.")


class RuleMatchResponse(BaseModel):
    """A security rule that matched the prompt."""

    rule_id: str
    rule_name: str
    description: str
    category: str
    severity: Severity


class AnalyzeResponse(BaseModel):
    """Firewall analysis outcome for a prompt."""

    original_prompt: str
    normalized_prompt: str
    matched_rules: list[RuleMatchResponse]
    severity: Severity
    risk_score: float
    decision: Decision
