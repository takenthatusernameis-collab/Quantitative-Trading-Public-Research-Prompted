# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12-33-35Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `00c554f` (chore(kilo): checkpoint agent session)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. Do NOT commit verification output.
4. Only after steps 1–3 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Baseline-integrity note (verified this session)

The interrupted-run recovery (`SEED=42 python3 run_all_verification.py --restore-only`) was run at 12:25Z and cleared the stale `.verify_snapshot/` marker (pid 37032, dead). After recovery, the working tree differs from HEAD on exactly **3** `experiments/*.json` files by ~1e-16 (`corr_spy` last-significant-digit drift):

- `experiments/cointegration_large_liquid.json`
- `experiments/dollar_neutral_lowbeta_large_liquid.json`
- `experiments/pairs_large_liquid.json`

This is **expected and correct, not a defect**. Both guards were run and give ground truth:

- `python3 scripts/check_goldens_clean.py` → **FAIL 3** (compares worktree vs HEAD).
- `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (compares worktree vs `ledger/golden_baseline.json`).

The worktree matches the pinned baseline for all 107 artifacts; the 3 mismatches are HEAD-only. Root cause: `ledger/golden_baseline.json` was last updated at commit `2c4ca4b` (2026-10-31 17:13Z), which pinned these 3 files to their canonical values. A later checkpoint commit at `32574a6` (2026-11-01 11:29Z) overwrote them in HEAD with float-drifted copies, and those drifted blobs are **not present in the git object store** (`git cat-file -e <pin>` → "blob NOT in object store"), so they cannot be recovered from any commit. The pinned baseline is the authoritative record (per AGENTS.md: *"the committed golden is the authoritative record, not the latest re-run"*), and the working tree already holds it. **Do not `git checkout -- experiments/`** — that would replace the canonical values with HEAD's drifted ones and break `check_golden_baseline.py`. The correct resolution, if these files must be committed, is to commit the worktree as-is (it already matches the pin); no re-pin is needed.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch). The SLSQP tangency QP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 sensitivity-grid and E042-primary artifacts still drift vs their goldens by 29–133 numeric diffs (down from 360–9273 after the E049 exit-status fix).

Do NOT re-pin to silence. The intended fix is a *research-engineering* change:
- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (for N ≤ 5 this is feasible and was used as the reference oracle in E049).
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:253`, which masks a negative denominator; at the 2019-10-16 rebalance it yields magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. A correct start point (a max-`mu_s'w` LP on the feasible simplex) makes SLSQP converge to the exact optimum there and **will change published numbers** — so it belongs to a deliberate re-pin, not a silent fix.
- After the fix, re-run the affected drivers (`experiments/run_e041.py`, `experiments/run_e042.py --n-sim ...`, `experiments/run_e042_lead.py`) and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Never leave a verification run half-finished (the `.verify_snapshot/` crash-safe marker exists precisely for this).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 entry; E041/E042 entries follow)
- AGENTS.md — full commands, reproducibility, and baseline-integrity conventions

## Durable links

- `handoff.md` → this file (latest)
- `handoff_next_session.md` → this file
- `handoff_current.md` → this file
- `HANDOFF_NEXT_SESSION_LATEST.md` → this file

(End of file)
", "filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-11-01T12-33-35Z.md