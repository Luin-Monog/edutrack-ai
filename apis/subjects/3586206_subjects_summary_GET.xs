// Get summary statistics for subjects
query "subjects/summary" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
  }

  stack {
    // Count total subjects for the user
    db.get subjects {
      filter = {user_id: $auth.id}
      aggregate = {count: {}}
    } as $count

    // Get subjects by visibility
    db.get subjects {
      filter = {user_id: $auth.id}
      aggregate = {count: {}, group_by: "visibility"}
    } as $by_visibility

    response = {
      total: $count.count
      by_visibility: $by_visibility
    }
  }
}