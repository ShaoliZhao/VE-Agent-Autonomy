import argparse
from .core import lock, run, verify

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd", required=True)
    a=sub.add_parser("lock"); a.add_argument("config"); a.add_argument("run_dir")
    a=sub.add_parser("run"); a.add_argument("run_dir")
    a=sub.add_parser("verify"); a.add_argument("run_dir"); a.add_argument("--require-final", action="store_true")
    args=p.parse_args()
    if args.cmd=="lock": lock(args.config,args.run_dir); print("locked")
    elif args.cmd=="run": print(run(args.run_dir))
    else:
        errors=verify(args.run_dir,args.require_final); print("verified" if not errors else "\n".join(errors)); raise SystemExit(bool(errors))

if __name__=="__main__": main()
