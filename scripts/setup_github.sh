#!/usr/bin/env bash
# =============================================================================
# CHIP 2026 — GitHub setup for the PUBLIC repository (safe first commit and push)
# =============================================================================
# Usage (from anywhere; it locates the repository root itself):
#   scripts/setup_github.sh check     # read-only report (default)
#   scripts/setup_github.sh init      # git init if needed, branch = main, set remote 'origin'
#   scripts/setup_github.sh commit    # run checks, show what will be committed, ask, then commit
#   scripts/setup_github.sh push      # ask, then `git push -u origin main` (never --force)
#
# Environment (optional):
#   REPO_URL     default https://github.com/Ajilaca/peruri-chipathon-2026.git
#   BRANCH       default main
#   MAX_MB       default 5     (files larger than this block the commit)
#   MSG          commit message for `commit`
#   ASSUME_YES=1 skip the y/N questions (for automation/tests)
#
# The repository is public. `check` therefore scans every file that would be committed for
#   - secrets (GitHub tokens, Anthropic keys, private keys, AWS keys)  -> blocks the commit
#   - files over MAX_MB                                                -> blocks the commit
#   - e-mail addresses and +62 phone numbers                           -> warning, review by hand
# and confirms that .venv, Quartus build products, tooling.env and settings.local.json are ignored.
# No sudo, no force-push, no history rewriting.
# =============================================================================
set -uo pipefail

MODE="${1:-check}"
REPO_URL="${REPO_URL:-https://github.com/Ajilaca/peruri-chipathon-2026.git}"
BRANCH="${BRANCH:-main}"
MAX_MB="${MAX_MB:-5}"
ASSUME_YES="${ASSUME_YES:-0}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT" || exit 1

FAIL=0; WARN=0
ok()   { printf '\033[32m[ OK ]\033[0m %s\n' "$*"; }
warn() { printf '\033[33m[WARN]\033[0m %s\n' "$*"; WARN=$((WARN+1)); }
bad()  { printf '\033[31m[FAIL]\033[0m %s\n' "$*"; FAIL=$((FAIL+1)); }
info() { printf '       %s\n' "$*"; }
confirm() { [ "$ASSUME_YES" = "1" ] && return 0; local a; read -r -p "$1 [y/N] " a; [ "$a" = "y" ] || [ "$a" = "Y" ]; }
in_repo() { git rev-parse --is-inside-work-tree >/dev/null 2>&1; }

case "$MODE" in check|init|commit|push) ;; *) echo "usage: $0 [check|init|commit|push]"; exit 2 ;; esac
command -v git >/dev/null 2>&1 || { bad "git not found (Ubuntu: sudo apt install git)"; exit 1; }

# ------------------------------------------------------------------------------- init
do_init() {
  if ! in_repo; then git init -q && ok "git repository initialised"; else ok "already a git repository"; fi
  git symbolic-ref HEAD "refs/heads/$BRANCH" && ok "default branch is '$BRANCH'"
  if git remote get-url origin >/dev/null 2>&1; then
    local cur; cur="$(git remote get-url origin)"
    if [ "$cur" = "$REPO_URL" ]; then ok "remote origin already $cur"
    else warn "remote origin is $cur (wanted $REPO_URL); not changing it. Use: git remote set-url origin <url>"; fi
  else
    git remote add origin "$REPO_URL" && ok "remote origin set to $REPO_URL"
  fi
}

# ------------------------------------------------------------------------------ checks
candidates() { git ls-files -co --exclude-standard; }

check_identity() {
  local n e; n="$(git config user.name || true)"; e="$(git config user.email || true)"
  if [ -n "$n" ] && [ -n "$e" ]; then ok "git identity: $n <$e>"
  else
    bad "git user.name / user.email not set. Run:"
    info "git config --global user.name  \"Your Name\""
    info "git config --global user.email \"the address linked to your GitHub account\""
  fi
}

check_gh() {
  if command -v gh >/dev/null 2>&1; then
    if gh auth status >/dev/null 2>&1; then
      ok "GitHub CLI logged in"
      if git remote get-url origin >/dev/null 2>&1; then
        local vis; vis="$(gh repo view --json visibility -q .visibility 2>/dev/null || true)"
        [ -n "$vis" ] && info "remote repository visibility: $vis"
      fi
    else warn "gh installed but not logged in: run  gh auth login  (choose GitHub.com, HTTPS, browser login)"; fi
  else
    warn "GitHub CLI 'gh' not installed (Ubuntu: sudo apt install gh). Optional: git over HTTPS still works with a token."
  fi
}

check_ignored() {
  local p missing=0
  for p in .venv/pyvenv.cfg scripts/tooling.env .claude/settings.local.json \
           quartus/proj/output_files/x.rpt quartus/proj/db/x sim_build/x; do
    if git check-ignore -q "$p"; then :; else bad "not git-ignored: $p"; missing=1; fi
  done
  [ "$missing" -eq 0 ] && ok "ignore rules cover .venv, build products, tooling.env, settings.local.json"
}

check_size() {
  local f big=0 limit=$((MAX_MB*1024*1024))
  while IFS= read -r f; do
    [ -f "$f" ] || continue
    if [ "$(stat -c %s "$f")" -gt "$limit" ]; then bad "file over ${MAX_MB} MB: $f ($(du -h "$f" | cut -f1))"; big=1; fi
  done < <(candidates)
  [ "$big" -eq 0 ] && ok "no file over ${MAX_MB} MB in the commit set"
}

SECRET_RE='ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|gho_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}|-----BEGIN ((RSA|EC|OPENSSH|DSA) )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}'
check_secrets() {
  local hits
  hits="$(candidates | tr '\n' '\0' | xargs -0 -r grep -IEn "$SECRET_RE" 2>/dev/null | sed -E 's/(:[0-9]+:).*/\1 <match hidden>/' || true)"
  if [ -n "$hits" ]; then bad "possible secret(s) in files to be committed (values hidden):"; printf '%s\n' "$hits" | sed 's/^/         /'
  else ok "no secret patterns found in the commit set"; fi
}

check_pii() {
  local hits host user
  hits="$(candidates | tr '\n' '\0' | xargs -0 -r grep -IEn '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\+62[ -]?[0-9]{2,4}' 2>/dev/null | cut -c1-160 || true)"
  if [ -n "$hits" ]; then
    warn "e-mail address or +62 phone number found (repo is PUBLIC; keep only what you intend to publish):"
    printf '%s\n' "$hits" | head -15 | sed 's/^/         /'
  else ok "no e-mail addresses or +62 phone numbers in the commit set"; fi
  # machine identity: host name and home path leak from tool logs (e.g. docs/TOOLING_INSTALL_LOG.md)
  host="$(hostname 2>/dev/null || true)"; user="${USER:-$(id -un 2>/dev/null || true)}"
  hits="$( { [ -n "$host" ] && candidates | tr '\n' '\0' | xargs -0 -r grep -IlF -- "$host" 2>/dev/null; \
             [ -n "$user" ] && candidates | tr '\n' '\0' | xargs -0 -r grep -IlF -- "/home/$user" 2>/dev/null; } | sort -u || true)"
  if [ -n "$hits" ]; then
    warn "this machine's host name or home path ('$host', '/home/$user') appears in files to be committed:"
    printf '%s\n' "$hits" | sed 's/^/         /'
    info "Logs are evidence, so do not edit them silently. Decide: publish as is, or redact before committing."
  fi
}

check_files() {
  local f
  for f in CLAUDE.md README.md .claude/settings.json; do
    [ -f "$f" ] && ok "present: $f" || warn "missing: $f"
  done
}

run_checks() {
  in_repo || { warn "not a git repository yet (run: scripts/setup_github.sh init)"; return 0; }
  check_identity; check_gh; check_ignored; check_size; check_secrets; check_pii; check_files
  if git remote get-url origin >/dev/null 2>&1; then ok "remote origin: $(git remote get-url origin)"
  else warn "no remote 'origin' (run: scripts/setup_github.sh init)"; fi
}

summary() { printf '\nSummary: %d failure(s), %d warning(s)\n' "$FAIL" "$WARN"; }

# ------------------------------------------------------------------------------- modes
case "$MODE" in
  check)
    run_checks
    if in_repo; then echo; echo "Would be committed (git status --short, first 40):"; git status --short | head -40; fi
    summary; [ "$FAIL" -eq 0 ]; exit $? ;;
  init)
    do_init; run_checks; summary; [ "$FAIL" -eq 0 ]; exit $? ;;
  commit)
    in_repo || { bad "not a git repository. Run: scripts/setup_github.sh init"; exit 1; }
    run_checks
    if [ "$FAIL" -ne 0 ]; then summary; echo "Fix the failures above, then run this again. Nothing was committed."; exit 1; fi
    echo; echo "About to commit these changes:"; git status --short | head -60
    confirm "Stage everything above (git add -A) and commit?" || { echo "aborted; nothing committed."; exit 1; }
    git add -A
    if git commit -q -m "${MSG:-chore: initial project scaffold (tooling, skills, docs)}"; then
      ok "committed: $(git log --oneline -1)"
    else bad "git commit failed (nothing to commit, or identity missing)"; exit 1; fi
    info "Next: scripts/setup_github.sh push" ;;
  push)
    in_repo || { bad "not a git repository"; exit 1; }
    git remote get-url origin >/dev/null 2>&1 || { bad "no remote 'origin'. Run: scripts/setup_github.sh init"; exit 1; }
    git rev-parse --verify HEAD >/dev/null 2>&1 || { bad "no commits yet. Run: scripts/setup_github.sh commit"; exit 1; }
    check_secrets; check_size
    [ "$FAIL" -eq 0 ] || { echo "Refusing to push while checks fail."; exit 1; }
    echo "Push branch '$BRANCH' to $(git remote get-url origin)  (PUBLIC repository)"
    confirm "Push now? (never forced)" || { echo "aborted; nothing pushed."; exit 1; }
    if git push -u origin "$BRANCH"; then ok "pushed. Open: ${REPO_URL%.git}"
    else
      bad "push failed. Common causes: not logged in (gh auth login), or the remote already has commits."
      info "If the remote has commits: git pull --rebase origin $BRANCH   (then push again). Do not force-push."
      exit 1
    fi ;;
esac
