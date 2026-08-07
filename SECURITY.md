# Security Policy

This repository contains public profile content, GitHub Pages assets, and automation. It is not a place for private support cases, credentials, unpublished source, customer data, or confidential vulnerability details.

## Reporting

For a vulnerability in Aegis, follow the reporting instructions in the Aegis repository's `SECURITY.md`.

For profile or Pages automation:

1. use GitHub private vulnerability reporting when it is enabled;
2. otherwise open a detail-free issue requesting a private contact channel;
3. do not include exploit steps, credentials, private repository data, personal information, internal hostnames, or sensitive logs in a public issue.

## Public-data rule

Assume that all repository content can be cloned, mirrored, cached, indexed, archived, and quoted. This includes commit history, deleted-file history, pull requests, issue comments, workflow logs, Pages output, generated receipts, and retained workflow artifacts.

Do not commit:

- personal access tokens, API keys, passwords, cookies, session material, private keys, or recovery codes;
- private repository names, internal paths, customer identifiers, provider configuration, or operational telemetry;
- raw API responses that may contain email addresses, IP addresses, repository metadata, or other personal data;
- screenshots that contain notifications, browser chrome, terminal history, credentials, private workspaces, or unredacted logs.

## Credential policy

- Authenticate interactively with GitHub CLI or a reviewed credential helper.
- GitHub Actions should use the repository-scoped `GITHUB_TOKEN` with the smallest job-level permissions required.
- Never pass tokens in command-line arguments, embed them in Git URLs, save them in `.env` files, or paste them into chat or issue threads.
- Workflow logs must not print authorization headers, credential-bearing URLs, or raw secrets.
- Any exposed credential must be revoked immediately and replaced. Removing it from the latest branch is not sufficient if it entered Git history or logs.

## Workflow policy

- Keep repository-wide default workflow permissions read-only.
- Grant `contents: write`, `pages: write`, or `id-token: write` only to the workflow or job that requires it.
- Pin third-party Actions to reviewed commit SHAs.
- Disable persisted checkout credentials unless a job intentionally pushes.
- Validate generated assets before publishing them.
- Treat external content, API responses, and generated SVG/HTML as untrusted input.

## Incident response

When sensitive material becomes public:

1. revoke or disable the affected credential or access path;
2. preserve a minimal incident timeline without copying the secret;
3. review account security, GitHub audit activity, workflow runs, artifacts, releases, Pages output, and mirrors;
4. rotate dependent credentials and invalidate sessions;
5. remove the material from the current branch;
6. decide whether Git history rewriting and cache-removal requests are justified;
7. verify that automation cannot regenerate the material.

## Supported content

Only the current `main` branch is maintained. Historical commits remain public records and are not supported deployment targets.
