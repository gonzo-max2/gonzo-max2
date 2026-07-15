# Security Policy

This repository contains public profile presentation assets and automation only.

## Reporting

Do not open a public issue containing credentials, tokens, private repository data, internal architecture secrets, or personal information.

## Credential policy

- Personal access tokens must never be committed.
- GitHub Actions must use the repository-scoped `GITHUB_TOKEN`.
- Generated assets must not contain raw API responses.
- Workflow logs must not print authorization headers.
- Any exposed token must be revoked immediately and replaced.

## Supported content

Only the current `main` branch is maintained.
