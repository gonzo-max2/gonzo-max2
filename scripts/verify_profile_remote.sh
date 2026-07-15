#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
set +x

readonly OWNER="${PROFILE_OWNER:-gonzo-max2}"
readonly REPOSITORY="${PROFILE_REPOSITORY:-gonzo-max2}"
readonly REPO_FULL="${OWNER}/${REPOSITORY}"

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

command -v gh >/dev/null 2>&1 || fail "GitHub CLI (gh) is required"

if [[ -z "${GH_TOKEN:-}" ]]; then
  printf 'Paste a NEW fine-grained GitHub token (input is hidden): ' >&2
  IFS= read -r -s GH_TOKEN
  printf '\n' >&2
fi
[[ -n "${GH_TOKEN:-}" ]] || fail "No GitHub token supplied"
export GH_TOKEN
trap 'unset GH_TOKEN GITHUB_TOKEN' EXIT INT TERM

login="$(gh api user --jq '.login')"
[[ "${login}" == "${OWNER}" ]] || fail "Authenticated as ${login}; expected ${OWNER}"

visibility="$(gh api "/repos/${REPO_FULL}" --jq '.visibility')"
default_branch="$(gh api "/repos/${REPO_FULL}" --jq '.default_branch')"
readme_path="$(gh api "/repos/${REPO_FULL}/readme" --jq '.path')"
workflow_permission="$(gh api "/repos/${REPO_FULL}/actions/permissions/workflow" --jq '.default_workflow_permissions')"

[[ "${visibility}" == "public" ]] || fail "Profile repository is not public"
[[ "${default_branch}" == "main" ]] || fail "Default branch is not main"
[[ "${readme_path}" == "README.md" ]] || fail "Root README.md was not found"
[[ "${workflow_permission}" == "write" ]] || fail "Workflow token permissions are not write"

printf 'Remote profile verification passed.\n'
printf 'Account:             %s\n' "${login}"
printf 'Repository:          %s\n' "${REPO_FULL}"
printf 'Visibility:          %s\n' "${visibility}"
printf 'Default branch:      %s\n' "${default_branch}"
printf 'Profile README:      %s\n' "${readme_path}"
printf 'Workflow permission: %s\n' "${workflow_permission}"
