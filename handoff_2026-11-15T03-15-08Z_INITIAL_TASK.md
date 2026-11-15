# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T03:15:08Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` @ `4fe5d039` ("chore(kilo): checkpoint agent session"); in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task (do first)

1. **Confirm baseline integrity**
   - `SEED=42 bash scripts/check.sh`
   - Expect exit 0 (`=== All checks passed ===`). If it fails with `ModuleNotFoundError`, install deps (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.
2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`).
   - Active/stale verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.
3. **Then idle awaiting explicit user direction.**
   - Do **not** make source changes or commits unless explicitly asked.
   - Do **not** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **not** re-pin baselines without explicit instruction and justification in the diff.
   - Do **not** commit `__pycache__/*.pyc` or other build artifacts.

## Current state

- **Working tree:** no source/data/research changes. Only `__pycache__/*.pyc` files are modified (build artifacts; gitignored output) — leave uncommitted.
- **Verification snapshot:** none active (`.verify_snapshot/` / `.verify_reports/` absent). No interrupted verification run.
- **Board:** empty; no peer coordination in flight.
- **Prior handoffs:** describe the same stable state; nothing material changed this turn.

## Known constraints (do not "fix" by re-pinning)

- **Canonical artifacts:** `experiments/*.json` are golden baselines; the suite overwrites then restores them. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`.
- **Seed:** always `SEED=42`. Data/fundamentals vintages and cache coverage are enforced (`ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, `scripts/check_data_coverage.py`). Runs use `QUANT_RESEARCH_OFFLINE=1` where applicable.
- **Extended drift (expected, reporting only):** 15/18 drivers 0-diff; **E041** has ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per ledger E049, decision REJECTED 3/5 unchanged) — still exceeds 1e-4 tolerance, **do not re-pin**. E029/E030 offline-reproducible with pinned snapshots. See `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) after `--extended`.
- **Working tree note:** only `__pycache__/*.pyc` churn is present; treat as non-canonical noise.

## References

- `AGENTS.md` — project commands, baseline integrity, reproducibility rules.
- `scripts/check.sh` — convention-robustness + golden guards (0.5c, 0.5d).
- `ledger/RESEARCH_LEDGER.md` — surviving validated strategies (E001–E043 complete) and open items (E041/E042 QP conditioning).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md` — CI template (maintainer-created only).