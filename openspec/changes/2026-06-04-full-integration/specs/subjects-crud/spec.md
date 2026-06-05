# subjects-crud Specification

## Purpose
Full CRUD for academic subjects in the Streamlit frontend, connected to the existing Xano subjects
endpoints. Adds professor and schedule fields to the subjects table.

## ADDED Requirements

### Requirement: Extended subjects table
The system SHALL store professor name and class schedule alongside the subject name.

#### Scenario: New fields in subjects table
- **WHEN** subjects.xs is updated with `text? professor` and `text? schedule`
- **THEN** the Xano table accepts those fields on create and update

### Requirement: List subjects from Xano
The system SHALL display the authenticated user's subjects from GET /subjects/list.

#### Scenario: User has subjects
- **WHEN** user opens the Disciplinas page
- **THEN** system fetches and displays all subjects with name, professor, schedule

#### Scenario: User has no subjects
- **WHEN** GET /subjects/list returns an empty list
- **THEN** system shows a welcome message with a "Criar primeira disciplina" prompt

### Requirement: Create subject
The system SHALL allow creating a new subject via POST /subjects.

#### Scenario: Valid creation
- **WHEN** user fills name, professor, schedule and submits
- **THEN** system calls POST /subjects and reloads the list

#### Scenario: Duplicate prevention
- **WHEN** a subject with the same name already exists in the list
- **THEN** system shows an error before calling the API

### Requirement: Edit subject
The system SHALL allow editing name, professor, and schedule via PATCH /subjects.

#### Scenario: Valid edit
- **WHEN** user modifies fields and confirms
- **THEN** system calls PATCH /subjects and reloads the list

### Requirement: Delete subject with confirmation
The system SHALL require confirmation before deleting via DELETE /subjects.

#### Scenario: Delete with confirmation
- **WHEN** user clicks delete and confirms
- **THEN** system calls DELETE /subjects and removes it from the list

### Requirement: Search by name
The system SHALL filter subjects by name using GET /subjects/search.

#### Scenario: Name search
- **WHEN** user types a search query and submits
- **THEN** system shows only matching subjects

### Requirement: Filter overdue
The system SHALL show which subjects have overdue tasks using GET /subjects/search with include_overdue.

#### Scenario: Overdue filter
- **WHEN** user enables "Tarefas em atraso" filter
- **THEN** system shows only subjects that have at least one overdue task
