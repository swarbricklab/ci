# QXUB Checkout

Clones a repository to NCI (National Computational Infrastructure) and checks out a specific branch via QXUB.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `nci-user` | Yes | - | NCI username |
| `nci-project` | No | `a56` | NCI project allocation |
| `repository` | Yes | - | Repository name |
| `pr-number` | Yes | - | Pull request number |
| `run-id` | Yes | - | GitHub Actions run ID |
| `branch-ref` | Yes | - | Branch reference to checkout |

## What it does

1. **Clones repository** to NCI scratch space via QXUB copyq
2. **Checks out PR branch** on the NCI system

## Prerequisites

- **QXUB Runner**: Must run on a self-hosted runner with QXUB installed
- **NCI Access**: Valid NCI credentials and project allocation
- **SSH Keys**: Configured for GitHub repository access from NCI

## Example Usage

```yaml
name: NCI Checkout

on:
  pull_request:
    branches: [main]

jobs:
  nci-checkout:
    runs-on: qxub-runner
    steps:
      - name: Clone and checkout on NCI
        uses: swarbricklab/ci/qxub-checkout@main
        with:
          nci-user: ${{ secrets.NCI_USER }}
          repository: ${{ github.event.repository.name }}
          pr-number: ${{ github.event.pull_request.number }}
          run-id: ${{ github.run_id }}
          branch-ref: ${{ github.head_ref }}
```

## Directory Structure

The repository is cloned to:
```
/scratch/<nci-project>/<nci-user>/ci/<repository>/pr-<pr-number>/run-<run-id>/
```
