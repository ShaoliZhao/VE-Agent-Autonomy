from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import Ledger, promote


def metric(values: list[str]) -> dict[str, float]:
    return {key: float(value) for key, value in (item.split("=", 1) for item in values)}


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("run")
    init.add_argument("--budget", type=float, required=True)
    record = commands.add_parser("record")
    record.add_argument("run"); record.add_argument("--candidate", required=True); record.add_argument("--tier", required=True)
    record.add_argument("--metric", action="append", default=[]); record.add_argument("--cost", type=float, required=True)
    promotion = commands.add_parser("promote")
    promotion.add_argument("run"); promotion.add_argument("--tier", required=True); promotion.add_argument("--keep", type=float, required=True)
    verify = commands.add_parser("verify"); verify.add_argument("run")
    args = parser.parse_args(); root = Path(args.run); ledger = Ledger(root / "ledger.jsonl")
    if args.command == "init":
        root.mkdir(parents=True, exist_ok=False)
        (root / "config.json").write_text(json.dumps({"budget": args.budget, "weights": {}}, indent=2) + "\n")
        ledger.append("init", {"budget": args.budget})
    elif args.command == "record":
        config = json.loads((root / "config.json").read_text())
        if ledger.spent() + args.cost > config["budget"]:
            raise SystemExit("budget exceeded")
        ledger.append("result", {"candidate_id": args.candidate, "tier": args.tier, "metrics": metric(args.metric), "cost": args.cost})
    elif args.command == "promote":
        config = json.loads((root / "config.json").read_text())
        rows = [e["payload"] for e in ledger.events() if e["kind"] == "result" and e["payload"]["tier"] == args.tier]
        weights = config["weights"] or ({key: 1.0 for key in rows[0]["metrics"]} if rows else {})
        selected = promote(rows, weights, args.keep)
        ledger.append("promotion", {"tier": args.tier, "selected": selected}); print("\n".join(selected))
    else:
        if not ledger.verify(): raise SystemExit("invalid ledger")
        print("ledger valid")


if __name__ == "__main__": main()
