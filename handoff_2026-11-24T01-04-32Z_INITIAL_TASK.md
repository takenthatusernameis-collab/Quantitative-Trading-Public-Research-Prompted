# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T01:04:32Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `2dbc2855` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Orientation (read first)

- This is an independent, reproducible quantitative-strategy research repo
  (2014–2026 US equities, futures, macro). Research phase is complete
  (E001–E043); surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts are `experiments/*.json`. They are committed and
  pinned by SHA-256 in `ledger/golden_baseline.json` (artifacts) and
  `ledger/data_baseline.json` (cached inputs).
- **Handoff file naming/discovery:** prior sessions drop a single
  `handoff_<UTC>_INITIAL_TASK.md` in the repo root. The ~500 symlinks
  (`handoff_CURRENT`, `handoff_LATEST`, `latest`, `next_session`, `.kilo/HANDOFF.md`,
  `.handoff/*`, etc.) are a stale farm that still point at
  `handoff_2026-11-23T19-02-10Z_INITIAL_TASK.md`. **Do not trust those pointers as
  "current"** — instead read the newest `handoff_*_INITIAL_TASK.md` by timestamp
  (this file) and/or `ls -t handoff_*.md | head`.

## Verified state at the time of writing (this session)

- `git status --porcelain` → empty (working tree clean; no `__pycache__` noise).
- `git rev-list --left-right --count origin/main...HEAD` → `0	0`
  (HEAD in sync with `origin/main`, nothing ahead/behind).
- This session made **no** code, experiment, ledger, baseline, or canonical-artifact
  changes and **no commit**. It created this handoff file only.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, do not
run the verification suite unprompted, do not move pre-registered gates, and do
not touch golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work top-to-bottom and stop as soon as a step is
genuinely done:

1. **Verify and stop.** Confirm cleanliness and sync
   (`git status --porcelain`, `git rev-list --left-right --count origin/main...HEAD`).
   If clean and in sync, report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).**
   `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended`
   (~21 min). Report per-driver drift precisely. **Never** re-pin an artifact to
   make a tolerance violation disappear.
3. **E041/E042 residual ill-conditioned-QP drift (~1e-05):** already root-caused and
   fixed by the E050 exact KKT active-set enumeration (ledger E049/E050); bit-reproducible
   at the 2026-11-23T05:17Z measurement. Only revisit if step 2 shows a *new* structural
   difference; never "fix" it by re-pinning.
4. **Handoff-farm cleanup (propose only).** The repo carries thousands of
   `handoff_*` files and ~500 symlinks. If this is a problem, *propose* (do not execute)
   a `.gitignore` + `git rm --cached` consolidation plan and let the user decide.
5. **Pre-registered research** only if the user explicitly requests it — with a
   `pre_registered` block, falsification expectations, and sensitivity grid stated
   *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
  If a run is interrupted, restore first: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout <last-good-commit> -- experiments/<file>`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without an
  explicit, intentional re-baseline instruction and a ledger entry justifying it.
- Do not reopen closed items E049/E050 or the E041/E042 drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template at
  `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys; never log secrets.
- Do not manufacture handoff refreshes to look busy — one durable file per session is enough.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py` — verification entry points
- Quick convention check: `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verify: `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-24T01-04-32Z_INITIAL_TASK.md` (repo root).
- Supersedes `handoff_2026-11-24T01-03-00Z_INITIAL_TASK.md` (same task, earlier timestamp).
- No code, experiments, ledgers, baselines, or canonical artifacts were modified.
  No commit was made (left uncommitted pending explicit user direction).