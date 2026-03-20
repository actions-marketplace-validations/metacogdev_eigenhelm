# Directives

Directives are actionable improvement suggestions generated from score attribution. Each directive identifies a specific code location and what to focus on.

## Anatomy of a directive

```
[high] extract_repeated_logic → MyClass (lines 15-42)
  #1 wl_hash_bin_04: contribution=+2.45, deviation=+2.4σ
```

- **Severity**: `[high]`, `[medium]`, or `[low]`
- **Category**: What kind of improvement to make
- **Target**: The code unit and line range
- **Evidence**: The feature driving the suggestion, with its deviation from corpus norms

## Severity levels

| Severity | Threshold | Meaning |
|----------|-----------|---------|
| `[high]` | normalized score ≥ 0.7 | Likely to materially improve the score |
| `[medium]` | normalized score ≥ 0.5 | Worth reviewing, may not be actionable |
| `[low]` | normalized score < 0.5 | Minor — address only if convenient |

!!! note
    For files under ~80 lines, `compression_structure` and `ncd_exemplar_distance` directives are automatically capped at `[medium]` severity, since high scores on these dimensions are expected for small modules.

## Directive categories

### From PCA dimensions (structural)

| Category | Trigger | What to do |
|----------|---------|------------|
| `reduce_complexity` | Halstead metrics (volume, difficulty, effort) deviate high | Simplify logic, extract helpers, reduce nesting |
| `extract_repeated_logic` | WL hash bins show positive deviation (repeated subtree shapes) | Factor out duplicated structural patterns |
| `review_structure` | WL hash bins show negative deviation (unusual structure) | Review for unconventional patterns that may confuse readers |

### From information-theoretic dimensions (direct)

| Category | Dimension | What to do |
|----------|-----------|------------|
| `review_token_distribution` | Token entropy | Code is too repetitive (low entropy) — look for duplicated blocks or boilerplate |
| `improve_compression` | Compression structure | Significant structural redundancy — look for repeated patterns |
| `review_structure` | NCD exemplar distance | Code is structurally unlike any known good exemplar |

## Declaration-aware directives

For files that are primarily type definitions or data tables (>= 60% declaration constructs), eigenhelm adjusts directive behavior:

- **Category override**: `extract_repeated_logic` becomes `review_structure` — because the repetition is inherent to the syntax (every dataclass looks the same), not a design smell.
- **Score dampening**: Manifold drift and alignment contributions are halved, reducing the overall score.
- **Output tag**: The file is tagged `[declaration-heavy]` so agents understand why the score is lower than usual.
- **JSON/SARIF**: A `declaration_ratio` field is included for programmatic consumption.

Files that are 100% type definitions (dataclasses, interfaces, structs with no data tables) are **skipped entirely** — they produce no actionable signal.

## Using directives effectively

**For humans**: Focus on `[high]` severity items. They point to the most impactful improvements.

**For AI agents**: Follow the [skill workflow](../integrations/agent-skills.md) — evaluate once, apply obvious fixes for rejects, re-evaluate once, then stop. Two passes maximum.

!!! tip "High scores on files with inline tests?"
    If a file contains both production and test code, high-severity directives like `improve_compression` or `review_structure` may be driven by repetitive test patterns rather than production code quality issues. Check the **region breakdown** in the output — if the production region scores well but the test region scores poorly, the directives are likely test-driven. See [Test code dilution](dimensions.md#test-code-dilution) for details.

## Controlling directives

```bash
# Only generate directives for scores above 0.5
eh evaluate myfile.py --directive-threshold 0.5

# Show top-5 features per dimension (default: 3)
eh evaluate myfile.py --top-n 5
```
