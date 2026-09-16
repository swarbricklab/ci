# GUSSID Schema Validation

Validates the GUSSIDs in an `index.csv` against the Swarbricklab GUSSID schema. Pure CSV parsing — no DVC or NCI access required, so it runs on a standard GitHub-hosted runner.

## The GUSSID schema

A **GUSSID** (globally unique semantic sample ID) identifies one sample in a registry:

```
<PREFIX>_<donor>_<SEG>_S<sample>
        e.g.  XEN_4615_T3_S1    SSC_3558_B0_S1    SNP_4262_TL_S1
```

| Segment | Rule |
|---------|------|
| `<PREFIX>` | Registry prefix (e.g. `XEN` Xenium, `SSC` Chromium, `WGS`, `SNP`, …). Set the `prefix` input to pin it. |
| `<donor>` | Donor identifier. Must equal the row's `donor_id` column. May itself contain `-`/`_`. |
| `<SEG>` | Tissue/compartment segment (see below). |
| `S<sample>` | **Must be an integer.** Distinguishes multiple samples of the *same* `SEG`, **numbered from 1** with no gaps or repeats. Which slide/section each `S` maps to lives in the other columns (`section_id`, `block_id`, …), not in the GUSSID. |

### The `<SEG>` (tissue/compartment) segment

`<SEG>` is one of:

- **`<compartment><number>`** — a compartment letter followed by an integer. Allowed compartment letters come from the `compartments` input (default `T`); e.g. `T` (tumour/tissue), `B` (blood/germline): `T0`, `T3`, `B0`, `B3`.
- **a bare letter-code** listed in the `letter-codes` input (no number) — e.g. `TL` (left), `TR` (right), `TN` (normal).

Anything else is **invalid** — in particular a compound like `T1G`, `T1AF`, or a bare `TA` that isn't a listed letter-code.

> **Registry-specific vocabulary.** The default (`compartments: T`, `letter-codes:` empty) is the strict Xenium schema. Registries that also have blood/germline samples set `compartments: T,B`; those with laterality/normal codes set `letter-codes: TL,TR,TN`.

### How a `T<n>` segment maps to `tissue_id`

When `check-tissue-match` is `true` (default), a numeric **`T`**-compartment segment must match the `tissue_id`:

| `tissue_id` | Expected `T` |
|-------------|--------------|
| equal to `donor_id` (bare) | `T0` |
| `<donor>-<N>` where `N` is a number | `T<N>` (e.g. `4615-3` → `T3`) |
| `<donor>-<letter>` single letter | `A`→`T1`, `B`→`T2`, `C`→`T3`, … (e.g. `BH174-B` → `T2`) |

Any other `tissue_id` shape can't be mapped and is reported as a **warning** (the tissue-match check is skipped for that row; the structural checks still apply). The tissue-match check applies only to `T`-compartment numeric segments — never to `B<n>` or letter-codes. Set `check-tissue-match: false` to skip it entirely (for registries whose `tissue_id` column doesn't carry the per-tissue value).

## What it checks

For every row with a non-blank GUSSID (blank = not yet minted, allowed):

1. **Format** — parses as `<PREFIX>_<donor>_<SEG>_S<int>` and `<SEG>` is an allowed compartment+number or letter-code (catches `T1G`, `TA`, non-integer `S`, …).
2. **Prefix** — matches the `prefix` input, if set.
3. **Donor** — the GUSSID donor segment equals the `donor_id` column.
4. **Tissue match** — a `T<n>` segment equals the number implied by `tissue_id` (when `check-tissue-match` is on).
5. **Sample numbering** — within each `(donor, SEG)`, the `S` values are unique, and (when `require-contiguous-samples` is on) exactly `1..k` with no gaps. Set `require-contiguous-samples: false` to allow gaps while still catching duplicates.
6. **Uniqueness** — no duplicate GUSSIDs.

Failures are emitted as GitHub `::error file=…,line=…::` annotations and the action exits non-zero.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `index-file` | No | `index.csv` | Path to the index CSV |
| `gussid-column` | No | `gussid` | GUSSID column name |
| `donor-column` | No | `donor_id` | Donor id column name |
| `tissue-column` | No | `tissue_id` | Tissue id column name |
| `prefix` | No | `` (any) | Require this exact GUSSID prefix (e.g. `XEN`) |
| `compartments` | No | `T` | Comma-separated compartment letters that may precede a number (e.g. `T,B`) |
| `letter-codes` | No | `` (none) | Comma-separated bare letter-code segments to allow (e.g. `TL,TR,TN`) |
| `check-tissue-match` | No | `true` | Enforce that `T<n>` matches `tissue_id` |
| `require-contiguous-samples` | No | `true` | Enforce `_S` runs `1..n` per `(donor, segment)`; set `false` to allow gaps (duplicates are still caught) |

## Example usage

Strict (Xenium):

```yaml
      - uses: swarbricklab/ci/gussid-schema-validation@main
        with:
          prefix: XEN
```

Registry with blood samples and laterality codes (Chromium):

```yaml
      - uses: swarbricklab/ci/gussid-schema-validation@main
        with:
          prefix: SSC
          compartments: T,B
          letter-codes: TL,TR,TN
```

## Prerequisites

- **Python 3** (present by default on GitHub-hosted runners).
