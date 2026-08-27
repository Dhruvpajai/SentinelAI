"""Unit tests for ThreatScorer."""

import unittest

from backend.firewall.models import RuleMatch, Severity
from backend.firewall.threat_scorer import ScoringPolicy, ThreatScorer


def _match(rule_id: str, severity: Severity) -> RuleMatch:
    return RuleMatch(
        rule_id=rule_id,
        rule_name=rule_id,
        description="test match",
        category="TEST",
        severity=severity,
    )


class TestThreatScorer(unittest.TestCase):
    """Tests for deterministic risk scoring from rule matches."""

    def setUp(self) -> None:
        self.scorer = ThreatScorer()

    def test_no_matches(self) -> None:
        score, severity = self.scorer.score("hello world", [])

        self.assertEqual(score, 0.0)
        self.assertEqual(severity, Severity.LOW)

    def test_one_low_match(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [_match("LOW-001", Severity.LOW)],
        )

        self.assertEqual(score, 15.0)
        self.assertEqual(severity, Severity.LOW)

    def test_one_medium_match(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [_match("MED-001", Severity.MEDIUM)],
        )

        self.assertEqual(score, 30.0)
        self.assertEqual(severity, Severity.MEDIUM)

    def test_one_high_match(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [_match("HIGH-001", Severity.HIGH)],
        )

        self.assertEqual(score, 50.0)
        self.assertEqual(severity, Severity.HIGH)

    def test_one_critical_match(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [_match("CRIT-001", Severity.CRITICAL)],
        )

        self.assertEqual(score, 80.0)
        self.assertEqual(severity, Severity.CRITICAL)

    def test_multiple_matches(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [
                _match("HIGH-001", Severity.HIGH),
                _match("LOW-001", Severity.LOW),
            ],
        )

        self.assertEqual(score, 65.0)
        self.assertEqual(severity, Severity.HIGH)

    def test_score_capped_at_100(self) -> None:
        score, severity = self.scorer.score(
            "prompt",
            [
                _match("CRIT-001", Severity.CRITICAL),
                _match("HIGH-001", Severity.HIGH),
                _match("HIGH-002", Severity.HIGH),
            ],
        )

        self.assertEqual(score, 100.0)
        self.assertEqual(severity, Severity.CRITICAL)

    def test_severity_threshold_low_upper_bound(self) -> None:
        policy = ScoringPolicy(
            points_by_severity={Severity.LOW: 24.0},
        )
        scorer = ThreatScorer(policy)

        score, severity = scorer.score("prompt", [_match("LOW-001", Severity.LOW)])

        self.assertEqual(score, 24.0)
        self.assertEqual(severity, Severity.LOW)

    def test_severity_threshold_medium_lower_bound(self) -> None:
        policy = ScoringPolicy(
            points_by_severity={Severity.LOW: 25.0},
        )
        scorer = ThreatScorer(policy)

        score, severity = scorer.score("prompt", [_match("LOW-001", Severity.LOW)])

        self.assertEqual(score, 25.0)
        self.assertEqual(severity, Severity.MEDIUM)

    def test_severity_threshold_high_lower_bound(self) -> None:
        policy = ScoringPolicy(
            points_by_severity={Severity.MEDIUM: 50.0},
        )
        scorer = ThreatScorer(policy)

        score, severity = scorer.score("prompt", [_match("MED-001", Severity.MEDIUM)])

        self.assertEqual(score, 50.0)
        self.assertEqual(severity, Severity.HIGH)

    def test_severity_threshold_critical_lower_bound(self) -> None:
        policy = ScoringPolicy(
            points_by_severity={Severity.HIGH: 75.0},
        )
        scorer = ThreatScorer(policy)

        score, severity = scorer.score("prompt", [_match("HIGH-001", Severity.HIGH)])

        self.assertEqual(score, 75.0)
        self.assertEqual(severity, Severity.CRITICAL)

    def test_custom_scoring_configuration(self) -> None:
        policy = ScoringPolicy(
            points_by_severity={
                Severity.LOW: 40.0,
                Severity.MEDIUM: 60.0,
            },
            medium_threshold=30.0,
            high_threshold=55.0,
            critical_threshold=90.0,
            max_score=100.0,
        )
        scorer = ThreatScorer(policy)

        score, severity = scorer.score(
            "prompt",
            [_match("LOW-001", Severity.LOW)],
        )

        self.assertEqual(score, 40.0)
        self.assertEqual(severity, Severity.MEDIUM)

    def test_invalid_thresholds_raise(self) -> None:
        with self.assertRaises(ValueError):
            ScoringPolicy(medium_threshold=80.0, high_threshold=50.0)


if __name__ == "__main__":
    unittest.main()
