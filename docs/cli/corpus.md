# eh corpus

Manage training corpora — sync source files from TOML manifests.

## Usage

```bash
eh corpus sync MANIFEST_PATH
```

## Corpus manifests

Manifests are TOML files describing where to find source code:

```toml
[corpus]
name = "elite-python"
language = "python"
class = "A"

[[corpus.sources]]
type = "github"
repo = "org/repo"
branch = "main"
paths = ["src/"]

[[corpus.sources]]
type = "local"
path = "/path/to/code"
```

## Example

```bash
eh corpus sync corpora/elite-python.toml
```

Downloads/copies source files to `corpus/elite-python/` for training.
