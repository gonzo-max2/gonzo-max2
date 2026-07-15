# Deployment

## Security first

Revoke every personal access token previously pasted into chat. Do not reuse it.

## Build and verify

```bash
python3 scripts/build_profile.py
python3 scripts/validate_profile.py
python3 scripts/verify_profile_os.py
```

## Deploy profile repository

```bash
chmod 700 scripts/deploy_profile_secure.sh
./scripts/deploy_profile_secure.sh
```

## Enable Pages

Set **Settings → Pages → Source** to **GitHub Actions**, then run **Deploy Profile OS**. Expected URL:

```text
https://gonzo-max2.github.io/gonzo-max2/
```
