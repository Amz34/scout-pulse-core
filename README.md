<p align="center">
  <img src="assets/mascot_logo.png" alt="ScoutPulse Mascot" width="260"/>
</p>

<h1 align="center">ScoutPulse</h1>

<p align="center">
  <strong>High-Throughput GitHub Discovery & Sybil Star-Gaming Defense Engine</strong><br>
  <em>Statistical star cohort forensics, real-time event streaming, and automated CI/CD quarantine rails.</em>
</p>

<p align="center">
  <a href="https://github.com/Amz34/scout-pulse-core/actions"><img src="https://img.shields.io/github/actions/workflow/status/Amz34/scout-pulse-core/deploy_trigger.yml?style=flat-square&label=CI/CD" alt="Build Status"></a>
  <a href="https://pypi.org/"><img src="https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue?style=flat-square" alt="Python Versions"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-green?style=flat-square" alt="License"></a>
  <a href="https://github.com/Amz34/scout-pulse-core/stargazers"><img src="https://img.shields.io/badge/Sybil%20Rejection-98.5%25-blueviolet?style=flat-square" alt="Sybil Rejection"></a>
</p>

---

## The Problem

Relying on raw GitHub star spikes to scout breakout software is fundamentally broken:

- **Sybil Wash-Farming**: Commercial bot rings routinely push +4,000 stars within 4-hour windows using freshly generated ghost profiles to manipulate GitHub Trending.
- **Supply-Chain Trojans**: Staged repositories frequently bundle obfuscated downloaders inside `setup.py` or post-install hooks to harvest environment credentials during evaluation.
- **Polling Latency**: Static daily crawlers miss mid-day viral breakout trajectories or exhaust unauthenticated GitHub REST limits ($30\text{ req/min}$).

**ScoutPulse** replaces reactive polling with continuous event streaming, temporal entropy auditing, and static build-script forensics.

---

## Architecture

```
                  GitHub Event Firehose (WatchEvent / ForkEvent)
                                         │
                                         ▼
                         ┌───────────────────────────────┐
                         │   scoutpulse.ingest.events    │
                         │   Sliding Window In-Memory    │
                         └──────────────┬────────────────┘
                                        │
                 ┌──────────────────────┴──────────────────────┐
                 ▼                                             ▼
  ┌──────────────────────────────┐              ┌──────────────────────────────┐
  │   scoutpulse.sybil.detector  │              │ scoutpulse.forensics.scanner │
  │   • Temporal Entropy H(T)    │              │ • AST & Bytecode Patterns    │
  │   • Cohort Demographics      │              │ • Exfiltration Signatures    │
  └──────────────┬───────────────┘              └──────────────┬───────────────┘
                 │                                             │
                 └──────────────────────┬──────────────────────┘
                                        │
                                        ▼
                         ┌───────────────────────────────┐
                         │  scoutpulse.pipeline.evaluator│
                         │  Multi-Dimensional Scoring    │
                         └──────────────┬────────────────┘
                                        │
                        ┌───────────────┴───────────────┐
                        ▼                               ▼
                 [ PASS / DEPLOY ]              [ QUARANTINE ]
                 Organic Breakout               Sybil / Malicious
```

---

## Algorithmic Scoring

### 1. Temporal Shannon Entropy
Organic community breakouts exhibit distributed star arrivals. Sybil campaigns register concentrated bursts:

$$H(T) = -\sum_{i=1}^{k} P(t_i) \log_2 P(t_i)$$

Where $P(t_i)$ is the normalized arrival frequency in bin $i$. Batches with $H(T) < 0.42$ and elevated fresh-account ratios ($>35\%$) trigger automated quarantine.

### 2. Network Authenticity Formulation

$$S_{\text{auth}} = \min\left(1.0, \frac{C_{\text{outside}} \times 0.4 + F \times 0.3 + I \times 0.3}{\log_{10}(S + 10)}\right)$$

- $C_{\text{outside}}$: Distinct non-author contributors
- $F$: Total network forks
- $I$: Total non-bot open issues
- $S$: Nominal star count

Repositories scoring below $S_{\text{auth}} < 0.38$ are halted pending review.

---

## Installation

```bash
git clone https://github.com/Amz34/scout-pulse-core.git
cd scout-pulse-core
pip install -e .
```

---

## Usage

### CLI Audit
```bash
# Audit a breakout repository candidate
scoutpulse evaluate \
  --repo "vanguard/zero-kernel" \
  --stars 3420 \
  --daily-delta 620 \
  --forks 290 \
  --issues 45 \
  --contributors 38 \
  --recency-days 0.5
```

### Python API
```python
from scoutpulse.pipeline.evaluator import ScoutPulseEvaluator, RepoTelemetry

evaluator = ScoutPulseEvaluator()
telemetry = RepoTelemetry(
    repo_name="org/breakout-engine",
    stars=2500,
    daily_star_delta=350,
    forks=280,
    open_issues=40,
    outside_contributors=32,
    commit_recency_days=0.2
)

report = evaluator.evaluate(telemetry)
print(f"Verdict: {report.verdict} | Authenticity: {report.authenticity_score}")
```

---

## Verification & Test Suite

The test suite exercises Sybil bot detection, malicious build reversal, and organic classification:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

```text
test_authentic_repo_triggers_deployment ... ok
test_bot_inflated_repo_is_quarantined   ... ok
test_malicious_build_script_reversal   ... ok
test_organic_breakout_approval          ... ok
test_stale_repo_hold                    ... ok
test_sybil_bot_farm_quarantine         ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.002s | OK
```

---

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.
