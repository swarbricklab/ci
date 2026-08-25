# QXUB Checkout

Clones a repository to NCI (National Computational Infrastructure) and checks out a specific branch via QXUB.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `nci-user` | Yes | - | NCI username |
| `nci-project` | No | `a56` | NCI project allocation |
| `repository` | Yes | - | Repository name |
| `pr-number` | No | `''` | Pull request number. When empty the workspace is keyed on `run-id` alone and the missing-DVC comment is skipped |
| `run-id` | Yes | - | GitHub Actions run ID |
| `branch-ref` | Yes | - | Branch reference to checkout |
| `workspace` | No | `''` | Explicit workspace path under `ci/<repository>/`, overriding the `pr-`/`run-` scheme |
| `dvc-mod` | No | `''` | NCI module providing `dt`/`dvc`. When set, clones with `dt clone` so the workspace uses the shared DVC cache. Empty means a plain `git clone` |
| `github-token` | No | `''` | Token for the DVC-pipeline check and missing-DVC PR comment |

## What it does

1. **Clones repository** to NCI scratch space via QXUB copyq
2. **Checks out PR branch** on the NCI system

## DVC repositories: set `dvc-mod`

By default the clone is a plain `git clone`, which leaves DVC unconfigured. The
workspace then falls back to a repository-local `.dvc/cache` that starts empty,
so every run re-fetches the repo's entire data set from the source remotes,
re-hashes it from cold, and the cleanup job deletes it again.

Passing `dvc-mod` switches the clone to `dt clone`, which configures:

- `cache.dir` -> the shared per-project cache, so data is hardlinked rather than copied
- `core.site_cache_dir` -> a persistent path, so DVC's hash state survives between runs
- the local remote -> the `/g/data` mirror

Measured on `bcarc_portal`, whose report imports total ~76 GB across ~9,800
files: materialising that tree took **2m36s** from the shared cache, against
**22m50s** for the fetch-and-copy a plain clone forces.

```yaml
      - uses: swarbricklab/ci/qxub-checkout@main
        with:
          nci-user: ${{ secrets.USER_NAME }}
          repository: ${{ github.event.repository.name }}
          pr-number: ${{ github.event.pull_request.number }}
          run-id: ${{ github.run_id }}
          branch-ref: ${{ github.head_ref }}
          dvc-mod: ${{ secrets.DVC_MOD }}
```

Leave it unset for repositories without DVC — the action supports those, and
reports their absence through the `has_dvc` output.

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
