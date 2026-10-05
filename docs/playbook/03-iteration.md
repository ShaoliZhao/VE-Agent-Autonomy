# Autonomous experiment loop

1. Inspect locked inputs and establish floor baselines.
2. Form a falsifiable hypothesis, expected metric effect and failure condition.
3. Create one candidate that changes a small number of factors.
4. Run cheap smoke validation, then one pseudo-holdout seed.
5. Promote only viable candidates to multiple seeds or expensive training.
6. Compare against the incumbent with uncertainty and per-metric deltas.
7. Write a reflection containing evidence, decision and next hypothesis.
8. Stop at budget exhaustion or when improvements fall below the predeclared threshold.
9. Rebuild the selected candidate from its recorded config and write the final prediction.

Use successive halving: many cheap candidates, fewer full runs. Reserve a fixed fraction of budget for reproducing the winner. Penalize invalid output, missing metrics, runtime overruns and high seed variance.

The agent should be allowed to abandon a hypothesis. It should never rewrite old metrics or silently replace an artifact under the same candidate ID.
