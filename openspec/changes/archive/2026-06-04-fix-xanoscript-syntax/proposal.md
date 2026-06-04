## Why

Os endpoints da feature `subjects` foram implementados com primitivas XanoScript incorretas, impedindo a integração com o banco de dados Xano. Os erros são de dois tipos: uso de `db.get` para queries multi-registro (quando o correto é `db.query` com cláusula `where`), e lógica de precondições invertida na função de validação de propriedade. Adicionalmente, a tabela `academic_tasks` não possui o campo `user_id`, bloqueando o endpoint de search.

## What Changes

- Corrigir `apis/subjects/3586202_subjects_list_GET.xs`: substituir `db.get` por `db.query` com filtro por `user_id`
- Corrigir `apis/subjects/3586206_subjects_summary_GET.xs`: substituir `db.get` por `db.query` e ajustar response para retornar contagem
- Corrigir `apis/subjects/3586207_subjects_search_GET.xs`: substituir `db.get` por `db.query` nos dois fetches e corrigir filtro de `academic_tasks` (sem `user_id` direto — buscar via subjects do usuário)
- Corrigir `functions/getting_started_template/267288_validate_subject_ownership.xs`: inverter as condições das precondições (lógica estava ao contrário)
- Adicionar campo `user_id` na tabela `tables/749169_academic_tasks.xs` para viabilizar filtro direto por usuário

## Capabilities

### Modified Capabilities
- `subject-management`: Endpoints list, get, create, update, delete passam a funcionar corretamente com o banco de dados
- `subject-security`: Função `validate_subject_ownership` passa a rejeitar acessos indevidos corretamente
- `subject-search`: Endpoint de search passa a buscar academic_tasks corretamente via relação de ownership

## Impact

- **APIs subjects**: 3 endpoints corrigidos (list, summary, search)
- **Função de segurança**: `validate_subject_ownership` corrigida — impacto crítico em qualquer endpoint que a utilize
- **Tabela `academic_tasks`**: Adição de coluna `user_id` (schema change no Xano — requer push e migration)
- **Sem breaking changes** para os endpoints que já funcionam (create, get, update, delete)
