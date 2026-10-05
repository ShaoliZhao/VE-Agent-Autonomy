# VEC Agent Autonomy Lab

An executable reference environment for testing whether an agent can complete a Virtual Embryo-style scientific modeling run without post-lock human steering.

The repository covers configuration locking, constrained execution, autonomous candidate search, budget accounting, failure recovery, final selection and evidence-compatible logs.

## Included components

- `vec_harness`: hashes the prompt, inputs, tools and run configuration; executes one locked controller; records events and the final artifact digest.
- `vec_search`: append-only, hash-chained candidate ledger with budget checks and deterministic successive-halving promotion.
- `vec_sandbox`: local resource governor and environment allowlist, plus a Docker isolation profile.
- `docs/playbook`: the rules-to-system architecture, iteration protocol, stack guide and agent-training ladder.
- `examples`: synthetic demonstrations that contain no competition data.

## What the lab evaluates

A complete benchmark scenario should test whether the agent can inspect declared inputs, create a legal pseudo-holdout, run multiple candidates, recover from a failed candidate, remain within budget, select one final candidate and write the expected artifact. Policy tests can inject a changed input, missing permission, timeout, invalid metric, overspent budget or attempted configuration mutation.

The lab scores executable outcomes and invariant violations. It does not use an LLM judge to certify competition eligibility and does not replace the organisers' private audit.

## Quick start

```bash
python3 -m unittest discover -s tests/harness -v
python3 -m unittest discover -s tests/search -v
python3 -m unittest discover -s tests/sandbox -v
python3 examples/harness/make_demo.py
python3 -m vec_harness.cli lock examples/harness/demo-config.json demo-run
python3 -m vec_harness.cli run demo-run
```

For an official run, place the locked controller inside a container or managed sandbox, mount declared inputs read-only, mount a separate output directory read-write and disable network access unless the locked configuration explicitly requires it.

## Agent improvement ladder

Start with prompt, tools, validation and recovery behavior. Once many automatically scored trajectories exist, train on successful state/action/result sequences with SFT or PEFT. Add preference training only when pairwise decisions are reliable. Use online RL or GRPO only when environments reset cleanly and rewards are deterministic enough to resist exploitation.

## Competition boundary

Humans may develop and test the system before the lock. After a submitted run is locked, the agent must evaluate intermediate results, select its own final candidate and write the prediction. Humans may choose among separately completed locked runs. Always confirm the current official rules.

MIT licensed. No challenge data or private trajectories are included.
