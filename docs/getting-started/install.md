# Installation

## uv (recommended)

```bash
uv tool install eigenhelm
```

With the HTTP server:

```bash
uv tool install "eigenhelm[serve]"
```

## pip

```bash
pip install eigenhelm
```

## From source

```bash
git clone https://github.com/metacogdev/eigenhelm.git
cd eigenhelm
uv sync --extra dev --extra serve
```

## Docker

```bash
docker build -t eigenhelm .
docker run --rm -v $(pwd):/code eigenhelm evaluate /code/myfile.py
```

## Verify installation

```bash
eh --version
```

## Requirements

- Python 3.11 or later
- Dependencies: tree-sitter, lizard, numpy, scipy (installed automatically)
