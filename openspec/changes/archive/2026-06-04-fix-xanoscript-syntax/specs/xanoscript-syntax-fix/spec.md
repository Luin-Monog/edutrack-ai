# xanoscript-syntax-fix Specification

## Purpose

Corrigir os arquivos XanoScript dos endpoints de subjects e da tabela academic_tasks para que a integração com o banco de dados Xano funcione corretamente. Os erros de sintaxe impedem toda e qualquer operação de listagem, busca e validação de propriedade.

## ADDED Requirements

### Requirement: Usar db.query para queries de múltiplos registros
O sistema SHALL usar `db.query` com cláusula `where` para recuperar listas de registros filtrados por campo, nunca `db.get` (reservado para registro único por campo).

#### Scenario: Listar subjects do usuário
- **WHEN** o endpoint GET /subjects/list é chamado com usuário autenticado
- **THEN** o sistema retorna todos os subjects com `user_id` igual ao `$auth.id` via `db.query`

#### Scenario: Summary de subjects
- **WHEN** o endpoint GET /subjects/summary é chamado
- **THEN** o sistema retorna a contagem total de subjects do usuário autenticado

#### Scenario: Search de subjects
- **WHEN** o endpoint GET /subjects/search é chamado
- **THEN** o sistema recupera subjects do usuário via `db.query` com `where = $db.subjects.user_id == $auth.id`

### Requirement: Corrigir lógica de preconditions em validate_subject_ownership
O sistema SHALL lançar erro quando o subject NÃO existe ou quando o `user_id` NÃO corresponde ao usuário solicitante — não o contrário.

#### Scenario: Subject não encontrado
- **WHEN** `validate_subject_ownership` é chamada com um `subject_id` inexistente
- **THEN** `db.get` retorna null e `precondition ($subject != null)` falha, retornando erro "Subject not found."

#### Scenario: Usuário não é dono do subject
- **WHEN** `validate_subject_ownership` é chamada com um `subject_id` pertencente a outro usuário
- **THEN** `precondition ($subject.user_id == $input.user_id)` falha, retornando erro "Access denied."

#### Scenario: Usuário é dono do subject
- **WHEN** `validate_subject_ownership` é chamada com `subject_id` e `user_id` correspondentes
- **THEN** ambas as preconditions passam e a função retorna null sem erro

### Requirement: Adicionar user_id na tabela academic_tasks
O sistema SHALL armazenar o `user_id` em `academic_tasks` para permitir filtro direto de tarefas por usuário sem join via subjects.

#### Scenario: Busca de tarefas por usuário no search endpoint
- **WHEN** o endpoint GET /subjects/search é chamado com `include_overdue = true`
- **THEN** o sistema recupera academic_tasks filtradas por `user_id` do usuário autenticado via `db.query`

### Requirement: Corrigir endpoint de search para usar db.query em academic_tasks
O sistema SHALL buscar academic_tasks via `db.query` com `where = $db.academic_tasks.user_id == $auth.id`, não via `db.get` por `user_id`.

#### Scenario: Fetch de tasks no sidecar de search
- **WHEN** o sidecar de search é chamado
- **THEN** `$user_tasks` contém todas as academic_tasks do usuário, não um único registro
