// List subjects for the authenticated user with pagination
query "subjects/list" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    int? page default=1
    int? limit default=10
  }

  stack {
    // Get subjects for the user
    db.get subjects {
      filter = {user_id: $auth.id}
      page = $input.page
      size = $input.limit
    } as $subjects

    response = $subjects
  }
}