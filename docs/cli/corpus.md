# eh corpus

Manage training corpora — sync source files from TOML manifests.

## Usage

```bash
eh corpus sync MANIFEST_PATH OUTPUT_DIR [--force]
eh corpus sync --all DIRECTORY OUTPUT_DIR [--force]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `MANIFEST_PATH` | Path to the .toml manifest file |
| `OUTPUT_DIR` | Directory to materialize the corpus into |

## Options

| Option | Description |
|--------|-------------|
| `--all DIRECTORY` | Scan directory for all .toml manifests and sync each (mutually exclusive with `MANIFEST_PATH`) |
| `--force` | Re-download all targets even if already present |

## Corpus manifests

Manifests are TOML files describing where to find source code:

```toml
[corpus]
name = "elite-python"
language = "python"
class = "A"

[[target]]
name = "httpx"
url = "https://github.com/encode/httpx"
ref = "0.28.1"
include = ["httpx/**/*.py"]
exclude = ["tests/**", "docs/**"]
description = "Async/sync HTTP client with clean layered design"

[[target]]
name = "rich"
url = "https://github.com/Textualize/rich"
ref = "v13.9.4"
include = ["rich/**/*.py"]
exclude = ["tests/**"]
description = "Terminal formatting library with composable renderables"
```

Each `[[target]]` entry requires: `name`, `url` (https), `ref` (git tag/branch), `include` (glob patterns), and `description`. `exclude` is optional.

## Example

```bash
# Sync a single manifest
eh corpus sync corpora/lang-python.toml corpus/lang-python

# Sync all manifests in a directory
eh corpus sync --all corpora/ corpus/
```
