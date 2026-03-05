# QXUB Cleanup

Cleans up temporary PR directories on NCI scratch space after a PR is merged.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `scratch-root` | Yes | Root directory for temp clones (e.g., `/scratch/a56/user/ci`) |
| `repository` | Yes | Repository name |
| `pr-number` | Yes | Pull request number |

## What it does

Removes the directory `{scratch-root}/{repository}/pr-{pr-number}` from NCI via `qxub exec`.

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
          scratch-root: /scratch/a56/${{ secrets.NCI_USER }}/ci
          repository: ${{ github.event.repository.name }}
          pr-number: ${{ github.event.pull_request.number }}
```
