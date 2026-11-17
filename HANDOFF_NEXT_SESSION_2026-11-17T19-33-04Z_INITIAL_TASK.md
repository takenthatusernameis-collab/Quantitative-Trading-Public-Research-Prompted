# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-17T19:33:04Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main`
**HEAD:** `0be2f2fd` — chore(kilo): checkpoint agent session
**Working tree:** clean (only untracked `__pycache__/*.pyc` build artifacts; no tracked diffs, no `.verify_snapshot/`)

---

## INITIAL TASK MESSAGE (read this first)

> **Task: establish a green baseline, then hold it.**
>
> 1. Read `AGENTS.md` and this handoff end-to-end before doing anything.
> 2. Run `board_read` to check for any coordinator task assignment. If a task is
>    posted, do that. If none, the default posture is: **research phase complete
>    (E001–E043); maintain baseline integrity and reproducibility.**
> 3. The current sandbox is **missing core Python deps** (`pandas`, `numpy` — and
>    therefore `scipy`, `statsmodels`, `pyarrow`, `yfinance`). Because of this,
>    `SEED=42 bash scripts/check.sh` exits non-zero **for environmental reasons
>    only** — the golden-artifact and data-coverage guards themselves pass (see
>    "Baseline state" below). First action: install dependencies, then re-run the
>    fast check.
>
>    ```bash
>    python3 -m pip install -r requirements.txt
>    SEED=42 bash scripts/check.sh      # expect ALL ... PASSED, exit 0
>    ```
>
> 4. If the fast check is green, proceed to quick verification:
>
>    ```bash
>    SEED=42 python3 run_all_verification.py --skip-slow   # or: make verify-quick
>    ```
>
> **Hard guardrails (binding, per `AGENTS.md`):**
> - Never leave a verification run half-finished. If interrupted, recover with
>   `SEED=42 python3 run_all_verification.py --restore-only` (or
>   `git checkout -- experiments/`).
> - Never commit verification output. Never re-pin goldens as a side effect of a
>   verification run. Re-pinning requires explicit, deliberate
>   `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
> - Always use `SEED=42`. Runs use `QUANT_RESEARCH_OFFLINE=1` where applicable.

---

## Baseline state (verified at handoff time)

- `experiments/*.json` goldens: **intact** — `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`,
  `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`.
- Pinned data inputs: **intact** — `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`.
- No `.verify_snapshot/` present; no verification run active; working tree clean of tracked changes.
- **Caveat:** `SEED=42 bash scripts/check.sh` currently exits 1 in this sandbox with
  `ModuleNotFoundError: No module named 'pandas'` / `'numpy'` (3 test errors in
  `tests/test_data_coverage.py`). This is an **environment gap, not a repo defect**.
  The `data/panel.parquet` FAIL lines and `tmp*/nope.json` lines in the output are
  the guard scripts' **intentional self-test fixtures** running in temp dirs — not
  real baseline failures. After installing `requirements.txt`, the check is expected
  to pass.

---

## Known constraints (do NOT "fix" by re-pinning)

- **E041 / E042 extended drift is expected and reporting-only.** E041 shows ~133
  numeric differences from 1-ulp sensitivity of an ill-conditioned QP (optimizer
  determinism fixed per ledger E049; decision REJECTED 3/5 and all gate flags
  unchanged). It exceeds the 1e-4 tolerance on purpose — **do not re-pin to silence**.
  See `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) after `--extended`.
- E029 (fundamentals) and E030 (16-ETF panel) are offline-reproducible via pinned
  snapshots (`data/fundamentals/`, `data/vintages.json`, `ledger/data_baseline.json`).
- **Cache coverage is an enforced invariant** (`scripts/check_data_coverage.py`); a
  missing/unpinned input is a live network download and yfinance is not bit-reproducible.
- **CI gate**: `.github/workflows/verification-gate.yml` cannot be created by automated
  agents — maintainer must create it via GitHub UI from
  `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

---

## Quick command reference

```bash
SEED=42 bash scripts/check.sh                       # fast convention/golden/data guard (seconds)
SEED=42 python3 run_all_verification.py             # quick full (~8 min)
SEED=42 python3 run_all_verification.py --extended  # + 18 more drivers (~21 min)
SEED=42 python3 run_all_verification.py --full      # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only   # recover goldens after interruption
```

## References

- `AGENTS.md` — commands, baseline integrity, reproducibility rules, conventions.
- `ledger/RESEARCH_LEDGER.md` — E001–E043 complete; open items (E041/E042 QP conditioning).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints.
- `scripts/check.sh`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Prior handoffs: `HANDOFF_NEXT_SESSION_2026-11-15T03-11-03Z.md`,
  `HANDOFF-2026-11-16T11-39-42Z.md` (same stable state).

---

*Created 2026-11-17T19:33:04Z at session start. Durable handoff — do not delete;
update in place if state changes materially.*