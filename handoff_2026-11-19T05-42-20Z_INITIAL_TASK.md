# Agentic Work Session Handoff

**Created:** 2026-11-19T05:42:20Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Baseline HEAD at handoff time:** `e8519e74daa63c9f21c4d390b3470782796edb37` (`chore(kilo): checkpoint agent session`, == `origin/main`)
**Status:** Open — awaiting next agentic work session
**Supersedes:** `handoff_2026-11-19T05-39-20Z_INITIAL_TASK.md` (current durable artifact only; no earlier content altered)

## Read this first (in order)

1. Read `AGENTS.md` fully — commands, baseline integrity, reproducibility rules, project conventions.
2. `git status --short --branch` and `git log --oneline -10`. Confirm the only dirty paths are the
   handoff pointer symlinks (expected after a handoff refresh). Nothing under `experiments/` may be dirty.
3. If `.verify_snapshot/` exists with an `ACTIVE.json` marker, an earlier verification run was
   interrupted. Recover **before** touching artifacts:
   `SEED=42 python3 run_all_verification.py --restore-only`
4. Confirm goldens are intact (both must pass):
   - `python3 scripts/check_goldens_clean.py` → ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
   - `python3 scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
5. Set up the environment (this runner has bare Python 3.12.3; numpy/pandas/scipy are **not** installed):
   `pip install -r requirements.txt`
6. Run the fast gate: `SEED=42 bash scripts/check.sh` (or `make check`). Do not start new research
   until it passes.
7. Then **await an explicit research instruction**. This handoff contains no new research task; the
   research phase is complete (E001–E051). Do not invent scope.
8. When you finish, leave your own timestamped durable handoff (procedure below).

## Verified state at handoff time

- `HEAD` == `origin/main`, tree clean except the repointed handoff pointers.
- `.verify_snapshot/` and `.verify_reports/` absent — no interrupted verification to recover.
- `git ls-files experiments/` → 138 canonical artifacts; `git diff --name-only HEAD -- experiments/` empty.
- `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` both pass.
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` present and parse.
- `scripts/check.sh` **not** run this session (dependencies missing); running it is the next session's
  first substantive verification step.

## Common commands (always `SEED=42`)

- Fast check (~seconds): `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Extended verify (~21 min): `SEED=42 python3 run_all_verification.py --extended`
- Full verify (~15 min): `SEED=42 python3 run_all_verification.py --full` (E042 n_sim=50 + 96-config grid)
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py`
- Individual drivers: `SEED=42 python3 experiments/run_e0NN.py` (e.g. `run_e042.py --n-sim 50`)

## Integrity rules (non-negotiable)

- `experiments/*.json` are the canonical artifacts. The verification suite overwrites them and
  restores them afterwards — **never leave a run half-finished, never commit verification output**.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of a
  verification run. The committed golden is the authoritative record. Re-pinning is a deliberate,
  separately reviewed change (`--update`) that must appear in the diff with its reason.
- Known accepted drift (do **not** "fix" by re-pinning): E041/E042 grid artifacts drift by 29–133
  numeric differences from 1-ulp sensitivity of an ill-conditioned tangency QP (ledger E049). E041's
  decision and gate flags are unchanged. E030/E029 are offline-reproducible and pinned; they now
  reproduce with 0 differences.
- `QUANT_RESEARCH_OFFLINE=1` is exported by the verification suite; an unpinned data input fails hard
  rather than silently downloading. Adding a data input = commit the cache file + `--update` the pin.
- Optimizer determinism: `src/portfolio_opt.py` validates solutions on constraints, not solver exit
  status; pinned by `tests/test_portfolio_opt.py`.
- No dedicated linter; use `python3 -m py_compile` on changed Python files and keep `__pycache__` out
  of commits.
- CI verification-gate workflow cannot be created by automated agents (controller cleans
  `.github/workflows/`; token lacks `workflows` scope). Maintainer must add it via the GitHub UI from
  `.github/workflow-templates/verification-gate.yml`; see `VERIFICATION_GATE_TEMPLATE.md`.
- Only commit when the user explicitly asks. Checkpoint commits (`chore(kilo): checkpoint agent
  session`) are made by the controller, not by you.

## Key references

- `ledger/RESEARCH_LEDGER.md` — all experiment dispositions (E001–E521+); read the tail for the most
  recent handoff-refresh entries.
- `ledger/PRIORITIZATION.md` — criterion weights and procedure for picking any future candidate.
- `AGENTS.md` — authoritative commands, coverage matrix, drift notes.
- `run_all_verification.py` — suite entry point (`--skip-slow`, `--restore-only`, `--extended`, `--full`).

## Durable handoff procedure (repeat each session)

1. Write `handoff_<YYYY-MM-DDTHH-MM-SSZ>_INITIAL_TASK.md` at the repo root with this same structure
   (timestamp, HEAD, status, read-this-first checklist, verified state, commands, integrity rules).
2. `python3 scripts/repoint_handoff.py handoff_<timestamp>_INITIAL_TASK.md` — repoints the 490 generic
   alias symlinks across `.`, `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
   Expect `checked=490 bad=0`. Never pass `--help` or any non-filename argument (it becomes the
   symlink target and corrupts the pointers).
3. Append a ledger entry to `ledger/RESEARCH_LEDGER.md` recording timestamp, HEAD, actions, the
   verification you actually ran, and the constraints honored (no re-pin, no verification output
   committed, no new research, no `__pycache__`).
4. Leave changes uncommitted unless the user explicitly asks for a commit.
