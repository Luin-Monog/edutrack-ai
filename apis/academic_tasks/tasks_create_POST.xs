// Create a new academic task linked to a subject for the authenticated user
query "academic_tasks/create" verb=POST {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    text title filters=trim
    text? description
    date due_date
    int subject_id
    text status?=pending filters=trim
    text priority?=media filters=trim
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
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  
    db.add academic_tasks {
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        subject_id : $input.subject_id
        user_id    : $auth.id
        status     : $input.status
        priority   : $input.priority
      }
    } as $task
  }

  response = $task
}