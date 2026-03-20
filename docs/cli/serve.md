# eh serve

Run the evaluation HTTP server.

## Usage

```bash
eh serve [OPTIONS]
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--model PATH` | _(bundled)_ | Path to .npz eigenspace model |
| `--host HOST` | `0.0.0.0` | Bind address |
| `--port PORT` | `8080` | Bind port |
| `--timeout-graceful-shutdown INT` | `30` | Seconds to wait for in-flight requests on SIGTERM |

## Example

```bash
eh serve --model models/general-polyglot-v1.npz --host 0.0.0.0 --port 8080
```

Requires the `serve` extra: `pip install "eigenhelm[serve]"`

See [HTTP API](../integrations/http-api.md) for endpoint documentation.
