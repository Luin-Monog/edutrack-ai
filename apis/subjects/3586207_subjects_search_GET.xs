// Search subjects by name/description OR by presence of overdue academic tasks.
// Calls the Python sidecar (sidecar_search_api.py) via external.request for complex filtering.
query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    // Optional: partial text to match against subject name or description
    text? query
    // Optional: when true, includes subjects that have overdue tasks even if name does not match
    bool? include_overdue
  }

  stack {
    // 1. Fetch all subjects belonging to the authenticated user
    db.get subjects {
      field_name  = "user_id"
      field_value = $auth.id
    } as $user_subjects

    // 2. Fetch all academic tasks for the authenticated user (drives overdue detection)
    db.get academic_tasks {
      field_name  = "user_id"
      field_value = $auth.id
    } as $user_tasks

    // 3. Resolve effective flag (default false when not supplied)
    set $flag_overdue = ($input.include_overdue == true)

    // 4. Call the Python search sidecar via HTTP.
    //    The sidecar (sidecar_search_api.py) runs on port 8787 and wraps scripts/subject_search.py.
    //    SUBJECT_SEARCH_URL env var should be set to: http://localhost:8787/search
    external.request {
      method  = "POST"
      url     = $env.SUBJECT_SEARCH_URL
      headers = {"Content-Type": "application/json"}
      body    = {
        subjects        : $user_subjects
        tasks           : $user_tasks
        query           : ($input.query ?? "")
        include_overdue : $flag_overdue
        current_date    : ""
      }
    } as $search_response

    // 5. Guard: surface any error returned by the sidecar
    precondition ($search_response.error == null) {
      error_type = "internal"
      error      = "Subject search service returned an error."
    }
  }

  response = $search_response
}
