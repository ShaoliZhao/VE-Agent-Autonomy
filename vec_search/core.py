from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def aggregate(metrics: dict[str, float], weights: dict[str, float]) -> float:
    if not weights or any(value < 0 for value in weights.values()):
        raise ValueError("weights must be non-negative and non-empty")
    missing = set(weights) - set(metrics)
    if missing:
        raise ValueError(f"missing metrics: {sorted(missing)}")
    denominator = sum(weights.values())
    if denominator <= 0:
        raise ValueError("weights must sum to a positive value")
    return sum(float(metrics[key]) * weight for key, weight in weights.items()) / denominator


def promote(records: Iterable[dict[str, Any]], weights: dict[str, float], keep: float) -> list[str]:
    rows = list(records)
    if not 0 < keep <= 1:
        raise ValueError("keep must be in (0, 1]")
    if not rows:
        return []
    ranked = sorted(rows, key=lambda row: (-aggregate(row["metrics"], weights), row["candidate_id"]))
    count = max(1, int(len(ranked) * keep))
    return [row["candidate_id"] for row in ranked[:count]]


class Ledger:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def events(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text().splitlines() if line.strip()]

    def append(self, kind: str, payload: dict[str, Any]) -> dict[str, Any]:
        previous = self.events()[-1]["hash"] if self.events() else "GENESIS"
        body = {"index": len(self.events()), "kind": kind, "payload": payload, "previous": previous}
        event = {**body, "hash": hashlib.sha256(_canonical(body)).hexdigest()}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
        return event

    def verify(self) -> bool:
        previous = "GENESIS"
        for index, event in enumerate(self.events()):
            body = {key: event[key] for key in ("index", "kind", "payload", "previous")}
            expected = hashlib.sha256(_canonical(body)).hexdigest()
            if event["index"] != index or event["previous"] != previous or event["hash"] != expected:
                return False
            previous = event["hash"]
        return True

    def spent(self) -> float:
        return sum(float(e["payload"].get("cost", 0)) for e in self.events() if e["kind"] == "result")
