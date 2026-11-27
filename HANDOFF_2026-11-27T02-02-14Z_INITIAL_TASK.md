# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-27T02:02:14Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `ff7b94bb7d70d1a10b2e7ac3b9b3474acc108313` == `origin/main` (`0	0` left/right). Working tree clean for canonical artifacts except incidental tracked bytecode `src/__pycache__/cache_keys.cpython-312.pyc` (safe to ignore or `git restore`).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (2026-11-27T02:02:14Z)

- **Research phase:** CLOSED (E001–E043). Authoritative dispositions in `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items. Do not start new experiments.
- **Live verification:** none in progress (`.verify_snapshot/` and `.verify_reports/` absent). No half-finished run to recover.
- **Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`; `pandas` missing). Run `pip install -r requirements.txt` before any verification.
- **Dependency-free guards:** `python3 scripts/check_goldens_clean.py`, `python3 scripts/check_golden_baseline.py`, `python3 scripts/check_data_coverage.py` (all expected PASS, exit 0).
- **Last baseline verification:** clean at 2026-11-26T19:17:39Z — 107 pinned goldens match baseline, 35 pinned data inputs present/tracked/unchanged. Not re-run this session (deps missing).
- **Last reproducibility measurement:** 2026-11-23T05:17Z (numpy 2.5.4 / scipy 1.18.1) — all 18 extended drivers reproduce with 0 differences.

## Initial task for the next session (CLEAR, prioritized — do ONE, in order, stop when genuinely done)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously:

1. **Verify-and-stop (highest value, ~8–21 min).**
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh
   SEED=42 python3 run_all_verification.py --extended
   ```
   Expected: all 18 extended drivers reproduce with 0 differences. Report drift precisely, then stop. Do NOT re-pin goldens.

2. **Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps).**
   ```bash
   SEED=42 python3 experiments/run_e041.py
   SEED=42 python3 experiments/run_e042.py --n-sim 2
   ```

3. **Propose (do NOT execute) the cleanup** of the runaway ~9,000 handoff/current/next/latest/initial_task artifacts. Draft a `.gitignore` entry plus a `git rm --cached` plan and present for maintainer approval. Keep a single durable `HANDOFF_<latest>.md`.

4. **Pre-registered research** only if explicitly requested — with `pre_registered` block, falsification expectations, and sensitivity grid stated before execution.

## Integrity rules (do not violate)

1. Never leave verification half-finished. Recover with `SEED=42 python3 run_all_verification.py --restore-only`.
2. Golden baseline SHA-256 pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output over canonical goldens (`experiments/*.json`).
4. Always use **SEED=42**.
5. Do not reopen closed E049/E050 or E041/E042 drift items.
6. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; maintainer must create via GitHub UI.
7. Never commit secrets/keys; never log secrets.
8. Do not manufacture another handoff refresh as a substitute for real work.

## Quick reference

```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                    # fast convention check (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only   # recover goldens if interrupted
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-27T02-02-14Z_INITIAL_TASK.md` (repo root). Supersedes operationally `handoff_2026-11-27T02-01-10Z_INITIAL_TASK.md` (retained for history; not modified).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.
