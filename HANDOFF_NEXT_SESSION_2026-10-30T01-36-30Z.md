# HANDOFF — 2026-10-30T02:33:59Z

## Session Context
- **Repo:** Quantitative-Trading-Public-Research-Prompted
- **Branch:** (check `git branch --show-current`)
- **State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baseline:** All canonical artifacts live in `experiments/*.json`. Golden fingerprints pinned in `ledger/golden_baseline.json`. Data coverage pinned in `ledger/data_baseline.json`.

## Current Integrity Notes
- **Verification safety:** A run must never be left half-finished. Backups live in gitignored `.verify_snapshot/` with `ACTIVE.json`. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- **Guards in place:** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (vs pinned fingerprints) run as part of `scripts/check.sh`.
- **Known drift:** E041 still shows numeric drift (133 differences) due to 1-ulp sensitivity of ill-conditioned QP despite optimizer determinism fix (E049). **Do not re-pin to silence this** — see ledger open item.
- **Pinned data:** E029 fundamentals pinned in `data/fundamentals/`; E030 panel pinned; vintage 2026-10-12 pinned in `data/vintages.json` (2026-10-11 committed separately).

## Recommended First Actions (for next agent)
1. **Check state**
   ```bash
   git status && git log --oneline -5
   ```

2. **Verify baseline integrity (fast)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Must pass with no golden mismatches and no stale snapshot pending.

3. **Run quick verification (if clean)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   ~8 min. Ensures drivers reproduce against current environment.

4. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` (focus E049 open item on E041 drift)
   - If planning changes to `experiments/`, only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification

## Next Task (clear initial objective)
**Objective:** Confirm clean baseline and report verification status.

**Acceptance criteria:**
- `scripts/check.sh` exits 0
- Quick verification completes successfully (or reports only known acceptable drift)
- Summary posted with: branch, HEAD, check status, verify-quick results, and any blockers

## Constraints
- Always use `SEED=42`
- Follow conventions in `AGENTS.md` (pre-registration, no post-hoc goalpost moves, don't commit verification output)
- Never re-pin goldens as a side effect of running verification
- If adding data inputs, commit file and update `ledger/data_baseline.json` via `scripts/check_data_coverage.py --update`
- Do not create GitHub workflows (controller restores them)
