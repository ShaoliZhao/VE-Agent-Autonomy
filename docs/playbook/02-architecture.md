# End-to-end architecture

```text
immutable inputs + prompt + tool policy + budget
                       |
                configuration lock
                       |
              autonomous manager agent
         / propose / run / evaluate / reflect \
        candidate registry -- local evaluator
                       |
             agent-selected final candidate
                       |
       prediction + trajectory + prompts + harness
```

Use separate directories for read-only data, mutable source, per-candidate artifacts and final output. Give the agent stable tools instead of unconstrained shell access where possible: inspect dataset schema, create candidate, launch training, evaluate pseudo-holdout, compare candidates, read failure logs, finalize prediction.

The evaluator should expose task-group metrics and seed uncertainty, not a single opaque reward. The selection policy may scalarize them, but the trace should retain the components. Never derive prediction content by inverting leaderboard scores.

Every candidate needs parent ID, code/config hash, seed, resource use, status, metrics and artifact hash. This lineage is the scientific memory of the agent.
