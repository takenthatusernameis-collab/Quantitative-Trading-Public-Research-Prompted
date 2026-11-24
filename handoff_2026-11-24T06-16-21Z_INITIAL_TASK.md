# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T06:16:21Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `4628016eb31d34148f7f097a7eb0fae85c351e88` ("chore(kilo): checkpoint agent session")
**Remote sync:** `origin/main` aligned with local `main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete (E001–E043). Authoritative dispositions and the surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items.
- **Working tree:** clean apart from `src/__pycache__/cache_keys.cpython-312.pyc` (pre-existing binary noise, not a canonical artifact). No `experiments/`, `data/`, `src/` source, `scripts/`, `tests/`, ledger, or baseline files were changed.
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` are **absent** (no interrupted verification pending; no `ACTIVE.json` marker).
- **Canonical baselines/artifacts:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned data/fundamentals inputs are unchanged and match HEAD.
- **Dependencies:** `pip install -r requirements.txt` is **NOT yet provisioned** in this environment (numpy/pandas/scipy/pyarrow absent). Required before any verification run.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT active-set enumeration, commit `72dc947`) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift; there is no remaining tolerance violation.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, move pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction. If your only action is to refresh this handoff, that is an explicitly requested maintenance task here — but do not manufacture repeated refreshes to appear busy.

If you must act autonomously, work in order and stop when the step is done:

1. **Verify and stop.** Confirm HEAD/remote alignment (`git status --short --branch`, `git rev-list --left-right --count origin/main...HEAD`). If clean, report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min; re-executes all committed drivers and compares to goldens). Report per-driver drift precisely; **do not** re-pin artifacts to make a tolerance violation disappear.
3. **E041/E042 residual ill-conditioned-QP drift (~1e-05):** already root-caused and fixed via the E050 exact KKT active-set enumeration (ledger E049/E050). Only revisit if step 2 shows a *new* structural difference; never "fix" it by re-pinning.
4. **Cleanup (propose only).** The repo root holds ~1,637 `handoff_*` files (git-tracked) plus large mirror trees. If this is a problem, *propose* (do not execute) a `.gitignore` + `git rm --cached` consolidation plan and let the user decide.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`). Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required via GitHub UI).
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-24T06:16:21Z` → `handoff_2026-11-24T06-16-21Z_INITIAL_TASK.md` (repo root).
- Root alias symlinks (`handoff_CURRENT`, `handoff_LATEST`, `next`, `initial_task`, etc.) and the `handoff/` and `.kilo/handoff/` mirror alias symlinks were repointed to this file.
- **Supersedes operationally:** the previous handoff artifacts (retained for history), including `handoff_2026-11-24T06-14-53Z_INITIAL_TASK.md` and `handoff_2026-11-24T06-12-42Z_INITIAL_TASK.md` / `...06-12-26Z...`.
- This session created this durable handoff (and repointed aliases) only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made (left uncommitted pending explicit direction).
- Handoff written by agent at 2026-11-24T06:16:21Z.