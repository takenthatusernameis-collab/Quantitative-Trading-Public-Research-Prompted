# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T07:18:23Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `633fddb0f7bcdefcab5b111e6098cb47a6880742` (`chore(kilo): checkpoint agent session`); local `main` in sync with `origin/main` at handoff time.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## INITIAL TASK for the next session

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before substantive work
1. `git status --short --branch` — confirm HEAD/remote alignment. Treat tracked `__pycache__/*.pyc` modifications as non-canonical build noise (do not commit).
2. Confirm `.verify_snapshot/` is absent. If an interrupted verification run is pending, recover first: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if HEAD is known-good per `ledger/golden_baseline.json`).
3. If deps are missing: `pip3 install -r requirements.txt` (or `pip3 install --break-system-packages -r requirements.txt` in this environment).
4. Before committing any substantive change: `SEED=42 bash scripts/check.sh` (or `make check`).

### If verification or reproduction is explicitly requested
- Always use `SEED=42`.
- Scopes: `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick, ~8 min), `--extended` (~21 min), `--full`.
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished and never commit verification output over goldens.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, the deliberate update command, and ledger justification.

---

## Current state (snapshot)

- **Research phase:** complete (E001–E051). Authoritative dispositions, surviving validated strategies, and open/closed items: `ledger/RESEARCH_LEDGER.md`. No actionable open, pending, or blocked research item recorded.
- **Canonical baseline:** 107 tracked `experiments/*.json` artifacts pinned in `ledger/golden_baseline.json`; data inputs/coverage pinned in `ledger/data_baseline.json`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism and exact KKT enumeration) and residual E041/E042 ill-conditioned-QP drift (~1-ulp, ~1e-05). Do not re-pin artifacts solely to silence that drift.
- **Working tree at handoff:** tracked `__pycache__/*.pyc` modifications only (build noise) plus this handoff deliverable and repointed generic pointer(s); no canonical research artifacts modified.
- **CI note:** `.github/workflows/` verification gate cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Guardrails

- Use `SEED=42` for reproducibility and verification.
- Never commit driver verification output over canonical goldens in `experiments/`.
- Never re-pin baselines without explicit instruction and ledger justification.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md`, `ledger/PRIORITIZATION.md` — dispositions and procedure.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.
- Prior durable handoff (retained): `handoff_2026-11-15T07:17:13Z_INITIAL_TASK.md`.

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T07:18:23Z_INITIAL_TASK.md` (root), mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/` per repo conventions.
- **Generic pointers repointed:** via `scripts/repoint_handoff.py` to this artifact.
- This session created this durable handoff and repointed generic pointers only; no code, experiments, ledgers, baselines, or canonical research artifacts were modified.
