// Mark an academic task as completed
query "academic_tasks/complete" verb=PATCH {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int task_id
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
      data = {status: "completed"}
    } as $updated
  }

  response = $updated
}