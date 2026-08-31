# DVC Remote Check

Posts the DVC diff for a PR as a comment, then validates that every DVC-tracked
file is present in **one or more** remotes — failing the check if any validated
remote is missing data.

Repos that keep a canonical store plus a mirror (e.g. an R2 bucket mirrored to
NCI) should pass **both** remotes via `dvc-remotes`, so the mirror cannot
silently drift out of sync and break downstream consumers that resolve imports
from it.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `base-ref` | No | `origin/main` | Base git reference to diff against |
| `dvc-remotes` | No | `''` | Space-separated list of remotes to validate (e.g. `bcarc-wts nci`). Every listed remote must contain all tracked data or the check fails |
| `dvc-remote` | No | `gs` | Single remote name. Back-compat only; **ignored when `dvc-remotes` is set** |
| `pr-number` | Yes | - | Pull request number for posting comments |
| `github-token` | Yes | - | Token for posting PR comments |

Use `dvc-remotes` for new workflows. `dvc-remote` remains for repos with a
single remote and is equivalent to passing that one name in `dvc-remotes`.

## What it does

1. **Installs remote credentials** via `dt auth credentials install -v`, when
   `dt` is on the runner (warns and continues if not).
2. **Posts the DVC diff** — `dt diff --old <base-ref> --new HEAD` between the
   base ref and HEAD, as a PR comment. The diff compares the `.dvc` hashes
   recorded in each git ref, so it is remote-independent; only the first remote
   is set as default to satisfy DVC. A failing `dt diff` fails the job.
3. **Validates data presence in each remote** — for every remote in turn:
   `dvc remote default <remote>` then `dvc data status --not-in-remote
   --granular`. Missing files are collected per remote into a single PR comment,
   and the check **fails** if any remote is short.

The diff is compared against git refs rather than the workspace because CI
checkouts don't materialize DVC-tracked data.

### Comment size

Both comments are truncated to 60000 bytes (GitHub caps comment bodies at
65536), cutting on a line boundary so a multi-byte character isn't split. A
comment that fails to post is downgraded to a warning — it must never mask the
real signal, which is the job's exit status from the data-presence check.

## Prerequisites

- **DVC** and **`dt`** on the runner (`dt` provides `dt diff` and credential
  install; the swarbricklab workflows use the `qxub-runner` self-hosted runner).
- **`gh` CLI** for posting PR comments.
- Credentials for each validated remote reachable by `dt auth credentials
  install` — see [Authentication Guide](../docs/authentication.md).
- `pull-requests: write` permission on the job, for the comments.

## Example Usage

```yaml
name: DVC Remote Check

on:
  pull_request:
    branches: [main]

jobs:
  dvc-check:
    if: ${{ github.event.pull_request.head.repo.fork == false }}
    runs-on: qxub-runner
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
          fetch-depth: 0

      - name: Check DVC remotes
        uses: swarbricklab/ci/dvc-remote-check@main
        with:
          dvc-remotes: bcarc-wts nci
          pr-number: ${{ github.event.pull_request.number }}
          github-token: ${{ github.token }}
```

## Outputs

- **PR comment**: the DVC diff (truncated if oversized).
- **PR comment**: per-remote list of files missing from remote storage, when any
  are missing.
- **Failure**: the check fails if DVC-tracked files are absent from any
  validated remote, or if `dt diff` / `dvc data status` errors.
