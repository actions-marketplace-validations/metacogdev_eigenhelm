# Scoring Dimensions

eigenhelm scores code across five dimensions. Each measures a different aspect of code quality, and together they produce a holistic assessment.

## Manifold drift

**Weight: 0.30** | Source: PCA reconstruction error

Measures how far a file's structural fingerprint sits from the learned code quality manifold. High drift means the code has unusual structural properties not seen in the training corpus.

**What drives high drift:**

- Unusual AST patterns (deeply nested conditionals, atypical class structures)
- Code that doesn't resemble any category in the training corpus
- Generated code with repetitive boilerplate

## Manifold alignment

**Weight: 0.30** | Source: PCA projection onto quality axes

Measures how well the code aligns with the principal directions of quality variation learned during training. Good alignment means the code varies from the corpus mean in the same directions that high-quality code does.

**What drives poor alignment:**

- Metric combinations rarely seen in quality code (e.g., high complexity + low vocabulary)
- Structural patterns orthogonal to the quality manifold

## Token entropy

**Weight: 0.15** | Source: Shannon entropy of byte stream

Measures the information density of the source code's byte stream. The normalized score is `1.0 - (entropy / 8.0)`, where 8.0 bits is the theoretical maximum for byte-level entropy. Lower entropy (more repetitive code) produces a higher score (worse).

This is a monotonic penalty — only low entropy is penalized. High-entropy code scores well on this dimension.

**What drives poor entropy scores:**

- Highly repetitive code (copy-pasted blocks, boilerplate)
- Files with large amounts of duplicated structure

## Compression structure

**Weight: 0.15** | Source: Birkhoff aesthetic measure

Applies the [Birkhoff aesthetic measure](https://en.wikipedia.org/wiki/Birkhoff%27s_aesthetic_measure) — an information-theoretic ratio of order to complexity:

$$M_Z = \frac{N \cdot H - K}{N \cdot H}$$

Where N = raw bytes, H = entropy (bits/byte), K = compressed bytes (zlib).

High values indicate the code has significant redundancy that compression can exploit — often a sign of structural repetition.

!!! note "Small files"
    Files under ~80 lines almost always score high on this dimension due to insufficient statistical mass. Directives from compression structure are capped at medium severity for small files.

## NCD exemplar distance

**Weight: 0.10** | Source: Normalized Compression Distance

Measures how similar the code is to the nearest high-quality exemplar stored in the model, using [Normalized Compression Distance](https://en.wikipedia.org/wiki/Normalized_compression_distance):

$$NCD(x, y) = \frac{C(xy) - \min(C(x), C(y))}{\max(C(x), C(y))}$$

Low NCD means the code structurally resembles a known good example. High NCD means it's unlike anything in the exemplar set.

## Test code dilution

When a source file contains both production code and inline test code (e.g., Rust `#[cfg(test)]` modules, Python `class TestFoo` blocks), the test code's structural signature can dominate the overall score. Repetitive test assertions, setup/teardown patterns, and boundary enumeration inflate manifold drift and compression metrics — masking genuine improvements to the production code.

eigenhelm detects inline test code and reports a **region breakdown** alongside the overall score:

```
myfile.rs
  decision: reject
  score:    0.72 (p19)
  regions:
    production (lines 1-80):   0.55 (p55)
    test (lines 81-270):       0.82 (p8)
```

The overall score is unchanged. The region breakdown shows that the production code (0.55) is substantially better than the overall score suggests — the test code (0.82) is pulling it up.

**Best practices:**

- In languages where tests are in separate files (Go `_test.go`, Java conventions), this isn't an issue — each file gets its own score.
- For Rust and Python where inline tests are common, use the region breakdown to assess production code quality independently.
- In CI, you can extract the production-only score from JSON output: `jq '.results[0].regions[] | select(.label == "production") | .score'`

**Currently detected patterns:**

| Language | Pattern |
|----------|---------|
| Rust | `#[cfg(test)] mod tests { ... }` |
| Python | `class Test*`, top-level `def test_*` |

## Weight configurations

Weights adjust based on available data:

| Scenario | Drift | Alignment | Entropy | Compression | NCD |
|----------|-------|-----------|---------|-------------|-----|
| Model + exemplars | 0.30 | 0.30 | 0.15 | 0.15 | 0.10 |
| Model only | 0.35 | 0.35 | 0.15 | 0.15 | 0.00 |
| Exemplars only | 0.00 | 0.00 | 0.30 | 0.30 | 0.40 |
| Neither (fallback) | 0.00 | 0.00 | 0.50 | 0.50 | 0.00 |
