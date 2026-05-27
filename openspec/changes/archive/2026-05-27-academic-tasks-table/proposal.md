# academic-tasks-table Proposal

## Purpose
Planejar a criação da tabela `academic_tasks` para permitir que o aluno registre e gerencie suas obrigações acadêmicas (lições, provas, trabalhos) vinculadas a cada disciplina.

## Why
Atualmente não existe uma tabela dedicada para armazenar tarefas e avaliações vinculadas a disciplinas. Sem esse esquema, não é possível rastrear prazos, status de conclusão ou associar deveres diretamente a um `subject`.

## Scope
- IN SCOPE: criação da tabela `academic_tasks` com os campos solicitados, incluindo a referência `subject_id` para a tabela `subjects`.
- OUT OF SCOPE: implementação de endpoints CRUD, interfaces de usuário, listagens, filtros ou relatórios.

## What Changes
- Banco: adicionar nova tabela `academic_tasks`.
- Campos: `title`, `description`, `due_date`, `status` e `subject_id`.
- Relação: `subject_id` referenciará a tabela existente `subjects` para garantir vinculação por disciplina.
- Regras de dados: `title`, `status` e `subject_id` devem ser usados para registrar claramente cada obrigação e manter consistência.

## Impact
- Migração DB necessária para criar a nova tabela.
- Dependência direta da tabela `subjects` existente.
- Seleção mínima de mudanças: apenas o esquema de dados será planejado, sem API ou lógica adicional.
