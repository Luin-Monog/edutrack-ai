# tasks-crud Specification

## Purpose
Full CRUD for academic tasks in the Streamlit frontend, backed by new Xano endpoints for the
academic_tasks table. All tasks are linked to a subject and filtered by the authenticated user.

## ADDED Requirements

### Requirement: Xano academic_tasks API group
The system SHALL expose REST endpoints for academic_tasks.

#### Scenario: Create task
- **WHEN** POST /academic_tasks is called with title, description, due_date, subject_id
- **THEN** system creates a record with user_id = $auth.id and status = "pending"

#### Scenario: List tasks
- **WHEN** GET /academic_tasks/list is called
- **THEN** system returns all tasks where user_id == $auth.id

#### Scenario: Get single task
- **WHEN** GET /academic_tasks/get is called with task_id
- **THEN** system returns the task if it belongs to $auth.id

#### Scenario: Update task
- **WHEN** PATCH /academic_tasks/update is called with task_id and updated fields
- **THEN** system validates ownership and updates the record

#### Scenario: Mark complete
- **WHEN** PATCH /academic_tasks/complete is called with task_id
- **THEN** system sets status = "completed" on the task

#### Scenario: Delete task
- **WHEN** DELETE /academic_tasks/delete is called with task_id
- **THEN** system validates ownership and deletes the record

### Requirement: List tasks in frontend
The system SHALL display the user's tasks from GET /academic_tasks/list, grouped by subject.

#### Scenario: Tasks displayed with overdue badge
- **WHEN** a task's due_date < today and status != completed
- **THEN** system shows a red "Atrasada" badge next to the task title

### Requirement: Create task in frontend
The system SHALL allow creating a task linked to an existing subject.

#### Scenario: Valid task creation
- **WHEN** user fills title, description, due_date, selects subject and submits
- **THEN** system calls POST /academic_tasks and reloads the list

### Requirement: Edit task in frontend
The system SHALL allow editing title, description, due_date, and status.

#### Scenario: Valid edit
- **WHEN** user modifies fields and confirms
- **THEN** system calls PATCH /academic_tasks/update and reloads

### Requirement: Mark task as complete
The system SHALL allow marking a task as complete with one click.

#### Scenario: Mark complete
- **WHEN** user clicks "Marcar como Concluída"
- **THEN** system calls PATCH /academic_tasks/complete and updates status display

### Requirement: Delete task with confirmation
The system SHALL require confirmation before deleting a task.

#### Scenario: Delete with confirmation
- **WHEN** user clicks delete and confirms
- **THEN** system calls DELETE /academic_tasks/delete and removes task from list

### Requirement: Filter tasks by status
The system SHALL allow filtering tasks by Todas / Pendente / Em andamento / Concluída.

#### Scenario: Status filter
- **WHEN** user selects a status from the filter dropdown
- **THEN** system shows only tasks matching that status
