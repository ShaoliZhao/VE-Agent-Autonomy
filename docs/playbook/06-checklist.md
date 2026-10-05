# Launch and audit checklist

- Freeze prompt, harness commit, model string, tool policy, budget and all input hashes.
- Confirm the agent can finish a synthetic end-to-end rehearsal.
- Make competition data read-only and final output a dedicated directory.
- Disable unneeded network access and secrets.
- Predeclare pseudo-holdouts, scorer version, candidate budget and stop rule.
- Log model calls, tool calls, commands, observations, metrics and artifact hashes.
- Ensure the agent, not a person, selects and writes the final prediction.
- Reproduce the winner from its candidate record before finalization.
- Package the unedited trajectory, every prompt and exact harness revision.
- Record framework and exact model string in the portal.
