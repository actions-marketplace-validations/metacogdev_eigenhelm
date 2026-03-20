# eh evaluate

Evaluate source files against an eigenspace model.

## Usage

```bash
eh evaluate [OPTIONS] [PATHS...]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `PATHS` | File or directory paths to evaluate. Discovers files recursively. |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--language LANG` | _(auto)_ | Language override (required for stdin) |
| `--model PATH` | _(bundled)_ | Path to .npz eigenspace model |
| `--format {human,json,sarif}` | `human` | Output format |
| `--classify` | off | Show accept/marginal/reject labels |
| `--strict` | off | Treat marginal as reject (exit code 2) |
| `--lenient` | off | Treat marginal as accept (exit code 0) |
| `--diff RANGE` | _(none)_ | Evaluate only files changed in git revision range |
| `--accept-threshold N` | _(model)_ | Override accept threshold |
| `--reject-threshold N` | _(model)_ | Override reject threshold |
| `--rank` | off | Relative ranking mode: sort by score |
| `--bottom N` | _(none)_ | Highlight bottom N files in rank mode |
| `--bottom-pct N` | _(none)_ | Highlight bottom N% in rank mode |
| `--top-n N` | 3 | Top features per dimension in attribution |
| `--directive-threshold N` | 0.3 | Minimum score to generate directives |
| `--scorecard` | off | Per-repository scorecard (M1-M5, Q1-Q5) |

## Examples

```bash
# Evaluate a single file with classification
eh evaluate myfile.py --classify

# Evaluate changed files in a PR
eh evaluate --diff origin/main...HEAD --classify

# JSON output for scripting
eh evaluate src/ --format json

# SARIF for GitHub Code Scanning
eh evaluate src/ --format sarif > results.sarif

# Strict mode for CI
eh evaluate src/ --strict --classify

# Rank files, highlight worst 10%
eh evaluate src/ --rank --bottom-pct 10
```

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | All files accepted (or marginal in lenient mode) |
| 1 | At least one file marginal (default mode) |
| 2 | At least one file rejected (or marginal in strict mode) |
| 3 | Runtime or configuration error |
