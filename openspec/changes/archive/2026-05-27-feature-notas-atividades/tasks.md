# feature-notas-atividades Tasks

IMPORTANTE: Manter o escopo estritamente ao pedido — somente o que é necessário para permitir que o professor lance notas.

- [ ] Criar tabela `activity_grades` (schema básico descrito em `design.md`).
  - Output sugerido: `tables/749169_activity_grades.xs` (nome/ID a confirmar)
  - Campos mínimos: `id`, `activity_id`, `student_id`, `grade`, `comment?`, `created_by`, `created_at`.
  - Garantir FKs e índices recomendados.

- [ ] Criar API POST `/activity_grades` para inserir um registro de nota.
  - Output sugerido: `apis/activity_grades/post_activity_grades.xs` ou `apis/grades/activity_grades_CREATE_POST.xs`.
  - Entrada: `activity_id`, `student_id`, `grade`, `comment?`.
  - Lógica: validação de autenticação, checagem de papel `teacher`, verificação de vínculo de conta, validação do valor de `grade`, persistência na tabela e resposta 201 com o registro criado.
  - Não implementar endpoints de leitura/edição/exclusão nesta tarefa.

- [ ] Adicionar validações de segurança e integridade de dados.
  - Regras: somente `teacher` pode post, activity & student devem pertencer à mesma organização/conta.

- [ ] Documentar os campos e exemplos de request/response em `apis/` (arquivo de spec Xano ou README interno), básico e objetivo.

Notas:
- Antes de gerar arquivos `.xs`, leia e siga os guidelines em `docs/` referenciados por `agents/AGENTS.md`. Se esses arquivos não existirem, solicitar revisão humana antes de executar push/migração.
