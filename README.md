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

### index-path-validation

Validates that paths referenced in an index CSV file (e.g., `index.csv`) are tracked by DVC. Supports configurable column names to work with different registry schemas.

**Inputs:**
- `index-file` (optional, default: `index.csv`): Path to the index CSV file
- `check-columns` (required): Comma-separated list of column names to validate (e.g., `path,fastqs,he_image`)

**Example usage:**
```yaml
- name: Checkout PR branch
  uses: actions/checkout@v4
  with:
    ref: ${{ github.head_ref }}
    fetch-depth: 0

- name: Validate index paths
  uses: swarbricklab/ci/index-path-validation@main
  with:
    check-columns: path,fastqs,he_image,cropped_image,alignment_image,loupe_alignment
```

### tree-snapshot-validation

Ensures that a tree snapshot file (e.g., `tree.txt`) stays synchronized with DVC-tracked files. Generates a current snapshot and compares it against the committed version.

**Inputs:**
- `tree-file` (optional, default: `tree.txt`): Path to the tree snapshot file

**Example usage:**
```yaml
- name: Checkout PR branch
  uses: actions/checkout@v4
  with:
    ref: ${{ github.head_ref }}
    fetch-depth: 0

- name: Validate tree snapshot
  uses: swarbricklab/ci/tree-snapshot-validation@main
```

## Requirements

- **dvc-remote-check**: Requires DVC, gsutil, and gh CLI installed on the runner
- **qxub-checkout**: Requires qxub installed and configured on the runner
- **index-path-validation**: Requires DVC and Python 3 installed on the runner
- **tree-snapshot-validation**: Requires DVC installed on the runner

## License

MIT
