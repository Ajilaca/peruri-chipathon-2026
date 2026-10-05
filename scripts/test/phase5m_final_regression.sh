#!/usr/bin/env bash
# scripts/test/phase5m_final_regression.sh -- Phase 5M V7 and V8 of evidence/phase05m/test_plan_s8.md (Amendment A1 of test_plan.md): the one full
# regression of the S6-S8 sequence, run on the final tree. Header: git SHA, dirty state, and the added / modified file counts since 288a78c (the commit
# before the first Phase 5M RTL file). Then, one after the other and unchanged: S6 verification, S7 verification, Phase 0-5 regression (V8), Phase 5 verification
# of the C4 wrappers. The formal runs are separate (formal/run/run_formal_phase5m*.py, formal/run/run_formal_phase5.py). Last line "OVERALL: PASS" only if every step
# returned 0. Usage: . scripts/env.sh && scripts/test/phase5m_final_regression.sh > <log>
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
echo "git SHA: $(git rev-parse HEAD)"
echo "working tree: $(git status --porcelain | grep -v '^??' | wc -l) tracked file(s) changed, $(git status --porcelain | grep -c '^??') untracked"
echo "files since 288a78c (committed): added $(git diff --name-status 288a78c HEAD | grep -c '^A'), modified $(git diff --name-status 288a78c HEAD | grep -c '^M'), deleted $(git diff --name-status 288a78c HEAD | grep -c '^D')"
echo "modified existing files since 288a78c:"
git diff --name-status 288a78c HEAD | grep '^M' | sed 's/^/  /'
overall=0
run() {
    echo "## $1"
    shift
    "$@"
    local rc=$?
    echo "## rc=$rc"
    [ "$rc" -eq 0 ] || overall=1
}
run "V7 S6 verification (phase5m_verify.sh)"            scripts/test/phase5m_verify.sh
run "V7 S7 verification (phase5m_verify_s7.sh)"         scripts/test/phase5m_verify_s7.sh
run "V8 Phase 0-5 regression (phase5_regression.sh)"    scripts/test/phase5_regression.sh
run "V8 Phase 5 verification (phase5_verify.sh)"        scripts/test/phase5_verify.sh
[ "$overall" -eq 0 ] && echo "OVERALL: PASS" || echo "OVERALL: FAIL"
exit "$overall"
