# feature-notas-atividades Proposal

## Purpose
Permitir que o professor lance notas para os alunos em atividades específicas.

## Why
Professores precisam registrar avaliações por atividade para manter histórico acadêmico, permitir feedback e calcular médias. Atualmente não há um endpoint específico para o envio de notas por atividade. Esta mudança implementa o mecanismo mínimo necessário para que um professor informe uma nota para um aluno numa atividade.

## Scope (escalonado)
- IN SCOPE: criação da tabela `activity_grades` e implementação de uma API POST `/activity_grades` para que o professor envie uma nota para um aluno em uma atividade específica.
- OUT OF SCOPE: consultas/ listagens (GET), edição (PATCH) ou exclusão (DELETE) de notas, relatórios agregados, interfaces de frontend.

## What Changes
- Banco: nova tabela `activity_grades` para armazenar lançamentos de notas.
- API: novo endpoint POST `/activity_grades` que aceita `activity_id`, `student_id`, `grade` e campos opcionais (`comment`).
- Regras de negócio: validação de permissões (somente usuário com papel `teacher`), verificação de vínculo da atividade e do aluno à mesma conta/organização, validação de intervalo de nota.

## Impact
- Migration DB: adicionar `activity_grades`.
- Segurança: endpoint protegido; somente professores autenticados podem usar.
- Dependências: assume existência de tabelas/recursos de `activities` (ou `academic_tasks`) e `users`.

## Constraints / Guiding Rules
- Seguir as diretrizes do projeto EduTrack AI (agents/AGENTS.md). Em especial: manter escopo limitado ao solicitado pelo usuário — NÃO criar endpoints de listagem ou leitura a menos que solicitado.
- `openspec/AGENTS.md` não foi encontrado no repositório; aplicando as regras definidas em `agents/AGENTS.md` como fallback.
