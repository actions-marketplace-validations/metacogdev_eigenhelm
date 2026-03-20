# Quick Start

## Evaluate a file

```bash
eh evaluate path/to/file.py --classify
```

The `--classify` flag adds accept/marginal/reject labels to the output.

## Evaluate a directory

```bash
eh evaluate src/ --classify
```

eigenhelm discovers all supported files recursively.

## Evaluate only changed files

```bash
eh evaluate --diff origin/main...HEAD --classify
```

Useful in CI to score only what changed in a PR.

## Read the output

```
myfile.py
  decision: marginal
  score:    0.55 (p78 — better than 78% of training corpus)
  confidence: high
  contributions:
    manifold_drift           0.13  (weight: 0.30, normalized: 0.43)
    manifold_alignment       0.12  (weight: 0.30, normalized: 0.40)
    token_entropy            0.07  (weight: 0.15, normalized: 0.46)
    compression_structure    0.14  (weight: 0.15, normalized: 0.92)
    ncd_exemplar_distance    0.09  (weight: 0.10, normalized: 0.92)
  directives:
    [low] reduce_complexity → MyClass (lines 7-50)
      #1 halstead_difficulty: contribution=-0.84, deviation=+1.6σ
```

**Score**: 0.0 (ideal) to 1.0 (worst). Lower is better.

**Percentile**: "p78" means this file scores better than 78% of the training corpus.

**Decision**:

| Decision | Hardcoded default | Meaning |
|----------|-------------------|---------|
| accept | score < 0.4 | Code quality is good |
| marginal | 0.4 ≤ score < 0.6 | Review directives, improve if straightforward |
| reject | score ≥ 0.6 | Quality issues need attention |

!!! note
    `eh init` generates `.eigenhelm.toml` with thresholds of 0.3/0.7. These override the hardcoded defaults above. Model-calibrated thresholds (from training corpus percentiles) also override when available.

**Directives**: Actionable suggestions with severity (`[high]`, `[medium]`, `[low]`) pointing to specific code locations.

**Regions**: When a file contains inline test code (Rust `#[cfg(test)]`, Python `class Test*`), eigenhelm shows a breakdown:

```
  regions:
    production (lines 1-80):  0.55 (p55)
    test (lines 81-270):      0.82 (p8)
```

This helps you see whether a bad score comes from production code or repetitive test patterns. See [Test code dilution](../concepts/dimensions.md#test-code-dilution) for details.

## Output formats

=== "Human (default)"

    ```bash
    eh evaluate myfile.py --classify
    ```

=== "JSON"

    ```bash
    eh evaluate myfile.py --format json
    ```

=== "SARIF"

    ```bash
    eh evaluate myfile.py --format sarif
    ```

    SARIF output integrates with GitHub Code Scanning and other static analysis dashboards.

## Initialize project config

```bash
eh init
```

Creates `.eigenhelm.toml` with sensible defaults. See [Configuration](configuration.md) for details.

## Set up for AI agents

Install the agent skill to give your coding agent the correct workflow:

```bash
# Via skills registry
npx skills add metacogdev/skills

# Or via eigenhelm CLI
eh skill --install
```

The skill teaches agents to evaluate after tests pass, apply obvious fixes for rejects, and stop after two passes — preventing the over-iteration trap where agents break working code to chase a score.

[Full agent integration guide](../integrations/agent-skills.md)

## Next steps

- [Understand the scoring dimensions](../concepts/dimensions.md)
- [Configure thresholds and models](configuration.md)
- [Set up AI agent integration](../integrations/agent-skills.md)
- [Add to your CI pipeline](../integrations/github-action.md)
