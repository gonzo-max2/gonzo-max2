#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
set +x

readonly OWNER="${PROFILE_OWNER:-gonzo-max2}"
readonly REPOSITORY="${PROFILE_REPOSITORY:-gonzo-max2}"
readonly REPO_FULL="${OWNER}/${REPOSITORY}"
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly SOURCE_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
readonly TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
readonly BRANCH="${PROFILE_DEPLOY_BRANCH:-profile/deploy-${TIMESTAMP}}"

TEMP_DIR=""

cleanup() {
  local exit_code=$?
  if [[ -n "${TEMP_DIR}" && -d "${TEMP_DIR}" ]]; then
    rm -rf -- "${TEMP_DIR}"
  fi
  exit "${exit_code}"
}
trap cleanup EXIT INT TERM

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

note() {
  printf '\n==> %s\n' "$*"
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "Required command not found: $1"
}

for command_name in gh git python3 mktemp rsync node; do
  require_command "${command_name}"
done

[[ -f "${SOURCE_DIR}/README.md" ]] || fail "README.md not found in ${SOURCE_DIR}"
[[ -f "${SOURCE_DIR}/PUBLIC_SURFACE.md" ]] || fail "PUBLIC_SURFACE.md not found in ${SOURCE_DIR}"

if [[ -n "${GH_TOKEN:-}" || -n "${GITHUB_TOKEN:-}" ]]; then
  fail "Unset GH_TOKEN and GITHUB_TOKEN. This script uses the reviewed GitHub CLI credential store and never accepts pasted tokens."
fi

note "Verifying GitHub CLI authentication"
gh auth status --hostname github.com >/dev/null
authenticated_login="$(gh api user --jq '.login')"
[[ "${authenticated_login}" == "${OWNER}" ]] || \
  fail "Authenticated as '${authenticated_login}', expected '${OWNER}'"

note "Verifying the existing public profile repository"
gh repo view "${REPO_FULL}" >/dev/null 2>&1 || \
  fail "Repository ${REPO_FULL} does not exist or is not accessible"

visibility="$(gh api "/repos/${REPO_FULL}" --jq '.visibility')"
[[ "${visibility}" == "public" ]] || \
  fail "Repository ${REPO_FULL} is '${visibility}'. This script will not change repository visibility."

default_branch="$(gh api "/repos/${REPO_FULL}" --jq '.default_branch')"
[[ "${default_branch}" == "main" ]] || \
  fail "Expected default branch 'main', found '${default_branch}'. This script will not rewrite repository settings."

note "Running local validation"
python3 "${SOURCE_DIR}/scripts/validate_profile.py"
python3 "${SOURCE_DIR}/scripts/verify_profile_os.py"
node --check "${SOURCE_DIR}/docs/app.js"

note "Preparing an isolated checkout"
TEMP_DIR="$(mktemp -d -t gonzo-profile-deploy.XXXXXXXX)"
repo_dir="${TEMP_DIR}/repo"
gh repo clone "${REPO_FULL}" "${repo_dir}" -- --quiet

cd "${repo_dir}"
git switch --create "${BRANCH}" "origin/main"

rsync -a --delete \
  --exclude '.git/' \
  --exclude '*.zip' \
  --exclude '*.sha256' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  "${SOURCE_DIR}/" "${repo_dir}/"

note "Validating the exact proposed checkout"
python3 scripts/validate_profile.py
python3 scripts/verify_profile_os.py
node --check docs/app.js
git diff --check

git config user.name "${PROFILE_GIT_NAME:-${authenticated_login}}"
git config user.email "${PROFILE_GIT_EMAIL:-${authenticated_login}@users.noreply.github.com}"
git add --all

if git diff --cached --quiet; then
  note "No public profile changes to propose"
  exit 0
fi

note "Creating a review branch"
git commit -m "docs(profile): propose reviewed public profile update"
git push --set-upstream origin "${BRANCH}"

note "Opening a draft pull request"
pr_url="$(gh pr create \
  --repo "${REPO_FULL}" \
  --base main \
  --head "${BRANCH}" \
  --draft \
  --title "Review public profile update ${TIMESTAMP}" \
  --body $'Automated draft created by scripts/deploy_profile_secure.sh.\n\nReview the complete public diff, generated assets, identity, claims, links, and workflow results before merge. This script does not change profile metadata, repository visibility, repository settings, workflow permissions, or the default branch.')"

printf '\nDraft pull request created: %s\n' "${pr_url}"
printf 'No profile metadata, visibility, Actions permissions, or default-branch settings were changed.\n'
