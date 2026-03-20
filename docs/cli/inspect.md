# eh inspect

Inspect a saved model's metadata and statistics.

## Usage

```bash
eh inspect [OPTIONS] MODEL_PATH
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--json` | off | Output as JSON instead of plain text |

## Example

```bash
eh inspect models/lang-python.npz
```

Displays: language, corpus class, principal component count, training file count, calibration thresholds, and score distribution statistics.

```bash
# Machine-readable output
eh inspect models/lang-python.npz --json
```
