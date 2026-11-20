HANDOFF — Quantitative-Trading-Public-Research-Prompted
Created: 2026-11-20T08:26:08Z
Status: idle / ready for next session

Context
- Repository: Quantitative-Trading-Public-Research-Prompted
- Root: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Research phase complete (E001–E043). Surviving strategies documented in ledger/RESEARCH_LEDGER.md.

Quick-start commands (SEED=42 always)
- Convention-robustness check + template validation (~seconds, offline): SEED=42 bash scripts/check.sh  (or `make check`)
- Quick full verification (~8 min; 8 drivers in 5a block): SEED=42 python3 run_all_verification.py  (or `make verify-quick`)
- Extended verification (~21 min; +18 committed drivers vs goldens): SEED=42 python3 run_all_verification.py --extended
- Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid): SEED=42 python3 run_all_verification.py --full
- Individual drivers: SEED=42 python3 src/batch_run.py --universe large_liquid ; SEED=42 python3 src/validate.py --universe large_liquid ; SEED=42 python3 experiments/run_e042.py --n-sim 50

Critical rules (read before running the suite)
- experiments/*.json are canonical research artifacts. Verification backs them up to gitignored .verify_snapshot/ (with ACTIVE.json marker holding owning pid) and restores afterwards. Never leave a verification run half-finished. Recovery: SEED=42 python3 run_all_verification.py --restore-only (or git checkout -- experiments/).
- scripts/check_goldens_clean.py fails when a tracked artifact under experiments/ differs from HEAD or a stale snapshot is pending. Fix any golden mismatch before committing.
- scripts/check_golden_baseline.py compares every tracked artifact under experiments/ against SHA-256 pinned in ledger/golden_baseline.json. Replacing an artifact requires re-pinning (python3 scripts/check_data_coverage.py --update), which puts the replacement in the diff.
- Cache coverage invariant: scripts/check_data_coverage.py resolves every data.download() call site statically and requires each cache file exist, be git-tracked, and match SHA-256 in ledger/data_baseline.json. The suite runs drivers with QUANT_RESEARCH_OFFLINE=1; a missing cache entry fails hard. To add a data input, commit the file and re-pin.
- Optimizer determinism (ledger E049): src/portfolio_opt.py validates solver answers on the problem's constraints, never on solver exit status. Tests: tests/test_portfolio_opt.py (first-class step of scripts/check.sh).
- E041 drift: optimizer defect fixed; remaining 133 numeric differences are 1-ulp QP sensitivity exceeding 1e-4 tolerance. Do NOT re-pin to silence — see ledger open item.
- Offline-reproducible since 2026-10-20: E029 (fundamentals pinned in data/fundamentals/ per data/fundamentals_vintages.json), E030 (16-ETF panel committed).

Dependencies: pip install -r requirements.txt (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional; optimizer falls back to scipy.optimize.

CI note: The intended CI gate (.github/workflows/verification-gate.yml) cannot be created by automated agents; a copyable template lives at .github/workflow-templates/verification-gate.yml. A maintainer must create the actual workflow via the GitHub UI.

Lint/format: python3 -m py_compile on changed files. No separate linter configured.

Open items / next steps
- Review ledger E049 open item regarding E041/E042 grid artifacts drifting by 29–133 differences (1-ulp QP sensitivity).
- Consider pinning any remaining unpinned data inputs to keep the suite offline-reproducible.

No in-progress work. Session ends clean.