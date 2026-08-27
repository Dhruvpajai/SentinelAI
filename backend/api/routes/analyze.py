"""Prompt analysis endpoint."""

from fastapi import APIRouter, Depends

from backend.api.dependencies import get_prompt_analyzer
from backend.api.schemas.analyze import (
    AnalyzeRequest,
    AnalyzeResponse,
    RuleMatchResponse,
)
from backend.firewall.interfaces import IPromptAnalyzer
from backend.firewall.models import PromptAnalysisRequest

router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze a prompt",
)
async def analyze_prompt(
    payload: AnalyzeRequest,
    analyzer: IPromptAnalyzer = Depends(get_prompt_analyzer),
) -> AnalyzeResponse:
    """Run the prompt firewall pipeline and return the analysis result."""
    result = analyzer.analyze(PromptAnalysisRequest(prompt=payload.prompt))
    return AnalyzeResponse(
        original_prompt=result.original_prompt,
        normalized_prompt=result.normalized_prompt,
        matched_rules=[
            RuleMatchResponse(
                rule_id=match.rule_id,
                rule_name=match.rule_name,
                description=match.description,
                category=match.category,
                severity=match.severity,
            )
            for match in result.matched_rules
        ],
        severity=result.severity,
        risk_score=result.risk_score,
        decision=result.decision,
    )
