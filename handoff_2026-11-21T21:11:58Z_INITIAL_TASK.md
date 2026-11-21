# Handoff — Kilo session

**Timestamp:** 2026-11-21T22:07:50Z
**Project:** Quantitative-Trading-Public-Research-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Task left for next session

No specific task was defined in this message. Clear the initial tasking when you assign work.

## Project state (summary)

- Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are committed golden artifacts — do not modify them except via `scripts/check_golden_baseline.py --update` after re-pinning.
- Verification commands: `make check` / `make verify-quick` / `make verify-extended` / `make verify-full`.
- `scripts/check.sh` runs convention robustness + template validation + goldens clean + golden baseline + portfolio opt tests.
- `QUANT_RESEARCH_OFFLINE=1` is used during verification so unpinned inputs fail hard.
- Seed: always `SEED=42`.

## Open items (from AGENTS.md ledger)

- E041 remaining 133 numeric diffs are 1-ulp sensitivity of ill-conditioned QP — do not re-pin to silence (open item in ledger).
- CI verification gate template exists at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via GitHub UI.
