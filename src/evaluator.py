"""
ScoutPulse Core Engine: CA + REA + EGM Algorithmic Engine
Combines Corrective Action, Risk & Exposure Assessment, and Enterprise Governance Maturity.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import math

@dataclass
class RepoTelemetry:
    repo_name: str
    stars: int
    daily_star_delta: int
    forks: int
    open_issues: int
    outside_contributors: int
    commit_recency_days: float
    has_malicious_signature: bool = False

@dataclass
class EGMResult:
    repo_name: str
    authenticity_score: float     # 0.0 to 1.0 (Sybil/bot resistance)
    rea_risk_level: str           # LOW, MEDIUM, CRITICAL (Risk & Exposure)
    ca_recommended_action: str    # Corrective Action directive
    egm_compliance_status: str    # PASS / REJECT / QUARANTINE
    pipeline_deployable: bool     # Trigger for automated CI/CD infra
    audit_telemetry: Dict[str, Any]

class ScoutPulseEvaluator:
    """Enterprise FDE Auditor for real-time repository ingestion & validation."""

    def __init__(self, authenticity_threshold: float = 0.38, star_spike_limit: int = 1500):
        self.authenticity_threshold = authenticity_threshold
        self.star_spike_limit = star_spike_limit

    def evaluate(self, telemetry: RepoTelemetry) -> EGMResult:
        # Calculate Authenticity Score: Bot/Wash-star rejection formula
        # S_auth = min(1.0, (C_unique * 0.4 + Forks * 0.3 + Issues * 0.3) / log10(Stars + 10))
        denom = math.log10(telemetry.stars + 10)
        numerator = (telemetry.outside_contributors * 0.4) + (telemetry.forks * 0.3) + (telemetry.open_issues * 0.3)
        raw_score = numerator / denom if denom > 0 else 0.0
        auth_score = round(min(1.0, max(0.0, raw_score)), 3)

        # REA: Risk & Exposure Assessment
        if telemetry.has_malicious_signature or (telemetry.daily_star_delta > self.star_spike_limit and auth_score < 0.25):
            risk_level = "CRITICAL"
            ca_action = "IMMEDIATE QUARANTINE: Drop from publishing pipeline; flag Sybil star farm."
            compliance = "REJECT"
            deployable = False
        elif telemetry.commit_recency_days > 90 or auth_score < self.authenticity_threshold:
            risk_level = "MEDIUM"
            ca_action = "DE-PRIORITIZE: Stale repository or unverified community distribution."
            compliance = "CONDITIONAL_HOLD"
            deployable = False
        else:
            risk_level = "LOW"
            ca_action = "INSTANT DEPLOY: Authentic organic breakout verified; route to content orchestrator."
            compliance = "PASS"
            deployable = True

        return EGMResult(
            repo_name=telemetry.repo_name,
            authenticity_score=auth_score,
            rea_risk_level=risk_level,
            ca_recommended_action=ca_action,
            egm_compliance_status=compliance,
            pipeline_deployable=deployable,
            audit_telemetry=asdict(telemetry)
        )
