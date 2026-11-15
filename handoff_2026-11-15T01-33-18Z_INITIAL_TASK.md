# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T01:33:18Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `b525dc8c` ("chore(kilo): checkpoint agent session"); in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - Expect exit 0 ("=== All checks passed ===").
   - Invoke with **bash** (not `python3`) to avoid a spurious harness failure.
   - If it fails with `ModuleNotFoundError`, install deps first: `pip3 install --break-system-packages -r requirements.txt`, then re-run. Do not treat a dependency error as a baseline failure.

2. **If checks fail for a real reason**
   - Tracked `experiments/*.json` differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Active/stale verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.
   - `__pycache__/*.pyc` differences are build noise — do not commit them.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** run verification suites unprompted (they overwrite/restore `experiments/*.json`; never leave a run half-finished).
   - Do **NOT** commit verification output or modify/re-pin canonical goldens/baselines (`experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`) without explicit instruction and ledger justification.
   - Do **NOT** reopen closed items (E049/E050, E041/E042 residual 1-ulp drift) or change pre-registered gates/outcomes.

---

## Current State (observed)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items indicated.
- **Working tree:** no intentional source/data/ledger/baseline changes. `git status` shows only `__pycache__/*.pyc` noise (ignore/do not commit).
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` absent (no interrupted verification pending).
- **Canonical artifacts:** `experiments/*.json` goldens and pinned fingerprints in `ledger/golden_baseline.json` / `ledger/data_baseline.json` are the authoritative record; treat HEAD as baseline unless checks prove otherwise.
- **Delta vs prior durable handoff:** this refresh updates the timestamp/HEAD pointer and restates the same idle/verify-first posture; no research substance changed.

---

## Key Commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Verification (only if explicitly requested; always SEED=42)
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

## Known Open Items / Guardrails

- **E049/E050 closed:** `src/portfolio_opt.py` validates solver answers on constraints, not solver exit status. Tangency QP is ill-conditioned — 1-ulp input changes can move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 numeric diffs. **Do not re-pin to silence.**
- **E041:** residual numeric drift remains open per ledger; do not re-pin.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via GitHub UI (template: `.github/workflow-templates/verification-gate.yml`); automated agents must not create workflows.
- **Always use `SEED=42`**. Never commit verification output, `__pycache__/*.pyc`, or secrets.

---

## Durable Artifact

Primary: `handoff_2026-11-15T01-33-18Z_INITIAL_TASK.md` (repo root).
Generic pointers/symlinks to be repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T01-33-18Z_INITIAL_TASK.md`.

Supersedes `handoff_2026-11-15T01-32-12Z_INITIAL_TASK.md` (HEAD at that handoff: `b525dc8c` context in prior session; this handoff recorded at `b525dc8c`).
