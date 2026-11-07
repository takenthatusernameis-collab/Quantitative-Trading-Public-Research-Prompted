# Handoff — 2026-11-07T19:25:47Z

## Repo state (as of handoff)
- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Platform: linux
- Git repo: yes (see `git status`/`git log` in next session)
- Research phase: complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (pinned). Verification guards active (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`).
- Verification snapshots live in `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker; must not be left pending.

## Initial task for next session
**Objective:** Get to a clean, verification-safe state and surface any actionable follow-ups without touching the pinned baselines.

### Steps (do in order)
1. **Inspect state**
   - `git status --short && git branch --show-current && git log -1 --oneline`
2. **Verify baseline integrity (fast)**
   - `SEED=42 bash scripts/check.sh`
   - Must pass with no golden mismatch. If it reports a pending snapshot/live run, do **not** re-run verification — recover first.
3. **Recover if needed**
   - If step 2 indicates recovery required: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if HEAD matches the intended baseline). See AGENTS.md "Baseline Integrity".
4. **Review open items**
   - Read `ledger/RESEARCH_LEDGER.md` for open items (notably E041 numeric drift / optimizer determinism notes). Do not re-pin goldens to silence drift.
5. **Report**
   - Summarize git state, check.sh result, any recovery performed, and concrete next actions (or "clean / no action needed").

## Gotchas (must follow)
- **Never leave verification half-finished.** A killed run can leave `.verify_snapshot/ACTIVE.json`; recover with `--restore-only`. `scripts/check_goldens_clean.py` will fail if a tracked `experiments/` file differs from HEAD or a stale snapshot is pending (live runs are reported, not failed).
- **Golden baseline is authoritative.** `scripts/check_golden_baseline.py` enforces SHA-256s in `ledger/golden_baseline.json`. Re-pinning requires explicit `--update` and must be intentional (do not do it as a side effect of running verification).
- **Drift is known in places.** E041 has remaining numeric drift due to ill-conditioned QP / solver behavior (status 8 allowed). Extended verification reports it; do not silence by re-pinning. See AGENTS.md and ledger E049.
- **Offline/data coverage enforced.** Verification uses `QUANT_RESEARCH_OFFLINE=1`. Unpinned inputs fail hard (`scripts/check_data_coverage.py`). E029/E030 fundamentals/panels are pinned.
- **No CI workflow creation.** `.github/workflows/verification-gate.yml` cannot be created by agents; use local `make check/verify-*`.

## Suggested first command
```bash
git status --short && git branch --show-current && git log -1 --oneline && echo "---" && SEED=42 bash scripts/check.sh
```