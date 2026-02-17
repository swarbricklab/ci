# Index Path Validation

Validates that paths referenced in an index CSV file are tracked by DVC.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `index-file` | No | `index.csv` | Path to the index CSV file |
| `check-columns` | Yes | - | Comma-separated list of column names to validate |

## What it does

1. **Reads the index CSV** and extracts paths from specified columns
2. **Lists DVC-tracked files** in the repository
3. **Validates** that all referenced paths are tracked by DVC
4. **Reports errors** with specific file and line locations

## Prerequisites

- **DVC**: Must be installed on the runner
- **Python 3**: For running the validation script

## Example Usage

```yaml
name: Validate Index

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

      - name: Validate index paths
        uses: swarbricklab/ci/index-path-validation@main
        with:
          index-file: index.csv
          check-columns: path,fastqs,he_image,cropped_image
```

## Supported Path Formats

The action handles various path formats:
- Relative paths: `data/sample1/file.txt`
- Paths with `./` prefix: `./data/sample1/file.txt`
- Directory paths: `data/sample1/`

## Ignored Values

The following values are ignored during validation:
- Empty strings
- `auto`, `n/a`, `na` (case-insensitive)
- `??`
