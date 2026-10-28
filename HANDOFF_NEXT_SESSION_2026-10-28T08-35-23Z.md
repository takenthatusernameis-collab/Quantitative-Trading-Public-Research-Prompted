# Handoff for Next Agentic Work Session
Timestamp (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)
Branch: $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted branch --show-current)
HEAD: $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted rev-parse --short HEAD)
Dirty files: $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted status --short | wc -l)

## Quick context (from AGENTS.md)
- Research phase complete (E001–E043). Surviving validated strategies in ledger/RESEARCH_LEDGER.md.
- Verification critical: experiments/*.json are canonical. run_all_verification.py backs up/restores; never leave half-finished. check_goldens_clean.py and check_golden_baseline.py are guards.
- Cache/data coverage enforced (ledger/data_baseline.json). E029 fundamentals pinned; E030 panel committed. Offline reproducibility required via QUANT_RESEARCH_OFFLINE in suite.
- Optimizer determinism noted (E049) — SLSQP status8 feasible ok; tangency QP ill-conditioned, some numeric drift expected in grids; do not re-pin to silence.

## Current session state
Recent commits:
$(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted log --oneline -5)

Dirty working tree (top 30):
$(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted status --short | head -30)

## Immediate next actions (clear)
1. **Check goldens/baseline before changes**: `SEED=42 bash scripts/check.sh` (or `make check`). Fix any golden mismatch by restoring to HEAD/ledger-pinned state, not by re-running verification mid-way.
2. **If need to verify**: prefer `make verify-quick` first. If extended needed, use `make verify-extended`. Never leave verification running without recovery plan; snapshot lives in `.verify_snapshot/` with ACTIVE.json.
3. **If working tree dirty**: review changes. Do not commit verification outputs. If interrupted verification left modified experiments/, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` then pin-check.
4. **Before committing**: ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass, and any new data files pinned via `scripts/check_data_coverage.py --update` if added.
5. **Follow project rules**: pre-registration, multiple-testing discipline, no goalpost moving. Use SEED=42 for reproducibility.

## Known watchouts
- E041/E042 grids may show numeric drift (ill-conditioned QP) — acceptable if structural unchanged; see ledger E049. Do not re-pin.
- E029/E030 offline reproducible due to pinned artifacts.
- CI workflow cannot be created by agents; template in .github/workflow-templates/.

## Suggested starting command
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
SEED=42 bash scripts/check.sh
```
