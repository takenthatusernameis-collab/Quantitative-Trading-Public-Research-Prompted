# Durable Handoff — Initial Task Message (next agentic work session)

**Created:** 2026-11-17T15:52:51Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## 1. Snapshot of state at handoff

- **HEAD:** `19b7779831a195d72eb956991d083b7f629ed64c` ("chore(kilo): checkpoint agent session") on `main`.
- **Sync:** `git rev-parse origin/main` == HEAD; `git rev-list --left-right --count origin/main...HEAD` → `0	0` (in sync).
- **Working tree:** only the 15 tracked `__pycache__/*.pyc` build artifacts under `scripts/`, `src/`, `tests/` are modified (gitignored bytecode; all guards ignore them). No source, driver, artifact, data, test, or ledger changes are uncommitted. No `.verify_snapshot/` or `.verify_reports/` present → no interrupted verification run to recover.
- **Research status:** repository is **closed**. Research phase E001–E051 complete; `experiments/*.json` are committed golden artifacts (107 pinned, fingerprints verified below). Durable-handoff bookkeeping entries continue in the ledger (last: E461 at 2026-11-17T14:56:44Z; this refresh is the next entry).
- **Prior handoff superseded:** `handoff_2026-11-17T14-59-29Z_INITIAL_TASK.md` (read, retained for history).
- **Delta vs prior handoff (`handoff_2026-11-17T14-59-29Z_INITIAL_TASK.md`, HEAD `c2162873` → live `19b77798`):** ledger-only change — the E461 entry was appended to `ledger/RESEARCH_LEDGER.md`. No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`. Prior research state adopted unchanged.

## 2. Verification performed this session (2026-11-17T15:52Z)

- `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (exit 0). This covers `check_json_artifacts.py`, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, the six unit-test modules (incl. `tests/test_portfolio_opt.py`), `verify_convention_robustness.py`, `scripts/validate_template.py`, and `scripts/check_experiment_imports.py` (all 27 drivers import cleanly).
- `python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`.
- Convention gate: E042 min-variance market-neutral blend reproduces PARTIAL 4/5 (G1/G3/G4/G5 PASS, G2 placebo-significance FAIL) — as recorded, not promoted.
- After the check: `git status --short -- experiments/ data/ src/ scripts/ tests/ research_state/` → clean; `.verify_snapshot/` / `.verify_reports/` absent. Nothing to recover.

## 3. Initial task for the next session

**No new research is requested. The research phase is closed.** If a new research direction is authorized, it must follow `ledger/PRIORITIZATION.md` (v1.2.7) and AGENTS.md pre-registration rules. Otherwise the default task is:

1. Confirm state: `git status --short`, `git rev-parse HEAD`, `git rev-list --left-right --count origin/main...HEAD`. Expect only `__pycache__/*.pyc` modifications and a clean tree.
2. `SEED=42 bash scripts/check.sh` (or `make check`) — fast offline check, seconds. Fix any golden mismatch BEFORE committing.
3. If deeper verification is warranted: `SEED=42 python3 run_all_verification.py` (quick, ~8 min) or `--extended` / `--full`. Never leave a run half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Record any substantive outcome as the next ledger entry (E462+) with live HEAD, UTC timestamp, delta, and constraints honored.
5. Do **NOT** commit unless explicitly directed.

## 4. Standing constraints / gates (read before acting)

- **Canonical artifacts:** `experiments/*.json` are committed goldens. The verification suite overwrites then restores them. Never leave a run half-finished.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD already carries a captured run, restore the pinned artifact per `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`; re-pin only deliberately via `python3 scripts/check_golden_baseline.py --update`, which shows the replacement in the diff).
- **Golden guards:** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (SHA-256 vs pinned baseline) are first-class steps of `scripts/check.sh` and the suite. Never re-pin as a side effect of a verification run.
- **Data coverage:** every `data.download()` call site must resolve to a git-tracked, SHA-256-pinned cache file per `ledger/data_baseline.json` (`scripts/check_data_coverage.py`; update with `--update` only when intentionally adding a pinned input). The suite re-runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Seed / conventions:** always `SEED=42`. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- **Known benign drift (do NOT re-pin to silence):** the tangency QP (`src/portfolio_opt.py` `max_sharpe` / `min_var`) remains ill-conditioned; a 1-ulp input perturbation moves the E041/E042 grid artifacts by ~1e-05, so `--extended` still reports E041 (and sometimes E042 grid) drifting by 29–133 numeric differences. This is a documented research-engineering decision (ledger E049 *Open item* + E050), not a defect to re-pin away. Optimizer determinism rule: judge a solver answer on the **problem's constraints**, never the solver's exit status (pinned by `tests/test_portfolio_opt.py`).
- **Do not commit verification output.** Do not commit `__pycache__/*.pyc`. No separate linter; run `python3 -m py_compile` on changed files.

## 5. Known open research items (all non-blocking; repository closed)

- **E049 open item (not a defect, left as-is):** the tangency QP is ill-conditioned even after the exit-status fix. Full remediation would replace the QP solve with a well-conditioned deterministic solver and re-pin the affected E041/E042 artifacts deliberately. Until then the artifacts intentionally drift and must not be re-pinned.
- **Deferred micro-fix (E050, second defect):** `src/portfolio_opt.py` `y0 = w_feas / max(mu_s'w_feas, 1e-12)` masks a negative denominator; at the 2019-10-16 rebalance it yields a magnitude ~8e+11 start that SLSQP turns into garbage (rejected by the feasibility screen, falling back to the LP vertex exactly as the golden). Correcting it would change published numbers → left for a deliberate re-pin decision.
- **CI gate:** `.github/workflows/verification-gate.yml` cannot be created by automated agents (controller restores/cleans `.github/workflows/`; repo `GITHUB_TOKEN` lacks `workflows` push). Template at `.github/workflow-templates/verification-gate.yml`; instructions in `VERIFICATION_GATE_TEMPLATE.md`. A maintainer must create the workflow via the GitHub UI.

## 6. Quick command reference

```bash
# Fast convention-robustness check + template validation (offline, seconds)
SEED=42 bash scripts/check.sh          # or: make check

# Quick full verification (~8 min) / Extended (~21 min) / Full (~15 min)
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (no writes)
SEED=42 python3 verify_convention_robustness.py

# Recover goldens after an interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Deliberate re-pin (only when intended; shows in the diff)
python3 scripts/check_golden_baseline.py --update

# Point all generic handoff aliases at this file
python3 scripts/repoint_handoff.py handoff_2026-11-17T15-52-51Z_INITIAL_TASK.md
```

## 7. Key references

- `AGENTS.md` — authoritative project commands, baseline-integrity rules, and conventions.
- `ledger/RESEARCH_LEDGER.md` — every experiment (E001–E051 research + durable-handoff entries), gates, falsification expectations, and the E049/E050 open items.
- `ledger/PRIORITIZATION.md` — ranking procedure and version history (v1.2.7: artifact-vs-code reconciliation).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — SHA-256 pins for artifacts and data caches.
- `.kilo/command/*.md`, `.kilo/agent/*.md`, `kilo.json` — Kilo config (put new commands/agents in `.kilo/`).

---
*End of handoff.*