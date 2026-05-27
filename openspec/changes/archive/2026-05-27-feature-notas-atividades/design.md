# feature-notas-atividades Design

## Overview
Esta seção descreve a modelagem e o fluxo para permitir que um professor lance uma nota para um aluno em uma atividade específica. O objetivo é implementar uma solução mínima, segura e compatível com XanoScript/Xano, seguindo as diretrizes do projeto.

## Data model (tabela `activity_grades`)
- `id` (UUID / serial): identificador único.
- `activity_id` (UUID / integer): referência à atividade (ex.: `activities` ou `academic_tasks`).
- `student_id` (UUID / integer): referência ao usuário-aluno (`users.user_id`).
- `grade` (decimal): valor da nota. Recomendado usar `decimal(5,2)` ou número real, validar intervalo.
- `scale` (text)? optional: por exemplo `percentage` ou `points` — opcional, dependendo da política local.
- `comment` (text, nullable): observações do professor.
- `created_by` (UUID / integer): id do usuário que lançou a nota (professor).
- `created_at` (timestamp): timestamp de criação.
- `updated_at` (timestamp, nullable): timestamp de atualização (se aplicável).

Constraints/Index:
- FK `activity_id` → activities (se existir) e `student_id` → users.
- Índice em `(activity_id, student_id)` para consulta rápida por lançamento (mesmo que GET não seja implementado agora).

## API: POST /activity_grades
Request body (JSON):
```
{
  "activity_id": "<id>",
  "student_id": "<id>",
  "grade": 87.5,
  "comment": "opcional"
}
```

Behavior:
- Autenticação obrigatória.
- Autorization: somente usuários com papel `teacher` podem executar.
- Verificações:
  - `activity_id` existe e pertence à mesma `account` do professor.
  - `student_id` existe e pertence à mesma `account` da atividade (ou do professor).
  - `grade` está dentro do intervalo permitido (por ex. 0–100) — valores inválidos retornam 400.
- Side effects:
  - Persistir registro em `activity_grades` com `created_by` = current user.
  - Criar um `event_log` (se aplicável) para auditoria (opcional, dependendo de políticas internas).

## Validation & Errors
- 400 Bad Request: missing or invalid fields.
- 401 Unauthorized: sem autenticação.
- 403 Forbidden: usuário não tem papel `teacher` ou não tem vínculo com a atividade/conta.
- 404 Not Found: `activity` ou `student` não encontrados.

## Notes on Implementation
- Antes de criar qualquer arquivo `.xs` de tabela ou função, consulte os guidelines em `docs/` mencionados em `agents/AGENTS.md`. Se os guidelines não existirem, seguir este design e pedir revisão humana.
- Manter escopo mínimo: implementar apenas o POST para lançamento de notas.
