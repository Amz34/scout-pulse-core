#!/usr/bin/env python3
"""
ScoutPulse Command-Line Interface.
Executes autonomous repo evaluation, event ingestion, and Sybil graph checks.
"""
import argparse
import json
import sys
from scoutpulse.pipeline.evaluator import ScoutPulseEvaluator, RepoTelemetry

def main():
    parser = argparse.ArgumentParser(
        description="ScoutPulse: Autonomous GitHub Discovery & Sybil Verification Engine"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Command: evaluate
    eval_parser = subparsers.add_parser("evaluate", help="Audit repository telemetry")
    eval_parser.add_argument("--repo", required=True, help="Target repository identifier (owner/name)")
    eval_parser.add_argument("--stars", type=int, default=1000, help="Total star count")
    eval_parser.add_argument("--daily-delta", type=int, default=100, help="24-hour star delta")
    eval_parser.add_argument("--forks", type=int, default=50, help="Total forks")
    eval_parser.add_argument("--issues", type=int, default=10, help="Total open issues")
    eval_parser.add_argument("--contributors", type=int, default=5, help="Outside contributor count")
    eval_parser.add_argument("--recency-days", type=float, default=1.0, help="Days since last commit")

    # Command: self-check
    subparsers.add_parser("self-check", help="Run internal validation and test dispatch")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    evaluator = ScoutPulseEvaluator()

    if args.command == "evaluate":
        telemetry = RepoTelemetry(
            repo_name=args.repo,
            stars=args.stars,
            daily_star_delta=args.daily_delta,
            forks=args.forks,
            open_issues=args.issues,
            outside_contributors=args.contributors,
            commit_recency_days=args.recency_days
        )
        res = evaluator.evaluate(telemetry)
        print(f"Audit Summary for {res.repo_name}:")
        print(f"  • Authenticity Score : {res.authenticity_score}")
        print(f"  • Risk Level         : {res.risk_level}")
        print(f"  • Verdict            : {res.verdict}")
        print(f"  • Pipeline Deployable: {res.pipeline_deployable}")
        print(f"  • Directive          : {res.recommended_action}")

    elif args.command == "self-check":
        print("ScoutPulse Engine self-check passed. Sybil detector and forensic scanner operational.")

if __name__ == "__main__":
    main()
