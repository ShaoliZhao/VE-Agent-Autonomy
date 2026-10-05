# Rules translated into system requirements

## The configuration lock

The lock must capture the initial prompts, harness revision, model string, tool permissions, data hashes, environment, evaluation split, budget and stopping rule. Changing any of these ends the run. Restarting an interrupted process with the same lock is allowed; resuming after changing permissions is a new run.

## Human boundary

Before lock: prototype freely, inspect outputs, rewrite prompts and improve the harness. After lock: do not read intermediate scores and tell the agent what to try next; do not select among its checkpoints; do not edit its prediction. A human may choose among completed locked runs.

## Evidence

Every submission needs a trajectory plus at least one other evidence kind before scoring. Prize eligibility requires trajectory, prompts and harness. Store framework and exact model string. Evidence must come from the producing run, remain unedited, and fit the 200 MB per-file and 600 MB per-team limits.

## Design consequence

The agent needs tools to inspect data, edit code, launch bounded jobs, read local pseudo-holdout results, compare candidates, recover from failures and finalize one output. The harness must make the final choice mechanically traceable.
