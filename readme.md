### Bus Route CLI Application

A command-line interface (CLI) application for managing bus routes, drivers, residents, and delivery schedules. This Flask-based application provides interactive commands for user management, scheduling, status updates, and communication between drivers and residents.

## Features

User Management: Create and list drivers and residents
Scheduling: Schedule drives for drivers to specific streets
Driver Operations: Update driver status and location, view driver inbox
Resident Operations: Request stops from drivers, view resident inbox
Testing: Run unit and integration tests

## Prerequisites

Python 3.7+
Flask
Click
Pytest
Flask-Migrate (for database migrations)

## Installation

Clone the repository:
```
git clone <repository-url>
cd <project-directory>
```
Install dependencies:
```
pip install -r requirements.txt
```
Initialize the database:
```
flask init
```

## Usage

Database Initialization

```
flask init
```
Creates and initializes the database with any required seed data.

## User Management

Create a new user:

```
flask user create
```
Prompts for:

Username
Password (hidden input)
Role (DRIVER or RESIDENT)
Street (if resident)
List all users:

```
flask user list
```
or for raw JSON output:

```
flask user list json
```

## Scheduling

Schedule a drive:

```
flask schedule drive
```
Prompts for:

Driver user ID
Street name 

## Driver Operations

Update status or view inbox:

```
flask driver status
```
Prompts for:

Driver user ID
Action ('set' to update status/location or 'get' to view inbox)
If setting status, also prompts for:

Status (OFF_DUTY, EN_ROUTE, DELIVERING)
Location note (optional)

## Resident Operations

Request a stop from a driver:

```
flask request stop
```
Prompts for:

Resident user ID
Confirmation to proceed
Driver user ID to request
Optional note

## Inbox Management

View inbox messages:

```
flask inbox
```
Prompts for:

Role (DRIVER or RESIDENT)
User ID

## Testing

Run all tests:

```
flask test
```
Run user unit tests:

```
flask test user unit
```
Run user integration tests:

```
flask test user int
```

## Command Summary

Command	Description
flask init	            Initialize database
flask user create	    Create new user (interactive)
flask user list	        List all users
flask schedule drive	Schedule drive for driver
flask driver status	    Update driver status or view inbox
flask request stop	    Request stop from driver
flask inbox	            View inbox messages
flask test	            Run test suite

## User Roles

DRIVER: Can schedule drives, update status, view inbox messages from residents
RESIDENT: Can request stops from drivers, view inbox messages from drivers

## Status Types

Drivers can have one of three statuses:

OFF_DUTY: Not currently working
EN_ROUTE: Traveling to destination
DELIVERING: Actively making deliveries

## Project Structure

text
App/
├── controllers/    # Business logic and command handlers
├── database/       # Database configuration and models
├── main.py         # Application factory
└── tests/          # Test suites

## Development

The application uses:

Flask for the web framework
Click for CLI command creation
Flask-Migrate for database migrations
Pytest for testing
To add new commands, follow the existing pattern of creating AppGroups and adding commands to them.

## 🧪 Testing and Validation

### Overview
The BreadVan / Bus Route CLI application includes both **automated backend testing** (via Pytest) and **API-level testing** (via Postman).  
These tests ensure that all features — from user creation to drive scheduling — work as intended and remain stable during updates.

---

## ⚙️ Pytest (Unit and Integration Tests)

### Description
Pytest is used to verify the functionality of individual modules (unit tests) and their combined workflows (integration tests).  
The tests cover:
- User creation and authentication  
- Database relationships (Drivers, Residents, Drives)  
- Drive scheduling and status updates  
- Resident stop requests and inbox communication

### Test Files
All test scripts are located in the `App/tests/` directory:
```
App/tests/
├── test_unit_models.py          # Verifies model behavior and relationships
├── test_unit_controllers.py     # Validates user creation, updates, and grouping logic
├── test_integration_api.py      # End-to-end API flow tests
└── test_app.py                  # Combined test suite entry point
```

### Commands

Run all tests:
```
pytest -q
```

Run detailed test output:
```
pytest -v
```

Clean and re-run tests:
```
find App -name "__pycache__" -type d -exec rm -rf {} + && pytest -q
```

Expected output:
```
=================================== test session starts ===================================
collected 13 items
App/tests/test_app.py ....................                           [100%]
=================================== 13 passed in 0.24s ====================================
```

### Coverage
| Component | Description | Example Test |
|------------|-------------|---------------|
| User Model | Checks password hashing and JSON output | `test_user_password_hashing()` |
| Controllers | Ensures create/update/list user functions work correctly | `test_create_user_and_list_grouped()` |
| Auth Logic | Validates JWT issuance and authentication flow | `test_authenticate()` |
| Drives & Requests | Simulates full driver–resident interaction | `test_schedule_and_status_update()` |

---

## 🌐 Postman API Testing

### Description
Postman tests simulate **real API requests** to validate the application’s REST endpoints and ensure end-to-end reliability.  
The collection automates login, user creation, drive scheduling, status updates, and stop requests using stored environment variables.

### Setup
1. Import the Postman collection:  
   ```
   /postman/BreadVan.postman_collection.json
   ```
2. Create a Postman environment:
   ```
   base_url = http://127.0.0.1:8080
   jwt = (leave blank)
   ```
3. Start the Flask app:
   ```
   flask --app wsgi.py run
   ```
4. Log in via `/api/auth/login` to auto-populate your JWT.
5. Run the full collection in **Collection Runner** using your environment.

### Key Tests
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/api/auth/login` | POST | Authenticates user, retrieves JWT |
| `/api/users` | GET | Returns grouped drivers and residents |
| `/api/users` | POST | Creates new driver or resident |
| `/api/users/<id>` | PUT | Updates username |
| `/api/drives` | POST | Creates a scheduled drive for a driver |
| `/api/drivers/<id>/status` | PUT | Updates driver status/location |
| `/api/requests` | POST | Resident requests or confirms stop |
| `/api/inbox/resident/<id>` | GET | Retrieves resident inbox |
| `/api/inbox/driver/<id>` | GET | Retrieves driver inbox |

### Running the Tests
In Postman:
1. Click **Runner → BreadVan API Collection**
2. Choose your **BreadVan Local Environment**
3. Click **Run Collection**
4. Confirm that all tests show **green “PASS”** indicators.

Expected result:
```
Collection run complete — 10/10 tests passed ✅
Total time: ~1.2s
Environment: BreadVan Local Env
```

---

## 📊 Test Reporting

| Test Category | Tool | Scope | Result |
|----------------|------|-------|--------|
| Unit Tests | Pytest | Models, Controllers | ✅ Passed |
| Integration Tests | Pytest | End-to-End Flow | ✅ Passed |
| API Tests | Postman | REST Endpoints | ✅ Passed |

---

## 🧾 Notes
- All endpoints except `/api/auth/login` require `Authorization: Bearer <jwt>`.  
- The local database uses SQLite by default.  
- Pytest runs against a clean, in-memory test DB each time.  
- Postman variables (`jwt`, `driverNo`, `residentNo`) are dynamically updated between requests.  
- Both test suites ensure the system adheres to RESTful conventions and business rules.

---
