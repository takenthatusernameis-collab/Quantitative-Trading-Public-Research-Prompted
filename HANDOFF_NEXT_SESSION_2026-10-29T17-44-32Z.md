# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-29T17:50:14Z

---

## Initial Task Message

> **Status:** Awaiting specific task assignment from the user.
>
> **Context:** This is a quantitative trading research repository (2014–2026 US equities, futures, macro data). All experiments are pre-registered with falsification expectations and promotion gates. Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
>
> **Next Steps:** The next agentic work session should:
> 1. Check the shared board (`board_read`) for any pending peer messages or task assignments.
> 2. Review `AGENTS.md` for project commands, conventions, and baseline integrity rules.
> 3. If a specific task is provided, proceed with the requested software engineering work (bug fixes, new functionality, refactoring, etc.).
> 4. If no task is assigned, await further user instructions.

---

## Project Quick Reference

- **Seed:** Always use `SEED=42`
- **Verification:** `make check`, `make verify-quick`, `make verify-extended`, `make verify-full`
- **Baseline integrity:** `experiments/*.json` are canonical; verification suite backs up and restores them
- **Data coverage:** Cached parquet in `data/` (gitignored except pinned vintages)
- **Dependencies:** `pip install -r requirements.txt`