// Table for academic tasks linked to subjects, supporting student obligations like lessons, exams, and assignments.
table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text title filters=trim
    text? description
    date due_date
    text status filters=trim
    int subject_id {
      table = "subjects"
    }

    int user_id {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "subject_id"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "due_date"}]}
  ]

  tags = ["academic-tasks"]
}