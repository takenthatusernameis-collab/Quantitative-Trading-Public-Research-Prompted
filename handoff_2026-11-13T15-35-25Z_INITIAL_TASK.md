# INITIAL TASK — Handoff for the Next Agentic Work Session

**Handoff timestamp (UTC):** 2026-11-13T15:35:25Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `5f642209 chore(kilo): checkpoint agent session` on `main`
**Sync with origin:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (HEAD == `origin/main`)
**Working tree:** clean for `experiments/` and `data/` (`git status --short experiments/ data/` → empty). Only tracked `__pycache__/*.pyc` bytecode files show as modified (binary, no functional impact).
**Interrupted run:** none — `.verify_snapshot/` absent; `.verify_reports/` absent.

---

## Verified state at handoff time

| Check | Command | Result |
|---|---|---|
| Goldens vs HEAD | `SEED=42 python3 scripts/check_goldens_clean.py` | **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD** (exit 0) |
| Data coverage | `SEED=42 python3 scripts/check_data_coverage.py` | **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0) |
| Tracked experiment artifacts | `git ls-files experiments/ \| wc -l` | 138 |

No research, source, data, experiment, or baseline substance changed during this handoff. Nothing was committed by this session.

---

## Project status

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`. Ledger entries E052+ are durable-handoff refreshes only.
- Canonical artifacts: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin them as a side effect of verification.**
- Closed / do not reopen: E049/E050 (optimizer determinism + exact KKT enumeration) and the residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin E041/E042 to silence drift.**

---

## Supersedes

This handoff supersedes `handoff_2026-11-13T15-33-50Z_INITIAL_TASK.md` (HEAD `a53be4364d459020fe72fab3d8e1ca1cebf3e0e0`). Delta from `a53be436` to `5f642209` is a single checkpoint commit whose only substantive path is `ledger/RESEARCH_LEDGER.md` (durable-handoff refresh); `git diff --name-only a53be436..5f642209 -- experiments/ data/ src/ tests/ scripts/` is empty.

---

## CLEAR INITIAL TASK for the next session

1. **Do not begin substantive research work until the user gives explicit direction.** First read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (tail), and this handoff.
2. **Confirm the baseline is healthy** (cheap, offline, already green as of this handooff):
   ```bash
   git status --short --branch
   SEED=42 bash scripts/check.sh          # or: make check
   ```
3. **If reproduction/verification is explicitly requested**, use `SEED=42` and the suites documented in `AGENTS.md` (`--quick` default, `--extended`, `--full`). The suite overwrites `experiments/*.json` while it runs and restores them afterwards — **never leave a run half-finished.** Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
4. **Before committing anything**, run `python3 scripts/check_goldens_clean.py` and `python3 scripts/check_golden_baseline.py`. If a golden mismatch appears, fix it before committing — never let a checkpoint commit capture verification output as the new baseline (this regressed the baseline four times historically; see `AGENTS.md`).
5. **Default disposition:** wait for explicit user instructions. Do not invent experiments, re-run verification unprompted, change pre-registered gates or outcomes, or re-pin goldens/data baselines.
6. **Leave the next durable handoff** when this session ends: a new `handoff_<UTC timestamp>_INITIAL_TASK.md` plus `python3 scripts/repoint_handoff.py <new file>` (repoints the generic canonical pointers in root, `.handoff/`, `.kilo/`, `.kilo/handoff/`, `handoff/`, `HANDOFFS/`).

## Guardrails

- **Reproducibility:** always `SEED=42`; use the pinned data vintages/caches (`data/vintages.json`, `data/fundamentals_vintages.json`) and never introduce live-network dependence into verification paths.
- **Golden artifacts:** never replace/"refresh" `experiments/*.json` or re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` as a side effect of verification.
- **Pre-registration discipline:** new experiments must state gates, falsification expectations, and sensitivity handling *before* execution; sensitivity grids are reported, not gated; record negative results honestly (REJECTED / PARTIAL).
- **CI:** do not create `.github/workflows/` gates as an automated agent — the template is `.github/workflow-templates/verification-gate.yml` and creating the real workflow is a maintainer action.
- Never commit or log secrets/keys. Do not commit `__pycache__` or other verification output.

## Verification commands (run only when explicitly requested)

```bash
SEED=42 bash scripts/check.sh                          # fast guards
SEED=42 python3 verify_convention_robustness.py        # reads JSONs, no writes
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only # recover goldens
make check | make verify | make verify-quick | make verify-extended | make verify-full
```

## Pending work

- **None.** Baseline verified green (goldens match HEAD, 35/35 data inputs); repository closed (E001–E043). Await explicit user-directed work.
