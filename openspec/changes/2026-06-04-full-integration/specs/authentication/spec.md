# authentication Specification

## Purpose
Define the authentication flow for the EduTrack AI Streamlit frontend, connecting to the existing
Xano auth endpoints (login, signup, profile, password-reset).

## ADDED Requirements

### Requirement: Auth gate
The system SHALL block access to all pages until the user authenticates.

#### Scenario: Unauthenticated visit
- **WHEN** a user opens the app without a valid token in session_state
- **THEN** system displays a Login/Signup screen (not the dashboard)

#### Scenario: Successful login
- **WHEN** user submits valid email + password to POST /auth/login
- **THEN** system stores the returned authToken in st.session_state and redirects to dashboard

#### Scenario: Successful signup
- **WHEN** user submits name + email + password to POST /auth/signup
- **THEN** system stores the returned authToken and redirects to dashboard

#### Scenario: Logout
- **WHEN** user clicks "Sair" in the sidebar
- **THEN** system clears st.session_state and returns to the login screen

### Requirement: Token persistence across pages
The system SHALL maintain the JWT token in st.session_state so every page can send authenticated requests.

#### Scenario: Navigating between pages
- **WHEN** user navigates from Disciplinas to Tarefas
- **THEN** the token remains in session_state and all API calls include Authorization header

### Requirement: Profile view and edit
The system SHALL allow the user to view their name and email and update them.

#### Scenario: View profile
- **WHEN** user opens the Perfil page
- **THEN** system calls GET /auth/me and displays current name and email

#### Scenario: Edit profile
- **WHEN** user submits changes to PATCH /user/edit_profile
- **THEN** system displays a success message and refreshes displayed data
