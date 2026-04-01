// Get summary statistics for subjects
query "subjects/summary" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Get subjects for the user
    db.get subjects {
      filter = {user_id: $auth.id}
    } as $subjects

    response = {
      total: 0
    }
  }
}