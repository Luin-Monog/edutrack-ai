// Create a new subject for the authenticated user
query "subjects/create" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name filters=trim
    text? description
    text? visibility
  }

  stack {
    // Get the user's account
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["account_id"]
    } as $user

    // Set default visibility
    var $visibility {
      value = $input.visibility ?? "private"
    }

    // Add the new subject to the database
    db.add subjects {
      data = {
        name: $input.name
        description: $input.description
        user_id: $auth.id
        account_id: $user.account_id
        visibility: "private"
      }
    } as $subject

    // Return the created subject
    response = $subject
  }
}