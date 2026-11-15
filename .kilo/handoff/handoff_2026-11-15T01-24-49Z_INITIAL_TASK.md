# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T01:24:49Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `3438fe0e` ("chore(kilo): checkpoint agent session", committed 2026-11-15 00:35:11 +0000); `origin/main...HEAD` = `0 0` (in sync)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0 ("=== All checks passed ==="). If it fails with `ModuleNotFoundError`, install deps (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.
   > Note: invoke `check.sh` with **bash** (not `python3`) — running it via `python3` yields a spurious exit 1 that is a harness mistake, not a baseline failure.

2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Active verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** commit `__pycache__/*.pyc` noise.

---

## Current State

- **Working tree:** no source/data changes. `git status --short | grep -v __pycache__ | grep -v '\.pyc'` is clean; only `__pycache__/*.pyc` build artifacts differ (gitignored build output — do not commit).
- **Verification snapshot:** none active (`.verify_snapshot/` and `.verify_reports/` absent). No interrupted verification run.
- **Goldens:** all 107 tracked `experiments/*.json` match HEAD; `check_goldens_clean.py` → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"; `check_golden_baseline.py` → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"; `check_data_coverage.py` → "ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED"; `check_json_artifacts.py` → "checked 114 committed JSON artifacts / ALL COMMITTED JSON ARTIFACTS PARSE OK".
- **Environment:** Python 3.12.3 with `requirements.txt` dependencies installed. If reset, run `pip3 install --break-system-packages -r requirements.txt` before trusting `check.sh`.
- **Delta vs prior durable handoff** (E347, 2026-11-15T00:33:47Z, HEAD `6abfd706`; prior artifact `handoff_2026-11-15T00-33-47Z_INITIAL_TASK.md`): checkpoint commits advanced HEAD `6abfd706` → `3438fe0e`. `git diff --name-only 6abfd706..3438fe0e` filtered for research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. **No research substance changed.**
- **Research phase:** complete (E001–E051). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Durable-handoff refreshes recorded through E347 (this refresh = E348).

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

## Known Open Items (read AGENTS.md / ledger before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Tangency QP is ill-conditioned — 1-ulp input changes can move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 numeric diffs. **Do not re-pin to silence.**
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity); 3 structural differences already fixed. Open in ledger; do not re-pin.
- **E344 ledger gap:** E344 refresh self-labeled but never persisted in the ledger; recorded as a documented unrecorded-artifact gap, not reconstructed.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via the GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output or `__pycache__/*.pyc`.

---

## Durable artifact

Primary: repo root `handoff_2026-11-15T01-24-49Z_INITIAL_TASK.md`.
Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/` (both `handoff_`-prefixed and bare-timestamp names), `.kilo/`, `.kilo/handoff/`.
Generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T01-24-49Z_INITIAL_TASK.md`.

Supersedes `handoff_2026-11-15T00-33-47Z_INITIAL_TASK.md` (ledger E347, HEAD `6abfd706`).