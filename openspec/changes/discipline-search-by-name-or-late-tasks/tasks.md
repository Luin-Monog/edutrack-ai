# discipline-search-by-name-or-late-tasks Tasks

- [x] Criar o helper Python em `scripts/subject_search.py` para calcular vencimento de tarefas e montar os critérios de busca.
- [x] Implementar o endpoint `GET /subjects/search` com autenticação do usuário e filtro por nome/atraso (`apis/subjects/3586207_subjects_search_GET.xs`).
- [x] Conectar o endpoint à leitura de `subjects` e `academic_tasks`, retornando somente disciplinas da conta do usuário autenticado.
- [x] Criar sidecar FastAPI (`sidecar_search_api.py`) para expor o script Python como microserviço HTTP (porta 8787), consumível via `external.request` no Xano.
- [x] Construir o app Streamlit (`app.py`) com Dashboard, Busca integrada ao script Python e Gerenciamento de Tarefas.
- [ ] Validar o comportamento com cenários de busca por termo, disciplinas com tarefas atrasadas e ausência de resultados (testes de integração com Xano real).
