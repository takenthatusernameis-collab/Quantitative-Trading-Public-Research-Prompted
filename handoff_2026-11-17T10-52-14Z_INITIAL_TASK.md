# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-17T10:52:14Z (UTC)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `8cc1b77c8a2ced6291b3e560bfdef48da4c5f744`
**Branch:** `main` (verify sync with `origin/main` before work)

## Repository State (at handoff)
- **Phase:** Research complete (E001–E043/E051 substantive). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. No active OPEN/PENDING/BLOCKED research items unless newly assigned.
- **Working tree:** clean at handoff creation (`git status --porcelain` empty).
- **Canonical artifacts:** `experiments/*.json` are golden baselines pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`. Do not replace or re-pin as a side effect of verification.
- **Primary convention:** close-to-close (v1.2.3). Overnight decomposition reported alongside where applicable.

## Initial Task for Next Session
1. **Orient:** Read `AGENTS.md`, this handoff, and `ledger/RESEARCH_LEDGER.md` (tail/recent entries) for current context and constraints.
2. **Confirm state:** Run `git status`, `git rev-parse HEAD`, and `git rev-list --left-right --count origin/main...HEAD`; investigate any drift from this handoff.
3. **Baseline integrity (required before committing):** Run `SEED=42 bash scripts/check.sh` (fast, offline). If it reports golden/baseline mismatch or stale `.verify_snapshot/`, fix/restore before committing — never commit captured verification output.
4. **If deeper verification is requested/warranted:** `SEED=42 python3 run_all_verification.py` (quick). For extended/full use `--extended` / `--full`. Never leave a run half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
5. **If assigned new work:** follow pre-registration, falsification gates, and reproducibility conventions in `AGENTS.md`; record outcomes in the ledger/artifacts as appropriate without moving goalposts.
6. **Handoff hygiene:** do not commit or push unless explicitly requested by the user. Update/create a new timestamped durable handoff if you make material changes.

## Key Commands
```bash
SEED=42 bash scripts/check.sh                          # fast gate (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py        # convention check only
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # extended (~21 min)
SEED=42 python3 run_all_verification.py --full         # full (~15 min)
SEED=42 python3 run_all_verification.py --restore-only # recover interrupted run
```

## Constraints / Known Caveats
- **Always `SEED=42`** for reproducible runs.
- **Never leave verification half-finished:** suite backs up/restores `experiments/`; interrupted runs can leave drift — restore before commit.
- **Do not re-pin baselines** (`ledger/golden_baseline.json`, `ledger/data_baseline.json`) to silence drift; re-pin only when intentionally replacing artifacts (visible, justified diff).
- **Known numeric drift:** E041/E042 have optimizer/ill-conditioning sensitivity (~1e-05 / bounded numeric diffs in extended reporting) — do not re-pin to mask; see ledger (E049 etc.).
- **CI:** `.github/workflows/verification-gate.yml` cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml`.
- **No secrets/credentials** in repo; follow existing code/data conventions.