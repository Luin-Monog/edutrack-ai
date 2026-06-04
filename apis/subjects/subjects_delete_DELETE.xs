// Delete a subject with ownership verification
query "subjects/delete" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
  }

  stack {
    // Fetch the subject
    db.get subjects {
      field_name  = "id"
      field_value = $input.subject_id
    } as $subject

    // Ensure the subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error      = "Subject not found."
    }

    // Ensure the subject belongs to the authenticated user
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error      = "Access denied."
    }

    // Delete the subject
    db.delete subjects {
      field_name  = "id"
      field_value = $input.subject_id
    }
  }

  response = {success: true}
}
