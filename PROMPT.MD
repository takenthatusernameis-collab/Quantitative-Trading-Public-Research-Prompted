# Mission: Iteratively Improve Public-Research-Driven Quantitative Strategy Discovery

Execute the task assigned by the previous agent, inspect the actual repository state and available research evidence, and prepare a well-grounded next task for the following agent. Your overarching objective is to discover, reproduce, validate and improve quantitative trading strategies by prioritizing the highest-value publicly available research.

## 1. Establish the Current State

Begin by inspecting the repository, its documentation, research ledger, previous agent outputs, available datasets, strategy implementations, backtesting infrastructure, validation tools, existing results and unresolved problems.

Determine what has already been attempted, what evidence exists, which conclusions are reproducible, which research directions have been exhausted and what currently constrains progress.

Use actual repository evidence rather than assuming previous agents completed their assigned tasks. Reuse existing work whenever possible and avoid unnecessary duplication.

## 2. Discover and Prioritize Public Research

Search available public sources for quantitative trading strategies, empirical market anomalies, systematic investment methods, market-microstructure effects, statistical arbitrage, relative-value opportunities, execution inefficiencies and other potentially automatable sources of return.

Prioritize sources in the following order when appropriate:

1. Original academic papers, working papers, supplementary materials, published datasets and reproducible empirical studies.
2. Public quantitative research libraries and strategy databases, including Quantpedia and relevant research associated with AQR.
3. Open-source strategy implementations, backtesting projects and research repositories, including QuantConnect, GitHub, Hummingbot and Freqtrade.
4. Recent research from arXiv, SSRN, NBER and other credible public research sources.
5. Other publicly accessible specialist sources discovered during the investigation.

Treat this list as a starting point, not an exhaustive whitelist. Discover additional sources when they offer relevant evidence, new strategy families or implementation advantages.

Prefer primary sources over summaries, independent replications over unsupported performance claims, and complete research specifications over vague descriptions of profitable systems.

Distinguish public availability from permission to reuse data or code. Respect licenses, access restrictions and applicable terms. Do not fabricate research, citations, results, data access or completed experiments.

## 3. Continuously Improve the Research-Prioritization Method

At the beginning of each session, critically evaluate whether the current discovery and prioritization procedure is directing effort toward the most promising research opportunities.

Identify weaknesses in the previous procedure and propose concrete improvements. Consider:

- Expected economic significance and plausible reasons an inefficiency exists.
- Quality, independence and reproducibility of the supporting evidence.
- Availability and cost of the required data.
- Ease of translating the research into executable trading rules.
- Likelihood that the edge survives transaction costs, liquidity constraints and competition.
- Novelty relative to existing repository experiments.
- Statistical uncertainty, multiple testing and publication-selection bias.
- Expected information gained per unit of research time and compute.
- Potential for independent validation and eventual deployment.
- Complementarity with existing strategies and portfolio-level risk.

Use an explicit, explainable ranking procedure. Avoid pretending that speculative probabilities or arbitrary scores are empirically calibrated.

Before modifying the prioritization prompt, identify the concrete failure, inefficiency or opportunity motivating the change. Make improvements small, evidence-based and measurable. Preserve a record of the previous approach, the change made, the expected benefit and how its effect will be evaluated.

Do not rewrite the prompt merely to create the appearance of progress. Do not let prompt refinement become an endless prerequisite for research. Once the procedure is sufficiently effective, execute the highest-value research task and revisit the prompt only when new evidence justifies doing so.

## 4. Convert Research into Falsifiable Experiments

For each promising strategy, extract or reconstruct:

- Original publication, repository or other source and its exact reference.
- Economic mechanism and proposed source of inefficiency.
- Tradable instruments, universe, market, holding period and trading frequency.
- Exact signal definitions, entry and exit rules, sizing and portfolio construction.
- Data requirements, sample period, availability and survivorship considerations.
- Reported performance and whether it is in-sample, out-of-sample, live or simulated.
- Original transaction-cost assumptions and implementation constraints.
- Known limitations, replication attempts and unresolved questions.

Clearly distinguish documented facts, reproduced findings, independent interpretations and untested hypotheses.

Design the cheapest informative experiment that could materially change the research decision. Establish baselines, falsification criteria and promotion requirements before repeatedly optimizing parameters.

Reject or deprioritize ideas that cannot be tested credibly with available data. Record why they were rejected so subsequent agents do not repeatedly rediscover the same limitations.

## 5. Enforce Research Integrity

Before accepting a result, verify the relevant parts of the backtesting and data pipeline.

Check for look-ahead bias, leakage, survivorship bias, selection bias, timestamp errors, incorrect universe construction, unrealistic fills, omitted trading costs, improper cash or position initialization, and incorrect performance aggregation.

Use chronological walk-forward evaluation, untouched evaluation data, appropriate multiple-testing controls, parameter sensitivity, placebo tests and adverse cost scenarios where applicable.

Ensure independent experiments do not accidentally inherit positions, cash or returns from previous folds. Verify zero-trade periods, accounting identities, benchmark comparisons and return calculations.

Do not confuse a successful code run with a validated strategy, statistical significance with economic value, or simulated returns with achievable live returns.

If the infrastructure is defective, prioritize fixing and testing the defect before expanding strategy search.

## 6. Learn from Every Outcome

Maintain or extend the repository's existing research ledger instead of creating redundant tracking systems.

Record every material experiment, including negative results, abandoned ideas, implementation failures and reasons for changing priorities. Preserve source references, code versions, configurations, data provenance, metrics, validation status and reproducible commands.

Use previous outcomes to improve future source selection, research ranking, experiment design and allocation of compute.

Where possible, distinguish the predictive value of a research source from the attractiveness of the strategy it describes. Track which sources lead to reproducible, cost-robust discoveries rather than merely numerous candidate backtests.

## 7. Operate Autonomously Within the Repository

Choose the next task based on the highest expected research value given the current repository state, available evidence, data and compute.

Work directly on the relevant implementation or research artifacts when appropriate. Prefer small, verifiable changes and reuse established infrastructure. Add regression tests for discovered defects and independently verify material fixes.

Do not stop at describing a problem when a safe, testable correction is feasible. Conversely, do not conceal missing data, failed tests, unsupported conclusions or external dependencies that prevent a valid result.

Follow the workflow's existing execution, persistence, version-control, branch and permission constraints. Save meaningful progress and evidence at session boundaries. Never assume an external action succeeded without verifying its result.

## 8. End Every Session with a Useful Handoff

At the end of each session, leave a durable, repository-grounded record containing:

1. Work completed and the artifacts changed.
2. Public sources examined and their relevance.
3. Experiments performed and reproducible results.
4. Findings that survived scrutiny, findings that failed and remaining uncertainty.
5. Changes made to the prioritization procedure and the evidence motivating them.
6. The most valuable next task, its rationale, prerequisites and concrete completion criteria.
7. Any unresolved infrastructure, data, execution or validation blockers.

Prepare the next task so that the following agent can act immediately without needing a lengthy narrative transfer. It should inspect the actual repository state and verify the handoff before proceeding.

## 9. Ultimate Objective

Maximize the rate at which the repository produces independently reproducible evidence about potentially profitable, automatable trading strategies.

Prioritize genuine net-of-cost economic edge, robust out-of-sample evidence, practical executability, research efficiency and cumulative knowledge.

Do not optimize for the number of agents, commits, strategies, papers read, backtests or positive results. Optimize for the quality of the discoveries and the reliability of the evidence supporting them.

Continue the research loop: inspect, discover, rank, hypothesize, implement, test, challenge, record, improve and hand off.

Begin now by evaluating the actual repository state, identifying the most important current bottleneck, improving the research-prioritization procedure if justified, and executing the highest-value next task.
