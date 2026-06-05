// Update a subject with ownership verification
query "subjects/update" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name
    text? description
    text? professor filters=trim
    text? schedule filters=trim
    text? visibility
  }

  stack {
    // Fetch the subject
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject
  
    // Ensure the subject exists
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    // Ensure the subject belongs to the authenticated user
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  
    // Apply the update
    db.edit subjects {
      field_name = "id"
      field_value = $input.subject_id
      data = {
        name       : $input.name
        description: $input.description
        professor  : $input.professor
        schedule   : $input.schedule
        visibility : $input.visibility
      }
    } as $updated
  }

  response = $updated
}