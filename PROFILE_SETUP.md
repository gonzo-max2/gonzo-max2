# GONZO // SYSTEMS Profile Setup

## Security first

The GitHub token previously pasted into chat must be revoked. Never store a personal access token in this repository, its README, workflow files, or commit history.

Use the repository-scoped `GITHUB_TOKEN` supplied automatically by GitHub Actions. The included metrics workflow needs no personal token.

## Install

The profile repository must be named exactly:

```text
gonzo-max2
```

under the account:

```text
gonzo-max2
```

For the README to appear on the public GitHub profile, the profile repository must be public and contain `README.md` at its root.

Copy the contents of this package into `gonzo-max2/gonzo-max2`, then commit and push:

```bash
git add README.md assets scripts .github PROFILE_SETUP.md
git commit -m "feat(profile): install GONZO systems profile"
git push origin main
```

## Enable activity refresh

In the repository:

1. Open **Settings → Actions → General**.
2. Under **Workflow permissions**, select **Read and write permissions**.
3. Save.
4. Open **Actions → Profile Metrics → Run workflow**.
5. Confirm that `assets/activity-dark.svg` and `assets/activity-light.svg` are updated by the workflow.

The workflow runs once per day and commits only when the generated activity assets change.

## Recommended profile configuration

Profile name:

```text
Mihail Petkov
```

Bio:

```text
Building proof-native autonomous systems, local-first AI infrastructure, and instrument-grade desktop products.
```

Location:

```text
Sofia, Bulgaria
```

Pinned repositories:

1. `gonzo-max2` — profile and engineering identity
2. A public MAYA overview or documentation repository when available
3. The strongest public systems project
4. A focused native/Rust project
5. A focused AI/runtime project
6. A focused real-time or audio project

Do not pin empty experiments, forks without substantial original work, or repositories without a professional README.

## Visual policy

- Keep the hero and architecture assets self-contained.
- Do not add a wall of third-party badges.
- Do not use fake contribution graphs.
- Do not embed visitor counters.
- Do not add animated typing banners.
- Do not expose private repository names that should remain confidential.
- Keep the profile focused on systems, evidence, architecture, and shipped capability.
