// Delete a subject with ownership checks
query "subjects/delete" verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
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

    // Delete the subject
    db.delete subjects {
      filter = {id: $input.subject_id}
    }

    response = {success: true}
  }
}