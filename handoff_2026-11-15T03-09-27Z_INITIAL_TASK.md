# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T03:09:27Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` @ `501c0ae3` ("chore(kilo): checkpoint agent session", 2026-11-15 02:22:38 +0000); in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task (do first)

1. **Confirm baseline integrity**
   - `SEED=42 bash scripts/check.sh`
   - Expect exit 0 (`=== All checks passed ===`). If it fails with `ModuleNotFoundError`, install deps (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.
2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`).
   - Active/stale verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.
3. **Then idle awaiting explicit user direction.**
   - Do **not** make source changes or commits unless explicitly asked.
   - Do **not** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **not** re-pin baselines without explicit instruction and justification in the diff.
   - Do **not** commit `__pycache__/*.pyc` or other build artifacts.

## Current state

- **Working tree:** no source/data/research changes. Only `__pycache__/*.pyc` files are modified (build artifacts; gitignored output) — leave uncommitted.
- **Verification snapshot:** none active (`.verify_snapshot/` / `.verify_reports/` absent). No interrupted verification run.
- **Goldens:** `experiments/*.json` (138 tracked) are the canonical baseline; treat as unchanged unless integrity checks say otherwise.
- **Environment:** Python 3.12.3. If reset, install deps with `pip3 install --break-system-packages -r requirements.txt` before trusting checks.
- **Delta vs prior durable handoff** (`handoff_2026-11-15T02-23-20Z_INITIAL_TASK.md`, HEAD `6339037f`, ledger E068): HEAD advanced `6339037f` → `501c0ae3`; **0 research-path changes** (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, `ledger/`). No research substance changed. This refresh = E069.

## Research status

- Research phase complete (E001–E051). Surviving validated strategies and dispositions are documented in `ledger/RESEARCH_LEDGER.md`.
- Convention: close-to-close v1.2.3 primary; always `SEED=42`.

## Key commands

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

## Known open items (see AGENTS.md / ledger before acting)

- **Optimizer determinism (E049/E050):** `src/portfolio_opt.py` validates solver answers on problem constraints (not exit status). Tangency QP is ill-conditioned (1-ulp sensitivity moves `min_var` ~1e-05); E041/E042 grid artifacts can drift (E041: 133 numeric diffs). **Do not re-pin to silence drift.** Rule pinned by `tests/test_portfolio_opt.py`.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.

## Durable artifact & pointers

- Primary: `handoff_2026-11-15T03-09-27Z_INITIAL_TASK.md` (repo root).
- Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical aliases repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T03-09-27Z_INITIAL_TASK.md`.
- Supersedes: `handoff_2026-11-15T02-23-20Z_INITIAL_TASK.md` (E068).
