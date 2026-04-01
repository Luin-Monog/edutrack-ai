// Table for academic subjects, allowing users to register and manage their disciplines
// with defined ownership, enabling access controls and future automations.
table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    text name filters=trim
    text? description
  
    // Owner of the subject
    int user_id {
      table = "user"
    }
  
    // Account for access control and sharing
    int account_id? {
      table = "account"
    }
  
    // Visibility level for access control
    enum visibility? {
      values = ["private", "account", "public"]
    }
  
    // Additional fields for future automations
    object metadata? {
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