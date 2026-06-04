// Table for academic subjects, allowing users to register and manage their disciplines
// with defined ownership, enabling access controls and future automations.
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    text? description
    int user_id {
      table = "user"
    }
  
    int? account_id {
      table = "account"
    }
  
    enum visibility?=private {
      values = ["private", "account", "public"]
    }
  
    object? metadata {
      schema {
        text? category
        text? code
        int? credits
        bool? active
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id"}]}
    {type: "btree", field: [{name: "account_id"}]}
    {type: "btree", field: [{name: "visibility"}]}
  ]

  tags = ["subjects-management"]
}