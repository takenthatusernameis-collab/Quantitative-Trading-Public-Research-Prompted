# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T12:44:22Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `10ce2f2f1e687a6913402065dc2e273c8516853b` ("chore(kilo): checkpoint agent session") — in sync with `origin/main` (`0 0`).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task for the next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, in order:**
1. **Verify state** (fast, ~seconds):
   ```bash
   git status --short --branch
   ls -d .verify_snapshot .verify_reports 2>/dev/null || echo "no snapshot/reports"
   SEED=42 bash scripts/check.sh
   ```
   Expected: HEAD aligned with origin, only `__pycache__/*.pyc` tracked diffs (do not commit), no snapshot, `=== All checks passed ===`.
   If `experiments/` differs from HEAD or a stale `.verify_snapshot/` exists: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`).
2. **Execute only the explicitly requested task** within existing pre-registered scope and guardrails.
3. **If verification is requested**, use `SEED=42` (quick ~8 min / extended ~21 min / full ~15 min). **Never commit driver verification output** over `experiments/*.json`; restore after any interruption. Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence mismatches — restore or justify per ledger/`AGENTS.md`.

## Current state (observed 2026-11-16T12:44Z)

- **Working tree:** no source/content changes. Tracked modifications limited to `__pycache__/*.pyc` under `scripts/`, `src/`, `tests/` — **do not commit**.
- **Interrupted verification:** `.verify_snapshot/` and `.verify_reports/` absent (no pending recovery).
- **Canonical artifacts:** `experiments/` goldens, `ledger/` (`RESEARCH_LEDGER.md`, `PRIORITIZATION.md`, `golden_baseline.json`, `data_baseline.json`), pinned `data/` inputs — all unmodified. Do not overwrite goldens with verification output.
- **Fast integrity check:** `SEED=42 bash scripts/check.sh` → exit 0 (`=== All checks passed ===`, 2026-11-16T12:44Z).
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
- Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); missing pinned caches must fail hard. Never commit secrets/keys.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T12-44-22Z_INITIAL_TASK.md` (repo root). Generic pointer aliases repointed to this file.
- **Supersedes operationally:** `handoff_2026-11-16T12-38-14Z_INITIAL_TASK.md`, `handoff_2026-11-16T12-37-21Z_INITIAL_TASK.md`, and earlier timestamped handoffs (retained for history).
- This session created this durable handoff only; no code, experiments, ledgers, or baselines were modified.