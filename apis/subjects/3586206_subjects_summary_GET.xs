// Get summary statistics for subjects of the authenticated user
query "subjects/summary" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Get all subjects for the user
    db.get subjects {
      field_name  = "user_id"
      field_value = $auth.id
    } as $subjects
  }

  response = {total: $subjects}
}