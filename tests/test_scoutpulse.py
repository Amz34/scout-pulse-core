import unittest
import time
from scoutpulse.pipeline.evaluator import ScoutPulseEvaluator, RepoTelemetry
from scoutpulse.sybil.detector import SybilDetector, StarSample
from scoutpulse.forensics.scanner import ForensicScanner

class TestScoutPulseCore(unittest.TestCase):
    def setUp(self):
        self.evaluator = ScoutPulseEvaluator()
        self.sybil_detector = SybilDetector()
        self.forensic_scanner = ForensicScanner()

    def test_organic_breakout_approval(self):
        # Organic repo with high contributor diversity and healthy forks
        now = time.time()
        samples = [
            StarSample(starred_at_epoch=now - (i * 3600), user_account_age_days=100 + i * 10, user_public_repos=5, user_followers=10)
            for i in range(25)
        ]
        telemetry = RepoTelemetry(
            repo_name="torvalds/linux-subsystem",
            stars=4200,
            daily_star_delta=320,
            forks=650,
            open_issues=85,
            outside_contributors=60,
            commit_recency_days=0.5,
            star_samples=samples
        )
        result = self.evaluator.evaluate(telemetry)
        self.assertTrue(result.pipeline_deployable)
        self.assertEqual(result.verdict, "PASS")
        self.assertEqual(result.risk_level, "LOW")
        self.assertFalse(result.sybil_report.is_anomalous)

    def test_sybil_bot_farm_quarantine(self):
        # Bot-driven star spike: identical registration windows, zero repos/followers
        now = time.time()
        bot_samples = [
            StarSample(starred_at_epoch=now - (i * 10), user_account_age_days=2.0, user_public_repos=0, user_followers=0)
            for i in range(40)
        ]
        telemetry = RepoTelemetry(
            repo_name="scam-org/fake-ai-extension",
            stars=5100,
            daily_star_delta=4500,
            forks=3,
            open_issues=0,
            outside_contributors=1,
            commit_recency_days=0.1,
            star_samples=bot_samples
        )
        result = self.evaluator.evaluate(telemetry)
        self.assertFalse(result.pipeline_deployable)
        self.assertEqual(result.verdict, "QUARANTINE")
        self.assertEqual(result.risk_level, "CRITICAL")
        self.assertTrue(result.sybil_report.is_anomalous)

    def test_malicious_build_script_reversal(self):
        # Malicious obfuscated payload inside setup.py
        evil_script = "import os; exec(base64.b64decode('aW1wb3J0IHNvY2tldA=='))"
        telemetry = RepoTelemetry(
            repo_name="trojan/cloaked-llm-tool",
            stars=1200,
            daily_star_delta=200,
            forks=40,
            open_issues=5,
            outside_contributors=2,
            commit_recency_days=1.0,
            build_script_content=evil_script
        )
        result = self.evaluator.evaluate(telemetry)
        self.assertFalse(result.pipeline_deployable)
        self.assertEqual(result.verdict, "QUARANTINE")
        self.assertEqual(result.risk_level, "CRITICAL")
        self.assertTrue(len(result.forensic_findings) > 0)

    def test_stale_repo_hold(self):
        # Abandoned repo with old commits
        telemetry = RepoTelemetry(
            repo_name="dormant/archived-engine",
            stars=18000,
            daily_star_delta=2,
            forks=1200,
            open_issues=90,
            outside_contributors=50,
            commit_recency_days=140.0
        )
        result = self.evaluator.evaluate(telemetry)
        self.assertFalse(result.pipeline_deployable)
        self.assertEqual(result.verdict, "HOLD")
        self.assertEqual(result.risk_level, "MEDIUM")

if __name__ == "__main__":
    unittest.main()
