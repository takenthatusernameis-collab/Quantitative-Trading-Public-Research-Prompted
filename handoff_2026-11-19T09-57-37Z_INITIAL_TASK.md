# Agentic Work Session Handoff — Initial Task Message

**Created**: 2026-11-19T09:57:37Z
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Repository state at creation**: HEAD `e60fe7fe0e0ff48e80eb11da20540d7af2810cdf` == `origin/main` (0 ahead / 0 behind), working tree clean, no `.verify_snapshot/`.

## Initial Task Message

You are continuing an independent, reproducible quantitative-research repository whose research phase is **closed** (E001–E043 experiments complete). **Do not** start new research, re-pin baselines, or change experiment artifacts unless the user explicitly asks. Orient, verify, then wait for instruction.

## Start Here (ordered)

1. **Orient**: `git log --oneline -5`, `git status --short --branch`, `git rev-parse HEAD`. Confirm HEAD matches `origin/main` and the tree is clean.
2. **Recover any interrupted verification**: if `.verify_snapshot/` exists, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before doing anything else. Never commit captured verification output.
3. **Confirm golden integrity** (fast, pure-stdlib, no deps needed):
   - `python3 scripts/check_goldens_clean.py` → all committed artifacts match HEAD
   - `python3 scripts/check_golden_baseline.py` → all pinned artifacts match the baseline
   - `git diff --name-only HEAD -- experiments/` → empty
4. **Install dependencies** (this runner has python 3.12.3 but no numpy/pandas/scipy): `pip install -r requirements.txt`.
5. **Run the fast gate**: `SEED=42 bash scripts/check.sh` (≈seconds, offline).
6. **Await explicit instruction.** If none is given, do not invent work; refresh the handoff (see *Recurring Handoff Procedure*) and report.
7. **Before ending**: leave your own timestamped handoff so the next session starts clean.

## Project Context

Independent reproducible research on 2014–2026 US equities, futures, and macro data. Every experiment is pre-registered (gates + falsification expectations + sensitivity grid) before execution. Negative results are recorded honestly (REJECTED / PARTIAL). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`; ranking criteria in `ledger/PRIORITIZATION.md`.

## Verification Scopes

| Command | Scope | Typical time |
|---|---|---|
| `SEED=42 bash scripts/check.sh` (`make check`) | convention robustness + template + golden guards | seconds |
| `SEED=42 python3 run_all_verification.py` (`make verify-quick`) | 8 drivers + batch_run + validate + E042 n_sim=2 | ~8 min |
| `... --extended` (`make verify-extended`) | quick + 18 more committed drivers, structural match | ~21 min |
| `... --full` (`make verify-full`) | E042 n_sim=50 + 96-config sensitivity grid | ~15 min |

Always use `SEED=42`. The suite backs up goldens into `.verify_snapshot/` (gitignored, with an owning-pid `ACTIVE.json`) and restores them afterwards; it self-recovers at startup and refuses to start while another live run owns the snapshot.

## Integrity Rules (non-negotiable)

- **Never commit verification output.** If a run is interrupted, restore first (`run_all_verification.py --restore-only`).
- **Never re-pin** `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect. The committed golden is the authoritative record, not the latest re-run. Re-pinning requires a deliberate `--update` that shows up in the diff.
- **Cache coverage is an enforced invariant**: every `data.download()` call site must have a pinned, git-tracked cache file matching `ledger/data_baseline.json`. The suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`, so a missing cache entry fails hard.
- **Optimizer determinism (ledger E049)**: `src/portfolio_opt.py` validates solver answers on the problem's constraints, never on the solver's exit status. Do not revert to status-gating.
- **Known residual drift**: E041/E042 artifacts drift by 1-ulp sensitivity of an ill-conditioned QP (E041 ~133 numeric diffs, 0 structural). This is expected; do **not** re-pin to silence it.
- **Commit policy**: do not commit unless the user explicitly asks.
- Do not commit `__pycache__` or scratch files.

## Key References

- `AGENTS.md` — commands, conventions, baseline-integrity rules
- `ledger/RESEARCH_LEDGER.md` — all experiments and decisions (append new entries here)
- `ledger/PRIORITIZATION.md` — candidate ranking procedure
- `experiments/` — git-tracked canonical research artifacts
- `run_all_verification.py`, `verify_convention_robustness.py` — verification suite
- `scripts/` — guards (`check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, `check_json_artifacts.py`), `repoint_handoff.py`, `repair_broken_handoff.py`

## Recurring Handoff Procedure

This repository keeps **one canonical handoff at the repo root** plus ~490 alias symlinks in `.`, `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.

1. Write `handoff_<UTC timestamp>_INITIAL_TASK.md` at the repo root (use `date -u +%Y-%m-%dT%H:%M:%SZ`; filename separator is `-` between HH-MM-SS, e.g. `handoff_2026-11-19T09-57-37Z_INITIAL_TASK.md`).
2. Repoint aliases: `python3 scripts/repoint_handoff.py <new-filename>`. Expect `repointed: 490` and `checked=490 bad=0`.
3. Verify: alias spot-check (`HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`, `handoff/CURRENT`, `.kilo/handoff/CURRENT`) resolves to the new file; confirm the canonical file's SHA-256.
4. Append a ledger entry (`## E527: Durable Handoff Refresh — Clear Initial Task Message (HEAD <sha>) [<timestamp>]`) summarizing state verified, SHA-256, and constraints honored.
5. Leave changes **uncommitted** unless the user asks for a commit.
6. If a stale pointer breaks, `python3 scripts/repair_broken_handoff.py` repairs the symlink graph.

## Environment Notes (this runner)

`/usr/bin/python3` is 3.12.3; `numpy`/`pandas`/`scipy` are **not** installed. `scripts/check.sh` was not executed this session; installing `requirements.txt` and running the fast gate are the next session's first substantive steps. Both golden guards are pure-stdlib and pass at HEAD `e60fe7fe0e0ff48e80eb11da20540d7af2810cdf`.
