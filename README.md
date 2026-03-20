# eigenhelm

**A conscience for agents, not an agent** — language-agnostic code aesthetic evaluation sidecar.

Eigenhelm scores agent-generated code against mathematical aesthetic metrics derived from
information theory, complexity science, and a PCA eigenspace trained on curated elite
corpora. It runs alongside code-generating agents as a real-time quality signal.

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)

---

## Quick Start

### Install

```bash
pip install eigenhelm
```

Or with uv (no venv required):

```bash
uv tool install eigenhelm
```

### Evaluate a file

A bundled model is included — no setup needed.

```bash
eh evaluate path/to/file.py --classify
```

### Evaluate a directory

```bash
eh evaluate src/ --rank
```

Ranks all files best-to-worst and highlights the bottom performers.

### What the scores mean

- **accept** (score < 0.4): Structurally sound. Move on.
- **marginal** (score 0.4-0.6): Fine. No action needed.
- **reject** (score > 0.6): Worth reviewing. Read the directives for guidance.

Scores are relative to elite open-source training corpora. Most production code scores marginal or reject — that's normal, not a problem.

---

## Agent Integration

Eigenhelm ships with a skill file that teaches AI agents how to use it correctly.

```bash
# Install via skills registry (recommended)
npx skills add metacogdev/skills

# Or install directly from eigenhelm CLI
eh skill --install
```

The skill encodes a tested workflow contract: evaluate after tests pass, two passes maximum, never sacrifice correctness for score. In controlled benchmarks across 3 project types, agents using the skill produced code rated 46% higher on design, robustness, and spec compliance by an independent reviewer, with no correctness regressions.

[Full agent integration guide](https://eigenhelm.sh/integrations/agent-skills/)

---

## CLI Reference

All commands are available as `eigenhelm <command>` or `eh <command>`:

| Command | Description |
|---------|-------------|
| `eh evaluate` | Evaluate source files against the aesthetic manifold |
| `eh train` | Train a new eigenspace model from a corpus directory |
| `eh inspect` | Inspect a saved model's metadata |
| `eh serve` | Run the evaluation HTTP server |
| `eh harness` | Run a statistical comparison harness across two code sets |
| `eh skill` | Install the agent skill file |
| `eh init` | Generate a starter `.eigenhelm.toml` configuration |
| `eh corpus` | Manage training corpora (sync from manifest) |

Run `eh --help` or `eh <command> --help` for details.

---

## HTTP API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness probe |
| `/evaluate` | POST | Evaluate a code unit |
| `/evaluate/batch` | POST | Evaluate multiple code units |

---

## Supported Languages

**Trained models**: Python, JavaScript, TypeScript, Go, Rust.

**Parser support** (feature extraction available, bring your own model): Java, C, C++, Ruby, Kotlin.

---

## Development Setup

```bash
git clone https://github.com/metacogdev/eigenhelm.git
cd eigenhelm
uv sync --extra dev --extra serve
uv run pytest
uv run ruff check .
```

---

## Architecture

```
eigenhelm/
├── virtue_extractor.py   — Tree-sitter + Lizard → FeatureVector (69 dimensions)
├── critic/               — AestheticCritic: 5-dim scoring (drift, alignment, entropy, compression, NCD)
├── declarations/         — Declaration-aware scoring (type defs, barrel files, data tables)
├── regions/              — Test/production code region detection
├── eigenspace/           — EigenspaceModel: PCA projection, drift scoring
├── attribution/          — Score attribution and directive generation
├── training/             — PCA training, calibration, exemplar selection
├── helm/                 — DynamicHelm: threshold-calibrated evaluation + PID steering
├── config/               — .eigenhelm.toml loader and models
├── output/               — SARIF 2.1.0 and JSON formatters
├── scoring/              — Per-repo scorecard (M1-M5, Q1-Q5)
├── harness/              — Statistical evaluation harness (Mann-Whitney U)
└── serve/                — FastAPI HTTP evaluation server
```

---

## Current Status

- **5-dim scoring**: manifold drift, alignment, entropy, compression, NCD exemplar distance
- **5 languages**: Python, JavaScript, TypeScript, Go, Rust — all discriminating (Cohen's d > 0.5)
- **Human correlation**: Spearman rho = 0.54 overall (n = 92, 5 languages), 0.66 Python-only (n = 52)
- **Declaration-aware**: Automatically detects type-definition and data-table files, adjusts scoring and directives
- **Agent-tested**: Skill contract validated in controlled arena (3 scenarios, 46% quality improvement)

---

## License

eigenhelm is licensed under the [GNU Affero General Public License v3.0](LICENSE).

### Commercial Licensing

Looking to use eigenhelm in a proprietary SaaS or enterprise product without AGPL-3.0
obligations? A commercial license is available.

Contact us at **licensing@eigenhelm.sh** to discuss terms.
