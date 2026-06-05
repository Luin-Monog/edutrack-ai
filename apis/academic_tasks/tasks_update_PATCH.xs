// Update an academic task with ownership validation
query "academic_tasks/update" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int task_id
    text? title filters=trim
    text? description
    date? due_date
    text? status filters=trim
    text? priority filters=trim
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.task_id
    } as $task
  
    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    precondition ($task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Access denied."
    }
  
    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.task_id
      data = {
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        priority   : $input.priority
      }
    } as $updated
  }

  response = $updated
}