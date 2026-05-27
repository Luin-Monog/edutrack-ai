// Search subjects by name/description OR by presence of overdue academic tasks.
// Calls the Python sidecar (sidecar_search_api.py) via external.request for complex filtering.
query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text? query
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

    // 3. Call the Python search sidecar via HTTP.
    //    The sidecar (sidecar_search_api.py) runs on port 8787.
    //    Set SUBJECT_SEARCH_URL env var to: http://localhost:8787/search
    external.request {
      method = "POST"
      url    = $env.SUBJECT_SEARCH_URL
      body   = {
        subjects        : $user_subjects
        tasks           : $user_tasks
        query           : $input.query
        include_overdue : $input.include_overdue
        current_date    : ""
      }
    } as $search_response
  }

  response = $search_response
}
