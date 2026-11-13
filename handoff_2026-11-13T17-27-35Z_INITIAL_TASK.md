# INITIAL TASK — Handoff for the Next Agentic Work Session

**Handoff timestamp (UTC):** 2026-11-13T17:27:35Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `870ad5ae chore(kilo): checkpoint agent session` on `main`
**Sync with origin:** `git rev-list --left-right --count origin/main...HEAD` → `0 0` (HEAD == `origin/main`)
**Working tree:** clean for `experiments/`, `data/`, and tracked source/ledger/test files. Only tracked `__pycache__/*.pyc` bytecode files are modified (no functional/source impact). No untracked substantive files. `.verify_snapshot/` absent; `.verify_reports/` absent.

---

## Verified state at handoff time

| Check | Command | Result |
|---|---|---|
| Goldens vs baseline fingerprint | `SEED=42 python3 scripts/check_golden_baseline.py` | **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (exit 0) |
| Goldens vs HEAD | `SEED=42 python3 scripts/check_goldens_clean.py` | **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD** (exit 0) |
| Data coverage | `SEED=42 python3 scripts/check_data_coverage.py` | **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0) |
| Tracked experiment artifacts | `git ls-files experiments/ \| wc -l` | **138** |

No research, source, data, experiment, or baseline substance changed by this handoff. Delta vs prior canonical handoff (`handoff_2026-11-13T16-40-43Z_INITIAL_TASK.md`, HEAD `69a0832e` → this handoff `870ad5ae`) under `experiments/ data/ src/ tests/ scripts/ ledger/`: **empty** (only `__pycache__` bytecode and handoff/ledger/checkpoint bookkeeping changed in intervening commits).

---

## Project status

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E047).** Surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`. Ledger entries E052+ are durable-handoff refreshes only.
- Canonical artifacts: `experiments/*.json` (138 tracked, 107 pinned in `ledger/golden_baseline.json`), `ledger/data_baseline.json` (35 inputs). **Do not modify or re-pin as a side effect of verification.**
- Closed / do not reopen: E049/E050 (optimizer determinism + exact KKT enumeration) and residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). **Do not re-pin E041/E042 to silence drift.**

---

## Supersedes

This handoff supersedes `handoff_2026-11-13T16-40-43Z_INITIAL_TASK.md` (HEAD `69a0832e`). Substantive delta in `experiments/ data/ src/ tests/ scripts/ ledger/`: **none** — this is a bookkeeping/handoff refresh with guards re-verified.

---

## CLEAR INITIAL TASK for the next session

1. **Do not begin substantive research work until the user gives explicit direction.** First read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (tail), and this handoff.
2. **Confirm baseline is healthy** before any work (cheap, offline):
   ```bash
   git status --short --branch
   SEED=42 bash scripts/check.sh          # or: make check
   ```
3. **If reproduction/verification is explicitly requested**, use `SEED=42` and suites in `AGENTS.md` (`verify-quick` default, `--extended`, `--full`). The suite overwrites `experiments/*.json` during runs and restores them afterwards — **never leave a run half-finished.** Recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
4. **Before committing anything**, run `python3 scripts/check_goldens_clean.py` and `python3 scripts/check_golden_baseline.py`. If a golden mismatch appears, fix it before committing — never capture verification output as the new baseline (historical regressions: d6042b0/9f20def→05b5353, 1623923→026d109, 701ed78→34396a9). `git checkout -- experiments/` only restores HEAD; if HEAD is bad, restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
5. **Default disposition:** wait for explicit user instructions. Do not invent experiments, re-run verification unprompted, change pre-registered gates/outcomes, or re-pin goldens/data baselines.
6. **Leave the next durable handoff** when this session ends: create `handoff_<UTC>_INITIAL_TASK.md` and run `python3 scripts/repoint_handoff.py <new file>` to repoint generic canonical pointers.

## Guardrails

- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (`data/vintages.json`, `data/fundamentals_vintages.json`); never introduce live-network dependence into verification paths.
- **Golden artifacts:** never replace/refresh `experiments/*.json` or re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` as a side effect of verification.
- **Pre-registration discipline:** new experiments must state gates, falsification expectations, and sensitivity handling *before* execution; sensitivity grids are reported, not gated; record negative results honestly (REJECTED / PARTIAL).
- **Verification safety:** `experiments/*.json` are overwritten then restored by `run_all_verification.py`; interrupted runs are recoverable via `.verify_snapshot/` / `--restore-only`. Never leave half-finished.
- **CI:** do not create `.github/workflows/` as an automated agent (controller strips workflows; token lacks permission). Template: `.github/workflow-templates/verification-gate.yml` — maintainer action only.
- Never commit or log secrets/keys. Do not commit `__pycache__` or verification output.

## Useful commands (run only when explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only # recover goldens
make check | make verify | make verify-quick | make verify-extended | make verify-full
```

## Pending work

- **None.** Baseline verified green at handoff (107/107 pinned goldens match fingerprint and HEAD; 35/35 data inputs present/tracked/unchanged; 138 experiment artifacts tracked). Repository closed (E001–E047). Await explicit user-directed work.
