// Search subjects by name/description or by presence of overdue academic tasks.
// Delegates complex filtering to the Python sidecar (sidecar_search_api.py) via HTTP.
query "subjects/search" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text? query
    bool? include_overdue
  }

  stack {
    // Fetch all subjects belonging to the authenticated user
    db.query subjects {
      where  = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $user_subjects

    // Fetch all academic tasks belonging to the authenticated user
    db.query academic_tasks {
      where  = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $user_tasks

    // Call the Python search sidecar.
    // Set env var SUBJECT_SEARCH_URL to: http://localhost:8787/search
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
