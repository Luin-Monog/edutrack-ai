import argparse
import json
from typing import Any, Dict


def calculate_progress(completed: float, total: float) -> Dict[str, Any]:
    """Calculate progress percentage from completed and total values.

    The percentage is clamped between 0 and 100. If total is zero or negative,
    the function returns 0.0 to avoid division by zero.
    """
    completed_value = float(completed)
    total_value = float(total)

    if total_value <= 0:
        percentage = 0.0
    else:
        percentage = (completed_value / total_value) * 100.0

    percentage = max(0.0, min(percentage, 100.0))

    return {
        "completed": completed_value,
        "total": total_value,
        "percentage": round(percentage, 2),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate task progress and print JSON output."
    )
    parser.add_argument(
        "--completed",
        type=float,
        default=3.0,
        help="Number of completed items (default: 3).",
    )
    parser.add_argument(
        "--total",
        type=float,
        default=5.0,
        help="Total number of items (default: 5).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = calculate_progress(args.completed, args.total)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
