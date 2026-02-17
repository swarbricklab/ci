---
name: ci-setup
description: Set up CI workflows in swarbricklab repositories using reusable GitHub Actions. Handles DVC remote checks, index validation, tree snapshots, and NCI/QXUB checkout. Includes GCP Workload Identity Federation authentication patterns.
---

# CI Setup

Read [docs/authentication.md](../../../docs/authentication.md) first for GCP auth.

## Actions

| Action | README |
|--------|--------|
| dvc-remote-check | [dvc-remote-check/README.md](../../../dvc-remote-check/README.md) |
| index-path-validation | [index-path-validation/README.md](../../../index-path-validation/README.md) |
| qxub-checkout | [qxub-checkout/README.md](../../../qxub-checkout/README.md) |
| tree-snapshot-validation | [tree-snapshot-validation/README.md](../../../tree-snapshot-validation/README.md) |

## Org Secrets

- `WIF_PROVIDER` - Workload Identity Federation provider
- `SERVICE_ACCOUNT` - GCP service account email

## Quick Start

```yaml
permissions:
  contents: read
  pull-requests: write
  id-token: write

steps:
  - uses: google-github-actions/auth@v2
    with:
      workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
      service_account: ${{ secrets.SERVICE_ACCOUNT }}
  - uses: google-github-actions/setup-gcloud@v2
  - uses: swarbricklab/ci/<action>@main
```
