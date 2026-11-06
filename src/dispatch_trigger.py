#!/usr/bin/env python3
"""
Autonomous Dispatcher: Triggers deployment pipeline when verified repositories pass CA/REA/EGM audits.
"""
import sys
import json
from src.evaluator import ScoutPulseEvaluator, RepoTelemetry

def run_scout_deployment_trigger():
    evaluator = ScoutPulseEvaluator()

    sample_candidates = [
        RepoTelemetry(
            repo_name="vanguard-org/zero-kernel-agent",
            stars=3420,
            daily_star_delta=620,
            forks=290,
            open_issues=45,
            outside_contributors=38,
            commit_recency_days=0.5
        ),
        RepoTelemetry(
            repo_name="shady-dev/crypto-stealer-wrapper",
            stars=4200,
            daily_star_delta=3800,
            forks=4,
            open_issues=0,
            outside_contributors=1,
            commit_recency_days=0.1,
            has_malicious_signature=True
        ),
        RepoTelemetry(
            repo_name="dormant-ai/ancient-wrapper",
            stars=12000,
            daily_star_delta=5,
            forks=900,
            open_issues=80,
            outside_contributors=40,
            commit_recency_days=180.0
        )
    ]

    print("══════════════════════════════════════════════════════════════")
    print(" 🚀 SCOUTPULSE AUTONOMOUS DISPATCH TRIGGER (FDE INFRA ENGINE)")
    print("══════════════════════════════════════════════════════════════")

    deployable_count = 0
    for repo in sample_candidates:
        res = evaluator.evaluate(repo)
        status_icon = "✅" if res.pipeline_deployable else "🛑"
        print(f"\n{status_icon} REPO: {res.repo_name}")
        print(f"   ├─ Authenticity Score : {res.authenticity_score}")
        print(f"   ├─ REA Risk Level     : {res.rea_risk_level}")
        print(f"   ├─ CA Action          : {res.ca_recommended_action}")
        print(f"   ├─ EGM Compliance     : {res.egm_compliance_status}")
        print(f"   └─ Pipeline Trigger   : {'[DISPATCHING GH DEPLOYMENT WORKFLOW]' if res.pipeline_deployable else '[ABORTED]'}")
        if res.pipeline_deployable:
            deployable_count += 1

    print("\n══════════════════════════════════════════════════════════════")
    print(f" [SUMMARY] {deployable_count}/{len(sample_candidates)} Candidate(s) triggered for instant cloud deployment.")
    print("══════════════════════════════════════════════════════════════")
    return deployable_count

if __name__ == "__main__":
    run_scout_deployment_trigger()
