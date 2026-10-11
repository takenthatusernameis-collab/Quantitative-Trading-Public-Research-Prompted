#!/usr/bin/env python3
"""Merge the separately-run Part A/B/C outputs of E024 into one JSON.

Part A (deterministic, ~20s) and Part B (50-sim placebo sweep, ~20 min)
were run in separate invocations because Part B is long-running and
Part C needs the raw/adjusted download. This merges the three
partial outputs (each written to the same path by run_e024.py) into a
single consolidated file with the pre-registered falsification
expectations evaluated from the merged data.
"""
import json
import os

OUT = os.path.join("experiments", "e024_convention_audit.json")

# Re-run Part A fresh (deterministic) so the merged file is self-consistent
# and reproducible; Part B and Part C are read from the partial outputs
# already written by run_e024.py.
import subprocess
subprocess.run(["python3", "experiments/run_e024.py", "--parts", "a"],
               check=True, capture_output=True)

base = json.load(open(OUT))
part_b = json.load(open(OUT))  # Part B run wrote its own partial output
# Re-read: Part B run overwrote the file with only part_b. Re-run Part A
# to restore it, then overlay Part B and Part C from saved copies.
# Simpler: re-run Part A (done above), then read the Part B and Part C
# partials that were written to the same path by their own runs.
# We saved them via the run_e024.py invocations above; re-derive by
# re-running is wasteful, so instead re-run A then B then C in sequence
# is what we want to avoid. Use the approach: re-run A, then re-run B
# and C by reading their partial outputs captured at the time of their
# runs. Since run_e024.py writes the whole result dict per run, the
# Part B run's file has part_b only; the Part C run's file has part_c
# only. We re-run A to get part_a, then re-run B and C to overlay.

# Strategy: run A, then B, then C in one go is the canonical path; this
# script exists only to avoid re-running the 20-min B sweep. So we
# re-run A (fast) and then re-run B and C by reading the partial
# outputs that were already produced. But those partials were
# overwritten by subsequent runs. Therefore the only reliable merge
# is to re-run all three. We do that here with a generous timeout,
# delegating to run_e024.py which writes the merged file itself when
# all parts are requested.
print("Merging requires re-running all parts; delegating to run_e024.py")
subprocess.run(["python3", "experiments/run_e024.py"],
               check=True)
print("Merged output written to", OUT)