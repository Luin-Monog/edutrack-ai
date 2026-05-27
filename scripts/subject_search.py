import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List
from dateutil import parser as date_parser


def parse_date(date_str: str) -> datetime:
    """Helper to parse date string robustly."""
    try:
        return date_parser.parse(date_str)
    except Exception:
        # Fallback to current datetime if parsing fails
        return datetime.now()


def search_subjects(
    subjects: List[Dict[str, Any]],
    tasks: List[Dict[str, Any]],
    query: str = "",
    include_overdue: bool = False,
    current_date_str: str = ""
) -> List[Dict[str, Any]]:
    """Filters subjects by name matching or presence of overdue tasks.

    A task is overdue if due_date < current_date and status != 'completed'.
    If query is not provided, returns subjects with overdue tasks.
    If query is provided, returns subjects where name matches OR subject has overdue tasks (if include_overdue is True).
    """
    current_date = parse_date(current_date_str) if current_date_str else datetime.now()
    
    # 1. Identify overdue tasks and their corresponding subject IDs
    overdue_subject_ids = set()
    for task in tasks:
        try:
            due_date_str = task.get("due_date")
            status = task.get("status", "").strip().lower()
            
            if not due_date_str or status == "completed":
                continue
                
            due_date = date_parser.parse(str(due_date_str))
            
            # Compare dates (ignoring time components if appropriate, or direct datetime comparison)
            if due_date < current_date:
                subject_id = task.get("subject_id")
                if subject_id is not None:
                    overdue_subject_ids.add(int(subject_id))
        except Exception as e:
            # Silently ignore individual malformed task parsing issues to ensure robustness
            continue

    # 2. Filter subjects
    filtered_subjects = []
    query_clean = query.strip().lower() if query else ""

    for subject in subjects:
        try:
            subject_id = subject.get("id")
            if subject_id is None:
                continue
            subject_id = int(subject_id)
            
            name = subject.get("name", "").strip().lower()
            description = subject.get("description", "").strip().lower()
            
            # Conditions
            name_matches = query_clean and (query_clean in name or query_clean in description)
            has_overdue_tasks = subject_id in overdue_subject_ids

            # If query is empty, we show subjects with overdue tasks (default behavior)
            if not query_clean:
                if has_overdue_tasks:
                    filtered_subjects.append(subject)
            else:
                # If query is provided, we match by name
                # If include_overdue is True, we match by name OR overdue tasks
                if name_matches or (include_overdue and has_overdue_tasks):
                    filtered_subjects.append(subject)
        except Exception:
            continue

    return filtered_subjects


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter subjects by name or overdue tasks."
    )
    parser.add_argument(
        "--subjects",
        type=str,
        required=True,
        help="JSON string or path to a JSON file containing subjects list."
    )
    parser.add_argument(
        "--tasks",
        type=str,
        required=True,
        help="JSON string or path to a JSON file containing tasks list."
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Query string to search in subject name or description."
    )
    parser.add_argument(
        "--include-overdue",
        action="store_true",
        help="Enable overdue tasks logic."
    )
    parser.add_argument(
        "--current-date",
        type=str,
        default="",
        help="Reference date for overdue calculation (default: now)."
    )
    return parser.parse_args()


def load_json_data(input_str: str) -> List[Dict[str, Any]]:
    """Loads JSON list from a raw string or a file path."""
    try:
        # Try loading as direct JSON string
        return json.loads(input_str)
    except json.JSONDecodeError:
        # Try loading as file path
        try:
            with open(input_str, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to parse JSON input: {e}")


def main() -> None:
    try:
        args = parse_args()
        subjects = load_json_data(args.subjects)
        tasks = load_json_data(args.tasks)
        
        result = search_subjects(
            subjects=subjects,
            tasks=tasks,
            query=args.query,
            include_overdue=args.include_overdue,
            current_date_str=args.current_date
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
