from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any


REQUIRED = {"work_dir", "output_dir", "wall_seconds", "cpu_seconds", "memory_mb", "file_mb", "max_processes", "network", "environment_allowlist"}


def load_policy(path: str | Path) -> dict[str, Any]:
    policy = json.loads(Path(path).read_text())
    missing = REQUIRED - set(policy)
    if missing: raise ValueError(f"missing policy fields: {sorted(missing)}")
    if policy["network"] not in {"none", "declared"}: raise ValueError("network must be none or declared")
    for key in ("wall_seconds", "cpu_seconds", "memory_mb", "file_mb", "max_processes"):
        if int(policy[key]) <= 0: raise ValueError(f"{key} must be positive")
    work = Path(policy["work_dir"]).expanduser().resolve(); output = Path(policy["output_dir"]).expanduser().resolve()
    if work == output: raise ValueError("output_dir must differ from work_dir")
    policy["work_dir"], policy["output_dir"] = str(work), str(output)
    return policy


def filtered_environment(allowlist: list[str]) -> dict[str, str]:
    safe = {key: os.environ[key] for key in allowlist if key in os.environ}
    safe.setdefault("PATH", os.environ.get("PATH", "/usr/bin:/bin"))
    return safe


def _limits(policy: dict[str, Any]):
    def apply() -> None:
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_CPU, (int(policy["cpu_seconds"]), int(policy["cpu_seconds"])))
            memory = int(policy["memory_mb"]) * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
            size = int(policy["file_mb"]) * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_FSIZE, (size, size))
            resource.setrlimit(resource.RLIMIT_NPROC, (int(policy["max_processes"]), int(policy["max_processes"])))
        except (ImportError, ValueError, OSError):
            pass
    return apply


def run(policy: dict[str, Any], command: list[str]) -> dict[str, Any]:
    work = Path(policy["work_dir"]); output = Path(policy["output_dir"])
    if not work.is_dir(): raise ValueError("work_dir does not exist")
    output.mkdir(parents=True, exist_ok=True)
    started = time.time()
    try:
        completed = subprocess.run(command, cwd=work, env=filtered_environment(policy["environment_allowlist"]),
                                   capture_output=True, text=True, timeout=int(policy["wall_seconds"]),
                                   preexec_fn=_limits(policy) if os.name == "posix" else None, check=False)
        result = {"status": "completed", "returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
    except subprocess.TimeoutExpired as exc:
        result = {"status": "timeout", "returncode": None, "stdout": exc.stdout or "", "stderr": exc.stderr or ""}
    result["elapsed_seconds"] = round(time.time() - started, 6)
    (output / "execution.json").write_text(json.dumps(result, indent=2) + "\n")
    return result
