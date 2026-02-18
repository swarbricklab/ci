# DVC Remote Check

Checks DVC remote status, calculates diff against a base branch, and validates that all data is present in remote storage.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `cache-bucket` | Yes | - | GCS bucket for DVC site cache (format: `gs://bucket-name/path`) |
| `base-ref` | No | `origin/main` | Base git reference to compare against |
| `dvc-remote` | No | `gs` | DVC remote name |
| `pr-number` | Yes | - | Pull request number for posting comments |
| `github-token` | Yes | - | GitHub token for posting PR comments |

## What it does

1. **Syncs DVC site cache** from a GCS bucket to speed up operations
2. **Calculates DVC diff** between the base branch and HEAD, posts as PR comment
3. **Validates remote data** - ensures all DVC-tracked files exist in the remote storage

## Prerequisites

- **GCP Authentication**: See [Authentication Guide](../docs/authentication.md)
- **DVC**: Must be installed on the runner
- **gsutil**: For syncing the site cache from GCS
- **gh CLI**: For posting PR comments (included in GitHub-hosted runners)

## Example Usage

```yaml
name: DVC Remote Check

on:
  pull_request:
    branches: [main]

jobs:
  dvc-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install DVC
        run: pip install dvc[s3]  # or dvc[gs] for GCS remotes

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Check DVC remote
        uses: swarbricklab/ci/dvc-remote-check@main
        with:
          cache-bucket: ${{ secrets.DVC_CACHE_BUCKET }}
          dvc-remote: your-remote-name
          pr-number: ${{ github.event.pull_request.number }}
          github-token: ${{ github.token }}
```

## Outputs

- **PR Comment**: DVC diff posted as a comment (or link to artifact if too large)
- **Artifact**: `dvc-diff.md` uploaded as workflow artifact
- **Failure**: Workflow fails if DVC-tracked files are missing from remote
