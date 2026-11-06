"""
Core evaluation pipeline combining Sybil defense, forensic analysis, and automated CI/CD dispatch.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import math
from ..sybil.detector import SybilDetector, StarSample, SybilReport
from ..forensics.scanner import ForensicScanner, ForensicFinding

@dataclass
class RepoTelemetry:
    repo_name: str
    stars: int
    daily_star_delta: int
    forks: int
    open_issues: int
    outside_contributors: int
    commit_recency_days: float
    build_script_content: Optional[str] = None
    star_samples: List[StarSample] = None

@dataclass
class AuditResult:
    repo_name: str
    authenticity_score: float
    risk_level: str              # LOW, MEDIUM, CRITICAL
    verdict: str                 # PASS, HOLD, QUARANTINE
    pipeline_deployable: bool
    sybil_report: SybilReport
    forensic_findings: List[ForensicFinding]
    recommended_action: str
    telemetry: Dict[str, Any]

class ScoutPulseEvaluator:
    """
    Enterprise Forward-Deployed Engineering (FDE) Repository Auditor.
    Computes deterministic authenticity scores and coordinates pipeline deployment decisions.
    """

    def __init__(
        self,
        authenticity_threshold: float = 0.38,
        star_spike_limit: int = 1500
    ):
        self.authenticity_threshold = authenticity_threshold
        self.star_spike_limit = star_spike_limit
        self.sybil_detector = SybilDetector()
        self.forensic_scanner = ForensicScanner()

    def evaluate(self, telemetry: RepoTelemetry) -> AuditResult:
        # 1. Forensic signature scan on build scripts
        findings: List[ForensicFinding] = []
        if telemetry.build_script_content:
            findings = self.forensic_scanner.scan_content(
                "build_script",
                telemetry.build_script_content
            )

        has_critical_findings = any(f.severity == "HIGH" for f in findings)

        # 2. Sybil star graph & temporal entropy audit
        samples = telemetry.star_samples or []
        sybil_report = self.sybil_detector.audit_star_cohort(
            samples,
            telemetry.stars,
            telemetry.forks,
            telemetry.daily_star_delta
        )

        # 3. Authenticity heuristic score calculation
        # S_auth = min(1.0, (C_outside * 0.4 + Forks * 0.3 + Issues * 0.3) / log10(Stars + 10))
        denom = math.log10(telemetry.stars + 10)
        numerator = (telemetry.outside_contributors * 0.4) + (telemetry.forks * 0.3) + (telemetry.open_issues * 0.3)
        raw_score = (numerator / denom) if denom > 0 else 0.0
        auth_score = round(min(1.0, max(0.0, raw_score)), 3)

        # 4. Multidimensional Decision Matrix
        if has_critical_findings or sybil_report.is_anomalous:
            risk_level = "CRITICAL"
            verdict = "QUARANTINE"
            action = f"IMMEDIATE ISOLATION: {sybil_report.rejection_reason or 'Malicious build execution signature detected.'}"
            deployable = False
        elif telemetry.commit_recency_days > 90 or auth_score < self.authenticity_threshold:
            risk_level = "MEDIUM"
            verdict = "HOLD"
            action = f"CONDITIONAL HOLD: Stale commits ({telemetry.commit_recency_days:.0f}d) or sub-threshold distribution."
            deployable = False
        else:
            risk_level = "LOW"
            verdict = "PASS"
            action = "DISPATCH DEPLOY: Verified community breakout; proceed with production publication."
            deployable = True

        return AuditResult(
            repo_name=telemetry.repo_name,
            authenticity_score=auth_score,
            risk_level=risk_level,
            verdict=verdict,
            pipeline_deployable=deployable,
            sybil_report=sybil_report,
            forensic_findings=findings,
            recommended_action=action,
            telemetry=asdict(telemetry)
        )
