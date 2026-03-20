# GitHub Action

eigenhelm is available as a GitHub Action for CI integration.

## Basic usage

```yaml
- uses: actions/checkout@v4
- uses: metacogdev/eigenhelm@v0
  with:
    paths: "src/"
```

## PR diff mode

Evaluate only files changed in a pull request:

```yaml
name: Code Quality
on: [pull_request]

jobs:
  eigenhelm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: metacogdev/eigenhelm@v0
        with:
          diff: origin/main...HEAD
```

## Strict mode

Fail the check if any file scores marginal or worse:

```yaml
- uses: metacogdev/eigenhelm@v0
  with:
    diff: origin/main...HEAD
    strict: "true"
```

## SARIF upload

Send results to GitHub Code Scanning:

```yaml
- uses: metacogdev/eigenhelm@v0
  with:
    diff: origin/main...HEAD
    sarif-upload: "true"
```

## All inputs

| Input | Default | Description |
|-------|---------|-------------|
| `paths` | `"."` | Files or directories to evaluate |
| `model` | _(bundled)_ | Path to .npz model file |
| `diff` | _(none)_ | Git revision range for changed files only |
| `format` | `"human"` | Output format: `human`, `json`, `sarif` |
| `classify` | `"true"` | Show accept/marginal/reject labels |
| `strict` | `"false"` | Treat marginal as reject |
| `lenient` | `"false"` | Treat marginal as accept |
| `version` | _(latest)_ | eigenhelm version to install |
| `sarif-upload` | `"false"` | Upload SARIF to GitHub Code Scanning |

## Outputs

| Output | Description |
|--------|-------------|
| `sarif-file` | Path to SARIF file (when applicable) |
| `exit-code` | Exit code from evaluation |
