import csv
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from algos.astar import astar
from algos.dijkstra import dijkstra
from main import build_city
from sim.traffic import apply_bidirectional_traffic_condition
from utils.metrics import measure_route_search


BENCHMARK_OUTPUT_DIR = PROJECT_ROOT / "experiments" / "output"
BENCHMARK_CSV_PATH = BENCHMARK_OUTPUT_DIR / "benchmark_results.csv"

SCENARIOS = [
    {
        "name": "Normal traffic A to D",
        "start": "A",
        "goal": "D",
        "traffic": []
    },
    {
        "name": "Accident on A-B",
        "start": "A",
        "goal": "D",
        "traffic": [
            ("A", "B", "ACCIDENT")
        ]
    },
    {
        "name": "Construction on C-D",
        "start": "A",
        "goal": "D",
        "traffic": [
            ("C", "D", "CONSTRUCTION")
        ]
    },
    {
        "name": "A-B closed",
        "start": "A",
        "goal": "D",
        "traffic": [
            ("A", "B", "CLOSED")
        ]
    },
    {
        "name": "Reverse route D to A",
        "start": "D",
        "goal": "A",
        "traffic": []
    }
]

ALGORITHMS = [
    ("Dijkstra", dijkstra),
    ("A*", astar)
]


def apply_scenario_traffic(graph, traffic_changes):
    for source, destination, condition in traffic_changes:
        apply_bidirectional_traffic_condition(
            graph,
            source,
            destination,
            condition
        )


def route_text(path):
    if not path:
        return "No route"

    return " -> ".join(path)


def run_benchmarks():
    rows = []

    for scenario in SCENARIOS:
        graph = build_city()
        apply_scenario_traffic(graph, scenario["traffic"])

        for algorithm_name, search_function in ALGORITHMS:
            result = measure_route_search(
                search_function,
                graph,
                scenario["start"],
                scenario["goal"]
            )

            rows.append({
                "scenario": scenario["name"],
                "algorithm": algorithm_name,
                "start": scenario["start"],
                "goal": scenario["goal"],
                "route": route_text(result["path"]),
                "cost": result["cost"],
                "nodes_explored": result["nodes_explored"],
                "execution_time_ms": result["execution_time_ms"]
            })

    return rows


def print_benchmark_table(rows):
    headers = [
        "Scenario",
        "Algorithm",
        "Route",
        "Cost",
        "Explored",
        "Time (ms)"
    ]
    table_rows = [
        [
            row["scenario"],
            row["algorithm"],
            row["route"],
            f"{row['cost']:.2f}",
            str(row["nodes_explored"]),
            f"{row['execution_time_ms']:.4f}"
        ]
        for row in rows
    ]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in table_rows))
        for index in range(len(headers))
    ]

    print("\nBenchmark Results")
    print("=" * (sum(widths) + 3 * (len(widths) - 1)))
    print(" | ".join(headers[index].ljust(widths[index]) for index in range(len(headers))))
    print("-" * (sum(widths) + 3 * (len(widths) - 1)))

    for row in table_rows:
        print(" | ".join(row[index].ljust(widths[index]) for index in range(len(row))))


def save_benchmark_csv(rows, output_path=BENCHMARK_CSV_PATH):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    headers = [
        "scenario",
        "algorithm",
        "start",
        "goal",
        "route",
        "cost",
        "nodes_explored",
        "execution_time_ms"
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows = run_benchmarks()
    print_benchmark_table(rows)
    save_benchmark_csv(rows)
    print(f"\nSaved CSV: {BENCHMARK_CSV_PATH}")


if __name__ == "__main__":
    main()
