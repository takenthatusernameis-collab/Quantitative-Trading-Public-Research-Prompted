# Agent Handoff — 2026-11-21T19:07:01Z

**Timestamp**: 2026-11-21T19:07:01Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Branch / HEAD**: `main` @ `eb154e4d` (`chore(kilo): checkpoint agent session`)
**Research phase**: COMPLETE (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`. This is a maintenance/reproducibility repo, not an open research queue.

## TL;DR — Start Here (ordered)

1. `git log --oneline -1 && git status` — confirm HEAD `eb154e4d` on `main` and a clean tree.
2. Check for an interrupted verification run: if `.verify_snapshot/ACTIVE.json` exists, recover first with
   `SEED=42 python3 run_all_verification.py --restore-only`. **Never commit while a snapshot is pending.**
3. Confirm golden integrity (both must exit 0):
   - `python3 scripts/check_goldens_clean.py`
   - `python3 scripts/check_golden_baseline.py`
4. Provision deps if imports fail (fresh runners often lack them): `pip install -r requirements.txt`.
5. Fast gate: `SEED=42 bash scripts/check.sh` (convention robustness + template validation, seconds, offline).
6. Only if a fuller check is explicitly wanted: `SEED=42 python3 run_all_verification.py` (quick, ~8 min).
   Extended = `--extended` (~21 min); Full = `--full` (~15 min, E042 n_sim=50 + 96-config grid).
7. Read **Open items** below. Await explicit user instruction before doing new research or promoting any strategy.
8. Before finishing, leave your own timestamped handoff and run
   `python3 scripts/repoint_handoff.py <your-new-handoff-file>` so the stable aliases follow you.

## Verification scopes

- `verify-quick`: re-executes 8 drivers (E012, E023, E024 --merge, E027, E035, E037, E039, E042-lead).
- `verify-extended`: additionally re-executes 18 committed drivers, compares to goldens with numeric_tol=1e-4 (bounded float drift tolerated; structural/string diffs still fail). Writes `.verify_reports/` (gitignored, reporting only).
- `verify-full`: E042 n_sim=50 + 96-config sensitivity grid.

## Integrity rules (do not violate)

- `experiments/*.json` are the canonical goldens. The suite overwrites them while running and restores after; a half-finished run silently replaces the baseline.
- If a run is interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <last-good-commit> -- experiments/`).
- `scripts/check_goldens_clean.py` (tracked-vs-HEAD) and `scripts/check_golden_baseline.py` (vs SHA-256 in `ledger/golden_baseline.json`) are both first-class steps of `scripts/check.sh`. Do not re-pin a golden as a side effect of a re-run.
- Cache coverage is enforced: `scripts/check_data_coverage.py` pins every driver input in `ledger/data_baseline.json`. A cache miss is a live yfinance download, which is not bit-reproducible. Do not add unpinned inputs.
- `SEED=42` is mandatory (walk-forward + placebo RNG).
- Do not commit unless the user explicitly asks.

## Open items (from ledger)

- **E041** — 133 numeric differences remain; ill-conditioned tangency QP (1-ulp sensitivity). Optimizer exit-status defect fixed in E049. **Do NOT re-pin to silence drift.**
- **E042** — grid artifacts drift by 29–133 differences, same root cause. **Do NOT re-pin.**
- **E050** — E049 open item closed: exact KKT enumeration routes the tangency QP.
- See `ledger/RESEARCH_LEDGER.md` entries E045, E048, E049, E050 for full context.

## Key references

- Commands & conventions: `AGENTS.md`
- Research record: `ledger/RESEARCH_LEDGER.md`
- Golden fingerprints: `ledger/golden_baseline.json`
- Data fingerprints: `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`
- Handoff tooling: `scripts/repoint_handoff.py`, `scripts/repair_broken_handoff.py`
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

## Environment

- Python 3; deps in `requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional (falls back to `scipy.optimize`).
- Offline verification enforced via `QUANT_RESEARCH_OFFLINE=1`.
- numpy/pandas/scipy may be absent on a fresh runner at handoff time — install before Python steps.

## State verified at handoff time (2026-11-21T19:07:01Z)

- HEAD `eb154e4d` on `main`; working tree clean.
- `python3 scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0).
- `python3 scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0).
- `.verify_snapshot/` absent — no interrupted verification run to recover.

## Recurring handoff procedure (for the next session)

1. Do your work; never leave a verification run half-finished.
2. Write `handoff_<UTC timestamp>Z_INITIAL_TASK.md` at repo root (clear ordered start-here checklist).
3. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
4. Run `python3 scripts/repoint_handoff.py handoff_<your-timestamp>Z_INITIAL_TASK.md` (verify: `checked=N bad=0`).
5. Append a `Durable handoff refresh` entry to `ledger/RESEARCH_LEDGER.md` recording HEAD, SHA-256, and the repoint audit.
6. Leave the new handoff uncommitted unless the user explicitly asks to commit.

(End of file)
