# CI Setup Skill

Quick reference for AI agents setting up CI workflows in swarbricklab repositories.

## Navigation

```
ci/
├── docs/authentication.md    # GCP auth pattern (READ FIRST)
├── dvc-remote-check/         # DVC diff + remote validation
├── index-path-validation/    # CSV path validation
├── qxub-checkout/            # NCI remote checkout
└── tree-snapshot-validation/ # Tree snapshot sync
```

Each action folder has a `README.md` with inputs table and example.

## Setup Workflow

1. **Create branch** in target repo
2. **Create `.github/workflows/<name>.yml`**
3. **Add GCP auth** (if action needs GCS/gsutil):
   ```yaml
   permissions:
     id-token: write
   steps:
     - uses: google-github-actions/auth@v2
       with:
         workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
         service_account: ${{ secrets.SERVICE_ACCOUNT }}
     - uses: google-github-actions/setup-gcloud@v2
   ```
4. **Add action step**: `uses: swarbricklab/ci/<action>@main`
5. **Commit, push, PR**

## Org Secrets (Available to All Repos)

| Secret | Purpose |
|--------|---------|
| `WIF_PROVIDER` | Workload Identity Federation provider path |
| `SERVICE_ACCOUNT` | GCP service account email |

Never hardcode GCP project IDs or service account names in workflows.

## Common Patterns

### DVC Remote Check
```yaml
- uses: swarbricklab/ci/dvc-remote-check@main
  with:
    cache-bucket: gs://<bucket>/<path>
    dvc-remote: <remote-name-from-dvc-config>
    pr-number: ${{ github.event.pull_request.number }}
    github-token: ${{ github.token }}
```

Find `dvc-remote` value in target repo's `.dvc/config` under `[core] remote = <name>`.

### Permissions Block
```yaml
permissions:
  contents: read
  pull-requests: write  # For PR comments
  id-token: write       # For WIF auth
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| "must specify workload_identity_provider or credentials_json" | Secrets not injected. Check `WIF_PROVIDER`/`SERVICE_ACCOUNT` exist at org level |
| "Unable to generate access token" | Repo not in WIF allowed list. Contact GCP admin |
| Auth step hangs | Missing `id-token: write` permission |
