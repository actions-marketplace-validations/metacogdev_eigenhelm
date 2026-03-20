# eh harness

Run a statistical comparison harness between two code sets using Mann-Whitney U tests.

## Usage

```bash
eh harness [OPTIONS]
```

## Purpose

The harness evaluates whether one corpus of code is statistically distinguishable from another in quality — used to validate that a model can discriminate between high and low-quality code.

## Example

```bash
eh harness --model models/lang-python.npz \
  --before corpus/elite-python \
  --after corpus/random-python
```

Outputs: mean/median scores per corpus, delta, Mann-Whitney U statistic, p-value, and significance at alpha=0.05. Use `--json` for machine-readable output.
