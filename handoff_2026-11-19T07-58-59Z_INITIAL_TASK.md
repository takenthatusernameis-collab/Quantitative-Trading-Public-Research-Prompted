# Agentic Work Session Handoff — Initial Task Message

**Created**: 2026-11-19T07:58:59Z
**Supersedes**: `handoff_2026-11-19T07-57-59Z_INITIAL_TASK.md` (as the current durable artifact only)
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Repository state at creation**: HEAD `371432f0` ("chore(kilo): checkpoint agent session") == `origin/main` (0 ahead / 0 behind), working tree clean, no `.verify_snapshot/`, no `.verify_reports/`.

## Initial Task Message

You are continuing an independent, reproducible quantitative-research repository whose
research phase is **closed** (E001–E051 experiments). Do **not** start new research, re-pin
baselines, or change experiment artifacts unless the user explicitly asks. Orient, verify,
then wait for instruction.

## Start Here (ordered)

1. **Orient**: `git log --oneline -5`, `git status --short --branch`, `git rev-parse HEAD`.
   Confirm HEAD matches `origin/main` and the tree is clean.
2. **Recover any interrupted verification**: if `.verify_snapshot/` exists, run
   `SEED=42 python3 run_all_verification.py --restore-only` before doing anything else.
   Never commit captured verification output.
3. **Confirm golden integrity** (fast, pure-stdlib):
   - `python3 scripts/check_goldens_clean.py`
   - `python3 scripts/check_golden_baseline.py`
   - `git diff --name-only HEAD -- experiments/` → empty
4. **Install dependencies**: `pip install -r requirements.txt`.
5. **Run the fast gate**: `SEED=42 bash scripts/check.sh` (≈seconds, offline).
6. **Await explicit instruction.** If none is given, do not invent work; refresh the
   handoff and report.
7. **Before ending**: leave your own timestamped handoff so the next session starts clean.

## Integrity Rules (non-negotiable)

- Never commit verification output.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect.
- Cache coverage is an enforced invariant; missing cache entry fails hard under `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer determinism (ledger E049): validate solver answers on constraints, never exit status.
- Known residual drift: E041/E042 1-ulp QP drift is expected; do not re-pin to silence.
- Do not commit unless the user explicitly asks.

## Key References

- `AGENTS.md` — commands, conventions, baseline-integrity rules
- `ledger/RESEARCH_LEDGER.md` — all experiments and decisions
- `ledger/PRIORITIZATION.md` — candidate ranking procedure
- `experiments/` — canonical research artifacts
- `scripts/` — guards and `repoint_handoff.py`

## Recurring Handoff Procedure

1. Write `handoff_<UTC timestamp>_INITIAL_TASK.md` at repo root.
2. Repoint aliases: `python3 scripts/repoint_handoff.py <new-filename>` (expect `repointed: 490`).
3. Verify alias spot-check resolves to the new file; confirm SHA-256.
4. Append a ledger entry summarizing state verified, SHA-256, constraints honored.
5. Leave changes uncommitted unless asked.
6. If a stale pointer breaks, run `python3 scripts/repair_broken_handoff.py`.

(End of file)
