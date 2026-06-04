// List all subjects for the authenticated user
query "subjects/list" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Get all subjects belonging to the authenticated user
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}