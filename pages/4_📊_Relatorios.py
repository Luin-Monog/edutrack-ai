import io
import csv
import streamlit as st
from datetime import datetime, timezone

import utils.xano_client as api
from utils.theme import UNDERDARK_CSS, SPORE_DIVIDER

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
st.markdown(UNDERDARK_CSS, unsafe_allow_html=True)

if "token" not in st.session_state:
    st.warning("Faça login primeiro.")
    st.page_link("app.py", label="Ir para o Login", icon="🔑")
    st.stop()

with st.sidebar:
    st.markdown(f"<div style='color:#a78bfa; font-size:.85rem;'>👤 {st.session_state.get('user_name','Usuário')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪 Sair", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("# 📊 Relatórios & Progresso")
st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)


# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner="Carregando dados do reino…")
def load(_token: str):
    subjects = api.subjects_list()
    tasks    = api.tasks_list()
    return subjects, tasks

try:
    subjects, tasks = load(st.session_state["token"])
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()


def _due_dt(task: dict):
    raw = task.get("due_date")
    if raw is None:
        return None
    try:
        return datetime.fromtimestamp(int(raw) / 1000, tz=timezone.utc)
    except Exception:
        return None


today = datetime.now(tz=timezone.utc)
subj_map = {s["id"]: s for s in subjects}

# ── Summary metrics ────────────────────────────────────────────────────────────
total_subj   = len([s for s in subjects if not s.get("archived")])
total_tasks  = len(tasks)
done_tasks   = len([t for t in tasks if t.get("status") == "completed"])
overdue_tasks= len([t for t in tasks if t.get("status") != "completed" and (d:=_due_dt(t)) and d < today])
progress_pct = int(done_tasks / total_tasks * 100) if total_tasks else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("📚 Disciplinas ativas",   total_subj)
c2.metric("📝 Total de tarefas",     total_tasks)
c3.metric("✅ Concluídas",           done_tasks)
c4.metric("⏰ Em atraso",            overdue_tasks)

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

# ── Progress per subject ───────────────────────────────────────────────────────
st.markdown("### 🌿 Progresso por Disciplina")

active_subjs = [s for s in subjects if not s.get("archived")]
if not active_subjs:
    st.info("Nenhuma disciplina ativa.")
else:
    for s in active_subjs:
        s_tasks = [t for t in tasks if t.get("subject_id") == s["id"]]
        s_done  = [t for t in s_tasks if t.get("status") == "completed"]
        s_over  = [t for t in s_tasks if t.get("status") != "completed" and (d:=_due_dt(t)) and d < today]
        pct = int(len(s_done) / len(s_tasks) * 100) if s_tasks else 0

        col_name, col_bar, col_stats = st.columns([2, 3, 2])
        with col_name:
            sem = f" · {s['semester']}" if s.get("semester") else ""
            st.markdown(f"**{s['name']}**{sem}")
        with col_bar:
            st.progress(pct / 100)
        with col_stats:
            overdue_badge = f'<span class="badge-overdue">⚠ {len(s_over)} atrasada{"s" if len(s_over)>1 else ""}</span>' if s_over else '<span class="badge-ok">✓ Em dia</span>'
            st.markdown(
                f'{pct}% &nbsp; ({len(s_done)}/{len(s_tasks)}) &nbsp; {overdue_badge}',
                unsafe_allow_html=True,
            )
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

# ── Tasks by status (bar chart) ────────────────────────────────────────────────
st.markdown("### 📈 Tarefas por Status")
col_chart, col_prio = st.columns(2)

with col_chart:
    try:
        import pandas as pd
        status_counts = {"Pendente": 0, "Em andamento": 0, "Concluída": 0}
        for t in tasks:
            s = t.get("status", "pending")
            if s == "pending":        status_counts["Pendente"] += 1
            elif s == "in_progress":  status_counts["Em andamento"] += 1
            elif s == "completed":    status_counts["Concluída"] += 1
        df_status = pd.DataFrame({"Status": list(status_counts.keys()), "Qtd": list(status_counts.values())})
        st.bar_chart(df_status.set_index("Status"), color="#8b5cf6")
    except Exception:
        st.info("Instale pandas para ver o gráfico.")

with col_prio:
    st.markdown("**Por Prioridade**")
    prio_counts = {"Alta": 0, "Média": 0, "Baixa": 0}
    for t in tasks:
        p = t.get("priority", "media")
        if p == "alta":   prio_counts["Alta"] += 1
        elif p == "media": prio_counts["Média"] += 1
        elif p == "baixa": prio_counts["Baixa"] += 1

    for label, count in prio_counts.items():
        pct_p = int(count / total_tasks * 100) if total_tasks else 0
        badge = "badge-alta" if label == "Alta" else "badge-media" if label == "Média" else "badge-baixa"
        st.markdown(
            f'<span class="{badge}">{label}</span> &nbsp; **{count}** tarefas ({pct_p}%)',
            unsafe_allow_html=True,
        )
        st.progress(pct_p / 100)

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

# ── Tasks by period (upcoming 30 days) ────────────────────────────────────────
st.markdown("### 📅 Tarefas por Prazo (próximas 30 dias)")
upcoming = sorted(
    [t for t in tasks if t.get("status") != "completed" and (d:=_due_dt(t)) and d >= today],
    key=lambda t: _due_dt(t),
)
if not upcoming:
    st.info("Nenhuma tarefa pendente com prazo definido.")
else:
    for t in upcoming[:20]:
        d       = _due_dt(t)
        due_str = d.strftime("%d/%m/%Y") if d else "—"
        days    = (d - today).days if d else 0
        subj    = subj_map.get(t.get("subject_id"), {}).get("name", "—")
        prio    = t.get("priority", "media")
        badge   = "badge-alta" if prio == "alta" else "badge-media" if prio == "media" else "badge-baixa"
        urgency = "🔴" if days <= 3 else "🟠" if days <= 7 else "🟢"
        st.markdown(
            f'<div class="fungi-card" style="margin-bottom:.4rem;">'
            f'<h4>{urgency} {t["title"]} <span class="{badge}" style="font-size:.7rem">{prio.capitalize()}</span></h4>'
            f'<p>📅 {due_str} · em {days} dia{"s" if days!=1 else ""} &nbsp;|&nbsp; 📚 {subj}</p></div>',
            unsafe_allow_html=True,
        )

st.markdown(SPORE_DIVIDER, unsafe_allow_html=True)

# ── CSV Export ─────────────────────────────────────────────────────────────────
st.markdown("### 💾 Exportar Dados")
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    # Export disciplines
    buf_s = io.StringIO()
    writer = csv.writer(buf_s)
    writer.writerow(["id", "name", "professor", "schedule", "semester", "description", "archived"])
    for s in subjects:
        writer.writerow([
            s.get("id"), s.get("name"), s.get("professor",""),
            s.get("schedule",""), s.get("semester",""),
            s.get("description",""), s.get("archived", False),
        ])
    st.download_button(
        label="📥 Exportar Disciplinas (CSV)",
        data=buf_s.getvalue().encode("utf-8"),
        file_name=f"edutrack_disciplinas_{today.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with col_exp2:
    # Export tasks
    buf_t = io.StringIO()
    writer = csv.writer(buf_t)
    writer.writerow(["id", "title", "description", "due_date", "status", "priority", "subject"])
    for t in tasks:
        d       = _due_dt(t)
        due_str = d.strftime("%Y-%m-%d") if d else ""
        subj    = subj_map.get(t.get("subject_id"), {}).get("name", "")
        writer.writerow([
            t.get("id"), t.get("title"), t.get("description",""),
            due_str, t.get("status",""), t.get("priority",""), subj,
        ])
    st.download_button(
        label="📥 Exportar Tarefas (CSV)",
        data=buf_t.getvalue().encode("utf-8"),
        file_name=f"edutrack_tarefas_{today.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
