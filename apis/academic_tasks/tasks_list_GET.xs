// List all academic tasks belonging to the authenticated user. No filter inputs.
query "academic_tasks/list" verb=GET {
  api_group = "Academic Tasks"
  auth = "user"

  input {
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $tasks
  }

  response = $tasks
}