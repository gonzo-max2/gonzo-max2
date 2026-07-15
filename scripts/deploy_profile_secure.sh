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
readonly PROFILE_NAME="${PROFILE_NAME:-Mihail Petkov}"
readonly PROFILE_BIO="${PROFILE_BIO:-Building proof-native autonomous systems, local-first AI infrastructure, and instrument-grade desktop products.}"
readonly PROFILE_LOCATION="${PROFILE_LOCATION:-Sofia, Bulgaria}"

TEMP_DIR=""
TOKEN_WAS_PROVIDED=0

cleanup() {
  local exit_code=$?
  unset GH_TOKEN GITHUB_TOKEN
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

require_command gh
require_command git
require_command python3
require_command mktemp
require_command rsync

if [[ ! -f "${SOURCE_DIR}/README.md" ]]; then
  fail "README.md not found in package root: ${SOURCE_DIR}"
fi

note "Validating local profile package"
python3 "${SOURCE_DIR}/scripts/validate_profile.py"

if [[ -z "${GH_TOKEN:-}" ]]; then
  printf '\nPaste a NEW fine-grained GitHub token (input is hidden): ' >&2
  IFS= read -r -s GH_TOKEN
  printf '\n' >&2
  TOKEN_WAS_PROVIDED=1
fi

[[ -n "${GH_TOKEN:-}" ]] || fail "No GitHub token supplied"
export GH_TOKEN
unset GITHUB_TOKEN

note "Validating GitHub identity"
authenticated_login="$(gh api user --jq '.login')"
[[ "${authenticated_login}" == "${OWNER}" ]] || \
  fail "Token belongs to '${authenticated_login}', expected '${OWNER}'"

note "Updating public profile metadata"
gh api \
  --method PATCH \
  /user \
  -f "name=${PROFILE_NAME}" \
  -f "bio=${PROFILE_BIO}" \
  -f "location=${PROFILE_LOCATION}" \
  >/dev/null

note "Ensuring profile repository exists"
if ! gh repo view "${REPO_FULL}" >/dev/null 2>&1; then
  gh api \
    --method POST \
    /user/repos \
    -f "name=${REPOSITORY}" \
    -f "description=GONZO // SYSTEMS — proof-native autonomous engineering and local-first infrastructure." \
    -F private=false \
    -F has_issues=true \
    -F has_projects=false \
    -F has_wiki=false \
    -F auto_init=false \
    >/dev/null
fi

visibility="$(gh api "/repos/${REPO_FULL}" --jq '.visibility')"
if [[ "${visibility}" != "public" ]]; then
  note "Making ${REPO_FULL} public so GitHub can render the profile README"
  gh api \
    --method PATCH \
    "/repos/${REPO_FULL}" \
    -f visibility=public \
    >/dev/null
fi

note "Configuring repository presentation and features"
gh api \
  --method PATCH \
  "/repos/${REPO_FULL}" \
  -f "description=GONZO // SYSTEMS — proof-native autonomous engineering and local-first infrastructure." \
  -F has_issues=true \
  -F has_projects=false \
  -F has_wiki=false \
  -F delete_branch_on_merge=true \
  >/dev/null

gh api \
  --method PUT \
  "/repos/${REPO_FULL}/topics" \
  -f 'names[]=systems-engineering' \
  -f 'names[]=autonomous-ai' \
  -f 'names[]=local-first' \
  -f 'names[]=rust' \
  -f 'names[]=tauri' \
  -f 'names[]=typescript' \
  -f 'names[]=python' \
  -f 'names[]=fastapi' \
  >/dev/null

note "Granting GitHub Actions the minimum write permission required for generated activity assets"
gh api \
  --method PUT \
  "/repos/${REPO_FULL}/actions/permissions/workflow" \
  -f default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=false \
  >/dev/null

note "Preparing clean repository checkout"
TEMP_DIR="$(mktemp -d -t gonzo-profile-deploy.XXXXXXXX)"
repo_dir="${TEMP_DIR}/repo"

if ! gh repo clone "${REPO_FULL}" "${repo_dir}" -- --quiet; then
  fail "Unable to clone ${REPO_FULL}"
fi

rsync -a --delete \
  --exclude '.git/' \
  --exclude '*.zip' \
  --exclude '*.sha256' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  "${SOURCE_DIR}/" "${repo_dir}/"

cd "${repo_dir}"
python3 scripts/validate_profile.py

git config user.name "${PROFILE_GIT_NAME:-Mihail Petkov}"
git config user.email "${PROFILE_GIT_EMAIL:-gonzo-max2@users.noreply.github.com}"

current_branch="$(git branch --show-current || true)"
if [[ "${current_branch}" != "main" ]]; then
  git checkout -B main
fi

git add --all

if git diff --cached --quiet; then
  note "Repository already contains the requested profile"
else
  note "Committing professional profile"
  git commit -m "feat(profile): install GONZO systems profile"
  git push --set-upstream origin main
fi

note "Setting main as the default branch"
gh api \
  --method PATCH \
  "/repos/${REPO_FULL}" \
  -f default_branch=main \
  >/dev/null

note "Triggering verified activity generation"
if gh workflow run profile-metrics.yml --repo "${REPO_FULL}" --ref main; then
  printf 'Workflow dispatched successfully.\n'
else
  printf 'WARNING: The profile was deployed, but the metrics workflow could not be dispatched yet.\n' >&2
  printf 'Open the repository Actions tab and run "Profile Metrics" manually.\n' >&2
fi

note "Remote verification"
remote_readme_url="$(gh api "/repos/${REPO_FULL}/contents/README.md" --jq '.html_url')"
repo_url="$(gh api "/repos/${REPO_FULL}" --jq '.html_url')"
profile_url="https://github.com/${OWNER}"

printf '\nDeployment completed.\n'
printf 'Repository: %s\n' "${repo_url}"
printf 'README:    %s\n' "${remote_readme_url}"
printf 'Profile:   %s\n' "${profile_url}"
printf '\nSecurity reminder: revoke the token after deployment if it was created only for this operation.\n'
