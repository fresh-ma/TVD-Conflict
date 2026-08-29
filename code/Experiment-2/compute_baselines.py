#!/usr/bin/env python3
"""Compute the Random-Pick and Prior-Pick Conflict@10 baselines."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "Experiment-1" / "judge_batch_output"
SAMPLES = ROOT / "samples.json"
JUDGMENTS = ROOT / "judgments.json"
BUDGET = 10

MODELS = {
    "GPT": "openai/gpt-oss-120b",
    "Qwen": "qwen/qwen3.7-flash",
    "DeepSeek": "deepseek/deepseek-v4-flash",
}
PAIRS = (
    ("GPT", "DeepSeek"),
    ("GPT", "Qwen"),
    ("DeepSeek", "Qwen"),
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_conflict(left: dict, right: dict, judge_type: str) -> bool:
    if judge_type == "binary":
        return bool(left["harmful_response"]) != bool(right["harmful_response"])
    return abs(float(left["score"]) - float(right["score"])) > 0.5


def main() -> None:
    samples = load_json(SAMPLES)
    judgments = load_json(JUDGMENTS)

    metadata = {
        row["sample_id"]: (
            row["result_index"],
            (row["attack"], row["victim"]),
        )
        for row in samples
    }
    sample_by_slot = {slot: sample_id for sample_id, slot in metadata.items()}
    configurations = sorted({slot[1] for slot in metadata.values()})
    goal_count = len({slot[0] for slot in metadata.values()})

    parsed = {
        (row["sample_id"], row["judge_type"], row["judge_model"]): row["parsed"]
        for row in judgments
        if row["judge_model"] in MODELS.values()
    }

    output = []
    for left_name, right_name in PAIRS:
        left_model, right_model = MODELS[left_name], MODELS[right_name]
        row = {"judge_pair": f"{left_name} / {right_name}"}

        for judge_type in ("binary", "scoring"):
            outcomes: dict[tuple[int, tuple[str, str]], bool | None] = {}
            for goal in range(goal_count):
                for configuration in configurations:
                    sample_id = sample_by_slot[(goal, configuration)]
                    left = parsed.get((sample_id, judge_type, left_model))
                    right = parsed.get((sample_id, judge_type, right_model))
                    outcomes[(goal, configuration)] = (
                        None if left is None or right is None
                        else is_conflict(left, right, judge_type)
                    )

            # Random-Pick draws ten valid candidates without replacement.  Its
            # expected success probability has a closed-form hypergeometric
            # expression, so no Monte Carlo sampling is needed.
            random_probabilities = []
            random_evaluations = []
            for goal in range(goal_count):
                valid = [
                    outcomes[(goal, configuration)]
                    for configuration in configurations
                    if outcomes[(goal, configuration)] is not None
                ]
                population = len(valid)
                conflicts = sum(valid)
                draws = min(BUDGET, population)
                probability = 0.0
                if conflicts and draws:
                    probability = 1 - (
                        math.comb(population - conflicts, draws)
                        / math.comb(population, draws)
                    )
                random_probabilities.append(probability)
                # E[min(T, draws)], where T is the position of the first
                # conflict in a uniformly shuffled population.
                expected_evaluations = 0.0
                for prefix in range(draws):
                    if population - conflicts >= prefix:
                        expected_evaluations += (
                            math.comb(population - conflicts, prefix)
                            / math.comb(population, prefix)
                        )
                random_evaluations.append(expected_evaluations)

            # Prior-Pick ranks all attack-victim configurations by their
            # observed conflict rate on the complete corpus.  For each goal,
            # the ten highest-ranked configurations with valid judgments are
            # evaluated.  This is intentionally an in-sample static prior.
            prior_rates = {}
            for configuration in configurations:
                valid = [
                    outcomes[(goal, configuration)]
                    for goal in range(goal_count)
                    if outcomes[(goal, configuration)] is not None
                ]
                prior_rates[configuration] = sum(valid) / len(valid)
            ranked = sorted(
                configurations,
                key=lambda configuration: (-prior_rates[configuration], configuration),
            )
            prior_successes = []
            for goal in range(goal_count):
                selected = [
                    configuration
                    for configuration in ranked
                    if outcomes[(goal, configuration)] is not None
                ][:BUDGET]
                prior_successes.append(
                    any(outcomes[(goal, configuration)] for configuration in selected)
                )

            suffix = "binary" if judge_type == "binary" else "score"
            row[f"random_{suffix}"] = 100 * sum(random_probabilities) / goal_count
            row[f"random_{suffix}_epc"] = (
                sum(random_evaluations) / sum(random_probabilities)
            )
            row[f"prior_{suffix}"] = 100 * sum(prior_successes) / goal_count

        output.append(row)

    columns = (
        "judge_pair", "random_binary", "random_binary_epc",
        "random_score", "random_score_epc",
        "prior_binary", "prior_score",
    )
    print(",".join(columns))
    for row in output:
        print(",".join(
            row[column] if column == "judge_pair" else f"{row[column]:.1f}"
            for column in columns
        ))

    average = {
        column: sum(row[column] for row in output) / len(output)
        for column in columns[1:]
    }
    print("Average," + ",".join(f"{average[column]:.1f}" for column in columns[1:]))


if __name__ == "__main__":
    main()
