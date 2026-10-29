# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T12:30:00Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main` (up to date with origin/main; HEAD `cadbd34`)
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. The working tree was left **clean** (only pyc noise, no verification output). If it ever holds verification output instead of committed goldens, restore first:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- Golden mismatch or stale `.verify_snapshot/`? Restore with `--restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification and a ledger entry.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
**Known non-green:** `run_e042_lead.py` fails — see *Open finding* below. All other 11 steps pass and goldens are restored at the end. If interrupted, run `--restore-only`; **do not commit** a half-finished run.

### 4. Orient to open work
- Read `AGENTS.md` (Baseline Integrity, Reproducibility sections).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040 (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only when the user provides a concrete objective.
- Numeric drift in E041/E042 is expected (ill-conditioned QP, 1-ulp sensitivity). Do **not** re-pin to silence it — see the open item in the ledger.

---

## Open Finding (new this session, 2026-10-29T12:30Z)

`SEED=42 python3 run_all_verification.py` reports `OVERALL: FAILURES DETECTED`, with the **sole** failure on `run_e042_lead.py` (exit 1 + JSON mismatch). Characterized precisely:

- **23 numeric differences, 0 structural** vs the committed `experiments/e042_lead_config_confirmatory.json`.
- **Deterministic across runs** (3 consecutive runs identical to the last bit) and **independent of BLAS threading** (`OMP_NUM_THREADS` 1/2/4/8 all identical).
- **Decision and gates unchanged:** `decision` REJECTED, `gates_passed_count` 4/5, `G2_placebo_z_gte_3.0` FAIL under both old (z 1.8121) and new (z 1.3219) values.
- The drift is concentrated in the `max_sharpe` tangency-QP path: `primary/oos_sharpe` 0.8659 -> 0.8009, `positive_folds` 27 -> 26, `equity_beta` -0.0009 -> -0.0013, `turnover` 0.0050 -> 0.0045, `is_sharpe` 0.5846 -> 0.5497, plus the 5 `/placebo_constrained` statistics. The `min_var`-only fields (`max_drawdown`, `sideways/sharpe_mean`) drift by <2e-08.
- This is the **documented E049 open item**: the tangency QP is ill-conditioned (1-ulp input perturbation moves answers by ~1e-05), so the artifact still drifts by 29-133 differences. The E049 fix removed the *dominant* environment dependence (the solver's exit status) but did not make the QP well conditioned.
- **Do NOT re-pin** `e042_lead_config_confirmatory.json` to silence this — the ledger's standing disposition is that the committed golden is the authoritative record, and the research conclusion is unchanged either way.

---

## Key Files to Read First
- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

---

## Gotchas / Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json` owning pid).
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); a maintainer must create it via the GitHub UI.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean, not to invent new research.

---

## Handoff Notes
- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` point here.
- Immediate predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T12-26-43Z.md`.