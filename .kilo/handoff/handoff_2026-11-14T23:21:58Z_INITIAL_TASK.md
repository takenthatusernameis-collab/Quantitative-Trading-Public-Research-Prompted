# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-14T23:21:58Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `9f88f171` ("chore(kilo): checkpoint agent session"); in sync with `origin/main` at session start
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree (source/data):** no research/source/data/config changes. `git status --short` shows modified tracked `__pycache__/*.pyc` artifacts only (e.g. `scripts/__pycache__`, `src/__pycache__`, `tests/__pycache__`) — build noise; do **not** commit or treat as research changes.
- **Verification snapshot:** no active `.verify_snapshot/` or `.verify_reports/` observed; no interrupted verification run indicated.
- **Goldens/baselines:** prior verified state is `experiments/*.json` matching HEAD with `ledger/golden_baseline.json` and `ledger/data_baseline.json` consistent (confirm with guards below before new work).
- **Research phase:** complete (E001–E051). Surviving validated strategies and dispositions documented in `ledger/RESEARCH_LEDGER.md`.
- **Delta vs prior durable handoff** (`handoff_2026-11-14T22:32:41Z_INITIAL_TASK.md`): handoff refresh only in this session; no research/code/ledger/baseline/data changes.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

1. **Confirm repo state**
   ```bash
   git status --short
   SEED=42 bash scripts/check.sh
   ```
   Expect `check.sh` exit 0 ("All checks passed") for a clean baseline. If it fails due to missing deps (`ModuleNotFoundError`), install first: `pip3 install --break-system-packages -r requirements.txt` — not a research/baseline failure.

2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Stale/active verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding. Do not start a new verification run while another live run owns the snapshot.
   - Golden baseline fingerprint mismatch → compare against `ledger/golden_baseline.json`; do **not** re-pin without explicit instruction and documented justification.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source, data, experiment, ledger, or baseline changes unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit instruction and justification in the diff.
   - Do **NOT** commit `__pycache__/*.pyc` or other build noise.
   - Do **NOT** create `.github/workflows/verification-gate.yml` as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).

---

## Key Commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Verification
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)

# Recovery / guards
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

---

## Known Open Items (see AGENTS.md / ledger/RESEARCH_LEDGER.md)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Tangency QP is ill-conditioned — 1-ulp input changes can move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 numeric diffs. **Do not re-pin to silence.**
- **E041 drift:** ~133 numeric differences (1-ulp QP sensitivity); structural differences fixed. Open in ledger — do not re-pin.
- **CI gate:** maintainer must create workflow via GitHub UI from `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output or `__pycache__/*.pyc`.

---

## Durable artifact & provenance

- **Primary:** `handoff_2026-11-14T23:21:58Z_INITIAL_TASK.md` (repo root)
- **Mirrors:** `handoff/` (and existing canonical mirror dirs if present)
- **Generic canonical pointers:** repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-14T23:21:58Z_INITIAL_TASK.md`
- **Supersedes:** `handoff_2026-11-14T22:32:41Z_INITIAL_TASK.md`. Prior timestamped handoff artifacts retained for history.
- This handoff refresh records no research/code/ledger/baseline/data changes.
