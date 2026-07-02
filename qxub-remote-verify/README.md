# QXUB Remote Verify

Verify DVC **remote** blob integrity on NCI via QXUB using `dt remote verify`.
Hashes every blob in the remote's store and compares it to the md5 implied by
its path, catching silent corruption and the truncated/partial blobs left behind
when a transfer is interrupted (e.g. a push hitting a walltime limit). Reads
blobs directly from the store — **no `dt pull`**.

Uses `dt remote verify`'s incremental ledger (`<remote>/.dt-verify/`): PR runs
re-hash only blobs new since the last pass; a scheduled `full: true` run re-hashes
everything.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `nci-user` | Yes | - | NCI username |
| `nci-project` | No | `a56` | NCI project allocation |
| `repository` | Yes | - | Repository name |
| `pr-number` | Yes | - | PR number, or a label (e.g. `scheduled`) for non-PR runs |
| `run-id` | Yes | - | GitHub Actions run ID |
| `branch-ref` | Yes | - | Branch/ref to clone (for `.dvc/config` remote resolution) |
| `remote` | No | `''` | Remote name to verify. Empty = default remote. **Must resolve to a local path** (gdata/SSH; not `s3://`) |
| `full` | No | `false` | Ignore/rebuild the ledger and re-hash every blob (scheduled deep sweep) |
| `jobs` | No | `16` | Hashing threads (`dt remote verify -j`) |
| `cpus` | No | `16` | CPUs to request for the qxub verify job |
| `mem` | No | `32GB` | Memory for the qxub verify job |
| `dvc-mod` | No | `dt` | NCI module providing `dvc`/`dt` |
| `post-comment` | No | `true` | Post a PR comment with the result (set `false` for scheduled runs) |
| `github-token` | Yes | - | Token for posting PR comments |

## What it does

1. Metadata-only clone of `branch-ref` to `/scratch/<project>/<user>/ci/<repo>/pr-<pr-number>/run-<run-id>` (copyq) — needed only to resolve the remote from `.dvc/config`.
2. `dt remote verify <remote> [--full] -j <jobs> --json` on the `normal` queue.
3. Parses the JSON report (`totals.bad`, `totals.incomplete`); posts a PR comment (when `post-comment: true`) listing each bad/incomplete blob, and **fails the check** if any are found.

Does **not** use `--fix`/deletion — corruption is repaired at source (re-derive + re-ingest).

## Prerequisites

- `qxub-runner` self-hosted runner (has `qxub` + NCI SSH).
- Repo secret `USER_NAME` (NCI username).
- `python3` on the runner (JSON parsing).
- **The target remote must be a locally-accessible filesystem path.** `s3://`/`gs://`
  remotes cannot be verified this way (`dt remote verify` reads blobs from disk).
  On NCI, `ssh://gadi-dm…/g/data/...` remotes resolve to their local path.

## Cost

The first run (or any `full: true` run) hashes the entire store — hours for a
large registry. Subsequent PR runs use the ledger and only hash new blobs. Scale
with `jobs`/`cpus`; `dt remote verify -w` (distributed workers) exists for very
large stores but this action runs single-node.

## Example Usage

Per-PR (incremental) + scheduled (full):

```yaml
# PR
- uses: swarbricklab/ci/qxub-remote-verify@main
  with:
    nci-user: ${{ secrets.USER_NAME }}
    repository: ${{ github.event.repository.name }}
    pr-number: ${{ github.event.pull_request.number }}
    run-id: ${{ github.run_id }}
    branch-ref: ${{ github.head_ref }}
    github-token: ${{ secrets.GITHUB_TOKEN }}

# scheduled
- uses: swarbricklab/ci/qxub-remote-verify@main
  with:
    nci-user: ${{ secrets.USER_NAME }}
    repository: ${{ steps.repo.outputs.name }}
    pr-number: scheduled
    run-id: ${{ github.run_id }}
    branch-ref: main
    full: 'true'
    post-comment: 'false'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

Always follow with `qxub-cleanup` to remove the scratch clone.
