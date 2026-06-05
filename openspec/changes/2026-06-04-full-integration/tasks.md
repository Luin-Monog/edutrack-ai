# Tasks — Full System Integration

## Backend (XanoScript)

- [x] BK-01: Add `text? professor` and `text? schedule` fields to `tables/subjects.xs`
- [x] BK-02: Update `apis/subjects/subjects_create_POST.xs` to accept professor and schedule
- [x] BK-03: Update `apis/subjects/subjects_update_PATCH.xs` to accept professor and schedule
- [x] BK-04: Create `apis/academic_tasks/api_group.xs`
- [x] BK-05: Create `apis/academic_tasks/tasks_create_POST.xs`
- [x] BK-06: Create `apis/academic_tasks/tasks_list_GET.xs`
- [x] BK-07: Create `apis/academic_tasks/tasks_get_GET.xs`
- [x] BK-08: Create `apis/academic_tasks/tasks_update_PATCH.xs`
- [x] BK-09: Create `apis/academic_tasks/tasks_complete_PATCH.xs`
- [x] BK-10: Create `apis/academic_tasks/tasks_delete_DELETE.xs`

## Frontend (Streamlit)

- [x] FE-01: Create `.streamlit/secrets.toml` with XANO_BASE_URL placeholder
- [x] FE-02: Create `utils/__init__.py`
- [x] FE-03: Create `utils/xano_client.py` — HTTP client with Bearer token injection
- [x] FE-04: Rewrite `app.py` — auth gate + connected dashboard (real Xano data)
- [x] FE-05: Rewrite `pages/1_📚_Disciplinas.py` — full CRUD connected to Xano
- [x] FE-06: Rewrite `pages/2_📝_Tarefas.py` — full CRUD connected to Xano
- [x] FE-07: Rewrite `pages/3_👤_Perfil.py` — profile view/edit + logout
