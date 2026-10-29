# Handoff for Next Agentic Work Session

**Created:** 2026-10-29T18:50:32Z
**Session Context:** Research phase complete (E001–E049). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md. Verification baseline integrity guards in place. Repository verified stable as of this handoff.

---

## Initial Task Message (START HERE)

> Repository is fully verified and in a stable state. **No new research is warranted.**
> Your primary task is to verify stability by running the extended verification suite, confirm the pre-existing known drifts remain unchanged, and report results.
> **Do not modify goldens, weaken tolerances, or change any gate logic.**
> If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
> All constraints from below still apply.

---

## Current State (verified at handoff time)

- **Branch:** `main`, up to date with `origin/main`. HEAD `65941f2` (chore(kilo): checkpoint agent session).
- **Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` show as modified — these are tracked files with mtime drift (pyc header embeds mtime); no source, experiment, or ledger changes. Do not commit them.
- **No `.verify_snapshot/`** active; no untracked files; no stale verification output.
- **`experiments/*.json` goldens match HEAD.**
- **`SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED**
- **Research phase complete (E001–E049).**

---

## Precise Task (bounded)

Re-run the verification suite to confirm stability:

```bash
SEED=42 python3 run_all_verification.py --extended
```

Expect the pre-existing E030/E041 drift below. **Do not** weaken tolerances, skip drivers, or modify committed goldens. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

After completion, report:
1. Overall pass/fail of the extended suite
2. Confirmation that E030 and E041 drifts match the known pattern (counts and nature) with no new structural diffs
3. Any anomalies (snapshot active, golden drift vs HEAD, data coverage issues)
4. Final state recommendation (stable / needs attention)

---

## Known Pre-Existing Drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone. Do **not** re-pin.
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

---

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated.
- Do not commit `__pycache__/*.pyc` — tracked but drift by mtime only; leave unstaged.
- Do not re-pin goldens or data baselines unless there is an explicit, documented need.

(End of file)
