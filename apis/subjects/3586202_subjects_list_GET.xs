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
    db.get subjects = {
      filter = {user_id: $auth.id}
      page = $page ?? 1
      size = $limit ?? 10
    } as $subjects

    response = $subjects
  }
}