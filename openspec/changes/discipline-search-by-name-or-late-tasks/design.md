# discipline-search-by-name-or-late-tasks Design

## Overview

Esta mudança adiciona um endpoint de busca dedicado para disciplinas, permitindo localizar matérias pelo nome ou por presença de tarefas atrasadas. O comportamento prioriza a experiência do usuário e reutiliza lógica Python para calcular atrasos sem duplicar regras em múltiplos pontos.

## Data Sources

- Tabela `subjects`: contém as disciplinas do usuário (`id`, `user_id`, `name`, `description`, etc.).
- Tabela `academic_tasks`: contém obrigações acadêmicas vinculadas às disciplinas (`subject_id`, `due_date`, `status`).

## Endpoint

- `GET /subjects/search`
- Inputs sugeridos:
  - `query` (text, opcional): termo para busca textual no nome da disciplina.
  - `include_overdue` (bool, opcional): habilita a lógica de tarefas atrasadas.

## Behavior

- O endpoint consulta as disciplinas do usuário autenticado.
- Para cada disciplina, calcula se há tarefas atrasadas usando a regra:
  - `due_date < hoje`
  - `status` diferente de `completed` (ou equivalente pendente/ativo)
- O resultado é composto por disciplinas que atendem a pelo menos um desses critérios:
  - nome/descrição contém o termo de busca
  - possui tarefa atrasada
- Quando `query` não é informado, o endpoint devolve disciplinas com tarefas atrasadas.

## Python Integration

- Criar um helper em `scripts/subject_search.py` para:
  - carregar dados de disciplinas e tarefas
  - calcular o estado de atrasos
  - retornar uma estrutura serializável com os registros filtrados
- O endpoint deve consumir essa lógica de forma centralizada para manter consistência entre futuras integrações.

## Validation & Error Handling

- Requer autenticação do usuário.
- Responder com lista vazia quando nenhum resultado for encontrado.
- Em caso de parâmetros inválidos, retornar erro de requisição malformada.
- Garantir que somente disciplinas do usuário autenticado sejam retornadas.
