## Context

The repository needs a small utility script to calculate progress percentage from completed and total counts. This script should be usable in automation, reporting or other Python consumers without depending on application-specific data structures.

## Goals / Non-Goals

**Goals:**
- Provide a reusable function that computes completed/total progress as a percentage.
- Return a JSON structure with the computed percentage and input metadata.
- Keep the implementation simple and robust against invalid totals.

**Non-Goals:**
- No API endpoint or UI integration is included.
- No persistence, database, or external service dependencies.
- No advanced progress tracking beyond completed vs total counts.

## Decisions

- Implement a single Python script at `scripts/calculate_progress.py` for easy reuse.
- Expose a `calculate_progress(completed, total)` function and a command-line entrypoint.
- Return a JSON object using Python's built-in `json` module to avoid external dependencies.
- Handle zero or negative totals gracefully to avoid division errors.

## Risks / Trade-offs

- [Risk] Using a script-based utility means consumers must import or invoke the script directly.
  → Mitigation: Keep the interface straightforward and document basic usage.
- [Risk] JSON output format changes may affect downstream consumers.
  → Mitigation: use stable key names and simple value types.
