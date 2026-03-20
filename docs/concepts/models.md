# Models

eigenhelm models are `.npz` files containing a trained PCA eigenspace, exemplar vectors, and calibration data.

## Bundled models

| Model | Languages | PCs | Vectors | Use case |
|-------|-----------|-----|---------|----------|
| `general-polyglot-v1.npz` | Python, JS, TS, Go, Rust | 36 | 8,228 | General-purpose (default) |
| `lang-python.npz` | Python | — | — | Python-specific |
| `lang-javascript.npz` | JavaScript | — | — | JavaScript-specific |
| `lang-typescript.npz` | TypeScript | — | — | TypeScript-specific |
| `lang-go.npz` | Go | — | — | Go-specific |
| `lang-rust.npz` | Rust | — | — | Rust-specific |
| `pattern-cli.npz` | Mixed | — | — | CLI tool patterns |
| `baseline.npz` | Python | — | — | Baseline reference |

When no model is specified, eigenhelm uses the bundled polyglot model.

## Choosing a model

- **Language-specific models** are more discriminating for their target language
- **The polyglot model** works across all supported languages and is the best default
- **Custom models** can be trained on your own curated corpora for domain-specific evaluation

## Training a custom model

```bash
# Prepare a corpus manifest
cat > my-corpus.toml << 'EOF'
[corpus]
name = "my-team-best"
language = "python"
class = "A"

[[target]]
name = "my-code"
url = "https://github.com/my-org/my-repo"
ref = "main"
include = ["src/**/*.py"]
description = "Our best production code"
EOF

# Sync the corpus to a local directory
eh corpus sync my-corpus.toml corpus/my-team-best

# Train
eh train corpus/my-team-best --language python -o models/my-model.npz
```

See [`eh train`](../cli/train.md) for the full training reference.

## Model contents

Each `.npz` model contains:

- **PCA components**: The principal component matrix defining the quality manifold
- **Corpus statistics**: Mean and standard deviation of the training feature vectors
- **Calibration data**: Empirical score distribution (p25/p75 thresholds) from the training corpus
- **Exemplar refs**: Compressed code content from selected high-quality samples, used for NCD comparison
- **Metadata**: Language, corpus class, training date, file count
