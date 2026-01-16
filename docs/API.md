# API Documentation

Base URL: `/api/`

## Table of Contents

### Core
- [Authentication](#authentication)
  - [User Registration](#user-registration)
  - [Login](#login)
  - [Refresh Token](#refresh-token)
  - [Verify Token](#verify-token)
  - [OAuth Social Login](#oauth-social-login)
  - [Logout](#logout)
  - [Delete Account](#delete-account)

### Course Management
- [Courses](#courses)
  - [List Courses (Public)](#list-courses-public)
  - [Get Course Details (Public)](#get-course-details-public)
  - [Get Course Prerequisites (Public)](#get-course-prerequisites-public)
- [Specializations](#specializations)
  - [List Specializations (Public)](#list-specializations-public)

### Templates & References
- [Checklist Templates](#checklist-templates)
  - [List Checkbox Allowed Courses](#list-checkbox-allowed-courses)
  - [List Additional Constraint Allowed Courses](#list-additional-constraint-allowed-courses)

### User Data Management
- [User Checklists](#user-checklists)
  - [List User Checklists](#list-user-checklists)
  - [Create User Checklist](#create-user-checklist)
  - [Update Checklist Node](#update-checklist-node)
- [User Courses](#user-courses)
  - [List User Courses](#list-user-courses)
  - [Add Course to List](#add-course-to-list)
  - [Remove Course from List](#remove-course-from-list)
- [Course Prerequisite Paths](#course-prerequisite-paths)
  - [List Prerequisite Paths](#list-prerequisite-paths)
  - [Create Prerequisite Path](#create-prerequisite-path)
  - [Delete Prerequisite Path](#delete-prerequisite-path)
- [Additional Constraints](#additional-constraints)
  - [List Additional Constraints](#list-additional-constraints)
  - [Update Additional Constraint](#update-additional-constraint)
- [Depth Lists](#depth-lists)
  - [List Depth Lists](#list-depth-lists)
  - [Create Depth List](#create-depth-list)
  - [Update Depth List](#update-depth-list)

### Reference
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Pagination](#pagination)
- [Filtering, Searching & Ordering](#filtering-searching--ordering)

---

## Authentication

All endpoints require authentication unless explicitly marked as public. Authentication uses JWT tokens stored in `httponly` cookies.

### Auth Endpoints

#### User Registration
```
POST /api/users/
```
Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "password": "securepassword",
  "re_password": "securepassword",
  "start_year": 2024,
  "captcha_token": "token_from_turnstile"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "start_year": 2024
}
```

**Rate Limited:** Yes (SignUpThrottle)

---

#### Login
```
POST /api/jwt/create/
```
Obtain access and refresh tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:** `200 OK` (Tokens set in httponly cookies)
```json
{}
```

**Rate Limited:** Yes (LoginThrottle)

---

#### Refresh Token
```
POST /api/jwt/refresh/
```
Generate a new access token using refresh token from cookies.

**Response:** `200 OK` (New access token set in httponly cookie)

**Rate Limited:** Yes (TokenRefreshThrottle)

---

#### Verify Token
```
POST /api/jwt/verify/
```
Verify the access token from cookies is valid.

**Response:** `200 OK` (if valid)

**Rate Limited:** Yes (TokenVerifyThrottle)

---

#### OAuth Social Login
```
POST /api/o/{provider}/
```
Login using OAuth provider (e.g., Google, GitHub).

**Parameters:**
- `provider` - OAuth provider name (e.g., `google-oauth2`, `github`)

**Request Body:**
```json
{
  "access_token": "oauth_token_from_provider"
}
```

**Response:** `201 Created` (Tokens set in httponly cookies)

**Rate Limited:** Yes (OAuthThrottle)

---

#### Logout
```
POST /api/logout/
```
Clear authentication cookies.

**Response:** `204 No Content`

**Rate Limited:** Yes (LogoutThrottle)

---

#### Delete Account
```
DELETE /api/delete-account/
```
Permanently delete the authenticated user account.

**Response:** `204 No Content` (Tokens cleared)

**Rate Limited:** Yes (DeleteAccountThrottle)

---

## Courses

### List Courses (Public)
```
GET /api/courses/
```
Get paginated list of courses with filtering, searching, and sorting.

**Query Parameters:**
- `code` - Filter by course code (e.g., `CS`)
- `number` - Filter by course number (e.g., `137`)
- `category` - Comma-separated categories (e.g., `math,cs`)
- `min_number` - Minimum course number
- `max_number` - Maximum course number
- `search` - Search by code or number
- `ordering` - Sort by field (code, number, uwflow ratings, etc.)

**Response:** `200 OK`
```json
{
  "count": 100,
  "next": "...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "code": "CS",
      "number": "137",
      "title": "Design of Usable Interactive Systems",
      "num_uwflow_ratings": 42,
      "uwflow_liked_rating": 85,
      "uwflow_easy_ratings": 72,
      "uwflow_useful_ratings": 88
    }
  ]
}
```

---

### Get Course Details (Public)
```
GET /api/courses/{id}/
```
Get detailed information about a specific course.

**Response:** `200 OK`
```json
{
  "id": 1,
  "code": "CS",
  "number": "137",
  "units": 3,
  "title": "Design of Usable Interactive Systems",
  "description": "...",
  "category": ["cs", "hum"],
  "corequisites": "...",
  "antirequisites": "...",
  "num_uwflow_ratings": 42,
  "uwflow_liked_rating": 85,
  "uwflow_easy_ratings": 72,
  "uwflow_useful_ratings": 88
}
```

---

### Get Course Prerequisites (Public)
```
GET /api/prerequisites/?target_course={course_id}
```
Get the prerequisite tree for a course (root nodes only).

**Query Parameters:**
- `target_course` - Course ID (required)

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 10,
      "target_course": { "id": 1, "code": "CS", "number": "137" },
      "node_type": "group",
      "leaf_course": null,
      "num_children_required": 2,
      "children": [
        {
          "node_type": "course",
          "leaf_course": { "id": 5, "code": "CS", "number": "115" }
        }
      ]
    }
  ]
}
```

---

## Specializations

### List Specializations (Public)
```
GET /api/specializations/
```
Get all available specializations/programs.

**Response:** `200 OK`
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "name": "Computer Science",
      "description": "Bachelor of Science in Computer Science"
    }
  ]
}
```

---

## Checklist Templates

### List Checkbox Allowed Courses
```
GET /api/checkbox-allowed-courses/?target_checkbox={checkbox_id}
```
Get list of courses allowed for a specific checklist checkbox (read-only).

**Query Parameters:**
- `target_checkbox` - ChecklistNode ID (required)

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "target_checkbox": 42,
      "courses": [
        { "id": 1, "code": "CS", "number": "137" },
        { "id": 2, "code": "CS", "number": "136" }
      ]
    }
  ]
}
```

---

### List Additional Constraint Allowed Courses
```
GET /api/additional-constraint-allowed-courses/?target_course={constraint_id}
```
Get list of courses allowed for a specific additional constraint (read-only).

**Query Parameters:**
- `target_course` - AdditionalConstraint ID (required)

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "target_checkbox": 42,
      "courses": [
        { "id": 1, "code": "CS", "number": "137" }
      ]
    }
  ]
}
```

---

## User Checklists

### List User Checklists
```
GET /api/user-checklists/
```
Get all checklists for the authenticated user.

**Query Parameters:**
- `year` - Filter by year
- `specialization` - Filter by specialization ID

**Response:** `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "year": 1,
      "specialization": 1,
      "units_required": 36,
      "taken_course_units": 12,
      "planned_course_units": 12,
      "completed": false,
      "nodes": [
        {
          "id": 10,
          "requirement_type": "head",
          "title": "First Year Requirements",
          "units_required": null,
          "units_gathered": null,
          "completed": false,
          "selected_course": null,
          "children": [...]
        }
      ]
    }
  ]
}
```

---

### Create User Checklist
```
POST /api/user-checklists/
```
Create a new checklist for the authenticated user based on a template.

**Request Body:**
```json
{
  "year": 1,
  "specialization": 1
}
```

**Response:** `201 Created`

**Note:** Automatically creates full tree structure with all requirements.

---

### Update Checklist Node
```
PATCH /api/user-checklist-nodes/{id}/
```
Update a checklist node (e.g., mark as complete, select course).

**Request Body:**
```json
{
  "completed": true,
  "selected_course": 5,
  "units_gathered": 3
}
```

**Response:** `200 OK`

**Note:** Automatically updates parent/head nodes when children change.

---

## User Courses

### List User Courses
```
GET /api/user-courses/
```
Get all courses for the authenticated user.

**Query Parameters:**
- `course_list` - Filter by list type: `taken`, `planned`, `wishlist`
- `course__code` - Filter by course code
- `course__number` - Filter by course number
- `category` - Comma-separated categories
- `search` - Search by course code/number
- `ordering` - Sort by field

**Response:** `200 OK`
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "course": { "id": 5, "code": "CS", "number": "137" },
      "course_list": "taken",
      "prereqs_met": null
    }
  ]
}
```

---

### Add Course to List
```
POST /api/user-courses/
```
Add a course to user's taken, planned, or wishlist.

**Request Body:**
```json
{
  "course": 5,
  "course_list": "taken"
}
```

**Response:** `201 Created`

**Note:** Automatically removes from other lists if exists.

---

### Remove Course from List
```
DELETE /api/user-courses/{id}/
```
Remove a course from user's lists.

**Response:** `204 No Content`

---

## Course Prerequisite Paths

### List Prerequisite Paths
```
GET /api/user-path-nodes/?target_course={user_course_id}
```
Get prerequisite path tree for a specific user course.

**Query Parameters:**
- `target_course` - UserCourse ID (required)

**Response:** `200 OK`
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "target_course": 5,
      "prerequisite_node": 10,
      "branch_completed": true,
      "parent": null,
      "children": [...]
    }
  ]
}
```

---

### Create Prerequisite Path
```
POST /api/user-path-nodes/
```
Create prerequisite path tree for a course.

**Request Body:**
```json
{
  "target_course": 5,
  "prerequisite_node": 10,
  "children": [
    {
      "prerequisite_node": 11,
      "children": []
    }
  ]
}
```

**Response:** `201 Created`

**Note:** Deletes existing tree for this course and creates new one.

---

### Delete Prerequisite Path
```
DELETE /api/user-path-nodes/{id}/
```
Remove a prerequisite path node.

**Response:** `204 No Content`

---

## Additional Constraints

### List Additional Constraints
```
GET /api/user-additional-constraints/?target_checklist={checklist_id}
```
Get all additional constraints for a user's checklist.

**Query Parameters:**
- `target_checklist` - UserChecklist ID (required)

**Response:** `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "requirement_type": "group",
      "title": "Breadth Requirements",
      "num_courses_required": 3,
      "num_courses_gathered": 1,
      "completed": false,
      "selected_course": null,
      "children": [...]
    }
  ]
}
```

---

### Update Additional Constraint
```
PATCH /api/user-additional-constraints/{id}/
```
Update an additional constraint (e.g., select a course).

**Request Body:**
```json
{
  "completed": true,
  "selected_course": 5
}
```

**Response:** `200 OK`

---

## Depth Lists

### List Depth Lists
```
GET /api/user-depth-lists/?target_checklist={checklist_id}
```
Get all depth lists for a user's checklist.

**Query Parameters:**
- `target_checklist` - UserChecklist ID (required)

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "target_checklist": 1,
      "is_chain": true,
      "total_units": 12,
      "num_courses": 4,
      "courses": [
        { "id": 5, "course": "CS137" },
        { "id": 6, "course": "CS136" }
      ]
    }
  ]
}
```

---

### Create Depth List
```
POST /api/user-depth-lists/
```
Create a new depth list for course grouping.

**Request Body:**
```json
{
  "target_checklist": 1,
  "is_chain": true,
  "courses": [5, 6, 7]
}
```

**Response:** `201 Created`

---

### Update Depth List
```
PATCH /api/user-depth-lists/{id}/
```
Update depth list courses or properties.

**Request Body:**
```json
{
  "courses": [5, 6, 7, 8],
  "is_chain": false
}
```

**Response:** `200 OK`

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

Common HTTP status codes:
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

---

## Rate Limiting

Different endpoints have different throttle limits:
- **SignUp:** Limited for new user registration
- **Login:** Limited for login attempts
- **OAuth:** Limited for social login
- **Token Refresh:** Limited for token refresh
- **Logout:** Limited for logout attempts
- **Delete Account:** Limited for account deletion

When rate limited, response includes `Retry-After` header.

---

## Pagination

List endpoints support cursor-based pagination:
- `count` - Total number of results
- `next` - URL to next page
- `previous` - URL to previous page
- `results` - Array of items

---

## Filtering, Searching & Ordering

List endpoints support:
- **Filtering** - Query parameters like `?code=CS&year=1`
- **Searching** - `?search=term` searches relevant fields
- **Ordering** - `?ordering=field` or `?ordering=-field` for descending
