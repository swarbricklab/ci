# Authentication

This document describes how to authenticate to Google Cloud Platform (GCP) in GitHub Actions workflows using the swarbricklab org secrets.

## Overview

The organization uses [Workload Identity Federation (WIF)](https://cloud.google.com/iam/docs/workload-identity-federation) for keyless authentication from GitHub Actions to GCP. This is more secure than service account keys as it eliminates the need to manage long-lived credentials.

## Required Org Secrets

The following secrets are available at the organization level:

| Secret | Description |
|--------|-------------|
| `WIF_PROVIDER` | Full Workload Identity Provider path |
| `SERVICE_ACCOUNT` | Service account email for GCP operations |

## Workflow Configuration

### Permissions

Your workflow must request the `id-token: write` permission for WIF to work:

```yaml
jobs:
  your-job:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write  # Required for Workload Identity Federation
```

### Authentication Step

Add this step before any GCP operations:

```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
    service_account: ${{ secrets.SERVICE_ACCOUNT }}

- name: Set up Cloud SDK
  uses: google-github-actions/setup-gcloud@v2
```

## Complete Example

```yaml
name: Example Workflow

on:
  pull_request:
    branches: [main]

jobs:
  gcp-task:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Use gsutil
        run: gsutil ls gs://your-bucket/
```

## Troubleshooting

### Error: "must specify exactly one of workload_identity_provider or credentials_json"

**Cause:** The secrets are not being injected. This typically happens when:
- The secrets don't exist at the org level
- The repository doesn't have access to the org secrets
- The workflow is triggered from a fork (secrets are not passed to fork PRs by default)

**Solution:** Verify the secrets exist in GitHub org settings (Settings → Secrets and variables → Actions → Organization secrets) and that the repository has access.

### Error: "Unable to generate access token"

**Cause:** The Workload Identity Pool is not configured to trust this repository.

**Solution:** The WIF pool must have an attribute condition that allows the repository. Contact your GCP administrator to add the repository to the allowed list.

## Legacy Pattern (Not Recommended)

Some older workflows use inline WIF configuration with `PROJECT_ID` and `PROJECT_NUMBER`:

```yaml
# Legacy - prefer using WIF_PROVIDER and SERVICE_ACCOUNT instead
- uses: google-github-actions/auth@v2
  with:
    service_account: grunner-ci-sa@${{ secrets.PROJECT_ID }}.iam.gserviceaccount.com
    workload_identity_provider: projects/${{ secrets.PROJECT_NUMBER }}/locations/global/workloadIdentityPools/hpci-workload-identity-pool/providers/github-provider
```

This still works but the `WIF_PROVIDER` and `SERVICE_ACCOUNT` secrets are preferred as they:
- Are easier to rotate
- Don't expose infrastructure details in workflows
- Reduce copy-paste errors
