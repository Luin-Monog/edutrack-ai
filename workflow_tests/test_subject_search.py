import sys
sys.path.append(".")
from scripts.subject_search import search_subjects

def run_tests():
    subjects = [
        {"id": 1, "name": "Matematica", "description": "Algebra"},
        {"id": 2, "name": "Fisica", "description": "Mecanica"},
        {"id": 3, "name": "Programacao Python", "description": "Linguagem Python"}
    ]
    
    tasks = [
        {"id": 101, "subject_id": 1, "due_date": "2026-05-01", "status": "pending"},
        {"id": 102, "subject_id": 2, "due_date": "2026-06-01", "status": "pending"},
        {"id": 103, "subject_id": 3, "due_date": "2026-05-15", "status": "completed"}
    ]
    
    # Test 1: Empty query, should return subjects with overdue tasks
    # Current date is 2026-05-20. Task 101 is overdue (due 2026-05-01, pending).
    res1 = search_subjects(subjects, tasks, query="", include_overdue=False, current_date_str="2026-05-20")
    assert len(res1) == 1, f"Expected 1 subject, got {len(res1)}"
    assert res1[0]["id"] == 1
    print("Test 1 passed: empty query returns overdue subjects")
    
    # Test 2: Search for 'python', no overdue flag, should return python subject
    res2 = search_subjects(subjects, tasks, query="python", include_overdue=False, current_date_str="2026-05-20")
    assert len(res2) == 1
    assert res2[0]["id"] == 3
    print("Test 2 passed: name match query works")
    
    # Test 3: Search for 'python' WITH overdue flag, should return python subject AND overdue Matematica subject
    res3 = search_subjects(subjects, tasks, query="python", include_overdue=True, current_date_str="2026-05-20")
    assert len(res3) == 2
    ids = {s["id"] for s in res3}
    assert ids == {1, 3}
    print("Test 3 passed: combined OR matching works")

    # Test 4: Search with no matches
    res4 = search_subjects(subjects, tasks, query="nonexistent", include_overdue=False, current_date_str="2026-05-20")
    assert len(res4) == 0
    print("Test 4 passed: no matches returns empty list")


if __name__ == "__main__":
    run_tests()
