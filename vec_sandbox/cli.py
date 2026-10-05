import argparse
import json

from .core import load_policy, run


def main() -> None:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="action", required=True)
    validate = sub.add_parser("validate"); validate.add_argument("policy")
    execute = sub.add_parser("run"); execute.add_argument("policy"); execute.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(); policy = load_policy(args.policy)
    if args.action == "validate": print("policy valid")
    else:
        command = args.command[1:] if args.command[:1] == ["--"] else args.command
        if not command: raise SystemExit("command required")
        result = run(policy, command); print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["returncode"] == 0 else 1)


if __name__ == "__main__": main()
