#!/usr/bin/env bash
# Sweep judge pairs and judge types over a sharded benchmark.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUNNER="${TVD_RUNNER:-$SCRIPT_DIR/run.sh}"

# Experiment defaults. CLI flags below override these values.
PAIRS_PATH="judge_pairs.json"
BENCH_PATH="bench/advbench_100.csv"
QUERY_COLUMN="request"
QUERY_LIMIT=100
BATCH_SIZE=5
SAMPLE_BUDGET=10
PARALLEL_JOBS=2
JUDGE_TYPES="binary,scoring"
SETTING="query_and_response"
SCORING_THRESHOLD=0.5
AGENT_CLI="codex"
AGENT_PROVIDER="subscription"
AGENT_MODEL="openai/gpt-5.6-luna"
MAX_TURNS=120
ENV_FILE=".env"
EXPERIMENT_DIR=""
DRY_RUN=0

usage() {
    cat <<'EOF'
Usage: ./run_benchmark.sh [options]

  --pairs PATH              Judge-pair JSON file (default: judge_pairs.json)
  --bench PATH              Benchmark CSV (default: bench/advbench_100.csv)
  --query-column NAME       Query column (default: request)
  --query-limit N           Number of benchmark queries (default: 100)
  --batch-size N            Queries per Agent run (default: 5)
  --budget N                Attempts per safe/unsafe sample (default: 10)
  --parallel N              Concurrent Agent runs (default: 2)
  --judge-types TYPES       Comma list: binary,scoring (default: both)
  --setting MODE            query_only | response_only | query_and_response
  --scoring-threshold N     Scoring conflict threshold (default: 0.5)
  --agent codex|claude|terminal
  --agent-provider MODE     subscription | openrouter
  --agent-model MODEL       OpenRouter Agent model
  --max-turns N             Claude Code turn cap (default: 120)
  --env-file PATH           API key file (default: .env)
  --experiment-dir PATH     Output directory; reuse it to resume
  --dry-run                 Prepare shards and job manifest without running
  -h, --help

Pair file format:
  [
    {"name": "qwen_vs_deepseek", "judge_a": "qwen/...", "judge_b": "deepseek/..."}
  ]
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pairs) PAIRS_PATH="$2"; shift 2 ;;
        --bench) BENCH_PATH="$2"; shift 2 ;;
        --query-column) QUERY_COLUMN="$2"; shift 2 ;;
        --query-limit) QUERY_LIMIT="$2"; shift 2 ;;
        --batch-size) BATCH_SIZE="$2"; shift 2 ;;
        --budget) SAMPLE_BUDGET="$2"; shift 2 ;;
        --parallel) PARALLEL_JOBS="$2"; shift 2 ;;
        --judge-types) JUDGE_TYPES="$2"; shift 2 ;;
        --setting) SETTING="$2"; shift 2 ;;
        --scoring-threshold) SCORING_THRESHOLD="$2"; shift 2 ;;
        --agent) AGENT_CLI="$2"; shift 2 ;;
        --agent-provider) AGENT_PROVIDER="$2"; shift 2 ;;
        --agent-model) AGENT_MODEL="$2"; shift 2 ;;
        --max-turns) MAX_TURNS="$2"; shift 2 ;;
        --env-file) ENV_FILE="$2"; shift 2 ;;
        --experiment-dir) EXPERIMENT_DIR="$2"; shift 2 ;;
        --dry-run) DRY_RUN=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
    esac
done

for value in "$QUERY_LIMIT" "$BATCH_SIZE" "$SAMPLE_BUDGET" "$PARALLEL_JOBS" "$MAX_TURNS"; do
    [[ "$value" =~ ^[1-9][0-9]*$ ]] || {
        echo "Query limit, batch size, budget, parallelism, and max turns must be positive integers." >&2
        exit 2
    }
done

case "$SETTING" in
    query_only|response_only|query_and_response) ;;
    *) echo "Invalid setting: $SETTING" >&2; exit 2 ;;
esac
case "$AGENT_CLI" in
    codex|claude|terminal) ;;
    *) echo "--agent must be codex, claude, or terminal" >&2; exit 2 ;;
esac
case "$AGENT_PROVIDER" in
    subscription|openrouter) ;;
    *) echo "--agent-provider must be subscription or openrouter" >&2; exit 2 ;;
esac
[[ "$SCORING_THRESHOLD" =~ ^([0-9]+([.][0-9]*)?|[.][0-9]+)$ ]] || {
    echo "--scoring-threshold must be a number between 0 and 1" >&2
    exit 2
}
awk -v value="$SCORING_THRESHOLD" 'BEGIN { exit !(value >= 0 && value <= 1) }' || {
    echo "--scoring-threshold must be a number between 0 and 1" >&2
    exit 2
}

absolute_path() {
    python3 - "$SCRIPT_DIR" "$1" <<'PY'
import pathlib, sys
root, value = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).expanduser()
print((value if value.is_absolute() else root / value).resolve())
PY
}

PAIRS_PATH="$(absolute_path "$PAIRS_PATH")"
BENCH_PATH="$(absolute_path "$BENCH_PATH")"
ENV_FILE="$(absolute_path "$ENV_FILE")"
[[ -f "$PAIRS_PATH" ]] || { echo "Pair file not found: $PAIRS_PATH" >&2; exit 2; }
[[ -f "$BENCH_PATH" ]] || { echo "Benchmark not found: $BENCH_PATH" >&2; exit 2; }
[[ -f "$ENV_FILE" ]] || { echo "Environment file not found: $ENV_FILE" >&2; exit 2; }
[[ -x "$RUNNER" ]] || { echo "Runner is not executable: $RUNNER" >&2; exit 2; }

if [[ -z "$EXPERIMENT_DIR" ]]; then
    EXPERIMENT_DIR="$SCRIPT_DIR/run/benchmark_$(date -u +%Y%m%d_%H%M%S)"
else
    EXPERIMENT_DIR="$(absolute_path "$EXPERIMENT_DIR")"
fi
mkdir -p "$EXPERIMENT_DIR/shards" "$EXPERIMENT_DIR/jobs"

JOBS_PATH="$EXPERIMENT_DIR/jobs.tsv"
python3 - \
    "$PAIRS_PATH" "$BENCH_PATH" "$QUERY_COLUMN" "$QUERY_LIMIT" "$BATCH_SIZE" \
    "$JUDGE_TYPES" "$EXPERIMENT_DIR" "$JOBS_PATH" <<'PY'
import csv
import json
import pathlib
import re
import sys

pairs_path, bench_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
query_column, query_limit, batch_size = sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
judge_types = [value.strip() for value in sys.argv[6].split(",") if value.strip()]
experiment, jobs_path = pathlib.Path(sys.argv[7]), pathlib.Path(sys.argv[8])

if not judge_types or any(value not in {"binary", "scoring"} for value in judge_types):
    raise SystemExit("--judge-types must contain only binary and/or scoring")
if len(set(judge_types)) != len(judge_types):
    raise SystemExit("--judge-types contains duplicates")

try:
    raw_pairs = json.loads(pairs_path.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    raise SystemExit(f"invalid judge-pair JSON: {exc}")
if not isinstance(raw_pairs, list) or not raw_pairs:
    raise SystemExit("judge-pair JSON must be a non-empty array")

pairs = []
names = set()
for index, raw in enumerate(raw_pairs, 1):
    if not isinstance(raw, dict):
        raise SystemExit(f"pair {index} must be an object")
    judge_a, judge_b = raw.get("judge_a"), raw.get("judge_b")
    if not all(isinstance(value, str) and value.strip() for value in (judge_a, judge_b)):
        raise SystemExit(f"pair {index} requires non-empty judge_a and judge_b")
    if judge_a == judge_b:
        raise SystemExit(f"pair {index} uses the same model twice")
    default_name = f"{judge_a.split('/')[-1]}_vs_{judge_b.split('/')[-1]}"
    name = raw.get("name", default_name)
    if not isinstance(name, str) or not name.strip():
        raise SystemExit(f"pair {index} has an invalid name")
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip()).strip("._-")
    if not name or name in names:
        raise SystemExit(f"pair {index} has an empty or duplicate normalized name")
    if any("\t" in value or "\n" in value for value in (judge_a, judge_b)):
        raise SystemExit(f"pair {index} model IDs cannot contain tabs or newlines")
    names.add(name)
    pairs.append((name, judge_a, judge_b))

with bench_path.open(newline="", encoding="utf-8-sig") as handle:
    reader = csv.DictReader(handle)
    if not reader.fieldnames or query_column not in reader.fieldnames:
        raise SystemExit(f"CSV has no {query_column!r} query column")
    fieldnames = reader.fieldnames
    rows = [row for row in reader if (row.get(query_column) or "").strip()][:query_limit]
if len(rows) < query_limit:
    raise SystemExit(f"benchmark has only {len(rows)} non-empty queries, expected {query_limit}")

shards = []
for start in range(0, len(rows), batch_size):
    shard_number = len(shards) + 1
    shard_rows = rows[start : start + batch_size]
    shard_path = experiment / "shards" / f"shard_{shard_number:03d}.csv"
    with shard_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(shard_rows)
    shards.append((shard_number, shard_path, len(shard_rows)))

jobs = []
for name, judge_a, judge_b in pairs:
    for judge_type in judge_types:
        for shard_number, shard_path, shard_size in shards:
            run_dir = experiment / "jobs" / name / judge_type / f"shard_{shard_number:03d}"
            jobs.append((name, judge_a, judge_b, judge_type, shard_number, shard_path, shard_size, run_dir))

with jobs_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
    writer.writerow((
        "job", "total_jobs", "pair_name", "judge_a", "judge_b", "judge_type",
        "shard", "shard_path", "query_count", "run_dir",
    ))
    for job_number, job in enumerate(jobs, 1):
        writer.writerow((job_number, len(jobs), *job))

print(f"Prepared {len(rows)} queries in {len(shards)} shards and {len(jobs)} jobs.")
PY

TOTAL_JOBS="$(awk 'END { print NR - 1 }' "$JOBS_PATH")"
echo "Experiment:  $EXPERIMENT_DIR"
echo "Judge pairs: $(python3 - "$PAIRS_PATH" <<'PY'
import json, pathlib, sys
print(len(json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))))
PY
)"
echo "Judge types: $JUDGE_TYPES"
echo "Queries:     $QUERY_LIMIT ($BATCH_SIZE per shard)"
echo "Budget:      $SAMPLE_BUDGET attempts per sample"
echo "Parallel:    $PARALLEL_JOBS Agent runs"
echo "Jobs:        $TOTAL_JOBS"

if ((DRY_RUN)); then
    echo "Dry run complete. Job manifest: $JOBS_PATH"
    exit 0
fi

if [[ -t 1 && -z "${NO_COLOR:-}" ]]; then
    CYAN=$'\033[1;36m'
    GREEN=$'\033[1;32m'
    YELLOW=$'\033[1;33m'
    RED=$'\033[1;31m'
    RESET=$'\033[0m'
else
    CYAN="" GREEN="" YELLOW="" RED="" RESET=""
fi

run_job() {
    local job_number="$1" pair_name="$2" judge_a="$3" judge_b="$4"
    local judge_type="$5" shard="$6" shard_path="$7" query_count="$8" run_dir="$9"
    mkdir -p "$run_dir"
    local exit_code
    if {
        echo
        echo "=== benchmark invocation $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
        "$RUNNER" \
            --worker \
            --setting "$SETTING" \
            --query-count "$query_count" \
            --sample-budget "$SAMPLE_BUDGET" \
            --bench "$shard_path" \
            --query-column "$QUERY_COLUMN" \
            --agent "$AGENT_CLI" \
            --agent-provider "$AGENT_PROVIDER" \
            --agent-model "$AGENT_MODEL" \
            --judge-a "$judge_a" \
            --judge-b "$judge_b" \
            --judge-type "$judge_type" \
            --scoring-threshold "$SCORING_THRESHOLD" \
            --max-turns "$MAX_TURNS" \
            --run-dir "$run_dir" \
            --env-file "$ENV_FILE"
    } >>"$run_dir/runner.log" 2>&1; then
        exit_code=0
    else
        exit_code=$?
    fi
    printf '%s\n' "$exit_code" >"$run_dir/runner.exit"
    return "$exit_code"
}

job_counts() {
    python3 - "$1" <<'PY'
import json, pathlib, sys
run_dir = pathlib.Path(sys.argv[1])
def count(name):
    try:
        value = json.loads((run_dir / name).read_text(encoding="utf-8"))
        return len(value.get("samples", []))
    except (FileNotFoundError, json.JSONDecodeError, AttributeError):
        return 0
print(count("successful.json"), count("attempt.json"))
PY
}

pids=()
labels=()
run_dirs=()
completed=0
failed=0

wait_first() {
    local pid="${pids[0]}" label="${labels[0]}" run_dir="${run_dirs[0]}" exit_code
    if wait "$pid"; then
        exit_code=0
    else
        exit_code=$?
        failed=$((failed + 1))
    fi
    completed=$((completed + 1))
    read -r success active < <(job_counts "$run_dir")
    if ((exit_code == 0)); then
        printf '%s[%d/%d] DONE%s %s | %striggered %d%s | remaining %d\n' \
            "$GREEN" "$completed" "$TOTAL_JOBS" "$RESET" "$label" \
            "$CYAN" "$success" "$RESET" "$active"
    else
        printf '%s[%d/%d] PARTIAL%s %s | %striggered %d%s | %sremaining %d%s | log: %s\n' \
            "$YELLOW" "$completed" "$TOTAL_JOBS" "$RESET" "$label" \
            "$CYAN" "$success" "$RESET" "$RED" "$active" "$RESET" "$run_dir/runner.log"
    fi
    pids=("${pids[@]:1}")
    labels=("${labels[@]:1}")
    run_dirs=("${run_dirs[@]:1}")
}

while IFS=$'\t' read -r job_number total_jobs pair_name judge_a judge_b judge_type \
    shard shard_path query_count run_dir; do
    [[ "$job_number" == "job" ]] && continue
    label="$pair_name/$judge_type/shard_$shard"
    printf '%s[launch %s/%s]%s %s\n' "$CYAN" "$job_number" "$total_jobs" "$RESET" "$label"
    run_job "$job_number" "$pair_name" "$judge_a" "$judge_b" \
        "$judge_type" "$shard" "$shard_path" "$query_count" "$run_dir" &
    pids+=("$!")
    labels+=("$label")
    run_dirs+=("$run_dir")
    if ((${#pids[@]} >= PARALLEL_JOBS)); then
        wait_first
    fi
done <"$JOBS_PATH"

while ((${#pids[@]})); do
    wait_first
done

SUMMARY_PATH="$EXPERIMENT_DIR/summary.csv"
python3 - "$JOBS_PATH" "$SUMMARY_PATH" "$SETTING" <<'PY'
import csv
import json
import pathlib
import statistics
import sys
from collections import defaultdict

jobs_path, summary_path = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
setting = sys.argv[3]
with jobs_path.open(newline="", encoding="utf-8") as handle:
    jobs = list(csv.DictReader(handle, delimiter="\t"))

groups = defaultdict(list)
for job in jobs:
    groups[(job["pair_name"], job["judge_a"], job["judge_b"], job["judge_type"])].append(job)

rows = []
for (name, judge_a, judge_b, judge_type), group in groups.items():
    total_queries = sum(int(job["query_count"]) for job in group)
    successes, active, attempts, covered = [], 0, [], set()
    failed_jobs = 0
    for job in group:
        run_dir = pathlib.Path(job["run_dir"])
        try:
            successes.extend(json.loads((run_dir / "successful.json").read_text())["samples"])
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            pass
        try:
            active += len(json.loads((run_dir / "attempt.json").read_text()).get("samples", []))
        except (FileNotFoundError, json.JSONDecodeError, AttributeError):
            active += int(job["query_count"]) * 2
        try:
            failed_jobs += int((run_dir / "runner.exit").read_text().strip()) != 0
        except (FileNotFoundError, ValueError):
            failed_jobs += 1

    for sample in successes:
        covered.add(sample.get("original_query", ""))
        try:
            attempts.append(int(sample["attempt"].split("/", 1)[0]))
        except (KeyError, AttributeError, ValueError):
            pass
    total_samples = total_queries * 2
    safe = sum(sample.get("judge_ground_truth") == "safe" for sample in successes)
    unsafe = sum(sample.get("judge_ground_truth") == "unsafe" for sample in successes)
    rows.append({
        "pair_name": name,
        "judge_a": judge_a,
        "judge_b": judge_b,
        "judge_type": judge_type,
        "setting": setting,
        "queries": total_queries,
        "samples": total_samples,
        "conflicts": len(successes),
        "conflict_rate": f"{len(successes) / total_samples:.4f}",
        "safe_conflicts": safe,
        "unsafe_conflicts": unsafe,
        "queries_with_conflict": len(covered),
        "query_coverage": f"{len(covered) / total_queries:.4f}",
        "mean_attempts_to_conflict": f"{statistics.mean(attempts):.3f}" if attempts else "",
        "active_samples": active,
        "exhausted_samples": max(total_samples - len(successes) - active, 0),
        "completed_jobs": len(group) - failed_jobs,
        "failed_jobs": failed_jobs,
        "total_jobs": len(group),
    })

fieldnames = list(rows[0]) if rows else []
with summary_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("\nRESULTS")
print(f"{'pair':<24} {'type':<8} {'conflicts':>10} {'rate':>8} {'coverage':>10} {'active':>8} {'failed':>8}")
for row in rows:
    print(
        f"{row['pair_name']:<24} {row['judge_type']:<8} "
        f"{row['conflicts']:>4}/{row['samples']:<5} {row['conflict_rate']:>8} "
        f"{row['query_coverage']:>10} {row['active_samples']:>8} {row['failed_jobs']:>8}"
    )
PY

echo "Summary: $SUMMARY_PATH"
if ((failed)); then
    echo "$failed job(s) remain incomplete; rerun with the same options and --experiment-dir '$EXPERIMENT_DIR'." >&2
    exit 1
fi
