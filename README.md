# ticketmaster

Minimal Flask API skeleton with health and version endpoints.

## Prerequisites

- Python 3.12+
- Docker (for container builds)

## Run locally

Dev server:

```bash
pip install -r requirements.txt
flask --app app run --port 8000
```

Production-style server:

```bash
gunicorn -w 2 -b 0.0.0.0:8000 wsgi:app
```

## Test

```bash
pytest
```

## Endpoints

- `GET /health` → `{"status": "ok"}`
- `GET /version` → `{"version": "<IMAGE_TAG or unknown>"}`

## Deployed URL

Through the Istio ingress at `https://api.vamsipothireddy.com/ticketmaster`:

- Health: `https://api.vamsipothireddy.com/ticketmaster/health`
- Version: `https://api.vamsipothireddy.com/ticketmaster/version`

The image tag is the git commit SHA, injected as `IMAGE_TAG` by the Helm chart.

## CI

`.github/workflows/ci.yml` calls the shared reusable pipeline in
`VamsiPothireddy-Dev/github-actions`. Repo secrets (`DOCKERHUB_USERNAME`,
`DOCKERHUB_TOKEN`, `K8S_REPO_TOKEN`, etc.) must be configured on this repo.
