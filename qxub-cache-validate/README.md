# QXUB Cache Validate

Validate DVC cache integrity on NCI via QXUB using `dt cache validate`, to detect
objects corrupted by interrupted network transfers (bytes that no longer match
their content-addressed md5). Self-contained: it clones the repo on NCI, pulls
the target data into the cache, re-hashes it, reports, and **fails the check** if
any object is corrupt.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `nci-user` | Yes | - | NCI username |
| `nci-project` | No | `a56` | NCI project allocation |
| `repository` | Yes | - | Repository name |
| `pr-number` | Yes | - | PR number, or a label (e.g. `scheduled`) for non-PR runs |
| `run-id` | Yes | - | GitHub Actions run ID |
| `branch-ref` | Yes | - | Branch/ref to clone and validate |
| `targets` | No | `''` | Space-separated workspace paths / `.dvc` files. Empty = **entire cache** |
| `dvc-mod` | No | `dt` | NCI module providing `dvc`/`dt` |
| `cpus` | No | `16` | CPUs for the validate job (checksum parallelism) |
| `mem` | No | `32GB` | Memory for the validate job |
| `post-comment` | No | `true` | Post a PR comment with the result (set `false` for scheduled runs) |
| `github-token` | Yes | - | Token for posting PR comments |

## What it does

1. Clones `branch-ref` to `/scratch/<project>/<user>/ci/<repo>/pr-<pr-number>/run-<run-id>` (copyq).
2. `dt pull --network <targets>` to populate the cache (empty `targets` pulls everything).
3. `dt cache validate --json <targets>` on the `normal` queue, then parses the JSON.
   `--json` exits 0 even on corruption, so the action itself fails the step when
   `corrupted` or `errors` is non-empty.
4. Posts a PR comment (when `post-comment: true`) listing each corrupt file with
   its expected vs actual md5.

Does **not** use `--fix` — corruption should be repaired at the source, not by
deleting the bad object in CI.

## Prerequisites

- Runs on the `qxub-runner` self-hosted runner (has `qxub` + NCI SSH).
- Repo secret `USER_NAME` (NCI username).
- `python3` available on the runner (JSON parsing).

## Cost

Validation re-hashes every object it checks. Scope PRs to changed `.dvc` files
(cheap); a full validate (empty `targets`) re-hashes the whole dataset and, for
large registries, takes hours — run it on a schedule, not per-PR.

## Example Usage

Per-PR, only the changed data:

```yaml
- name: Determine changed .dvc targets
  id: targets
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    files=$(gh api repos/${{ github.repository }}/pulls/${{ github.event.pull_request.number }}/files \
      --paginate --jq '.[].filename' | grep -E '\.dvc$' | tr '\n' ' ' || true)
    echo "targets=$files" >> "$GITHUB_OUTPUT"

- name: Validate cache for changed data
  if: steps.targets.outputs.targets != ''
  uses: swarbricklab/ci/qxub-cache-validate@main
  with:
    nci-user: ${{ secrets.USER_NAME }}
    repository: ${{ github.event.repository.name }}
    pr-number: ${{ github.event.pull_request.number }}
    run-id: ${{ github.run_id }}
    branch-ref: ${{ github.head_ref }}
    targets: ${{ steps.targets.outputs.targets }}
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

Scheduled full validate:

```yaml
- uses: swarbricklab/ci/qxub-cache-validate@main
  with:
    nci-user: ${{ secrets.USER_NAME }}
    repository: ${{ github.event.repository.name }}
    pr-number: scheduled
    run-id: ${{ github.run_id }}
    branch-ref: main
    post-comment: 'false'
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

Always follow with `qxub-cleanup` to remove the scratch clone.
