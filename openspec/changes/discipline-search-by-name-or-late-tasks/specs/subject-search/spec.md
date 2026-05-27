# subject-search Specification

## Purpose

Permitir que usuários encontrem disciplinas por texto ou por presença de tarefas atrasadas, usando uma busca centrada em resultados úteis e acionáveis.

## ADDED Requirements

### Requirement: Subject search by name or overdue tasks

The system SHALL allow authenticated users to search their own subjects through a dedicated endpoint that combines name matching with overdue task detection.

#### Scenario: Search subjects by partial name
- **WHEN** an authenticated user sends a GET request to `/subjects/search?query=python`
- **THEN** the system returns subjects owned by the user whose name or description contains `python`
- **AND** includes only disciplines from the authenticated user

#### Scenario: Search returns subjects with overdue tasks
- **WHEN** an authenticated user sends a GET request to `/subjects/search`
- **THEN** the system identifies overdue academic tasks using the current date and task status
- **AND** returns subjects linked to those overdue tasks

#### Scenario: Combined OR filtering
- **WHEN** an authenticated user searches for a term and the subject has overdue tasks
- **THEN** the system returns the subject when either the name matches the search term or the subject has overdue tasks

#### Scenario: No matches
- **WHEN** no subject matches the search term and no overdue tasks are found
- **THEN** the system returns an empty list
