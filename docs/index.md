# eigenhelm

**Catch low-quality AI-generated code before it lands.**

eigenhelm scores changed files in CI, gives coding agents concrete refactoring directives, and helps teams measure code quality over time — using information theory, not style rules.

```bash
uv tool install eigenhelm
eh evaluate --diff origin/main...HEAD --strict
```

---

## Why teams use eigenhelm

<div class="grid cards" markdown>

- :material-shield-check: **Gate AI-generated PRs**

    Score every changed file in CI. Block merges that fall below quality thresholds. Works with GitHub Actions, pre-commit, or any CI system.

- :material-chart-line: **Measure quality drift**

    Track scores across repos and over time. Compare models, prompts, or agents with a single statistical metric backed by Mann-Whitney U tests.

- :material-robot: **Give agents a feedback loop**

    Agents receive actionable directives — not just a score. `[high] extract_repeated_logic → MyClass (lines 15-42)` tells the agent exactly what to fix and where.

</div>

---

## Quick example

```bash
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

Each file gets a score from 0.0 (ideal) to 1.0, a classification (**accept** / **marginal** / **reject**), and **actionable directives** pointing to specific code units that can be improved.

---

## How it works

eigenhelm extracts a 69-dimensional structural fingerprint from each file using tree-sitter and projects it into a PCA eigenspace trained on curated elite corpora. The score combines five dimensions:

| Dimension | What it measures |
|-----------|-----------------|
| **Manifold drift** | Distance from the learned code quality manifold |
| **Manifold alignment** | Alignment with principal quality axes |
| **Token entropy** | Information density of the byte stream |
| **Compression structure** | Structural regularity (Birkhoff aesthetic measure) |
| **NCD exemplar distance** | Similarity to nearest high-quality exemplar |

[Learn more about the scoring model →](concepts/how-it-works.md)

---

## Integrate in 30 seconds

=== "GitHub Action"

    ```yaml
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - uses: metacogdev/eigenhelm@v0
      with:
        diff: origin/main...HEAD
        strict: "true"
    ```

=== "Pre-commit"

    ```yaml
    repos:
      - repo: https://github.com/metacogdev/eigenhelm
        rev: v0.4.0
        hooks:
          - id: eigenhelm-check
    ```

=== "HTTP API"

    ```bash
    eh serve --port 8080
    curl -X POST http://localhost:8080/v1/evaluate \
      -H "Content-Type: application/json" \
      -d '{"source": "def add(a, b): return a + b", "language": "python"}'
    ```

=== "Agent skill"

    ```bash
    npx skills add metacogdev/skills --skill eigenhelm
    ```

---

## Outputs

- **Human** — readable terminal output with color and classification
- **JSON** — machine-readable for scripting and dashboards
- **[SARIF 2.1.0](https://sarifweb.azurewebsites.net/)** — upload to GitHub Code Scanning, VS Code, or any SARIF viewer

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

**Trained models**: Python, JavaScript, TypeScript, Go, Rust.

**Parser support** (feature extraction available, bring your own model): Java, C, C++, Ruby, Kotlin.

---

## License

eigenhelm is licensed under [AGPL-3.0](license.md). A [commercial license](mailto:licensing@eigenhelm.sh) is available for proprietary use.
