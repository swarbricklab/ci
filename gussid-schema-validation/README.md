# GUSSID Schema Validation

Validates the GUSSIDs in an `index.csv` against the Swarbricklab GUSSID schema. Pure CSV parsing — no DVC or NCI access required, so it runs on a standard GitHub-hosted runner.

## The GUSSID schema

A **GUSSID** (globally unique semantic sample ID) identifies one sample in a registry:

```
<PREFIX>_<donor>_T<tissue>_S<sample>
        e.g.  XEN_4615_T3_S1        SSC_BH174_T1_S2
```

| Segment | Rule |
|---------|------|
| `<PREFIX>` | Registry prefix (e.g. `XEN` for Xenium, `SSC` for Chromium). Set the `prefix` input to pin it. |
| `<donor>` | Donor identifier. Must equal the row's `donor_id` column. May itself contain `-`/`_`. |
| `T<tissue>` | **Must be an integer**, and must match the row's `tissue_id` (see below). A letter or compound infix — `TA`, `T1G`, `T1AF` — is **invalid**. |
| `S<sample>` | **Must be an integer.** Distinguishes multiple samples of the *same* tissue, **numbered from 1** with no gaps or repeats. Which slide/section each `S` corresponds to lives in the other columns (`section_id`, `block_id`, `out_dir`, …), not in the GUSSID. |

### How `T<tissue>` maps to `tissue_id`

The tissue number is derived from the `tissue_id` column:

| `tissue_id` | Expected `T` |
|-------------|--------------|
| equal to `donor_id` (bare) | `T0` |
| `<donor>-<N>` where `N` is a number | `T<N>` (e.g. `4615-3` → `T3`) |
| `<donor>-<letter>` single letter | `TA`→`T1`, `B`→`T2`, `C`→`T3`, … (e.g. `BH174-B` → `T2`) |

Any other `tissue_id` shape can't be mapped and is reported as a **warning** (the tissue-match check is skipped for that row; the structural checks still apply).

## What it checks

For every row with a non-blank GUSSID (blank = not yet minted, allowed):

1. **Format** — parses as `<PREFIX>_<donor>_T<int>_S<int>` (catches non-integer `T`/`S`, e.g. `TA`, `T1G`).
2. **Prefix** — matches the `prefix` input, if set.
3. **Donor** — the GUSSID donor segment equals the `donor_id` column.
4. **Tissue match** — `T<n>` equals the number implied by `tissue_id`.
5. **Tissue ↔ T bijection** — within a donor, each `tissue_id` maps to exactly one `T` and vice versa.
6. **Sample numbering** — within each `(donor, T)`, the `S` values are exactly `1..k` (contiguous, from 1, unique).
7. **Uniqueness** — no duplicate GUSSIDs.

Failures are emitted as GitHub `::error file=…,line=…::` annotations and the action exits non-zero.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `index-file` | No | `index.csv` | Path to the index CSV |
| `gussid-column` | No | `gussid` | GUSSID column name |
| `donor-column` | No | `donor_id` | Donor id column name |
| `tissue-column` | No | `tissue_id` | Tissue id column name |
| `prefix` | No | `` (any) | Require this exact GUSSID prefix (e.g. `XEN`) |

## Example usage

```yaml
name: PR Validation - Index Schema

on:
  pull_request:
    branches: [main]

jobs:
  gussid-schema:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
      - uses: swarbricklab/ci/gussid-schema-validation@main
        with:
          prefix: XEN
```

## Prerequisites

- **Python 3** (present by default on GitHub-hosted runners).
