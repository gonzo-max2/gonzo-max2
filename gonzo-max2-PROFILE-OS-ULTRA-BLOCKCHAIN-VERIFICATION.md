# GONZO Profile OS Ultra — Blockchain Verification

**Package:** `gonzo-max2-PROFILE-OS-ULTRA-BLOCKCHAIN-20260715.zip`  
**Verified:** 2026-07-15  
**Repository:** [gonzo-max2/gonzo-max2](https://github.com/gonzo-max2/gonzo-max2)

## Package checksum

```text
SHA-256: 479f2def191ed218d6146c6542a6349ed8c71040007d57c51e6238d22cd6de1a
```

## Local verification (executed)

```bash
python3 scripts/build_profile.py
python3 scripts/validate_profile.py
python3 scripts/verify_profile_os.py
```

| Check | Result |
|-------|--------|
| Build | `systems: 9`, `generated_assets: 8` |
| Validate | `19` README asset references |
| Verify OS | `passed: true` |

## Surfaces installed

| Surface | Path |
|---------|------|
| GitHub README | `README.md` |
| GitHub Pages | `docs/index.html` |
| Canonical data | `content/profile.json` |
| Architecture | `PROFILE_OS_ARCHITECTURE.md` |
| Deployment | `DEPLOYMENT.md` |

## Blockchain demonstrator

Educational local proof-chain (intent → policy → action → proof → receipt). SHA-256 via Web Crypto API. No wallet, token, RPC, or custody.

## Pages URL

```text
https://gonzo-max2.github.io/gonzo-max2/
```

Enable **Settings → Pages → Source: GitHub Actions**, then run the **Deploy Profile OS** workflow.

## Post-push operator steps

1. Revoke any PAT previously exposed in chat.
2. Confirm Actions read/write permissions for workflows.
3. Run **Profile Metrics** workflow after deploy.
4. Pin public repos on the profile README if desired.