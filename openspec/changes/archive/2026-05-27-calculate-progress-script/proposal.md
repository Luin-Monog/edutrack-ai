## Why

A small Python helper script is needed to calculate task progress as a percentage from completed and total counts, and return that result as JSON. This makes progress reporting reusable in scripts, automation, or integrations without duplicating calculation logic.

## What Changes

- Add a Python script at `scripts/calculate_progress.py`.
- Implement a function that computes progress percentage using completed and total values.
- Return the result as JSON with clear keys for the computed percentage and metadata.
- Add minimal documentation or usage examples in the script.

## Capabilities

### New Capabilities
- `progress-calculation`: Define a reusable progress calculation utility that returns normalized JSON output.

### Modified Capabilities
- 

## Impact

- Adds a new Python utility script under `scripts/`.
- Introduces a deterministic progress calculation behavior for other automation or frontend integration.
- No API or database changes.
