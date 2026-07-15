# GONZO Profile OS Architecture

## Product boundary

The repository has two presentation surfaces sharing one source of truth:

1. `README.md` — GitHub-native, fast, accessible, self-contained, and safe.
2. `docs/` — GitHub Pages experience with progressive enhancement and deeper animation.

`content/profile.json` is canonical. `scripts/build_profile.py` generates README assets, synchronizes Pages data, and creates a machine-readable receipt.

## Motion architecture

- CSS-only orbit and proof-continuum motion.
- IntersectionObserver reveal transitions.
- Canvas 2D constellation with adaptive point count, clamped DPR, requestAnimationFrame, and visibility suspension.
- Pointer tilt limited to fine-pointer devices and throttled to one animation frame.
- Complete `prefers-reduced-motion` shutdown.

## Blockchain demonstrator

The blockchain section is a local educational proof-chain. Five blocks represent intent, policy, action, proof, and receipt. Each digest is SHA-256 over block index, payload, and previous hash. The browser Web Crypto API performs hashing. Changing one payload produces a verifiable chain failure.

No wallet, token, external chain, RPC endpoint, transaction signing, custody, or financial interaction exists.

## Security and performance

No third-party JavaScript, remote fonts, analytics, or tracking pixels are used. Canvas DPR is clamped to 1.75, node count is bounded, rendering pauses when hidden, and the service worker caches only first-party static assets.
