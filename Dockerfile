FROM python:3.11-slim
WORKDIR /workspace
RUN useradd --create-home --uid 10001 agent
COPY --chown=agent:agent . /workspace
USER agent
CMD ["python", "examples/sandbox/worker.py"]
