// Update a subject with ownership checks
query "subjects/update" verb=PATCH {
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
    precondition ($subject.user_id == $auth.id) {
      error_type = "permissionerror"
      error = "Access denied."
    }

    // Build update data
    var $update_data {
      value = {}
    }

    if ($input.name != null) {
      $update_data = $update_data + {name: $input.name}
    }

    if ($input.description != null) {
      $update_data = $update_data + {description: $input.description}
    }

    if ($input.visibility != null) {
      $update_data = $update_data + {visibility: $input.visibility}
    }

    // Update the subject
    db.update subjects {
      filter = {id: $input.subject_id}
      data = $update_data
    } as $updated

    response = $updated
  }
}