#!/usr/bin/env python3
"""Summarize budget-matched TVD-Conflict runs for the paper table."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "run"
        / "benchmark_240_me"
        / "jobs",
    )
    parser.add_argument("--budget", type=int, default=10)
    parser.add_argument("--target", choices=("safe", "unsafe"), default="unsafe")
    args = parser.parse_args()

    print("run,goals,conflicts,conflict_at_budget,evaluations_per_conflict")
    for run in sorted(args.root.glob("*/*/*")):
        if not run.is_dir():
            continue

        successes: dict[str, int] = {}
        goals: set[str] = set()
        for path in run.glob("shard_*/successful.json"):
            rows = json.loads(path.read_text(encoding="utf-8")).get("samples", [])
            for row in rows:
                goal = row["original_query"]
                goals.add(goal)
                if row["judge_ground_truth"] != args.target:
                    continue
                attempt = int(row["attempt"].split("/", 1)[0])
                successes[goal] = min(attempt, successes.get(goal, attempt))

        # Successful files omit exhausted goals, so recover the full goal set
        # from per-attempt logs.
        for path in run.glob("shard_*/logs/*"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            rows = payload if isinstance(payload, list) else [payload]
            for row in rows:
                sample = row.get("sample", row)
                goal = sample.get("original_query")
                if goal:
                    goals.add(goal)

        if not goals:
            continue
        found = {goal: attempt for goal, attempt in successes.items() if attempt <= args.budget}
        total_evaluations = sum(found.values()) + args.budget * (len(goals) - len(found))
        epc = total_evaluations / len(found) if found else float("inf")
        print(
            f"{run.relative_to(args.root)},{len(goals)},{len(found)},"
            f"{100 * len(found) / len(goals):.1f},{epc:.2f}"
        )


if __name__ == "__main__":
    main()
