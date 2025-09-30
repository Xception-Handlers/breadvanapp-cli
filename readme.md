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