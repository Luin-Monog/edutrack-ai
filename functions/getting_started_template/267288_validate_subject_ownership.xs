// Validates if a user owns a subject.
function "Subjects/validate_subject_ownership" {
  input {
    int subject_id
    int user_id
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subject_id
      output = ["user_id"]
    } as $subject
  
    precondition ($subject == null) {
      error = "Subject not found."
    }
  
    precondition ($subject.user_id != $input.user_id) {
      error = "Access denied."
    }
  }

  response = null
}