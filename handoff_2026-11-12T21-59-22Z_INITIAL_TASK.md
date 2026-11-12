# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-12T21:59:22Z
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Git HEAD:** ad19e4f06f96ec2ffdf104a316ff05688477f49b (2026-11-12, latest "chore(kilo): checkpoint agent session") on `main`, tracking `origin/main` (in sync, +0 -0)
**Working tree at handoff:** clean (0 tracked modifications, 0 untracked). `.verify_snapshot/` absent — no interrupted verification run to recover.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Surviving validated strategies and all dispositions are documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical golden artifacts; integrity is pinned in `ledger/golden_baseline.json` (107 pinned goldens) and data cache coverage in `ledger/data_baseline.json` (35 pinned data inputs). 138 tracked entries under `experiments/` (107 goldens + 31 drivers).
- Prior durable handoff `handoff_2026-11-12T21-57-38Z_INITIAL_TASK.md` (HEAD `84afa8b3`) read and superseded.
- **Closed/resolved (do not reopen):** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do not re-pin E041/E042 artifacts to silence drift.

## First actions for the next session
1. **Confirm baseline integrity before any substantive change:**
   ```bash
   git status --short --branch
   SEED=42 bash scripts/check.sh
   ```
   (`check.sh` runs golden cleanliness, golden baseline fingerprints, data coverage, py_compile/tests, convention checks.) Do **not** commit if this reports mismatches. Treat tracked `__pycache__` modifications explicitly (restore/discard/commit only with explicit direction).
2. **If you need to reproduce/verify experiment drivers (only when explicitly requested):**
   - Quick: `SEED=42 python3 run_all_verification.py` / `make verify-quick` (~8 min)
   - Extended: `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended` (~21 min)
   - Full: `SEED=42 python3 run_all_verification.py --full` / `make verify-full`
   - The suite overwrites `experiments/*.json` during runs and restores them; **never leave a run half-finished**. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts as documented in `AGENTS.md`).
3. **Read context before proposing work:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent handoff notes as needed.

## Default disposition
**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

## Critical conventions / guardrails
- **Reproducibility:** always use `SEED=42`. Use pinned data vintages/caches; do not introduce live network dependence in verification paths.
- **Golden artifacts:** do not replace/"refresh" `experiments/*.json` or re-pin `ledger/golden_baseline.json` as a side effect of verification. If an artifact change is genuinely required, make it explicit, justified, and re-pin deliberately (`python3 scripts/check_golden_baseline.py --update`) as a reviewed change.
- **Data additions:** committing new cached inputs requires `python3 scripts/check_data_coverage.py --update` and pin updates per `AGENTS.md`.
- **Pre-registration discipline:** any new experiment must state gates, falsification expectations, and sensitivity handling before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known open drift:** E041/E042 grid artifacts have documented 1-ulp/ill-conditioned optimizer sensitivity (see `AGENTS.md` and ledger E049/open item) — **do not re-pin to silence**.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys; never log secrets.

## Reproduction / verification commands (run only if explicitly requested)
```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Pending work
- No explicit pending tasks were left in this handoff. Proceed by confirming baseline health (`scripts/check.sh`), then take user-directed research/maintenance work consistent with the completed research phase and conventions above.