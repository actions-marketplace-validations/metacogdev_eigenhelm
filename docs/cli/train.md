# eh train

Train a new eigenspace model from a corpus directory.

## Usage

```bash
eh train [OPTIONS]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--corpus PATH` | required | Path to synced corpus directory |
| `--language LANG` | required | Target language |
| `--output PATH` | required | Output .npz model path |
| `--corpus-class {A,B,C}` | `A` | Corpus quality class |
| `--min-files N` | 10 | Minimum files required to train |

## Example

```bash
# Sync a corpus from manifest
eh corpus sync corpora/my-corpus.toml

# Train
eh train --corpus corpus/my-corpus --language python --output models/my-model.npz

# Verify
eh inspect models/my-model.npz
```

## Corpus classes

| Class | Description |
|-------|-------------|
| A | Elite — curated, reviewed, exemplary code |
| B | Good — production code from quality projects |
| C | Mixed — broad collection, mixed quality |

Higher-class corpora produce more discriminating models.
