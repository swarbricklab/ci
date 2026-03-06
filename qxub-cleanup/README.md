# QXUB Cleanup

Cleans up temporary PR directories on NCI scratch space after a PR is merged.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `nci-user` | Yes | - | NCI username |
| `nci-project` | No | `a56` | NCI project allocation |
| `repository` | Yes | - | Repository name |
| `pr-number` | Yes | - | Pull request number |

## What it does

Removes the directory `/scratch/{nci-project}/{nci-user}/ci/{repository}/pr-{pr-number}` from NCI via `qxub exec`.

## Example Usage

```yaml
name: Cleanup PR

on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    if: github.event.pull_request.merged == true
    runs-on: [self-hosted, nci]

    steps:
      - name: Cleanup NCI scratch
        uses: swarbricklab/ci/qxub-cleanup@main
        with:
          nci-user: ${{ secrets.NCI_USER }}
          nci-project: a56
          repository: ${{ github.event.repository.name }}
          pr-number: ${{ github.event.pull_request.number }}
```
