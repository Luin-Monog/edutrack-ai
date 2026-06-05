# Proposal: Reino Fungi & Underdark — Visual Redesign + Feature Evolution

## Why

The remaining checklist items require new backend fields, a new Reports page, and a complete
visual identity. The theme chosen by the user — Reino Fungi & Underdark — draws from deep
underground bioluminescent aesthetics: dark cave purples, glowing cyan spore accents, amethyst
borders, and mushroom-orange highlights.

## What Changes

### Backend (XanoScript)
1. `tables/subjects.xs` — add `text? semester` (ex: "2026.1") and `bool? archived?=false`
2. `tables/academic_tasks.xs` — add `enum priority?=media { Baixa, Media, Alta }`
3. `apis/subjects/subjects_create_POST.xs` — accept `semester`, `archived`
4. `apis/subjects/subjects_update_PATCH.xs` — accept `semester`, `archived`
5. `apis/academic_tasks/tasks_create_POST.xs` — accept `priority`
6. `apis/academic_tasks/tasks_update_PATCH.xs` — accept `priority`

### Frontend (Streamlit)
7. `utils/theme.py` — shared CSS constants for the Fungi/Underdark palette
8. `app.py` — apply new theme globally; improve login/signup layout
9. `pages/1_📚_Disciplinas.py` — add semester field, archive/unarchive button,
   progress bar per subject (% tasks completed), priority badge
10. `pages/2_📝_Tarefas.py` — add priority field (Baixa/Média/Alta) with color badges
11. `pages/4_📊_Relatorios.py` — new page: progress per subject, tasks by period,
    CSV export (disciplines + tasks)

## Visual Identity — Reino Fungi & Underdark

| Token          | Value     | Usage                          |
|----------------|-----------|--------------------------------|
| `bg-deep`      | `#080612` | Page background                |
| `bg-surface`   | `#120d24` | Cards, sidebar                 |
| `bg-elevated`  | `#1e1438` | Inputs, expanders              |
| `border`       | `#3b1f72` | Card borders                   |
| `accent-violet`| `#8b5cf6` | Primary buttons, active tab    |
| `accent-cyan`  | `#22d3ee` | Glowing highlights, badges     |
| `accent-fungi` | `#f97316` | Overdue, warnings              |
| `accent-spore` | `#c084fc` | Secondary labels               |
| `text-primary` | `#ede9fe` | Headings                       |
| `text-muted`   | `#a78bfa` | Captions, descriptions         |
| `success`      | `#4ade80` | Completed, ok states           |

Glowing effects via `box-shadow` with cyan/violet on interactive elements.

## Impact

- No existing data is lost; new fields are nullable with defaults.
- Subjects and tasks keep all existing functionality.
- New Reports page is additive only.
- All pages get the new theme; login screen gets a redesigned hero layout.
