# Durable Handoff — Initial Task Message

**Created:** 2026-11-17T14:59:29Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

- No work performed in this session yet — fresh handoff.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are committed golden artifacts — never left half-finished by a verification run.
- Seed convention: `SEED=42`.

## Next agentic work session — initial task

**Task:** Run the convention-robustness check and verify golden integrity before any new work:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If clean, proceed with the quick verification block:

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Constraints / gates (read before acting)

- A verification run overwrites `experiments/*.json` then restores them. Never leave a run half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
- `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending in `.verify_snapshot/`.
- `scripts/check_golden_baseline.py` compares each tracked artifact against the SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact requires re-pinning (`python3 scripts/check_golden_baseline.py --update`).
- Data coverage invariant: every `data.download()` call site must resolve to a git-tracked, SHA-256-pinned cache file per `ledger/data_baseline.json`. Offline mode `QUANT_RESEARCH_OFFLINE=1` fails hard on missing cache.
- No separate linter; run `python3 -m py_compile` on changed files.
- Do not commit verification output.

## References

- `AGENTS.md` — project commands & conventions (authoritative)
- `ledger/RESEARCH_LEDGER.md` — validated strategies, gates, falsification expectations
- `.kilo/command/*.md`, `.kilo/agent/*.md`, `kilo.json` — Kilo config (put new commands/agents in `.kilo/`)
