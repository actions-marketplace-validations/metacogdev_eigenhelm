# Installation

## pip

```bash
pip install eigenhelm
```

With the HTTP server:

```bash
pip install "eigenhelm[serve]"
```

## uv (no venv required)

```bash
uv tool install eigenhelm
```

## From source

```bash
git clone https://github.com/metacogdev/eigenhelm.git
cd eigenhelm
uv sync --extra dev --extra serve
```

## Docker

The Docker image runs the evaluation server by default:

```bash
docker build -t eigenhelm .
docker run -p 8080:8080 eigenhelm
```

To use the CLI via Docker, override the entrypoint:

```bash
docker run --rm --entrypoint eh -v $(pwd):/code eigenhelm evaluate /code/myfile.py
```

## Verify installation

```bash
eh --version
```

## Requirements

- Python 3.11 or later
- Dependencies: tree-sitter, lizard, numpy, scipy (installed automatically)
