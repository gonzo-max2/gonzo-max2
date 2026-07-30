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
Maya
```

Bio:

```text
Building Nova: local-first AI code change with deterministic evidence, durable apply and rollback.
```

Location:

```text
Sofia, Bulgaria
```

Pinned repositories:

1. `gonzo-max2` — profile and engineering identity
2. `maya-codex-nexus` — evidence-governed AI workbench
3. `aegis-unified-0.9.0` — public local-AI runtime work
4. Nova only after a deliberate decision to make a public case study

Do not pin empty experiments, forks without substantial original work, or repositories without a professional README.

## Visual policy

- Keep the hero and architecture assets self-contained.
- Do not add a wall of third-party badges.
- Do not use fake contribution graphs.
- Do not embed visitor counters.
- Do not add animated typing banners.
- Do not expose private repository names that should remain confidential.
- Keep the profile focused on systems, evidence, architecture, and shipped capability.

## Fully automated secure deployment

The package includes an installer that performs the complete deployment without storing a personal access token:

```bash
chmod 700 scripts/deploy_profile_secure.sh
./scripts/deploy_profile_secure.sh
```

The installer:

1. Validates all local README and SVG assets.
2. Prompts for a newly generated token with terminal echo disabled.
3. Verifies the authenticated account is `gonzo-max2`.
4. Updates the profile name, bio, and location.
5. Creates `gonzo-max2/gonzo-max2` when missing.
6. Makes the profile repository public.
7. Configures repository metadata, topics, and feature policy.
8. Sets workflow token permissions to `write`.
9. Synchronizes the complete profile package.
10. Commits and pushes to `main`.
11. Triggers the verified activity workflow.
12. Returns repository, README, and profile locations.

The token remains only in the deployment process environment and is unset on exit.

Remote verification:

```bash
chmod 700 scripts/verify_profile_remote.sh
./scripts/verify_profile_remote.sh
```

Do not pass tokens as command-line arguments, embed them in Git URLs, place them in shell history, or save them in `.env` files.


## Profile OS and GitHub Pages

Set **Settings → Pages → Source** to **GitHub Actions**, run **Deploy Profile OS**, and open `https://gonzo-max2.github.io/gonzo-max2/`. The Pages layer includes bounded Canvas motion, scroll reveal, pointer tilt, animated proof continuum, an interactive SHA-256 blockchain proof chain, dark/light themes, reduced-motion support, and offline caching.
