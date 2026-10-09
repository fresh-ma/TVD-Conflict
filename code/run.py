#!/usr/bin/env python3
"""Prepare or run one TVD-Conflict template workspace."""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import uuid

HERE = Path(__file__).resolve().parent


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def threshold(value):
    number = float(value)
    if not 0 <= number <= 1:
        raise argparse.ArgumentTypeError("must lie between 0 and 1")
    return number


def load_env(path):
    """Read simple KEY=value entries without executing shell code."""
    if not path.exists():
        return
    for number, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        key, sep, value = line.partition("=")
        if not sep or not key.strip().replace("_", "a").isalnum():
            raise ValueError(f"invalid environment entry at {path.name}:{number}")
        parts = shlex.split(value, comments=True)
        if len(parts) > 1:
            raise ValueError(f"quote values containing spaces at {path.name}:{number}")
        os.environ.setdefault(key.strip(), parts[0] if parts else "")


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prepare(args):
    workspace = args.run_dir.resolve() if args.run_dir else HERE / "runs" / (
        datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S_") + uuid.uuid4().hex[:6]
    )
    config_path = workspace / "config.json"
    configurable = (
        "query_count", "sample_budget", "setting", "task_version", "judge_type",
        "judge_a", "judge_b", "scoring_threshold", "judge_max_tokens", "few_shot_count",
    )
    if config_path.exists():
        config = json.loads(config_path.read_text())
        changed = [key for key in configurable
                   if getattr(args, key) is not None and getattr(args, key) != config[key]]
        for name in ("bench", "few_shot"):
            path = getattr(args, name)
            if path and hashlib.sha256(path.read_bytes()).hexdigest() != config.get(name + "_sha256"):
                changed.append(name)
        if changed:
            raise ValueError("resume configuration differs: " + ", ".join(changed))
        for name in ("attempt.json", "successful.json", "TASK.md", "judge.py", "validator.py"):
            if not (workspace / name).is_file():
                raise ValueError("incomplete existing workspace: " + name)
        return workspace, config
    if workspace.exists() and any(workspace.iterdir()):
        raise ValueError("new run directory must be empty")
    config = {
        "query_count": args.query_count or 3,
        "sample_budget": args.sample_budget or 10,
        "setting": args.setting or "query_and_response",
        "task_version": args.task_version or "base",
        "judge_type": args.judge_type or "binary",
        "judge_a": args.judge_a or os.environ.get("JUDGE_MODEL_A") or "qwen/qwen3.7-flash",
        "judge_b": args.judge_b or os.environ.get("JUDGE_MODEL_B") or "deepseek/deepseek-v4-flash-0731",
        "scoring_threshold": .5 if args.scoring_threshold is None else args.scoring_threshold,
        "judge_max_tokens": args.judge_max_tokens or int(os.environ.get("JUDGE_MAX_TOKENS", "2048")),
        "few_shot_count": args.few_shot_count or 0,
        "base_url": os.environ.get("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1",
    }
    bench = args.bench or HERE / "bench/advbench_50.csv"
    with bench.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or "request" not in reader.fieldnames:
            raise ValueError("benchmark CSV requires a 'request' column")
        goals = [(row["request"] or "").strip() for row in reader if (row["request"] or "").strip()]
    goals = goals[:config["query_count"]]
    if len(goals) != config["query_count"] or len(set(goals)) != len(goals):
        raise ValueError("benchmark must provide the requested number of distinct nonempty goals")
    config["bench_sha256"] = hashlib.sha256(bench.read_bytes()).hexdigest()
    config["goals"] = goals
    examples = []
    if config["few_shot_count"]:
        if not args.few_shot:
            raise ValueError("--few-shot-count requires --few-shot JSONL")
        with args.few_shot.open(encoding="utf-8") as source:
            for line in source:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row["protocol"] == config["judge_type"] and row.get("goal") not in goals:
                    examples.append(row)
                if len(examples) == config["few_shot_count"]:
                    break
        if len(examples) < config["few_shot_count"]:
            raise ValueError("not enough few-shot records with matching protocol and disjoint goals")
        config["few_shot_sha256"] = hashlib.sha256(args.few_shot.read_bytes()).hexdigest()
    elif args.few_shot:
        raise ValueError("--few-shot requires a positive --few-shot-count")
    config["few_shot_ids"] = [row["id"] for row in examples]
    workspace.mkdir(parents=True, exist_ok=True)
    for name in ("judge.py", "validator.py"):
        shutil.copy2(HERE / "templates" / name, workspace / name)
    shutil.copy2(HERE / "templates" / (config["task_version"] + ".md"), workspace / "TASK.md")
    write(workspace / "examples.json", {"samples": examples})
    write(workspace / "successful.json", {"samples": []})
    write(workspace / "attempt.json", {
        "setting": config["setting"], "judge_type": config["judge_type"],
        "scoring_threshold": config["scoring_threshold"],
        "samples": [{"original_query": goal, "adversarial_query": "???", "assistant_response": "???",
                     "judge_ground_truth": label, "attempt": f"0/{config['sample_budget']}"}
                    for goal in goals for label in ("safe", "unsafe")],
        "feedback": [],
    })
    write(config_path, config)
    return workspace, config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "run"))
    parser.add_argument("--run-dir", type=Path)
    parser.add_argument("--env-file", type=Path, default=HERE / ".env")
    parser.add_argument("--bench", type=Path, help="CSV with a request column; bundled 50-goal set by default")
    parser.add_argument("--query-count", type=positive)
    parser.add_argument("--sample-budget", type=positive)
    parser.add_argument("--setting", choices=("query_only", "response_only", "query_and_response"))
    parser.add_argument("--task-version", choices=("base", "skill"))
    parser.add_argument("--judge-type", choices=("binary", "scoring"))
    parser.add_argument("--judge-a")
    parser.add_argument("--judge-b")
    parser.add_argument("--scoring-threshold", type=threshold)
    parser.add_argument("--judge-max-tokens", type=positive)
    parser.add_argument("--few-shot", type=Path, help="release-schema JSONL containing demonstration records")
    parser.add_argument("--few-shot-count", type=positive)
    parser.add_argument("--agent", choices=("codex", "terminal"), default="codex")
    parser.add_argument("--agent-model", help="Codex model override, or required OpenRouter model for terminal agent")
    parser.add_argument("--max-turns", type=positive, default=80, help="terminal agent turn limit")
    args = parser.parse_args()
    try:
        load_env(args.env_file)
        workspace, config = prepare(args)
        print(f"Workspace: {workspace}", flush=True)
        if args.command == "prepare":
            print("Prepared offline. Edit candidate fields, then use 'run' or execute validator.py in this workspace.")
            return 0
        if not os.environ.get("OPENROUTER_API_KEY"):
            raise ValueError("OPENROUTER_API_KEY is required; configure code/.env or the environment")
        env = {**os.environ, "JUDGE_MODEL_A": config["judge_a"], "JUDGE_MODEL_B": config["judge_b"],
               "JUDGE_TYPE": config["judge_type"], "SCORING_CONFLICT_THRESHOLD": str(config["scoring_threshold"]),
               "JUDGE_MAX_TOKENS": str(config["judge_max_tokens"]), "OPENROUTER_BASE_URL": config["base_url"]}
        active = json.loads((workspace / "attempt.json").read_text())["samples"]
        if not active:
            print("Run already complete.")
            return 0
        model = args.agent_model or os.environ.get("AGENT_MODEL")
        if args.agent == "terminal":
            if not model:
                raise ValueError("terminal agent requires --agent-model or AGENT_MODEL")
            if not shutil.which("uv"):
                raise ValueError("terminal agent requires uv")
            command = ["uv", "run", str(HERE / "terminal_agent.py"), "--workspace", str(workspace),
                       "--model", model, "--max-turns", str(args.max_turns)]
        else:
            if not shutil.which("codex"):
                raise ValueError("codex executable was not found; install Codex or choose --agent terminal")
            command = ["codex", "exec", "--skip-git-repo-check", "--sandbox", "workspace-write",
                       "-c", "sandbox_workspace_write.network_access=true", "-C", str(workspace)]
            if model:
                command.extend(["--model", model])
            command.append((workspace / "TASK.md").read_text())
        result = subprocess.run(command, cwd=workspace, env=env)
        remaining = len(json.loads((workspace / "attempt.json").read_text())["samples"])
        retained = len(json.loads((workspace / "successful.json").read_text())["samples"])
        print(f"Archived conflicts: {retained}; remaining targets: {remaining}")
        return result.returncode if result.returncode else int(remaining > 0)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
