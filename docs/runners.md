# Self-Hosted Runners

The organization uses self-hosted GitHub Actions runners on GCP for specialized workloads.

## Available Runners

| Label | Purpose |
|-------|---------|
| `qxub-runner` | NCI/QXUB operations |

## When to Use

Use self-hosted runners (`runs-on: qxub-runner`) for:
- Actions that require QXUB/NCI access
- Workflows needing pre-installed tools (qxub, gcloud SDK)

Use GitHub-hosted runners (`runs-on: ubuntu-latest`) for:
- Standard CI tasks
- Actions that only need GCP API access (via WIF)

## Runner Image

- Image: `ghcr.io/swarbricklab/qxub-runner:stable`
- Base: Ubuntu 20.04 (required for OpenSSL 1.1.1 compatibility)
- Preinstalled: qxub, gcloud SDK, SSH defaults

## Authentication

Self-hosted runners authenticate to GCP using the same WIF pattern. See [authentication.md](authentication.md).

## Infrastructure

Runners are managed in the `swarbricklab/qxub` repository.
