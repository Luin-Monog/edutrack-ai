# academic-tasks-table Design

## Goal
Definir o esquema da tabela `academic_tasks` para suportar o registro e o gerenciamento de obrigações acadêmicas vinculadas a disciplinas.

## Table Schema
- `title` (text): título da tarefa, prova ou trabalho. Deve ser um campo de texto claro e obrigatório.
- `description` (text): descrição detalhada da obrigação. Campo de texto livre, opcional para permitir observações contextuais.
- `due_date` (date): data de entrega ou realização. Permite controle temporal das obrigações.
- `status` (text): status atual da obrigação, por exemplo `pending`, `in_progress`, `completed` ou outro valor de texto relevante.
- `subject_id` (reference): referência para a tabela `subjects` existente, garantindo que cada obrigação esteja vinculada a uma disciplina.

## Constraints
- `subject_id` deve formar uma relação de integridade referencial com `subjects`.
- `title`, `status` e `subject_id` devem ser definidos como obrigatórios para garantir registros consistentes.
- `description` pode ser opcional para acomodar tarefas curtas ou chamadas de prova simples.
- `due_date` deve ser armazenado como data para permitir ordenação e validação posterior de prazos.

## Notes
- A tabela deve seguir o padrão de nomes em `snake_case` usado pelo projeto.
- A tabela `subjects` já existe no sistema e serve como ponto de ligação natural para cada obrigação acadêmica.
