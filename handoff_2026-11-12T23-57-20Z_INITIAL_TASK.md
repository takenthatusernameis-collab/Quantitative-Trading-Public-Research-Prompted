# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-12T23:57:20Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `91c2830a88fcfa78cf1d2325ba445c2d52d7218f` (`chore(kilo): checkpoint agent session`, 2026-11-12 23:04:24 +0000) on `main`, tracking `origin/main` (0 ahead, 0 behind)
**Working tree at handoff:** clean at session start. This session adds only this durable handoff and updates the generic canonical handoff pointers to it. `.verify_snapshot/` absent — no interrupted verification run to recover.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Authoritative dispositions, evidence, and history: `ledger/RESEARCH_LEDGER.md` (through E183; E052+ are durable-handoff refreshes only).
- Canonical artifacts: `experiments/*.json` (107 golden JSONs + 31 drivers = 138 tracked entries), `ledger/golden_baseline.json`, and `ledger/data_baseline.json`. Do not modify or re-pin them as a side effect of verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Supersedes operationally:** `handoff_2026-11-12T23-54-58Z_INITIAL_TASK.md`. Delta since that handoff is handoff/pointer churn only; no research, source, data, experiment, or baseline substance changed.

## Initial task for the next session
1. **Do not start substantive work until the user gives explicit direction.** First read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and this handoff.
2. **If baseline verification is requested**, confirm state and run the fast checks:
   ```bash
   git status --short --branch
   SEED=42 bash scripts/check.sh
   ```
   Environment note (not a repository regression): this container may lack dependencies (e.g. `pandas`), causing `scripts/check.sh` to stop early with `ModuleNotFoundError`. Install `pip install -r requirements.txt` before relying on the full fast-check result. If a real mismatch is reported, stop and do not commit.
3. **If reproduction/verification is explicitly requested**, use `SEED=42` and the suites documented in `AGENTS.md` (quick, `--extended`, or `--full`). The suite overwrites `experiments/*.json` during runs and restores them; **never leave a run half-finished**. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or restore the pinned artifacts as documented in `AGENTS.md`.
4. **Default disposition:** wait for explicit user instructions. Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.

## Critical guardrails
- **Reproducibility:** always use `SEED=42`; use pinned data vintages/caches and do not introduce live-network dependence in verification paths.
- **Golden artifacts:** never replace/"refresh" `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. A genuine artifact change must be explicit, justified, and deliberately re-pinned (`python3 scripts/check_golden_baseline.py --update` / `python3 scripts/check_data_coverage.py --update`) as a reviewed change.
- **Pre-registration discipline:** new experiments must state gates, falsification expectations, and sensitivity handling before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp/ill-conditioned optimizer sensitivity — do not re-pin to silence.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit or log secrets/keys.

## Verification commands (run only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh                         # fast guards (requires dependencies)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Pending work
- None. Confirm baseline health when dependencies are available, then await/execute only explicit user-directed work consistent with the completed research phase and the conventions above.
