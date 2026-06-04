// Validates that a subject exists and belongs to the requesting user.
function "Getting Started Template/validate_subject_ownership" {
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
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($subject.user_id == $input.user_id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  }

  response = null
}