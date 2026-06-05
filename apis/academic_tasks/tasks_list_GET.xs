// List all academic tasks belonging to the authenticated user
query "academic_tasks/list" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
    int? subject_id
    text? status
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $tasks
  }

  response = $tasks
}
