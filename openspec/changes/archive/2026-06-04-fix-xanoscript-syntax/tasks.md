## 1. Tabela academic_tasks

- [x] 1.1 Adicionar campo `user_id` (int, referência à tabela `user`) em `tables/749169_academic_tasks.xs`
- [x] 1.2 Adicionar index btree em `user_id` na mesma tabela

## 2. Função de Segurança

- [x] 2.1 Corrigir precondition de existência em `validate_subject_ownership`: `$subject == null` → `$subject != null`
- [x] 2.2 Corrigir precondition de propriedade em `validate_subject_ownership`: `$subject.user_id != $input.user_id` → `$subject.user_id == $input.user_id`

## 3. Endpoints de Subjects

- [x] 3.1 Reescrever `3586202_subjects_list_GET.xs`: substituir `db.get` por `db.query` com `where = $db.subjects.user_id == $auth.id`
- [x] 3.2 Reescrever `3586206_subjects_summary_GET.xs`: substituir `db.get` por `db.query` com `return = {type: "count"}` e corrigir response
- [x] 3.3 Reescrever `3586207_subjects_search_GET.xs`: substituir ambos os `db.get` por `db.query` com cláusulas `where` corretas

## 4. Verificação dos endpoints que já estão corretos

- [x] 4.1 Confirmar que `3586201_subjects_create_POST.xs` não precisa de alterações
- [x] 4.2 Confirmar que `3586203_subjects_get_GET.xs` não precisa de alterações
- [x] 4.3 Confirmar que `3586204_subjects_update_PATCH.xs` não precisa de alterações
- [x] 4.4 Confirmar que `3586205_subjects_delete_DELETE.xs` não precisa de alterações
