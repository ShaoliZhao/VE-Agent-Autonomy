# Model and framework choices

## Agent frameworks

`smolagents` is a strong small starting point: its core abstractions are easy to audit, it supports code and tool-calling agents, multiple model providers and sandbox backends. OpenHands provides a fuller software-agent SDK and sandbox lifecycle. SWE-agent is useful for understanding agent-computer interfaces and trajectory-first evaluation. LangGraph is appropriate when an explicit persistent state machine matters more than a compact code-agent loop.

## Model serving

Use a hosted model first unless privacy or cost requires local inference. For local Hugging Face models, pin model revision, tokenizer revision, chat template, quantization and generation parameters. Use Accelerate for hardware portability and distributed execution; vLLM is useful when repeated agent rollouts dominate cost.

## Scientific training

The embryo model and the coding agent are separate systems. Train scientific models with ordinary PyTorch/Transformers/Accelerate tooling. Use PEFT/LoRA when adapting a large pretrained biological or language model under limited hardware. Do not fine-tune the coding agent merely because PEFT makes it possible.

## Observability

Use append-only local JSONL as the source of truth. OpenTelemetry-compatible traces may mirror it for visualization, latency and token accounting, but an external dashboard should not be the only evidence copy.
