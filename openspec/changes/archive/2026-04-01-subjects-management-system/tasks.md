## 1. Database Schema

- [x] 1.1 Create subject table schema in Xano with all required fields
- [x] 1.2 Add appropriate indexes for performance (user_id, status, created_at)
- [x] 1.3 Verify table relationships with existing user table

## 2. Security Functions

- [x] 2.1 Create validate_subject_ownership function for property checks
- [x] 2.2 Test ownership validation with different user scenarios
- [x] 2.3 Add error handling for security violations

## 3. CRUD API Endpoints

- [x] 3.1 Create subjects API group in Xano
- [x] 3.2 Implement POST /subjects/create endpoint with validation
- [x] 3.3 Implement GET /subjects/list endpoint with pagination and filters
- [x] 3.4 Implement GET /subjects/get endpoint with ownership verification
- [x] 3.5 Implement PATCH /subjects/update endpoint with partial updates
- [x] 3.6 Implement DELETE /subjects/delete endpoint with ownership checks

## 4. Analytics Endpoints

- [x] 4.1 Implement GET /subjects/summary endpoint for basic statistics
- [x] 4.2 Add credit calculations and status breakdowns
- [x] 4.3 Test analytics with various data scenarios

## 5. Testing and Validation

- [x] 5.1 Test all CRUD operations with proper authentication
- [x] 5.2 Verify data isolation between users
- [x] 5.3 Test error scenarios (unauthorized access, invalid data)
- [x] 5.4 Validate pagination and filtering functionality

## 6. Documentation

- [x] 6.1 Update system context documentation
- [x] 6.2 Document API endpoints and usage
- [x] 6.3 Add examples for common use cases