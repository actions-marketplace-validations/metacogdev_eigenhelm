# eh init

Generate a starter `.eigenhelm.toml` with sensible defaults.

## Usage

```bash
eh init [OPTIONS]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--force` | off | Overwrite existing `.eigenhelm.toml` |
| `--output PATH` | `.` | Directory to write config into |

## Example

```bash
eh init
```

Creates `.eigenhelm.toml` and `.eigenhelm/` cache directory. Adds `.eigenhelm/` to `.gitignore` (creates the file if it doesn't exist).
