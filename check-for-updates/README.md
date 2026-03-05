# Check for Updates

Checks for available updates and posts the status to a PR comment.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `pr-number` | Yes | - | Pull request number for posting comments |
| `github-token` | Yes | - | GitHub token for posting PR comments |

## What it does

1. **Installs credentials** via `dt auth credentials install` if `dt` is available
2. **Checks for updates** using `dt updates --status`
3. **Posts results** as a PR comment

This action always passes regardless of whether updates are available — it's informational only.

## Prerequisites

- **dt CLI**: Must be installed on the runner
- **gh CLI**: For posting PR comments (included in GitHub-hosted runners)

## Example Usage

```yaml
name: Check for Updates

on:
  pull_request:
    branches: [main]

jobs:
  check-updates:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4

      - name: Check for updates
        uses: swarbricklab/ci/check-for-updates@main
        with:
          pr-number: ${{ github.event.pull_request.number }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Output

Posts a PR comment with the update status from `dt updates --status`.
