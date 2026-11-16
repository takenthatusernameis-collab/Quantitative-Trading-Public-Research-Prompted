# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T13:37:06Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `9c2df624` ("chore(kilo): checkpoint agent session") — in sync with `origin/main`.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. **Verify state** (fast, ~seconds):
   ```bash
   git status --short --branch
   ls -d .verify_snapshot .verify_reports 2>/dev/null || echo "no snapshot/reports"
   SEED=42 bash scripts/check.sh
   ```
   Expected: HEAD aligned with `origin/main`, only `__pycache__/*.pyc` tracked diffs (do **not** commit; import noise), no snapshot, `=== All checks passed ===`.
2. If `experiments/` differs from HEAD or a stale/interrupted `.verify_snapshot/` exists: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip install -r requirements.txt`.
4. Execute only the explicitly requested task within existing pre-registered scope and guardrails.
5. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**. Primary convention: close-to-close v1.2.3 (overnight reported alongside).
- Scopes (see `AGENTS.md`): `make check` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8 min), `--extended` (~21 min), `--full` (~15 min).
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Current state (verified at handoff)

- **Working tree:** no source/content changes. Tracked modifications limited to `__pycache__/*.pyc` under `scripts/`, `src/`, `tests/` (import noise) — **do not commit**; discard/restore if needed before committing other work.
- **HEAD:** `9c2df624` == `origin/main`; `git status -sb` shows `## main...origin/main` with no ahead/behind.
- **Interrupted verification:** `.verify_snapshot/` and `.verify_reports/` absent (no pending recovery).
- **Integrity check (this session):** `SEED=42 bash scripts/check.sh` → exit 0, `=== All checks passed ===` at 2026-11-16T13:37Z.
- **Canonical artifacts:** `experiments/*.json` goldens, `ledger/` (`RESEARCH_LEDGER.md`, `PRIORITIZATION.md`, `golden_baseline.json`, `data_baseline.json`), pinned `data/` and `data/fundamentals/` inputs — unchanged by this session. Do not overwrite goldens with verification output.
- **Research phase:** complete (E001–E043). Authoritative dispositions/open items: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ~1-ulp/ill-conditioned QP drift (~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification. Primary convention: close-to-close v1.2.3 (overnight reported alongside).
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); missing pinned caches must fail hard. Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/PRIORITIZATION.md` — strategy ranking
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T13-37-06Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified.