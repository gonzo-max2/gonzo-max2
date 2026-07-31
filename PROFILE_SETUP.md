# Public Profile Maintenance

This repository is the public front door for the `gonzo-max2` account. Treat every file, commit, issue, pull request, workflow log, artifact, and GitHub Pages asset as publishable and permanently indexable.

## Public identity

Use one identity consistently across the GitHub profile and product repositories:

```text
Name: Gonzo Max
Bio: Building local-first agent runtimes with explicit authority, recovery, and evidence-backed completion.
Location: optional; publish only when deliberately useful
```

The public profile should point to three repositories:

1. `gonzo-max2/gonzo-max2` — profile, public-surface policy, and portfolio site;
2. `gonzo-max2/aegis-unified-0.9.0` — the open Aegis runtime;
3. `gonzo-max2/maya-codex-nexus` — a sanitized MAYA product case study.

Do not expose private repository names, internal paths, customer data, provider configuration, credentials, unpublished screenshots, or unsupported maturity claims merely to make the profile look busier. GitHub already contains enough decorative archaeology.

## Authentication

Use GitHub CLI's credential store rather than pasting tokens into files, chat, shell arguments, Git URLs, or `.env` files:

```bash
gh auth login --web --git-protocol https
gh auth status
```

If a credential is exposed, revoke it immediately, review account and Actions activity, rotate dependent credentials, and assess whether history cleanup is required. Removing a token from the latest commit does not remove it from Git history or external caches.

## Local validation

From the repository root:

```bash
python3 scripts/validate_profile.py
python3 scripts/verify_profile_os.py
node --check docs/app.js
```

Review the exact public diff before pushing:

```bash
git status --short
git diff --check
git diff --stat
git diff
```

## GitHub Actions policy

Keep the repository-wide default workflow permission read-only. Grant write access only inside the workflow and job that needs it.

The activity workflow needs scoped `contents: write` because it commits generated SVG assets. Validation and Pages build jobs should remain read-only except for the dedicated Pages deployment permissions.

Third-party Actions should be pinned to reviewed commit SHAs, not only mutable major-version tags. Workflow credentials should not persist in the checkout unless a job explicitly needs to push.

## Publishing workflow

Use a branch and pull request for profile changes:

```bash
git switch -c profile/<change-name>
git add --all
git commit -m "docs(profile): <clear change>"
git push -u origin HEAD
gh pr create --draft --fill
```

Before merge, verify:

- the profile README renders correctly in dark and light themes;
- GitHub Pages works at desktop and narrow widths;
- reduced-motion and keyboard navigation remain usable;
- every project claim links to current public evidence;
- no private product name or operational detail slipped into generated data;
- generated assets and receipts match the source revision;
- validation and deployment workflows pass.

## Canonical public surfaces

`README.md` and `docs/index.html` are the current human-facing surfaces. Generated profile data, manifests, and legacy visual assets must stay aligned with those surfaces or be retired. A stale generator quietly restoring old identities and private project names is not automation; it is a time-delayed disclosure mechanism.
