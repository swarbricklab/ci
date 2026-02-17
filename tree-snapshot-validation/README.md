# Tree Snapshot Validation

Ensures that a tree snapshot file stays synchronized with DVC-tracked files.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `tree-file` | No | `tree.txt` | Path to the tree snapshot file |

## What it does

1. **Generates current tree snapshot** using `dvc list --dvc-only --tree`
2. **Compares** the generated snapshot against the committed `tree.txt`
3. **Fails** if there are any differences

## Prerequisites

- **DVC**: Must be installed on the runner

## Example Usage

```yaml
name: Validate Tree

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
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
        run: pip install dvc

      - name: Validate tree snapshot
        uses: swarbricklab/ci/tree-snapshot-validation@main
```

## Regenerating the Tree File

If the validation fails, regenerate and commit the tree file:

```bash
dvc list --dvc-only --tree . > tree.txt
git add tree.txt
git commit -m "Update tree.txt"
```

## Purpose

The tree snapshot provides a human-readable record of DVC-tracked files in the repository. It serves as:
- Documentation of the data structure
- A change detection mechanism for PRs
- An audit trail of data changes over time
