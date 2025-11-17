# GitHub Actions Library

This repository contains reusable GitHub Actions for common CI/CD workflows.

## Actions

### dvc-remote-check

Checks DVC remote status, calculates diff against a base branch, and validates that all data is present in remote storage.

**Inputs:**
- `cache-bucket` (required): GCS bucket for DVC site cache (format: `gs://bucket-name/path`)
- `base-ref` (optional, default: `origin/main`): Base git reference to compare against
- `dvc-remote` (optional, default: `gs`): DVC remote name
- `pr-number` (required): Pull request number for posting comments
- `github-token` (required): GitHub token for posting PR comments

**Example usage:**
```yaml
- name: Checkout PR branch
  uses: actions/checkout@v4
  with:
    ref: ${{ github.head_ref }}
    fetch-depth: 0

- name: Check DVC remote
  uses: swarbricklab/ci/dvc-remote-check@main
  with:
    cache-bucket: gs://cicd-demo-remote-state/site-cache
    pr-number: ${{ github.event.pull_request.number }}
    github-token: ${{ github.token }}
```

### qxub-checkout

Clones a repository to NCI via QXUB and checks out a specific branch.

**Inputs:**
- `nci-user` (required): NCI username
- `nci-project` (optional, default: `a56`): NCI project allocation
- `repository` (required): Repository name
- `pr-number` (required): Pull request number
- `run-id` (required): GitHub Actions run ID
- `branch-ref` (required): Branch reference to checkout
- `dvc-env` (optional, default: `dvc3`): DVC environment name on NCI

**Example usage:**
```yaml
- name: Clone and checkout on NCI
  uses: swarbricklab/ci/qxub-checkout@main
  with:
    nci-user: ${{ secrets.NCI_USER }}
    repository: ${{ github.event.repository.name }}
    pr-number: ${{ github.event.pull_request.number }}
    run-id: ${{ github.run_id }}
    branch-ref: ${{ github.head_ref }}
```

## Requirements

- **dvc-remote-check**: Requires DVC, gsutil, and gh CLI installed on the runner
- **qxub-checkout**: Requires qxub installed and configured on the runner

## License

MIT
