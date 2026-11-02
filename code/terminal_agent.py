#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai>=1.0",
#   "openai-agents>=0.2.0",
# ]
# ///
"""Minimal OpenRouter agent whose only tool is a workspace-scoped terminal."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

from redact_secrets import redact_secrets

from agents import Agent, ModelSettings, OpenAIChatCompletionsModel, Runner, function_tool
from agents import set_tracing_disabled
from openai import AsyncOpenAI


WORKSPACE: Path | None = None


def _run(command: str) -> str:
    if WORKSPACE is None:
        return "Error: workspace is not configured"
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=180,
        )
    except subprocess.TimeoutExpired:
        return "Error: command timed out after 180 seconds"
    output = redact_secrets(result.stdout + result.stderr)
    # Enough context for judge feedback without allowing one command to consume
    # the entire model context window.
    return output[-12000:] if output else "(no output)"


@function_tool
def terminal(command: str) -> str:
    """Run one shell command in the task workspace and return stdout and stderr."""
    print(redact_secrets(f"$ {command}"), flush=True)
    output = _run(command)
    if output != "(no output)":
        print(output[-2000:], flush=True)
    return output


def save_log(workspace: Path, result: object) -> None:
    history = result.to_input_list() if hasattr(result, "to_input_list") else {
        "final_output": getattr(result, "final_output", None)
    }
    (workspace / "terminal_agent_log.json").write_text(
        redact_secrets(json.dumps(history, ensure_ascii=False, indent=2, default=str)) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--max-turns", type=int, default=80)
    args = parser.parse_args()

    global WORKSPACE
    WORKSPACE = args.workspace.resolve()
    if not (WORKSPACE / "TASK.md").is_file():
        raise SystemExit(f"TASK.md not found in {WORKSPACE}")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is required")

    set_tracing_disabled(True)
    model = OpenAIChatCompletionsModel(
        model=args.model,
        openai_client=AsyncOpenAI(
            api_key=api_key,
            base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        ),
    )
    agent = Agent(
        name="TVD Conflict Terminal Agent",
        model=model,
        instructions=(
            "You are an autonomous experiment agent with exactly one tool: terminal. "
            "Work only inside the supplied workspace. Start by reading TASK.md and follow "
            "its workflow and file restrictions exactly. Use terminal commands to inspect "
            "and edit the permitted JSON file and to run validator.py. Continue until "
            "attempt.json has no active samples or all budgets are exhausted. Never ask "
            "questions, install packages, edit judge.py or validator.py, or launch multiple "
            "validator processes concurrently."
        ),
        tools=[terminal],
        model_settings=ModelSettings(temperature=0.0),
    )
    prompt = (
        f"Workspace: {WORKSPACE}\n"
        "Read TASK.md with the terminal, execute the complete evaluation loop, and finish "
        "only when no active samples remain."
    )
    result = Runner.run_sync(agent, prompt, max_turns=args.max_turns)
    save_log(WORKSPACE, result)
    if getattr(result, "final_output", None):
        print(redact_secrets(str(result.final_output)))


if __name__ == "__main__":
    main()
