# Configuration

eigenhelm uses `.eigenhelm.toml` for project-level configuration. Run `eh init` to generate a starter file.

## Threshold hierarchy

Settings are resolved in priority order:

1. **CLI flags** (`--accept-threshold`, `--reject-threshold`, `--strict`, `--lenient`)
2. **Config file** (`.eigenhelm.toml`)
3. **Model calibration** (empirical p25/p75 from training corpus)
4. **Hardcoded defaults** (accept=0.4, reject=0.6)

## Full config reference

```toml
# .eigenhelm.toml

# Path to a pre-trained eigenspace model (.npz)
# model = "models/eigenspace.npz"

# Default language override for all files
# language = "python"

# Global accept/reject thresholds
[thresholds]
accept = 0.4
reject = 0.6

# Treat all "warn" decisions as "reject" (useful for strict CI)
# strict = false

# Path-specific threshold overrides (last-match-wins)
[[paths]]
glob = "src/core/**"
[paths.thresholds]
accept = 0.3
reject = 0.5

[[paths]]
glob = "vendor/**"
[paths.thresholds]
accept = 0.6
reject = 0.9

# Map non-standard extensions to language keys
[language_overrides]
".jsx" = "javascript"
".tsx" = "typescript"
```

## Models

eigenhelm ships with bundled models for common use cases:

| Model | Languages | Use case |
|-------|-----------|----------|
| `general-polyglot-v1.npz` | Python, JS, TS, Go, Rust | General-purpose polyglot evaluation |
| `lang-python.npz` | Python | Python-specific evaluation |
| `lang-javascript.npz` | JavaScript | JavaScript-specific evaluation |
| `lang-typescript.npz` | TypeScript | TypeScript-specific evaluation |
| `lang-go.npz` | Go | Go-specific evaluation |
| `lang-rust.npz` | Rust | Rust-specific evaluation |

When no model is specified, eigenhelm uses the bundled polyglot model.

## Strict and lenient modes

```bash
# Strict: marginal → reject (exit code 1)
eh evaluate src/ --strict

# Lenient: marginal → accept (exit code 0)
eh evaluate src/ --lenient
```

In CI, `--strict` is recommended to prevent marginal code from merging.
