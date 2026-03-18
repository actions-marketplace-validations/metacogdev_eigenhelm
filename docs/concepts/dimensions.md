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

Measures the information density of the source code. Well-written code tends to have moderate entropy — not too repetitive (low entropy) and not too noisy (high entropy).

The normalized penalty is `1.0 - (entropy / 8.0)`, so lower entropy (more repetitive) scores worse.

**What drives poor entropy:**

- Highly repetitive code (copy-pasted blocks)
- Extremely terse or obfuscated code

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

## Weight configurations

Weights adjust based on available data:

| Scenario | Drift | Alignment | Entropy | Compression | NCD |
|----------|-------|-----------|---------|-------------|-----|
| Model + exemplars | 0.30 | 0.30 | 0.15 | 0.15 | 0.10 |
| Model only | 0.35 | 0.35 | 0.15 | 0.15 | 0.00 |
| Exemplars only | 0.00 | 0.00 | 0.30 | 0.30 | 0.40 |
| Neither (fallback) | 0.00 | 0.00 | 0.50 | 0.50 | 0.00 |
