# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T12:48:44Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E057). Baseline verified clean. Working tree clean. No live verification snapshot. No open task.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean. Research phase is complete (E001–E057); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
>
> **First action (required):** Run the fast integrity check before doing anything else:
> ```bash
> SEED=42 bash scripts/check.sh
> ```
> - If it exits 0 with no golden mismatches/stale snapshots → repo is in a good state. Read `ledger/RESEARCH_LEDGER.md` to confirm no open items, then wait for the user's next instruction. Do **not** re-run verification to "confirm" further.
> - If it reports golden mismatch or stale snapshot → recover per `AGENTS.md` (e.g. `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate). Never modify committed goldens to silence known issues.
>
> **Constraints:** Never commit verification output. Never re-pin goldens to silence drift (notably E041/E042 numeric drift from ill-conditioned QP per ledger E049). Honor pinned caches (`data/vintages.json`, `data/fundamentals/`). Follow `AGENTS.md`. Do **not** invent tasks — wait for explicit user instruction unless the ledger contains an unambiguous concrete next step you can act on without guessing.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- `AGENTS.md` — full commands & conventions
- Preceding handoff: `HANDOFF_NEXT_SESSION_2026-11-02T10-42-33Z.md`

(End of file)
