# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T09:17:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `1ba9d8eb916a1af138dbb4b255c38e7679bac84a` — equals `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0	0`). The controller emits `chore(kilo): checkpoint agent session` commits continuously, so the short SHA drifts between sessions; the verified research state below is what matters, not the SHA.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (freshly measured this session, 2026-11-26T09:17:05Z)

- **Research phase:** CLOSED (E001–E043). Authoritative dispositions in `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items. Do not start new experiments.
- **Working tree:** clean for canonical artifacts (`experiments/`, `data/`). Only tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` is modified — safe to ignore or `git restore`.
- **Live verification:** none in progress (`.verify_snapshot/` and `.verify_reports/` absent).
- **Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.
- **Dependency-free guards (ran this session, all PASS, exit 0):**
  - `python3 scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`
  - `python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`
  - `python3 scripts/check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED`
  - `git diff HEAD -- experiments/` empty.
- **Last full reproducibility measurement:** 2026-11-23T05:17Z (numpy 2.5.4 / scipy 1.18.1) — all 18 extended drivers reproduce with **0 differences**. Not re-run this session (deps missing).

## Repo hygiene warning (read first)

This repository has a runaway handoff-refresh problem: ~9,000 of ~9,540 git-tracked files are handoff/current/next/latest/initial_task artifacts. Each session has been asked to "leave a timestamped initial task message," complied by writing one more near-duplicate stub, and recorded a one-line ledger entry congratulating itself. **Do NOT manufacture another "refreshed the handoff" ledger entry as your deliverable.** A handoff is only worth writing if it changes what the next session *does*. If you have no explicit user instruction, verifying state and stopping is a complete, correct outcome.

## Initial task for the next session (CLEAR, prioritized — do ONE, in order, stop when genuinely done)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously:

1. **Verify-and-stop (highest value, ~8–21 min).**
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh                       # fast: goldens clean, golden baseline, data coverage, optimizer determinism
   SEED=42 python3 run_all_verification.py --extended  # 26 drivers vs committed goldens, numeric_tol=1e-4
   ```
   Expected: all 18 extended drivers reproduce with **0 differences**; `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` written (gitignored, outside `experiments/`). Report drift precisely (per-driver differences, numeric vs structural, worst drift as a multiple of tolerance), then stop. **Do NOT re-pin goldens** to silence drift — none remains. Re-pin only for a deliberate code change recorded in the ledger first (E050 precedent).

2. **Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps).**
   ```bash
   SEED=42 python3 experiments/run_e041.py             # market-neutral portfolio (REJECTED 3/5)
   SEED=42 python3 experiments/run_e042.py --n-sim 2   # min-var confirmatory (PARTIAL 4/5, lead artifact)
   ```
   E041 numeric diffs went 354 → 133 → **0** after the E050 exact active-set solver (commit `72dc947`). Both must stay bit-reproducible.

3. **Propose (do NOT execute) the cleanup.** The handoff pollution is the real defect. Draft — do not run — a `.gitignore` entry plus a `git rm --cached` plan for the ~9,000 handoff/current/next/latest/initial_task files and convenience symlinks, and present it for maintainer approval. Executing mass deletion/repinning without explicit approval is out of scope.

4. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Integrity rules (do not violate)

1. Never leave verification half-finished — it overwrites `experiments/*.json` and restores after. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <pinned-commit> -- experiments/<file>`; the pinned commit is the last one whose SHA-256 matches `ledger/golden_baseline.json`).
2. Golden baseline SHA-256 is pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output — it silently replaces the canonical baseline (see reverted commits `d6042b0`/`9f20def`→`05b5353`, `1623923`→`026d109`, `701ed78`→`34396a9`).
4. Always use **SEED=42** for reproducibility/verification runs.
5. Do not reopen closed E049/E050 or E041/E042 drift items.
6. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.
7. Never commit secrets/keys; never log secrets.

## Quick reference

```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py             # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-26T09-17-05Z_INITIAL_TASK.md` (repo root). `CURRENT.md` and `current.md` repoint to this file so the next session resolves `current` to it.
- **No new aliases and no mirror dirs created.**
- **Supersedes operationally:** `handoff_2026-11-26T09-16-12Z_INITIAL_TASK.md` (and all prior `HANDOFF_*` / `handoff_*` artifacts, retained for history; not modified).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.