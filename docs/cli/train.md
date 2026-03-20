# eh train

Train a new eigenspace model from a corpus directory.

## Usage

```bash
eh train CORPUS_DIR --language LANG -o OUTPUT [OPTIONS]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `CORPUS_DIR` | Root directory of the code corpus (positional, required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output PATH` | required | Output .npz model path |
| `--language LANG` | required | Target language key (e.g., `python`, `go`, `multi`) |
| `--corpus-class {A,B}` | `A` | Corpus quality class |
| `--n-components INT` | _(auto)_ | Explicit number of principal components |
| `--variance-threshold FLOAT` | `0.90` | Min cumulative explained variance for auto-select |
| `--version TEXT` | _(package version)_ | Model version string |
| `--force` | off | Overwrite existing output file |

## Example

```bash
# Sync a corpus from manifest
eh corpus sync corpora/my-corpus.toml corpus/my-corpus

# Train
eh train corpus/my-corpus --language python -o models/my-model.npz

# Verify
eh inspect models/my-model.npz
```

## Corpus classes

| Class | Description |
|-------|-------------|
| A | Single-language — curated, reviewed, exemplary code in one language |
| B | Cross-language pattern — structural patterns across multiple languages |
