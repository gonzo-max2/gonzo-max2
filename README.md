# Gonzo Max

I build local-first software systems where models may propose work, but deterministic software owns authority, execution, recovery, and proof.

My public work concentrates on agent runtimes, developer tooling, product interfaces, and the parts that matter after a demo meets a real operating system.

## Aegis

[![Aegis CI](https://github.com/gonzo-max2/aegis-unified-0.9.0/actions/workflows/ci.yml/badge.svg)](https://github.com/gonzo-max2/aegis-unified-0.9.0/actions/workflows/ci.yml)
[![Project site](https://img.shields.io/badge/project-site-63c7da)](https://gonzo-max2.github.io/aegis-unified-0.9.0/)
[![License: Apache--2.0](https://img.shields.io/badge/license-Apache--2.0-69757c)](https://github.com/gonzo-max2/aegis-unified-0.9.0/blob/main/LICENSE)

![Aegis Studio showing a guarded engineering run](https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-live.webp)

[Aegis](https://github.com/gonzo-max2/aegis-unified-0.9.0) is a local-first execution runtime for coding and workspace agents. A model can propose a plan and request tools. Deterministic code owns permission checks, approvals, workspace confinement, process cleanup, reversible changes, receipts, and the final completion decision.

```text
model proposal
      ↓
typed intent and workspace scope
      ↓
permission, policy, and approval
      ↓
bounded execution
      ↓
changes and verification receipts
      ↓
verified completion or an explicit blocker
```

The project ships two operator surfaces: `aegis`, a scrollback-first terminal interface, and `aegisui`, a React Studio for inspecting plans, approvals, changes, failures, and evidence. Both consume the same runtime events.

<picture>
  <source media="(max-width: 720px)" srcset="https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-mobile.png">
  <img alt="Aegis Studio desktop interface" src="https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-desktop.png" width="100%">
</picture>

Aegis is a serious pre-production alpha for one operator on a trusted workstation. Current `main` contains the 0.10.4 semantic-runtime work. The latest tagged stable release remains [v0.9.2](https://github.com/gonzo-max2/aegis-unified-0.9.0/releases/tag/v0.9.2) while newer release evidence is completed.

## Public repositories

### [Aegis](https://github.com/gonzo-max2/aegis-unified-0.9.0)

Open local-first agent execution runtime with a Python core, React Studio, policy controls, recovery, and evidence-backed completion.

### [MAYA Codex Nexus](https://github.com/gonzo-max2/maya-codex-nexus)

A sanitized product case study for a private local-first engineering workbench. It presents real interface captures and controlled technical-review options without publishing the application source.

### [Profile and public policy](https://github.com/gonzo-max2/gonzo-max2)

This profile, the Pages site, generated activity, and the account's public-maintenance boundary.

Other work remains private until it has a deliberate public purpose, an evidence boundary, and a reviewable release surface. A portfolio does not improve by leaking every directory name it has ever met.

## Engineering focus

- deterministic lifecycle and state ownership;
- recovery from cancellation, failure, partial execution, and drift;
- strict path, process, credential, and network boundaries;
- interfaces that reveal real state instead of decorative progress;
- tests through the actual launcher and packaged artifact;
- release provenance tied to an exact commit.

My working rule is simple: a system should explain what it changed, why it had authority, what verified the result, and how to recover when any of those statements are false.

## Evidence and maintenance

- [Public surface](PUBLIC_SURFACE.md)
- [Security policy](SECURITY.md)
- [Aegis architecture, tests, and validation](https://github.com/gonzo-max2/aegis-unified-0.9.0)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/activity-light.svg">
  <img alt="Verified GitHub engineering activity" src="./assets/activity-dark.svg" width="100%">
</picture>

## Contact

For technical collaboration, product diligence, or licensing discussions, open a short non-confidential issue in this profile repository.
