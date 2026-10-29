# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T13:29:38Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main`
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. If verification output present, restore:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```

### 4. Orient to open work
- Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` (focus E049, E040).
- No mandated next research task. Research phase complete. Proceed only when user provides concrete objective.
- Numeric drift in E041/E042 is expected; do not re-pin.

---

## Gotchas / Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished.
- If no new objective given, maintain baseline (`check.sh` + quick verification) and report clean.

---

## Handoff Notes
- Durable handoff target updated.
