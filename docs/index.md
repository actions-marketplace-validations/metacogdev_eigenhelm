# eigenhelm

**A conscience for agents, not an agent.**

eigenhelm is a language-agnostic code aesthetic evaluation sidecar. It scores code against mathematical aesthetic metrics derived from information theory, complexity science, and a PCA eigenspace trained on curated elite corpora.

It runs alongside code-generating agents as a real-time quality signal — not to replace judgment, but to surface when generated code drifts from the structural patterns found in high-quality human-written code.

---

## What it does

eigenhelm evaluates source code across **five dimensions**:

| Dimension | What it measures |
|-----------|-----------------|
| **Manifold drift** | Distance from the learned code quality manifold |
| **Manifold alignment** | Alignment with principal quality axes |
| **Token entropy** | Information density of the token stream |
| **Compression structure** | Structural regularity via Birkhoff aesthetic measure |
| **NCD exemplar distance** | Similarity to nearest high-quality exemplar |

Each file gets a score from 0.0 (ideal) to 1.0, a classification (accept / marginal / reject), and **actionable directives** pointing to specific code units that can be improved.

---

## Quick example

```bash
# Install
uv tool install eigenhelm

# Evaluate a file
eh evaluate mymodule.py --classify
```

```
mymodule.py
  decision: accept
  score:    0.38 (p62 — better than 62% of training corpus)
  confidence: high
  contributions:
    manifold_drift           0.10  (weight: 0.30, normalized: 0.33)
    manifold_alignment       0.09  (weight: 0.30, normalized: 0.30)
    token_entropy            0.06  (weight: 0.15, normalized: 0.40)
    compression_structure    0.08  (weight: 0.15, normalized: 0.53)
    ncd_exemplar_distance    0.05  (weight: 0.10, normalized: 0.50)
```

---

## Use cases

- **CI gating** — fail PRs that introduce low-quality generated code
- **Agent sidecar** — give coding agents a quality signal during generation
- **Pre-commit hook** — catch quality regressions before they land
- **Corpus benchmarking** — compare code quality across repositories or teams

---

## Get started

<div class="grid cards" markdown>

- :material-download: **[Installation](getting-started/install.md)**

    Install via pip, uv, or Docker

- :material-rocket-launch: **[Quick Start](getting-started/quickstart.md)**

    Evaluate your first file in 60 seconds

- :material-cog: **[Configuration](getting-started/configuration.md)**

    Customize thresholds, models, and paths

- :material-github: **[GitHub Action](integrations/github-action.md)**

    Add eigenhelm to your CI pipeline

</div>

---

## Supported languages

Python, JavaScript, TypeScript, Go, Rust, Java, C, C++, Ruby, Swift.

---

## License

eigenhelm is licensed under [AGPL-3.0](license.md). A [commercial license](mailto:licensing@eigenhelm.dev) is available for proprietary use.
