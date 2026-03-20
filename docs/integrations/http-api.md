# HTTP API

eigenhelm includes a FastAPI-based evaluation server for real-time scoring.

## Start the server

```bash
eh serve --model models/general-polyglot-v1.npz --host 0.0.0.0 --port 8080
```

Requires the `serve` extra: `uv tool install "eigenhelm[serve]"`

## Endpoints

### `GET /health`

Liveness probe. Always returns 200.

```bash
curl http://localhost:8080/health
```

```json
{"status": "healthy", "model_loaded": true}
```

### `GET /ready`

Readiness probe. Returns 503 during startup.

```bash
curl http://localhost:8080/ready
```

```json
{"status": "ready", "model_loaded": true}
```

### `POST /v1/evaluate`

Evaluate a single code unit.

```bash
curl -X POST http://localhost:8080/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "source": "def add(a, b):\n    return a + b\n",
    "language": "python"
  }'
```

**Request body:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `source` | string | yes | — | Source code to evaluate |
| `language` | string | yes | — | Language identifier |
| `file_path` | string | no | — | Optional file path for reporting |
| `top_n` | int | no | 3 | Top features per dimension in attribution |
| `directive_threshold` | float | no | 0.3 | Minimum score to generate directives |

**Response:**

```json
{
  "decision": "accept",
  "score": 0.32,
  "structural_confidence": "high",
  "percentile": 68.5,
  "percentile_available": true,
  "violations": [
    {
      "dimension": "manifold_drift",
      "raw_value": 2.5,
      "normalized_value": 0.6,
      "contribution": 0.25
    }
  ],
  "contributions": [
    {
      "dimension": "manifold_drift",
      "normalized_value": 0.6,
      "weight": 0.30,
      "weighted_contribution": 0.18
    }
  ],
  "attribution": {
    "dimensions": [...],
    "directives": [
      {
        "category": "reduce_complexity",
        "dimension": "manifold_drift",
        "normalized_score": 0.8,
        "severity": "high",
        "source_location": {
          "code_unit_name": "MyClass",
          "start_line": 10,
          "end_line": 25
        }
      }
    ],
    "top_n": 3,
    "directive_threshold": 0.3,
    "vocabulary_version": "v1"
  }
}
```

### `POST /v1/evaluate/batch`

Evaluate multiple code units in a single request.

```bash
curl -X POST http://localhost:8080/v1/evaluate/batch \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {"source": "def add(a, b):\n    return a + b\n", "language": "python"},
      {"source": "const add = (a, b) => a + b;\n", "language": "javascript"}
    ]
  }'
```

**Request body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `files` | array | yes | Array of evaluation request objects |

**Response:**

```json
{
  "results": [...],
  "summary": {
    "overall_decision": "warn",
    "total_files": 2,
    "accepted": 1,
    "warned": 1,
    "rejected": 0,
    "mean_score": 0.42
  }
}
```

## Error responses

| Status | Body | Cause |
|--------|------|-------|
| 422 | `{"error": "validation_error", "detail": [...]}` | Invalid request body |
| 413 | `{"error": "request_too_large", "detail": "..."}` | Source exceeds size limit (1 MB per file, 10 MB per request) |
| 504 | `{"error": "evaluation_timeout", "detail": "..."}` | Evaluation exceeded 30s timeout |

## Docker

```bash
docker build -t eigenhelm .
docker run -p 8080:8080 eigenhelm
```

The image entrypoint is `eigenhelm-serve` with default flags `--host 0.0.0.0 --port 8080`.
