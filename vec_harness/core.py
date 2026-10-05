import hashlib, json, os, subprocess, time
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()


def lock(config_path, run_dir):
    config_path, run_dir = Path(config_path).resolve(), Path(run_dir).resolve(); run_dir.mkdir(parents=True, exist_ok=False)
    config = json.loads(config_path.read_text())
    required = {"framework", "model", "command", "prompts", "harness_files", "inputs", "budget", "final_artifact"}
    if not required.issubset(config): raise ValueError(f"missing keys: {sorted(required-set(config))}")
    paths = config["prompts"] + config["harness_files"] + config["inputs"]
    inventory = {str(Path(p).resolve()): digest(Path(p).resolve()) for p in paths}
    payload = {"schema": 1, "created_at": time.time(), "config": config, "config_source_sha256": digest(config_path), "inventory": inventory}
    (run_dir / "lock.json").write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    (run_dir / "events.jsonl").write_text(json.dumps({"event":"locked","time":time.time()})+"\n")
    return payload


def verify(run_dir, require_final=False):
    run_dir = Path(run_dir); payload = json.loads((run_dir / "lock.json").read_text()); errors=[]
    for path, expected in payload["inventory"].items():
        if not Path(path).is_file() or digest(path) != expected: errors.append(f"changed or missing: {path}")
    final = Path(payload["config"]["final_artifact"])
    if require_final and not final.is_file(): errors.append(f"missing final artifact: {final}")
    return errors


def run(run_dir):
    run_dir = Path(run_dir).resolve(); errors = verify(run_dir)
    if errors: raise RuntimeError("; ".join(errors))
    payload = json.loads((run_dir/"lock.json").read_text()); config=payload["config"]
    env = {"PATH": os.environ.get("PATH", ""), "VEC_RUN_DIR": str(run_dir), "VEC_BUDGET_JSON": json.dumps(config["budget"])}
    started=time.time()
    with (run_dir/"stdout.log").open("a") as out, (run_dir/"stderr.log").open("a") as err:
        result=subprocess.run(config["command"], stdout=out, stderr=err, env=env, text=True, timeout=config["budget"].get("wall_seconds"))
    final=Path(config["final_artifact"]); event={"event":"completed","time":time.time(),"seconds":time.time()-started,"returncode":result.returncode,"final_sha256":digest(final) if final.is_file() else None}
    with (run_dir/"events.jsonl").open("a") as f: f.write(json.dumps(event)+"\n")
    return event
