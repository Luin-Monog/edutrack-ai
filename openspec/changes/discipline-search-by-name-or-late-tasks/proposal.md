## Why

O fluxo atual de disciplinas permite listar conteúdos, mas não oferece uma busca combinada por texto ou por tarefas vencidas. Esse endpoint de busca melhora a descoberta das disciplinas e ajuda o usuário a localizar rapidamente matérias com pendências, especialmente quando há integração com tarefas acadêmicas.

## What Changes

- Criar uma nova capacidade de busca de disciplinas com filtro por nome e por tarefas atrasadas.
- Introduzir um endpoint dedicado para buscar disciplinas do usuário com lógica de combinação OR.
- Integrar uma rotina em Python para avaliar tarefas vencidas e aplicar o filtro de forma reutilizável.

## Capabilities

### New Capabilities
- `subject-search`: busca de disciplinas por nome e por tarefas atrasadas.

### Modified Capabilities
- 

## Impact

- Adiciona um novo endpoint de busca ligado ao domínio de disciplinas.
- Requer leitura de `subjects` e `academic_tasks` para montar a seleção de resultados.
- Introduz lógica Python reutilizável para detectar pendências vencidas e combinar filtros.
