import unittest
from src.evaluator import ScoutPulseEvaluator, RepoTelemetry

class TestScoutPulseEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = ScoutPulseEvaluator()

    def test_authentic_repo_triggers_deployment(self):
        repo = RepoTelemetry(
            repo_name="org/authentic-agent",
            stars=2500,
            daily_star_delta=400,
            forks=310,
            open_issues=45,
            outside_contributors=55,
            commit_recency_days=1.0
        )
        result = self.evaluator.evaluate(repo)
        self.assertTrue(result.pipeline_deployable)
        self.assertEqual(result.egm_compliance_status, "PASS")
        self.assertEqual(result.rea_risk_level, "LOW")

    def test_bot_inflated_repo_is_quarantined(self):
        repo = RepoTelemetry(
            repo_name="scam/sybil-stars",
            stars=5000,
            daily_star_delta=4500,
            forks=2,
            open_issues=0,
            outside_contributors=1,
            commit_recency_days=0.2,
            has_malicious_signature=True
        )
        result = self.evaluator.evaluate(repo)
        self.assertFalse(result.pipeline_deployable)
        self.assertEqual(result.egm_compliance_status, "REJECT")
        self.assertEqual(result.rea_risk_level, "CRITICAL")

if __name__ == "__main__":
    unittest.main()
