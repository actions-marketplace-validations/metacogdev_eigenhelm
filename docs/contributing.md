# Contributing

See [CONTRIBUTING.md](https://github.com/metacogdev/eigenhelm/blob/main/CONTRIBUTING.md) for the full contribution guide.

## Quick setup

```bash
git clone https://github.com/metacogdev/eigenhelm.git
cd eigenhelm
uv sync --extra dev --extra serve
```

## Run tests

```bash
# All tests
uv run pytest

# Fast tests only (unit + contract)
uv run pytest tests/unit tests/contract

# Lint
uv run ruff check .
```

## Code conventions

- Python 3.11+
- All value objects use `@dataclass(frozen=True)`
- Summary `all_passed` fields are computed `@property`, not manually set
- Zero new external dependencies — stdlib preferred
