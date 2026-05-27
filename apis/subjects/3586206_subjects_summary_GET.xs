// Get summary statistics for subjects
query "subjects/summary" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Get subjects for the user
    db.get subjects {
      field_name = "user_id"
      field_value = $auth.id
    } as $subjects
  }

  response = {total: $subjects.length}
}