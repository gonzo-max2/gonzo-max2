# GONZO // SYSTEMS — APEX Profile OS Architecture

## Product definition

APEX is a two-surface public engineering identity system:

1. **GitHub-native profile README** — self-contained dark/light SVG presentation, concise technical narrative, public-safe project descriptions, real activity telemetry, and no third-party statistics renderer.
2. **GitHub Pages Profile OS** — dependency-free interactive systems atlas with bounded motion, domain-specific runtime scenes, cryptographic proof demonstration, maturity disclosure, and case-study evidence.

Both surfaces share `content/profile.json` as their canonical content authority.

## Visual architecture

The Pages surface deliberately avoids a generic card dashboard. It uses:

- A full-viewport spatial systems core.
- An asymmetric editorial systems atlas.
- A six-phase MAYA proof continuum.
- A deterministic Vozime trip lifecycle scene.
- Native Canvas audio and RF visualizations.
- A realtime motion-response scene for AURELIS.
- An interactive SHA-256/Merkle proof fabric.
- Evidence-first case studies and maturity disclosure.

## Motion architecture

Motion is bounded and state-bearing:

- CSS orbit and signal transitions communicate runtime continuity.
- `IntersectionObserver` reveals content once as it enters the viewport.
- Canvas 2D ambient nodes use adaptive density, clamped device-pixel ratio, and `requestAnimationFrame`.
- Audio and RF canvases reflect their respective domain models.
- The browser pauses ambient work when the document is hidden.
- Pointer depth is enabled only for fine-pointer devices.
- `prefers-reduced-motion` disables nonessential movement.
- A visible Motion/Still control allows operator override.

No third-party JavaScript, animation library, analytics package, remote font, wallet SDK, or WebGL framework is loaded.

## Blockchain proof fabric

The blockchain section is an explicitly labelled research and educational system:

- Five receipts represent intent, policy, action, verification, and completion.
- Each receipt commits to its sequence, payload, and previous digest.
- SHA-256 uses the browser Web Crypto API with a deterministic pure-JavaScript fallback for non-secure local preview contexts.
- Receipt hashes aggregate into a Merkle tree.
- Injecting a mutation invalidates the dependent causal path.
- Rebuilding receipts restores a valid proof root.

The demonstration does not connect to a wallet, custody funds, sign transactions, call a blockchain RPC endpoint, issue a token, or claim a production decentralized network.

## Accessibility

- Semantic landmark structure and skip navigation.
- Keyboard-accessible tabs, buttons, and anchors.
- Visible focus indicators.
- SVG `title` and `desc` metadata.
- Dark and light themes.
- Reduced-motion and forced-colors support.
- No color-only maturity labels in textual surfaces.
- No raw animation required to understand content.

## Security

- No credentials in repository content.
- Secret-pattern gates cover GitHub, OpenAI-style, and fine-grained token formats.
- GitHub Actions use repository-scoped `GITHUB_TOKEN`.
- Deployment credentials are accepted only through a hidden prompt or process environment.
- Public project descriptions are deliberately architecture-level and public-safe.
- Research maturity is disclosed instead of implied as production readiness.

## Build and proof pipeline

```text
content/profile.json
        │
        ├── scripts/build_apex_assets.py ──> assets/apex/*.svg
        ├── scripts/build_profile.py ──────> docs/data/profile.json
        │                                  receipts/profile-build.json
        ├── scripts/validate_profile.py ──> README/SVG integrity
        ├── scripts/verify_profile_os.py ─> security-and-structure receipt
        └── scripts/ui_smoke_test.py ─────> interaction receipt
```

The smoke test verifies system switching, MAYA phase switching, Vozime trip-state switching, blockchain mutation detection, blockchain repair, and duplicate-ID absence.
