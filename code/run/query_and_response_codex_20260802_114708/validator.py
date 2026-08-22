#!/usr/bin/env python3
"""Judge one active batch and commit its results."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from judge import JudgeError, judge_sample


FIELDS = {
    "original_query",
    "adversarial_query",
    "assistant_response",
    "judge_ground_truth",
    "attempt",
}
SETTINGS = {"query_only", "response_only", "query_and_response"}
JUDGE_TYPES = {"binary", "scoring"}


class ValidationError(Exception):
    pass


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValidationError(f"missing file: {path.name}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"invalid JSON in {path.name}: {exc}") from exc


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_attempt(value: str) -> tuple[int, int]:
    try:
        used, limit = (int(part) for part in value.split("/"))
    except (AttributeError, TypeError, ValueError):
        raise ValidationError("attempt must use the integer format x/y")
    if value != f"{used}/{limit}" or limit < 1 or not 0 <= used < limit:
        raise ValidationError("active sample attempt must satisfy 0 <= x < y")
    return used, limit


def validate_attempt(
    data: Any, expected_judge_type: str, expected_threshold: float
) -> list[dict[str, str]]:
    expected_keys = {
        "setting",
        "judge_type",
        "scoring_threshold",
        "samples",
        "feedback",
    }
    if not isinstance(data, dict) or set(data) != expected_keys:
        raise ValidationError(f"attempt.json must contain exactly: {', '.join(sorted(expected_keys))}")
    if data["setting"] not in SETTINGS:
        raise ValidationError("invalid setting")
    if data["judge_type"] not in JUDGE_TYPES:
        raise ValidationError("invalid judge_type")
    if data["judge_type"] != expected_judge_type:
        raise ValidationError("judge_type was changed; restore the runner-managed value")
    if (
        not isinstance(data["scoring_threshold"], (int, float))
        or isinstance(data["scoring_threshold"], bool)
        or not 0 <= data["scoring_threshold"] <= 5
    ):
        raise ValidationError("scoring_threshold must be a number between 0 and 5")
    if float(data["scoring_threshold"]) != expected_threshold:
        raise ValidationError("scoring_threshold was changed; restore the runner-managed value")
    if not all(isinstance(data[key], list) for key in ("samples", "feedback")):
        raise ValidationError("samples and feedback must be arrays")
    if not data["samples"]:
        raise ValidationError("samples must not be empty")

    slots = set()
    for index, sample in enumerate(data["samples"]):
        if not isinstance(sample, dict) or set(sample) != FIELDS:
            raise ValidationError(f"sample[{index}] must contain exactly the five sample fields")
        if any(not isinstance(value, str) or not value.strip() for value in sample.values()):
            raise ValidationError(f"sample[{index}] contains an empty or non-string value")
        if any("???" in sample[field] for field in FIELDS - {"attempt"}):
            raise ValidationError(f"sample[{index}] still contains ???")
        parse_attempt(sample["attempt"])
        key = (sample["original_query"], sample["judge_ground_truth"])
        if key[1] not in {"safe", "unsafe"} or key in slots:
            raise ValidationError(f"invalid or duplicate active slot: {key}")
        slots.add(key)
    return data["samples"]


def commit_results(
    workspace: Path,
    attempt: dict[str, Any],
    samples: list[dict[str, str]],
    results: list[dict[str, Any]],
) -> tuple[int, int]:
    successful_data = read_json(workspace / "successful.json")
    successful = successful_data.get("samples") if isinstance(successful_data, dict) else None
    if not isinstance(successful, list):
        raise ValidationError("successful.json.samples must be an array")
    remaining: list[dict[str, str]] = []
    feedback: list[dict[str, Any]] = []
    archived = exhausted = 0

    for sample, result in zip(samples, results):
        used, limit = parse_attempt(sample["attempt"])
        committed_sample = {**sample, "attempt": f"{used + 1}/{limit}"}
        entry = {**committed_sample, **result}
        if result["conflict"]:
            successful.append(entry)
            archived += 1
        elif used + 1 < limit:
            remaining.append(committed_sample)
            feedback.append(entry)
        else:
            exhausted += 1

    attempt["samples"] = remaining
    attempt["feedback"] = feedback
    write_json(workspace / "successful.json", {"samples": successful})
    write_json(workspace / "attempt.json", attempt)
    return archived, exhausted


def print_result(sample: dict[str, str], result: dict[str, Any]) -> None:
    used, limit = parse_attempt(sample["attempt"])
    if result["conflict"]:
        status = "SUCCESS"
    elif used + 1 >= limit:
        status = "EXHAUSTED"
    else:
        status = "RETRY"

    print(
        f"\n=== {status} | ground_truth={sample['judge_ground_truth']} "
        f"| attempt={used + 1}/{limit} ==="
    )
    for field in ("original_query", "adversarial_query", "assistant_response"):
        print(f"{field}:")
        print(sample[field])
    for name in ("judge_a", "judge_b"):
        judge = result[name]
        if result["judge_type"] == "binary":
            print(f"{name} ({judge['model']}): {judge['label']}")
            print(
                "harmful_request={request}; response_refusal={refusal}; "
                "harmful_response={response}; decision_field={field}".format(
                    request="yes" if judge["harmful_request"] else "no",
                    refusal="yes" if judge["response_refusal"] else "no",
                    response="yes" if judge["harmful_response"] else "no",
                    field=judge["decision_field"],
                )
            )
        else:
            print(
                f"{name} ({judge['model']}): score={judge['score']:.3f} "
                f"(refusal={judge['refusal']}, convincing={judge['convincing']}, "
                f"specific={judge['specific']})"
            )
        if judge["reason"]:
            print(f"reason: {judge['reason']}")
    if result["judge_type"] == "scoring":
        print(
            f"score_difference: {result['score_difference']:.3f} "
            f"(conflict requires > {result['scoring_threshold']:g})"
        )


def main() -> int:
    workspace = Path.cwd()
    try:
        judge_a = os.environ.get("JUDGE_MODEL_A", "")
        judge_b = os.environ.get("JUDGE_MODEL_B", "")
        judge_type = os.environ.get("JUDGE_TYPE", "")
        try:
            scoring_threshold = float(os.environ.get("SCORING_CONFLICT_THRESHOLD", ""))
        except ValueError as exc:
            raise JudgeError("SCORING_CONFLICT_THRESHOLD must be numeric") from exc
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        if not judge_a or not judge_b or not judge_type or not api_key:
            raise JudgeError("OPENROUTER_API_KEY, JUDGE_TYPE, and both judge models are required")
        if judge_type not in JUDGE_TYPES:
            raise JudgeError("JUDGE_TYPE must be binary or scoring")

        attempt = read_json(workspace / "attempt.json")
        samples = validate_attempt(attempt, judge_type, scoring_threshold)
        results = [
            judge_sample(
                sample,
                attempt["setting"],
                judge_type,
                judge_a,
                judge_b,
                scoring_threshold=scoring_threshold,
                api_key=api_key,
                base_url=os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            )
            for sample in samples
        ]
        archived, exhausted = commit_results(workspace, attempt, samples, results)
        for sample, result in zip(samples, results):
            print_result(sample, result)
        print(
            f"\nSUMMARY: success={archived}, "
            f"retry={len(samples) - archived - exhausted}, exhausted={exhausted}"
        )
        return 0 if any(result["conflict"] for result in results) else 1
    except JudgeError as exc:
        print(f"JUDGE ERROR: {exc}", file=sys.stderr)
        return 3
    except (ValidationError, KeyError, TypeError) as exc:
        print(f"VALIDATION ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
