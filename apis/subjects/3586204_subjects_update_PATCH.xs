// Update a subject with ownership checks
query "subjects/update" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name
    text? description
    text? visibility
  }

  stack {
    // Get the subject
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    // Check if subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    // Check ownership
    precondition ($subject.user_id != $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    // Update the subject with provided fields
    db.update subjects {
      filter = {id: $input.subject_id}
      data = {
        name: $input.name
        description: $input.description
        visibility: $input.visibility
      }
    } as $updated

    response = $updated
  }
}