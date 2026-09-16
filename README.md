# GitHub Actions Library

Reusable GitHub Actions for common CI/CD workflows in the swarbricklab organization.

## Actions

| Action | Description |
|--------|-------------|
| [dvc-remote-check](dvc-remote-check/) | Post the PR DVC diff and validate tracked data is present in one or more remotes |
| [qxub-checkout](qxub-checkout/) | Clone repository to NCI and checkout branch via QXUB |
| [index-path-validation](index-path-validation/) | Validate that index CSV references DVC-tracked paths |
| [gussid-schema-validation](gussid-schema-validation/) | Validate GUSSIDs in an index CSV against the GUSSID schema |
| [tree-snapshot-validation](tree-snapshot-validation/) | Ensure tree snapshot is synchronized with DVC files |

## Documentation

- [Authentication Guide](docs/authentication.md) - GCP auth with Workload Identity Federation
- [Self-Hosted Runners](docs/runners.md) - GCP runner infrastructure
- [Creating Actions](docs/creating-actions.md) - How to add new actions

## Quick Start

Most actions that interact with GCP require authentication. Add these steps before using the action:

```yaml
jobs:
  your-job:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Required for WIF

    steps:
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
```

See each action's README for complete examples.

## License

MIT
