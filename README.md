# Gonzo Max

I design and build local-first software systems where automation is useful
without becoming the authority. My work sits at the intersection of agent
runtimes, developer tooling, product interfaces, recovery, and evidence-backed
execution.

The public project I am concentrating on now is
[Aegis](https://github.com/gonzo-max2/aegis-unified-0.9.0): a guarded runtime
that places deterministic software between a model and the operating system.

## Aegis

[![Aegis CI](https://github.com/gonzo-max2/aegis-unified-0.9.0/actions/workflows/ci.yml/badge.svg)](https://github.com/gonzo-max2/aegis-unified-0.9.0/actions/workflows/ci.yml)
[![Project site](https://img.shields.io/badge/project-site-63c7da)](https://gonzo-max2.github.io/aegis-unified-0.9.0/)
[![License: Apache--2.0](https://img.shields.io/badge/license-Apache--2.0-69757c)](https://github.com/gonzo-max2/aegis-unified-0.9.0/blob/main/LICENSE)

![Aegis Studio showing a guarded engineering run](https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-live.webp)

Aegis is a local-first execution runtime for coding and workspace agents. A
model can propose a plan and request tools; deterministic code owns permission
checks, approvals, path confinement, process cleanup, reversible changes,
receipts, and the final completion decision.

```text
model proposal
      ↓
typed intent and exact workspace scope
      ↓
permission, risk, policy, and approval
      ↓
bounded and cancellable execution
      ↓
diff, process, network, and verification receipts
      ↓
verified completion or an explicit resumable blocker
```

The runtime has two operator surfaces:

- `aegis` is a scrollback-first terminal interface with one transcript, one
  composer, and one live status row.
- `aegisui` is a React Studio for inspecting plans, tool receipts, file
  changes, approvals, specialist work, failures, and proof.

Both surfaces consume the same runtime events. Neither can bypass policy or
turn model prose into completion evidence.

<picture>
  <source
    media="(max-width: 720px)"
    srcset="https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-mobile.png"
  >
  <img
    alt="Current Aegis 0.10 Studio desktop interface"
    src="https://raw.githubusercontent.com/gonzo-max2/aegis-unified-0.9.0/main/docs/evidence/aegis-studio-desktop.png"
    width="100%"
  >
</picture>

### What is implemented

- Workspace-confined file, process, Git, web, browser, and SSH tools
- Typed policy decisions, risk classification, and approval boundaries
- Persistent missions, checkpoints, continuation, and truthful terminal states
- Exact tool receipts, file deltas, proof manifests, and rollback data
- Permission-scoped specialist agents with reduced tool registries
- Ollama, OpenAI, Anthropic, and Google provider adapters
- Native CLI and React control surfaces over one canonical runtime
- Verified episodic memory derived from bounded outcomes rather than assistant
  prose
- Reproducible Python packages, pinned browser CI, and portable-image contracts

### Current boundary

Aegis is a serious pre-production alpha for one operator on a trusted
workstation. It is not presented as a hostile multi-tenant security boundary,
an independently audited enterprise platform, or a foundation model. Public
claims are intentionally narrower than the architecture.

The latest stable release remains
[v0.9.2](https://github.com/gonzo-max2/aegis-unified-0.9.0/releases/tag/v0.9.2).
Current `main` contains the 0.10 verified-memory and public-interface work while
its release evidence is being completed.

## Engineering focus

I care most about the parts of software that fail when a demo becomes a real
tool:

- lifecycle ownership and deterministic state transitions;
- recovery from cancellation, provider failure, partial execution, and drift;
- strict boundaries around paths, processes, credentials, and network access;
- interfaces that reveal real runtime state instead of decorative progress;
- accessible, responsive product surfaces with restrained motion;
- tests that prove behavior through the actual launcher and packaged artifact;
- release provenance that ties a public claim to an exact commit.

My working rule is straightforward: a system should be able to explain what it
changed, why it had authority to change it, what verified the result, and how to
recover if any of those statements are false.

## Selected work

### [Aegis Unified](https://github.com/gonzo-max2/aegis-unified-0.9.0)

The public agent-governance runtime described above. Python, SQLite,
prompt-toolkit, Rich, FastAPI, React, TypeScript, Vite, Playwright, Ollama, and
provider APIs.

### [MAYA Codex Nexus](https://github.com/gonzo-max2/maya-codex-nexus)

A local engineering workbench exploring model orchestration, transactional
workspaces, proof-native interaction, and desktop runtime integration.

Other work spans native audio and DSP, realtime interaction, mobile product
systems, recovery tooling, and UI-quality automation. I treat those as
engineering domains rather than a collection of brand names.

## Evidence and maintenance

The Aegis repository contains its architecture, security boundary, changelog,
tests, current interface captures, release workflows, and validation evidence.
The profile activity panel below is generated by a repository-owned GitHub
Actions workflow using GitHub's API; it is not a third-party stat image.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/activity-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./assets/activity-light.svg">
  <img alt="Verified GitHub engineering activity" src="./assets/activity-dark.svg" width="100%">
</picture>

## Contact

For technical collaboration, product diligence, or licensing discussions, open
a short non-confidential issue in this profile repository. Do not post
credentials, private source, customer data, or other sensitive material in a
public issue.
