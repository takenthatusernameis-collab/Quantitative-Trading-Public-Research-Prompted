# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T04:13:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `19fcf0c9d87e87c7ab2de7e32397d6a7cc331447` ("chore(kilo): checkpoint agent session", committed 2026-11-15T04:12:01Z); `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research item.
- **Baseline integrity (verified this session, exit 0):**
  - `SEED=42 bash scripts/check.sh` → **"=== All checks passed ==="** (py_compile, JSON parse, goldens clean vs HEAD, pinned golden-baseline match, data coverage, `tests/test_portfolio_opt.py`, convention robustness, template validation, experiment imports).
  - `python3 scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`.
  - `python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`.
- **Verification snapshot:** `.verify_snapshot/ACTIVE.json` absent; `.verify_reports/` absent. No verification run in progress, none interrupted.
- **Working tree:** no source/experiment/ledger/baseline/data changes. Only `__pycache__/*.pyc` build artifacts differ (gitignored noise — never commit).
- **Closed — do not reopen:** E049/E050 (optimizer determinism / exact KKT enumeration) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## INITIAL TASK for the next session (clear)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment; ignore `__pycache__/*.pyc` noise.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Install deps if needed: `pip3 install --break-system-packages -r requirements.txt`.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes (see `AGENTS.md`): `make check` (fast guards); `SEED=42 python3 verify_convention_robustness.py` (read-only); `SEED=42 python3 run_all_verification.py` (quick ~8 min); `--extended` (~21 min); `--full`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items (research through E051; handoff refreshes through E352).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts (107 tracked golden JSONs).
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-15T04-13-05Z_INITIAL_TASK.md` (repo root), mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Supersedes operationally:** `handoff_2026-11-15T04-11-33Z_INITIAL_TASK.md` (retained for history).
- Canonical generic pointers repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-15T04-13-05Z_INITIAL_TASK.md`.
- This session created this durable handoff only; no code, experiments, ledgers, baselines, or canonical artifacts were modified.