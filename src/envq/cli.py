from __future__ import annotations
import argparse, json
from envq.adapters.controlled_dlm import ControlledDLMAdapter
from envq.adapters.phantom_style import PhantomStyleAdapter


def main() -> None:
    p = argparse.ArgumentParser(prog="envq")
    p.add_argument("baseline", choices=["controlled-dlm", "phantom-style"])
    p.add_argument("--tasks", nargs="+", default=["t0", "t1", "t2"])
    args = p.parse_args()
    if args.baseline == "controlled-dlm":
        tasks = args.tasks if args.tasks != ["t0", "t1", "t2"] else ["authority-conflict", "unknown-missing-evidence"]
        records = ControlledDLMAdapter().run(tasks)
    else:
        records = PhantomStyleAdapter().run(args.tasks)
    for r in records:
        print(json.dumps(r.__dict__, default=lambda x: x.__dict__, sort_keys=True))


if __name__ == "__main__":
    main()
