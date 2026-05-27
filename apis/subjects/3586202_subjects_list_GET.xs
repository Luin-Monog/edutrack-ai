// List subjects for the authenticated user with pagination
query "subjects/list" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int? page
    int? limit
  }

  stack {
    // Get subjects for the user
    db.get subjects {
      field_name  = "user_id"
      field_value = $auth.id
    } as $subjects
  }

  response = $subjects
}