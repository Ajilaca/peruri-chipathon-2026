<!-- claim-lint: skip-file (template) -->
# Result — Phase <N>: <name>

Copy to `docs/results/result_phase<N>.md`. Fill it **only from evidence produced in this repository**.
Anything not proven stays `MISSING`. Validate with
`python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase<N>.md`.

- Status: NOT DONE   (DONE only if every row in section 1 is PASS; PARTIAL if some are MISSING or FAIL)
- Date (UTC): <YYYY-MM-DD HH:MM>
- Git commit (HEAD when verified): <short sha>
- Environment: <OS; Python; tool versions, copied from command output>

## 1. Done-criteria (copied from docs/ROADMAP.md, unchanged)
| # | Criterion | Evidence (`path` under docs/evidence/ or tests, or `cmd: ...`) | Status |
|---|---|---|---|
| 1 | <criterion> | `<path>` | MISSING |

Status is PASS, FAIL or MISSING. PASS needs at least one backticked evidence item that exists.
Simulation-only results are labelled "simulation only" in the criterion text.

## 2. What was produced
| Path | Purpose |
|---|---|
| <path> | <purpose> |

## 3. Numbers (each labelled MEASURED, ESTIMATE, or cited [n])
| Quantity | Value | Label | Evidence |
|---|---|---|---|
| <quantity> | <value> | MEASURED | `<path>` |

## 4. Standards and sources pinned
<Standard and revision, errata state read, test-vector source with commit hash and sha256, oracle name/version/licence.>

## 5. Coverage and limits
<What the tests do NOT cover; sample-vector caveats; what was not run.>

## 6. Deviations, failures and open issues
<Every failure or deviation, honestly, with the log path. "None" only if true.>

## 7. Decisions needed
<Link docs/decisions/PENDING.md items or new ADRs.>

## 8. Claims made in this phase
<"None", or each claim with its label. Run /proposal-claims on any text meant for judges.>

## 9. Reproduce
```bash
<exact commands, from repo root>
```

## 10. Approval
- [ ] Human approver (name, date): 
      Next phase starts only after a team member ticks this box. Claude never ticks it.
