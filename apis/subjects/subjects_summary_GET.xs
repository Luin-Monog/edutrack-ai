// Return the total count of subjects for the authenticated user
query "subjects/summary" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Count all subjects belonging to the authenticated user
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "count"}
    } as $total
  }

  response = {total: $total}
}