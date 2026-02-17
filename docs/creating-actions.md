# Creating New Actions

Guide for adding reusable GitHub Actions to this repository.

## Directory Structure

```
<action-name>/
├── action.yml    # Action definition (required)
└── README.md     # Documentation (required)
```

## action.yml Template

```yaml
name: 'Action Name'
description: 'Brief description of what the action does'
inputs:
  example-input:
    description: 'Description of the input'
    required: true
  optional-input:
    description: 'Optional input with default'
    required: false
    default: 'default-value'

runs:
  using: 'composite'
  steps:
    - name: Step name
      shell: bash
      run: |
        echo "Hello ${{ inputs.example-input }}"
```

## README.md Template

```markdown
# Action Name

Brief description.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `example-input` | Yes | - | Description |

## What it does

1. Step one
2. Step two

## Prerequisites

- List dependencies
- See [Authentication Guide](../docs/authentication.md) if GCP needed

## Example Usage

\`\`\`yaml
- uses: swarbricklab/ci/<action-name>@main
  with:
    example-input: value
\`\`\`
```

## Conventions

1. **Composite actions only** - Use `runs: using: 'composite'`
2. **Shell scripts** - Use `shell: bash` for all run steps
3. **SSH configuration** - If DVC operations need SSH:
   ```yaml
   - name: Configure SSH for DVC
     shell: bash
     run: |
       export GIT_SSH_COMMAND="ssh -i ~/.ssh/atlas_key -F ~/.ssh/config"
       echo "GIT_SSH_COMMAND=$GIT_SSH_COMMAND" >> $GITHUB_ENV
   ```
4. **Error handling** - Use `set -euo pipefail` in shell scripts
5. **PR comments** - Accept `github-token` input for posting comments

## Testing

1. Create a feature branch
2. Test in a downstream repo by referencing the branch:
   ```yaml
   uses: swarbricklab/ci/<action>@feature-branch
   ```
3. Open PR for review (branch protection enforced)

## Updating the Skill

After adding a new action, update [.github/skills/ci-setup/SKILL.md](../.github/skills/ci-setup/SKILL.md) to include it in the actions table.
