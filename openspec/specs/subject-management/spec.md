# subject-management Specification

## Purpose
TBD - created by archiving change subjects-management-system. Update Purpose after archive.
## Requirements
### Requirement: Subject Creation
The system SHALL allow authenticated users to create new academic subjects with required fields (name) and optional fields (description, code, semester, credits, status, metadata).

#### Scenario: Successful subject creation
- **WHEN** an authenticated user sends a POST request to `/subjects/create` with valid subject data
- **THEN** the system creates a new subject record linked to the user's ID
- **AND** returns the created subject with all provided fields plus timestamps

#### Scenario: Subject creation with missing required fields
- **WHEN** an authenticated user sends a POST request to `/subjects/create` without the required name field
- **THEN** the system returns a validation error
- **AND** no subject record is created

### Requirement: Subject Retrieval
The system SHALL allow authenticated users to retrieve their own subjects with optional filtering and pagination.

#### Scenario: List all user subjects
- **WHEN** an authenticated user sends a GET request to `/subjects/list`
- **THEN** the system returns all subjects owned by the user
- **AND** includes pagination metadata (limit, offset, total count)

#### Scenario: List subjects with status filter
- **WHEN** an authenticated user sends a GET request to `/subjects/list?status=active`
- **THEN** the system returns only subjects with status "active" owned by the user

#### Scenario: Get specific subject
- **WHEN** an authenticated user sends a GET request to `/subjects/get?subject_id={id}`
- **THEN** the system returns the subject if it belongs to the user
- **AND** returns a not found error if the subject doesn't exist or belongs to another user

### Requirement: Subject Update
The system SHALL allow authenticated users to update their own subjects with partial data.

#### Scenario: Successful subject update
- **WHEN** an authenticated user sends a PATCH request to `/subjects/update` with valid subject_id and update data
- **THEN** the system updates only the provided fields
- **AND** returns the updated subject record
- **AND** updates the updated_at timestamp

#### Scenario: Update non-owned subject
- **WHEN** an authenticated user sends a PATCH request to `/subjects/update` with a subject_id that doesn't belong to them
- **THEN** the system returns an access denied error
- **AND** no data is modified

### Requirement: Subject Deletion
The system SHALL allow authenticated users to delete their own subjects.

#### Scenario: Successful subject deletion
- **WHEN** an authenticated user sends a DELETE request to `/subjects/delete` with a valid subject_id
- **THEN** the system permanently removes the subject record
- **AND** returns a success confirmation

#### Scenario: Delete non-owned subject
- **WHEN** an authenticated user sends a DELETE request to `/subjects/delete` with a subject_id that doesn't belong to them
- **THEN** the system returns an access denied error
- **AND** no data is modified

