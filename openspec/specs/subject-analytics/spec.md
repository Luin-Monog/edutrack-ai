# subject-analytics Specification

## Purpose
TBD - created by archiving change subjects-management-system. Update Purpose after archive.
## Requirements
### Requirement: Subject Summary Statistics
The system SHALL provide authenticated users with summary statistics of their subjects including counts by status and total credits.

#### Scenario: Get subject summary
- **WHEN** an authenticated user sends a GET request to `/subjects/summary`
- **THEN** the system returns aggregated statistics including:
  - Count of active subjects
  - Count of completed subjects
  - Count of archived subjects
  - Total credits across all subjects
  - Total credits for active subjects
  - Total credits for completed subjects

#### Scenario: Summary with no subjects
- **WHEN** an authenticated user with no subjects sends a GET request to `/subjects/summary`
- **THEN** the system returns all counts as zero
- **AND** total credits as zero

### Requirement: Subject Analytics Data
The system SHALL provide detailed analytics data for user subjects including averages and breakdowns.

#### Scenario: Access to analytics data
- **WHEN** the system needs to calculate analytics for a user
- **THEN** it SHALL have access to all subject records with their metadata
- **AND** SHALL be able to aggregate data by status, credits, and creation dates

#### Scenario: Analytics calculations
- **WHEN** calculating subject analytics
- **THEN** the system SHALL compute:
  - Average credits per subject
  - Maximum credits among all subjects
  - Status distribution percentages
  - Total subject count

