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
  --corpus-a corpus/elite-python \
  --corpus-b corpus/random-python
```

Outputs: effect size (Cohen's d), U statistic, p-value, and a pass/fail determination.
