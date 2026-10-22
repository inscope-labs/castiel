#!/usr/bin/env bash
# Commit the regenerated merged spec file, or open/update a pull request for it.
# Inputs (environment): SPEC_DIR, MODE (pr|commit), BASE_BRANCH. In pr mode the
# gh CLI needs GH_TOKEN. Does nothing when the merged file is unchanged.
set -euo pipefail

SPEC_DIR="${SPEC_DIR:?SPEC_DIR is required}"
MODE="${MODE:-pr}"
BASE_BRANCH="${BASE_BRANCH:?BASE_BRANCH is required}"
case "$MODE" in
  pr|commit) ;;
  *) echo "::error::Unknown mode: $MODE (expected pr or commit)"; exit 2 ;;
esac
NAME="$(basename "$SPEC_DIR")"
OUT="$SPEC_DIR/$NAME-spec-full.md"
SOURCE_SHA="$(git rev-parse --short HEAD)"
MESSAGE="Regenerate $NAME-spec-full.md"

git add -- "$OUT"
if git diff --cached --quiet; then
  echo "$OUT is up to date; nothing to do."
  exit 0
fi

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

case "$MODE" in
  commit)
    git commit -q -m "$MESSAGE"
    # Other merge-spec runs may push to the same branch at the same time; rebase and retry.
    pushed=0
    for attempt in 1 2 3 4 5; do
      if git push origin "HEAD:${BASE_BRANCH}"; then pushed=1; break; fi
      echo "Push attempt ${attempt} was rejected; rebasing onto origin/${BASE_BRANCH} and retrying."
      git fetch -q origin "${BASE_BRANCH}"
      git rebase -q "origin/${BASE_BRANCH}" || { git rebase --abort || true; break; }
      sleep $((attempt * 2))
    done
    if [ "$pushed" != "1" ]; then
      echo "::error::Push to ${BASE_BRANCH} failed. If the branch is protected, run this workflow with mode=pr."
      exit 1
    fi
    echo "Committed $OUT to ${BASE_BRANCH}."
    ;;
  pr)
    BRANCH="automation/merge-spec-${NAME}"
    git checkout -q -B "$BRANCH"
    git commit -q -m "$MESSAGE"
    git push --force origin "$BRANCH"
    OPEN="$(gh pr list --head "$BRANCH" --base "$BASE_BRANCH" --state open --json number --jq 'length')"
    if [ "$OPEN" = "0" ]; then
      gh pr create --base "$BASE_BRANCH" --head "$BRANCH" \
        --title "$MESSAGE" \
        --body "Regenerated \`$OUT\` from the individual spec files at \`${SOURCE_SHA}\` by the merge-spec workflow. Generated file; do not edit by hand." || {
        echo "::error::Could not open a pull request. Enable Settings > Actions > General > 'Allow GitHub Actions to create and approve pull requests', or run with mode=commit."
        exit 1
      }
    else
      echo "A pull request for $BRANCH is already open; branch updated."
    fi
    ;;
  *)
    echo "::error::Unknown mode: $MODE (expected pr or commit)"
    exit 2
    ;;
esac
