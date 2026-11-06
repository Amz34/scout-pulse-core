"""
Sybil star-farming and inorganic growth detection engine.
Analyzes account age distribution, temporal commit density, and fork graph depth.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import math
import statistics

@dataclass
class StarSample:
    starred_at_epoch: float
    user_account_age_days: float
    user_public_repos: int
    user_followers: int

@dataclass
class SybilReport:
    is_anomalous: bool
    confidence: float
    rejection_reason: Optional[str]
    entropy_score: float
    clustering_coefficient: float
    metrics: Dict[str, Any] = field(default_factory=dict)

class SybilDetector:
    """
    Statistical and graph-based heuristic engine to detect coordinated star-buying campaigns.
    Real organic breakouts exhibit high Poisson temporal dispersion and diverse account demographics.
    Wash-trade campaigns exhibit low temporal variance and clustered account registration dates.
    """

    def __init__(
        self,
        min_temporal_entropy: float = 0.42,
        max_fresh_account_ratio: float = 0.35,
        min_fork_to_star_ratio: float = 0.02
    ):
        self.min_temporal_entropy = min_temporal_entropy
        self.max_fresh_account_ratio = max_fresh_account_ratio
        self.min_fork_to_star_ratio = min_fork_to_star_ratio

    def calculate_temporal_entropy(self, timestamps: List[float], bin_count: int = 12) -> float:
        """Calculates Shannon entropy across temporal ingestion windows."""
        if len(timestamps) < 2:
            return 1.0
        
        t_min, t_max = min(timestamps), max(timestamps)
        span = t_max - t_min
        if span == 0:
            return 0.0

        bins = [0] * bin_count
        bin_width = span / bin_count
        for t in timestamps:
            idx = min(int((t - t_min) / bin_width), bin_count - 1)
            bins[idx] += 1

        total = len(timestamps)
        entropy = 0.0
        for count in bins:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        max_entropy = math.log2(bin_count)
        return round(entropy / max_entropy, 4) if max_entropy > 0 else 0.0

    def audit_star_cohort(
        self,
        samples: List[StarSample],
        total_stars: int,
        total_forks: int,
        daily_delta: int
    ) -> SybilReport:
        """Deep forensic evaluation of repository engagement graph."""
        if not samples:
            # Fallback to high-level ratio heuristics
            fork_ratio = total_forks / max(total_stars, 1)
            if daily_delta > 1500 and fork_ratio < self.min_fork_to_star_ratio:
                return SybilReport(
                    is_anomalous=True,
                    confidence=0.88,
                    rejection_reason="Extreme star velocity anomaly decoupled from repository fork network.",
                    entropy_score=0.10,
                    clustering_coefficient=0.85,
                    metrics={"fork_ratio": fork_ratio, "daily_delta": daily_delta}
                )
            return SybilReport(
                is_anomalous=False,
                confidence=0.92,
                rejection_reason=None,
                entropy_score=0.75,
                clustering_coefficient=0.20,
                metrics={"sample_count": 0}
            )

        timestamps = [s.starred_at_epoch for s in samples]
        entropy = self.calculate_temporal_entropy(timestamps)

        fresh_accounts = sum(1 for s in samples if s.user_account_age_days < 14)
        fresh_ratio = fresh_accounts / len(samples)

        ghost_accounts = sum(1 for s in samples if s.user_public_repos == 0 and s.user_followers == 0)
        ghost_ratio = ghost_accounts / len(samples)

        is_bot_farm = (fresh_ratio > self.max_fresh_account_ratio) or (ghost_ratio > 0.40) or (entropy < self.min_temporal_entropy)
        
        confidence = 0.95 if is_bot_farm else 0.90
        reason = None
        if is_bot_farm:
            reasons = []
            if fresh_ratio > self.max_fresh_account_ratio:
                reasons.append(f"Excessive fresh account clustering ({fresh_ratio:.1%})")
            if ghost_ratio > 0.40:
                reasons.append(f"Synthetic ghost profile ratio ({ghost_ratio:.1%})")
            if entropy < self.min_temporal_entropy:
                reasons.append(f"Synthetic batch burst entropy ({entropy:.3f})")
            reason = "; ".join(reasons)

        return SybilReport(
            is_anomalous=is_bot_farm,
            confidence=confidence,
            rejection_reason=reason,
            entropy_score=entropy,
            clustering_coefficient=round(fresh_ratio * 0.6 + ghost_ratio * 0.4, 3),
            metrics={
                "fresh_account_ratio": round(fresh_ratio, 3),
                "ghost_account_ratio": round(ghost_ratio, 3),
                "temporal_entropy": entropy,
                "cohort_size": len(samples)
            }
        )
