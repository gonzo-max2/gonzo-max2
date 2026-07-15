# APEX Profile OS Deployment

## 1. Revoke exposed credentials

Any personal access token pasted into chat, terminal output, screenshots, or source must be revoked before deployment. Never reuse an exposed credential.

## 2. Build and verify locally

```bash
python3 scripts/build_profile.py
python3 scripts/validate_profile.py
python3 scripts/verify_profile_os.py
node --check docs/app.js
```

Optional offline browser interaction audit:

```bash
python3 -m pip install playwright==1.57.0
python3 -m playwright install chromium
python3 scripts/ui_smoke_test.py
```

## 3. Deploy securely

```bash
chmod 700 scripts/deploy_profile_secure.sh
./scripts/deploy_profile_secure.sh
```

The installer:

- Prompts for a newly generated token with terminal echo disabled.
- Verifies the authenticated account is `gonzo-max2`.
- Creates or updates the profile repository.
- Makes the profile repository public, which GitHub requires to display the profile README.
- Pushes the complete Profile OS.
- Enables workflow write permission for generated activity assets.
- Triggers the profile metrics workflow.

The token is not written to disk by the installer.

## 4. Enable GitHub Pages

Open **Settings → Pages** and select **GitHub Actions** as the source, then run:

- **Build APEX Profile OS**
- **Deploy APEX Profile OS**
- **Profile Metrics**

Expected Pages URL:

```text
https://gonzo-max2.github.io/gonzo-max2/
```

## 5. Verify remote state

```bash
chmod 700 scripts/verify_profile_remote.sh
./scripts/verify_profile_remote.sh
```
