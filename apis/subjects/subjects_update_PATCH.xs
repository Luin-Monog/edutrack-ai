// Update a subject with ownership verification
query "subjects/update" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int subject_id
    text? name
    text? description
    text? professor
    text? schedule
    text? semester
    text? visibility
    bool? archived
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }

    db.edit subjects {
      field_name = "id"
      field_value = $input.subject_id
      data = {
        name       : $input.name
        description: $input.description
        professor  : $input.professor
        schedule   : $input.schedule
        semester   : $input.semester
        visibility : $input.visibility
        archived   : $input.archived
      }
    } as $updated
  }

  response = $updated
}
