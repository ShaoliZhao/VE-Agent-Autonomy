# When to fine-tune the agent

Fine-tuning is justified only after the harness produces many completed, automatically scored trajectories and repeated failure modes are visible.

Start with prompt and tool improvements. Next, use successful trajectories for supervised fine-tuning of planning or tool-call formats. PEFT keeps this adaptation small. Preference optimization can learn pairwise choices when candidate comparisons are reliable. GRPO becomes reasonable when each rollout runs in an isolated stateful environment and receives a deterministic reward composed from validity, local scientific metrics, cost and completion.

Keep training tasks separate from final competition data. Split trajectory problems by project or pseudo-stage so the agent cannot memorize one evaluator. Hold out complete tasks for evaluation. Reward hacking is likely if the agent can edit the evaluator, overwrite prior metrics or choose its own reward inputs.

TRL now supports tool-using agent training through per-rollout environments with `reset` and `get_reward`. Treat this as an advanced option. A noisy pseudo-holdout reward can train the agent to exploit the holdout rather than improve hidden-stage generalization.
