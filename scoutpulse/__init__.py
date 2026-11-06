"""
ScoutPulse core package initialization.
High-throughput event-driven GitHub repository intelligence & Sybil audit engine.
"""
__version__ = "0.2.0"
__author__ = "Aamir Zameer (Amz34)"
__license__ = "Apache-2.0"

from .pipeline.evaluator import ScoutPulseEvaluator, RepoTelemetry, AuditResult
from .sybil.detector import SybilDetector
from .ingest.events import GitHubEventIngester

__all__ = [
    "ScoutPulseEvaluator",
    "RepoTelemetry",
    "AuditResult",
    "SybilDetector",
    "GitHubEventIngester",
]
