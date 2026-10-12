# Research Prioritization Procedure

Version 1.0 (initial bootstrap). Records the explicit ranking criteria used to select
public research for testing. Each experiment entry in the ledger cites the ranking
rationale that motivated it.

## Ranking Criteria (weighted, transparent, not empirically calibrated)

| Criterion | Weight | What it means |
|---|---|---|
| Economic plausibility | 0.20 | Clear mechanism; why would an inefficiency persist? |
| Evidence quality | 0.20 | Independent replication, out-of-sample, no obvious bias |
| Data availability | 0.12 | Free/low-cost data, no survivorship, sufficient history |
| Implementation ease | 0.05 | Direct translation to executable rules |
| Cost robustness | 0.12 | Edge survives realistic transaction costs and slippage |
| Turnover/Capacity | 0.08 | Turnover, liquidity, capacity constraints for implementability |
| Novelty vs existing | 0.03 | Not duplicating experiments already in the ledger |
| Statistical rigor | 0.05 | Multiple-testing awareness, uncertainty quantified |
| Complementarity | 0.05 | Adds diversification to existing strategy set |
| Validation potential | 0.04 | Can be independently verified / walk-forward tested |
| Data integrity | 0.06 | Signal/return series free of stitching, split, survivorship, roll artifacts; data construction understood |

## Source Priority Order

1. Original academic papers / working papers with reproducible empirical studies
2. Quantpedia / AQR research libraries
3. Open-source implementations (QuantConnect, Freqtrade, etc.)
4. arXiv / SSRN / NBER recent research
5. Other publicly accessible specialist sources

## Procedure

1. Inspect repository state (ledger, experiments, data, code).
2. Search public sources for candidate strategies.
3. Score each candidate on the criteria above.
4. Pick the highest-scoring untested candidate.
5. Design the cheapest falsifiable experiment.
6. Run, validate for biases, record in ledger (including negatives).
7. Re-rank remaining candidates; repeat.

## Version History

### v1.0 (2026-10-10)
- Initial bootstrap procedure.
- Motivation: repository was empty; needed a baseline ranking method.
- Expected benefit: explicit, auditable criteria to avoid ad-hoc selection.
- Evaluation: compare strategy hit-rate and OOS Sharpe against random baseline over next 10 experiments.
### v1.1 (2026-10-10) - Active
- Motivation: With strong gross results on broad universe, need to explicitly account for turnover/capacity and strengthen cost robustness.
- Changes:
  - Cost robustness: 0.12 (was 0.10)
  - Turnover/Capacity: 0.08 (new) - penalize high turnover, liquidity/capacity constraints
  - Novelty vs existing: 0.05 (was 0.10)
  - Data availability: 0.12 (was 0.15)
  - Implementation ease: 0.08 (was 0.10)
  - Economic plausibility: 0.20, Evidence quality: 0.20, Statistical rigor: 0.05, Complementarity: 0.05, Validation potential: 0.05
- Expected benefit: Better discrimination between gross vs net edge; forces turnover quantification.
### v1.2 (2026-10-11) - Active
- Motivation: E016 found that raw stitched futures (yfinance `=F` continuous contracts) contain large roll-seam artifacts (median gaps 0.3-2.5%; CL 2020 wedge of -306%/-127% overnight) that moved TSM OOS Sharpe by 21% (0.590 raw vs 0.717 de-seamed) and flipped its bear-market Sharpe (-1.06 to +0.15). E015's multi-asset results were computed on contaminated futures data. A candidate's data-construction risk must be screened before backtesting, not discovered after.
- Changes:
  - Data integrity: 0.06 (new) - is the signal/return series free of stitching, roll, split and survivorship artifacts; is the data construction understood?
  - Implementation ease: 0.05 (was 0.08)
  - Novelty vs existing: 0.03 (was 0.05)
  - Validation potential: 0.04 (was 0.05)
- Expected benefit: Catches artifact-dominated candidates early (e.g. futures on stitched series, split-unadjusted equities); redirects effort to strategies whose data pipeline is validated.
- Evaluation: E016/E017 are the first experiments scored under v1.2 and confirm the criterion's value: E017 showed roll artifacts move rolled-futures TSM OOS Sharpe by ~3x on the extended sample (0.225 raw vs 0.680 de-seamed) and quantified E015's multi-asset inflation at -0.248 Sharpe (2.086 raw vs 1.838 de-seamed, replicated exactly). Data-integrity screening is now a mandatory pre-backtest pass for any futures/stitched series.
- Evaluation: E018 (third experiment under v1.2) validated the procedure's validation-first direction: on the roll-corrected panel it cleanly REJECTED realized-roll-yield carry at the pre-registered bar (carry-specific placebo z=2.65 < 3; the blended-null z=2.80 from E017 overstated it) and failed the pre-registered 18m TSM confirmatory run on Sharpe (0.805 < 1.0 despite z=3.76) — both honest negatives recorded with goalposts unmoved. The procedure continues to route effort onto data-construction-validated assets and enforces pre-registered falsification.
### v1.2.1 (2026-10-11) - Active
- Motivation: E019 found that the E018 handoff narrative stated "the equity flagship carries full equity beta (beta ~0.9)" — FALSE for the registered monthly-rebalanced construction (E015 recorded beta -0.066; E019 re-verified -0.065). The mis-stated premise did not change E019's gates (Sharpe/bear-based), but it mis-framed the experiment's rationale (a beta-offset story instead of the actual return-stream-diversification story) and would have mis-led any agent acting on the handoff without checking artifacts.
- Changes:
  - Mandatory pre-registration step added: before pre-registering a follow-up experiment, verify every factual premise in the handoff against the recorded experiment JSONs/artifacts; record any correction in the new entry's `pre_registered` block (as E019 did with `premise_correction`) and re-examine whether the gates depend on the corrected premise.
- Expected benefit: Keeps handoff narratives honest without slowing the loop; premises that survive verification are stated with evidence, premises that fail are corrected before they can propagate into gate design or interpretation.
- Evaluation: E019 is the first experiment scored under v1.2.1 and its premise-correction record is the template; a future handoff whose premise fails verification and would have changed a gate is the success case to watch for.
- Evaluation: Track turnover and net Sharpe under varying cost assumptions for top strategies.
### v1.2.2 (2026-10-11) - Active
- Motivation: E021 (pairs trading, Gatev et al. 2006) was the highest-scoring
  untested candidate under v1.2.1 (Complementarity 0.05, Evidence quality 0.20,
  Economic plausibility 0.20) and FAILED cleanly: OOS Sharpe 0.315 vs a
  pair-level placebo z of 0.77, 3/5 pre-registered gates, no formation/max-pairs
  configuration clears the 0.8 bar. The failure is not a data or implementation
  artifact (the module was audited and rewritten for a stateful-signal bug), so
  it is a genuine sample-period negative. The lesson: high academic evidence
  quality and complementarity do not guarantee a reproducible edge on a given
  universe/sample, and "replicated elsewhere" is not "replicable here". The
  procedure should discount candidates whose supporting evidence is primarily
  out-of-sample-in-other-markets and require a within-sample falsification
  expectation before committing compute.
- Changes:
  - Evidence quality: add an explicit sub-split — "independent replication
    *on a comparable universe/sample*" (high) vs "replicated in other
    markets/eras only" (discounted). Many pairs/stat-arb results fall in the
    second bucket.
  - Novelty vs existing: 0.03 (unchanged) but now interpreted as
    "uncorrelated *and* not already exhausted on this data", not merely
    "different family".
  - Add a mandatory pre-experiment falsification expectation field: for each
    candidate, record the cheapest test that would reject it *before* running,
    and require the recorded outcome (pass/fail) to be reported even when it
    fails. E021's placebo z is the template.
- Expected benefit: Redirects effort away from candidates whose published
  edge is sample/era-specific and toward candidates with a plausible
  within-sample mechanism (e.g. macro momentum on FRED, E022), and makes
  negative results informative rather than surprising.
- Evaluation: E022 (macro momentum) is the first experiment under v1.2.2; the
  success case is a pre-registered falsification test that rejects the
  candidate cleanly *and* the ledger records the falsification expectation
  before the run.
### v1.2.2 evaluation (E022, 2026-10-11)
- E022 (macro momentum, Brooks 2017 directional variant) was the first
  experiment under v1.2.2. The pre-registered falsification expectation
  (mean per-cell |Spearman| >= 0.03, >= 8/15 sign matches) was recorded
  before running and reported: NOT falsified (mean |rho| = 0.077, 11/15
  sign matches) — the within-sample-mechanism screen correctly identified
  that the signals carry predictive content on this universe/sample,
  unlike E021 (pairs) whose failure was sample-specific.
- The walk-forward then honestly rejected the strategy at the
  pre-registered bar (OOS Sharpe 0.428 < 0.8; placebo z = 2.00 < 3.0;
  3/5 gates) while preserving the genuine findings (bear-regime Sharpe
  +0.792, COVID +2.01, 2022-bear +1.87, beta -0.011). The v1.2.2 loop
  worked as designed: the falsification expectation filtered for
  within-sample plausibility, the gates enforced the promotion bar, and
  the negative result is informative (macro momentum is a diversifier,
  not a standalone component, on this US-only implementation).
- Lesson recorded: the v1.2.1 premise-verification step caught a
  non-existent citation ("Brooks & Moskowitz 2022" -> Brooks 2017 AQR
  white paper) before it propagated into gate design — the second
  confirmed success case for that step.
### v1.2.3 (2026-10-11) - Active
- Motivation: E023 (Economic Trend blend, Brooks/Feilbogen/Ooi/Akant
  2024) was the second experiment under v1.2.2 and exposed a
  procedure-level blind spot: the paper's *correlation* premise
  replicated cleanly (inter-sleeve corr 0.226; per-asset weight corr
  mean 0.350 vs the paper's ~0.3/~0.4) and both pre-registered
  falsification expectations passed, yet the *performance* claim
  failed decisively (blend 50/50 OOS 0.128 c2c vs price-trend
  sleeve 0.539; matched-placebo z=-0.36; 3/6 gates). The v1.2.2
  falsification-expectation layer correctly did NOT block the
  experiment (it screens mechanism presence, not edge size), but
  the loop spent a full experiment learning that a published blend
  claim can hold in correlation while failing in performance on a
  different universe/sample. Two corrective insights: (1) a
  candidate's *published performance* must be discounted when the
  supporting sample differs materially from the test universe (the
  paper is 1970-2022 global multi-asset; this test is 2014-2026
  US-only 3 ETFs) — the "implementation gaps vs paper" list is now
  a mandatory scored input, not just documentation; (2) E023's
  decomposition revealed that BOTH sleeves' edges are
  overnight-concentrated (macro 0.516 overnight / -0.147 intraday;
  trend 1.064 / 0.539) — the third convention-dependent result in a
  row (E019 demotion by E020; E023). The execution convention now
  dominates measured edge across the repository, so convention
  choice must be pre-registered and audited before further strategy
  search (mission section 5).
- Changes:
  - Evidence quality: published performance claims are discounted
    by the materiality of the universe/sample gap (recorded in the
    pre-registration block as "implementation gaps vs paper"); a
    candidate whose edge depends on breadth (global multi-asset,
    5+ decades) scores lower on a 3-ETF, 12-year US test.
  - Data integrity: add "execution-convention concentration" to the
    screening question — is the candidate's edge concentrated in one
    trading session (overnight vs intraday)? If unknown, the first
    experiment must decompose it.
  - New mandatory deliverable for experiments that mix or inherit
    conventions: a convention-robustness column (both c2c and
    overnight) in every results table.
- Expected benefit: prevents spending full experiments on blend/
  combination claims whose premises hold but whose performance does
  not transfer; converts the E020/E023 convention lesson into a
  standing measurement standard.
- Evaluation: E024 (overnight-intraday decomposition audit) is the
  first experiment under v1.2.3 — it institutionalizes the
  convention policy (Part D) and quantifies the overnight share of
  every validated strategy's edge. Success case: the audit's
  convention-robust ranking changes at least one promotion decision
  or confirms the current promoted set under both conventions.
- Screening record (2026-10-11): variance-risk-premium / options-
  based strategies (Baltussen et al. 2018) verified INFEASIBLE with
  available data — yfinance option chains are point-in-time only
  (historical expirations raise ValueError; only current/future
  expirations are listed; direct probe). Family rejected as
  infeasible; do not re-propose without a new historical-options
  data source. Recorded so subsequent agents do not re-derive it.

### v1.2.4 (2026-10-12) - Active
- Motivation: E033 QMJ feasibility screen produced GROUND-TRUTH evidence
  confirming the fundamental-data wall that sank E029 (profitability/
  investment), E031 (accruals) and E032 (PEAD). A direct yfinance 1.7.0
  probe of all 132 large_liquid tickers shows the free `t.quarterly_*`
  APIs return only the trailing ~6 quarters per ticker (earliest
  2025-01-31), versus ~50 quarters required for a 504-trading-day
  formation window over 2014-2026. Earliest formation close ≈ Q3 2027.
- Findings that survived scrutiny:
  1. Any candidate requiring quarterly income-statement / balance-sheet /
     cash-flow data is DATA-INFEASIBLE on the available (yfinance) data
     for a 2014-2026 walk-forward — QMJ (profitability + growth +
     leverage-safety + payout), accruals, GP/AG, SUE all fall here.
  2. Price + dividend proxies remain fully available (daily price 2014+
     for 130/130; dividends to 1962 for 118/130), so price/dividend/
     volume-only candidates are NOT blocked.
- Changes:
  - Data integrity screening: add an explicit "fundamental-data
    depth" question — does the candidate require quarterly financials
    AND can they be obtained for ≥50 quarters back to 2012? Candidates
    that fail are scored DATA-INFEASIBLE (gate-0 abort) without compute.
  - Evidence quality: candidates whose published edge is documented only
    on accounting-dependent constructs score Evidence quality DOWN one
    band when no fundamental-data source is available (v1.2.2 discount
    reinforced with hard data, not assumption).
- Expected benefit: prevents another full-session wasted on a
  data-infeasible fundamental-factor test; keeps effort on price/
  dividend/volume-only candidates that are actually runnable here.
- Evaluation: E033 recorded DATA-INFEASIBLE (gate-0 aborted, 0 compute
  beyond the probe); no agent commits full compute to an accounting-
  dependent factor until a historical-fundamentals feed exists.
