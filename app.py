import streamlit as st
import subprocess
import json
import sys
import os
from datetime import datetime

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="EduTrack AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS customizado ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* Cards de disciplina */
.subject-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: .75rem;
    transition: border-color .2s;
}
.subject-card:hover { border-color: #6366f1; }
.subject-card h4 { color: #e2e8f0; margin: 0 0 .3rem; font-size: 1rem; }
.subject-card p  { color: #94a3b8; margin: 0; font-size: .85rem; }
.tag-overdue {
    background: #7f1d1d; color: #fca5a5;
    border-radius: 6px; padding: 2px 8px;
    font-size: .75rem; font-weight: 600;
}
.tag-ok {
    background: #14532d; color: #86efac;
    border-radius: 6px; padding: 2px 8px;
    font-size: .75rem; font-weight: 600;
}

/* Metric overrides */
[data-testid="metric-container"] {
    background: #1e293b;
    border-radius: 10px;
    padding: .75rem 1rem;
    border: 1px solid #334155;
}
</style>
""", unsafe_allow_html=True)

# ── Dados de demo (simulam retorno do Xano) ──────────────────────────────────
DEMO_SUBJECTS = [
    {"id": 1, "name": "Cálculo Diferencial", "description": "Limites, derivadas e integrais"},
    {"id": 2, "name": "Python para Data Science", "description": "Pandas, NumPy e visualização"},
    {"id": 3, "name": "Banco de Dados Relacionais", "description": "SQL, modelagem e normalização"},
    {"id": 4, "name": "Estruturas de Dados", "description": "Listas, árvores, grafos e algoritmos"},
    {"id": 5, "name": "Inteligência Artificial", "description": "Machine learning e redes neurais"},
]

DEMO_TASKS = [
    {"id": 1, "subject_id": 1, "title": "Lista 3 – Derivadas", "due_date": "2024-03-01", "status": "pending"},
    {"id": 2, "subject_id": 1, "title": "Prova parcial",        "due_date": "2024-04-10", "status": "pending"},
    {"id": 3, "subject_id": 3, "title": "Diagrama ER",          "due_date": "2024-02-20", "status": "pending"},
    {"id": 4, "subject_id": 2, "title": "Projeto final",        "due_date": "2099-12-31", "status": "pending"},
    {"id": 5, "subject_id": 5, "title": "Artigo de revisão",    "due_date": "2024-01-15", "status": "completed"},
]

# ── Helpers ───────────────────────────────────────────────────────────────────
PYTHON_EXE = os.path.join(os.path.dirname(__file__), ".venv", "Scripts", "python.exe")
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "scripts", "subject_search.py")


def run_search(subjects, tasks, query="", include_overdue=False):
    """Chama o script Python de busca como subprocesso e retorna o resultado."""
    cmd = [
        PYTHON_EXE, SCRIPT_PATH,
        "--subjects", json.dumps(subjects, ensure_ascii=False),
        "--tasks",    json.dumps(tasks,    ensure_ascii=False),
        "--query",    query,
    ]
    if include_overdue:
        cmd.append("--include-overdue")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        if result.returncode != 0:
            st.error(f"Erro no script de busca:\n{result.stderr}")
            return []
        return json.loads(result.stdout)
    except Exception as exc:
        st.error(f"Falha ao executar busca: {exc}")
        return []


def count_overdue(subject_id, tasks):
    today = datetime.now()
    count = 0
    for t in tasks:
        if t.get("subject_id") != subject_id:
            continue
        if t.get("status", "").lower() == "completed":
            continue
        try:
            from dateutil import parser as dp
            if dp.parse(str(t["due_date"])) < today:
                count += 1
        except Exception:
            pass
    return count


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 EduTrack AI")
    st.markdown("---")
    menu = st.radio(
        "Navegar",
        ["🏠 Dashboard", "🔍 Busca de Disciplinas", "📋 Tarefas"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Innovation Lab · v0.2.0")

# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
if menu == "🏠 Dashboard":
    st.title("🏠 Dashboard")
    st.markdown("Bem-vindo ao **EduTrack AI** — seu assistente acadêmico inteligente.")

    today = datetime.now()
    total_subjects = len(DEMO_SUBJECTS)
    overdue_tasks  = sum(
        1 for t in DEMO_TASKS
        if t.get("status", "") != "completed"
        and __import__("dateutil.parser", fromlist=["parse"]).parse(str(t["due_date"])) < today
        if True
    )
    pending_tasks = sum(1 for t in DEMO_TASKS if t.get("status") != "completed")

    col1, col2, col3 = st.columns(3)
    col1.metric("📚 Disciplinas",       total_subjects)
    col2.metric("⏰ Tarefas Atrasadas", overdue_tasks,  delta=f"-{overdue_tasks} em atraso", delta_color="inverse")
    col3.metric("📝 Tarefas Pendentes", pending_tasks)

    st.markdown("---")
    st.subheader("Disciplinas com Tarefas Atrasadas")

    overdue_results = run_search(DEMO_SUBJECTS, DEMO_TASKS, query="", include_overdue=False)
    if overdue_results:
        for s in overdue_results:
            n = count_overdue(s["id"], DEMO_TASKS)
            st.markdown(
                f'<div class="subject-card"><h4>{s["name"]} '
                f'<span class="tag-overdue">⚠ {n} atrasada{"s" if n>1 else ""}</span></h4>'
                f'<p>{s.get("description","")}</p></div>',
                unsafe_allow_html=True,
            )
    else:
        st.success("🎉 Nenhuma disciplina com tarefas atrasadas!")

# ═════════════════════════════════════════════════════════════════════════════
# BUSCA DE DISCIPLINAS
# ═════════════════════════════════════════════════════════════════════════════
elif menu == "🔍 Busca de Disciplinas":
    st.title("🔍 Busca de Disciplinas")
    st.markdown(
        "Encontre disciplinas pelo **nome** ou veja quais têm **tarefas atrasadas**. "
        "O filtro usa o script Python `scripts/subject_search.py` diretamente."
    )

    col_q, col_flag = st.columns([3, 1])
    with col_q:
        query_input = st.text_input(
            "Buscar por nome ou descrição",
            placeholder="ex: python, banco de dados…",
            key="search_query",
        )
    with col_flag:
        st.markdown("<br>", unsafe_allow_html=True)
        include_overdue = st.checkbox("Incluir atrasadas", value=True, key="include_overdue")

    if st.button("🔎 Buscar", type="primary", use_container_width=True):
        with st.spinner("Executando busca…"):
            results = run_search(
                DEMO_SUBJECTS, DEMO_TASKS,
                query=query_input,
                include_overdue=include_overdue,
            )

        st.markdown(f"**{len(results)} resultado(s) encontrado(s)**")
        st.markdown("---")

        if results:
            for s in results:
                n_late = count_overdue(s["id"], DEMO_TASKS)
                tag = (
                    f'<span class="tag-overdue">⚠ {n_late} atrasada{"s" if n_late>1 else ""}</span>'
                    if n_late else
                    '<span class="tag-ok">✓ Em dia</span>'
                )
                st.markdown(
                    f'<div class="subject-card"><h4>{s["name"]} {tag}</h4>'
                    f'<p>{s.get("description","")}</p></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("Nenhuma disciplina encontrada para os critérios informados.")

    # Instrução do endpoint Xano
    with st.expander("📡 Como integrar ao Xano"):
        st.markdown("""
**Endpoint criado:** `GET /subjects/search`

| Parâmetro | Tipo | Descrição |
|---|---|---|
| `query` | string (opcional) | Termo para busca textual |
| `include_overdue` | bool (opcional) | Inclui disciplinas com tarefas atrasadas |

**Fluxo no Xano:**
1. Busca `subjects` e `academic_tasks` do usuário autenticado
2. Chama o sidecar Python via `external.request → POST http://localhost:8787/search`
3. Retorna a lista filtrada

**Para rodar o sidecar:**
```bash
.venv\\Scripts\\python sidecar_search_api.py
```
""")

# ═════════════════════════════════════════════════════════════════════════════
# TAREFAS
# ═════════════════════════════════════════════════════════════════════════════
elif menu == "📋 Tarefas":
    st.title("📋 Gerenciamento de Tarefas")

    today = datetime.now()
    for task in DEMO_TASKS:
        subject = next((s for s in DEMO_SUBJECTS if s["id"] == task["subject_id"]), {})
        subject_name = subject.get("name", "—")
        from dateutil import parser as dp
        try:
            due = dp.parse(str(task["due_date"]))
            due_str = due.strftime("%d/%m/%Y")
            is_late  = due < today and task.get("status") != "completed"
        except Exception:
            due_str = task["due_date"]
            is_late  = False

        status_icon = "✅" if task.get("status") == "completed" else ("🔴" if is_late else "🟡")
        st.markdown(
            f'<div class="subject-card">'
            f'<h4>{status_icon} {task["title"]}</h4>'
            f'<p>📚 {subject_name} &nbsp;|&nbsp; 📅 {due_str}'
            f'{" &nbsp;|&nbsp; <span class=\'tag-overdue\'>Atrasada</span>" if is_late else ""}'
            f'</p></div>',
            unsafe_allow_html=True,
        )