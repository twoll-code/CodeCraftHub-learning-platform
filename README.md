CodeCraftHub is a beginner-friendly learning course tracker built with Python and Flask.

The project provides a REST API that allows developers to create, view, update, and delete courses they want to learn. Course data is stored in a simple `courses.json` file, so no database setup is required.

This project is designed to help beginners understand:

- How REST APIs work
- HTTP methods such as `GET`, `POST`, `PUT`, and `DELETE`
- JSON request and response data
- Flask routes
- Reading and writing data to a JSON file
- Basic API validation and error handling

---

## Features

- Create a new course
- View all courses
- View one course by ID
- Update an existing course
- Delete a course
- Automatically generate course IDs
- Store courses in `courses.json`
- Automatically create `courses.json` if it does not exist
- Track course status
- Validate target dates
- Validate required fields
- Validate allowed status values
- Return JSON responses
- Handle missing courses
- Handle invalid JSON
- Handle file read and write errors

---

## Course fields

Each course contains the following fields:

| Field | Description | Required |
|---|---|---|
| `id` | Automatically generated numeric ID | No |
| `name` | Course name | Yes |
| `description` | Course description | Yes |
| `target_date` | Planned completion date in `YYYY-MM-DD` format | Yes |
| `status` | Current learning status | Yes |
| `created_at` | Automatically generated UTC timestamp | No |

### Allowed status values

The `status` field must contain one of these exact values:

```text
Not Started
In Progress
Completed
```

### Example course

```json
{
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST principles.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-10-20T12:30:45.123456+00:00"
}
```

---

## Project structure

```text
codecrafthub/
├── app.py
├── courses.json
└── README.md
```

### `app.py`

Contains the Flask application, routes, validation logic, and JSON file handling.

### `courses.json`

Stores all courses as a JSON array.

Example:

```json
[
    {
        "id": 1,
        "name": "REST API Fundamentals",
        "description": "Learn HTTP methods and REST principles.",
        "target_date": "2026-12-15",
        "status": "Not Started",
        "created_at": "2026-10-20T12:30:45.123456+00:00"
    }
]
```

If this file does not exist when the application starts, the application creates it automatically with an empty list:

```json
[]
```

### `README.md`

Contains project documentation and instructions.

---

# Installation

## Requirements

Before installing CodeCraftHub, make sure you have:

- Python 3.9 or newer
- `pip`
- A terminal or command prompt
- `curl` for testing the API

You can check your Python version with:

```bash
python --version
```

On some systems, you may need to use:

```bash
python3 --version
```

---

## Step 1: Create the project directory

```bash
mkdir codecrafthub
cd codecrafthub
```

---

## Step 2: Create a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

### Windows

```bash
python -m venv venv
```

### macOS or Linux

```bash
python3 -m venv venv
```

---

## Step 3: Activate the virtual environment

### Windows Command Prompt

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
source venv/bin/activate
```

After activation, your terminal may show `(venv)` at the beginning of the command line.

---

## Step 4: Install Flask

```bash
pip install Flask
```

If your system uses `pip3`, run:

```bash
pip3 install Flask
```

---

You do not need to manually create `courses.json`. The application creates it automatically when it starts.

---

# Running the application

From the project directory, activate your virtual environment and run:

```bash
python app.py
```

On macOS or Linux, you may need:

```bash
python3 app.py
```

You should see output similar to:

```text
* Running on http://127.0.0.1:5000
```

The API is now available at:

```text
http://127.0.0.1:5000
```

Keep this terminal window open while testing the API.

To stop the application, press:

```text
Ctrl + C
```

---

# API overview

The API uses the following base URL:

```text
http://127.0.0.1:5000
```

The main resource is:

```text
/api/courses
```

## Available endpoints

| HTTP method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/courses` | Create a new course |
| `GET` | `/api/courses` | Get all courses |
| `GET` | `/api/courses/<id>` | Get one course |
| `PUT` | `/api/courses/<id>` | Update one course |
| `DELETE` | `/api/courses/<id>` | Delete one course |

Replace `<id>` with a real course ID, such as `1`.

For example:

```text
/api/courses/1
```

---

# Understanding the HTTP methods

## `GET`

Used to retrieve data.

Examples:

```text
GET /api/courses
GET /api/courses/1
```

## `POST`

Used to create new data.

Example:

```text
POST /api/courses
```

## `PUT`

Used to update an existing resource.

Example:

```text
PUT /api/courses/1
```

## `DELETE`

Used to remove an existing resource.

Example:

```text
DELETE /api/courses/1
```

---

# API documentation

## Create a course

### Request

```text
POST /api/courses
```

### Example request using `curl`

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST principles.",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

### Request fields

```json
{
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST principles.",
    "target_date": "2026-12-15",
    "status": "Not Started"
}
```

You should not include `id` or `created_at`. The application generates these automatically.

### Successful response

Status:

```text
201 Created
```

Response:

```json
{
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST principles.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-10-20T12:30:45.123456+00:00"
}
```

The actual `created_at` value will be different.

---

## Get all courses

### Request

```text
GET /api/courses
```

### Example using `curl`

```bash
curl http://127.0.0.1:5000/api/courses
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
[
    {
        "id": 1,
        "name": "REST API Fundamentals",
        "description": "Learn HTTP methods, status codes, and REST principles.",
        "target_date": "2026-12-15",
        "status": "Not Started",
        "created_at": "2026-10-20T12:30:45.123456+00:00"
    }
]
```

If there are no courses, the response is:

```json
[]
```

---

## Get one course

### Request

```text
GET /api/courses/<id>
```

### Example using course ID `1`

```bash
curl http://127.0.0.1:5000/api/courses/1
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
    "id": 1,
    "name": "REST API Fundamentals",
    "description": "Learn HTTP methods, status codes, and REST principles.",
    "target_date": "2026-12-15",
    "status": "Not Started",
    "created_at": "2026-10-20T12:30:45.123456+00:00"
}
```

---

## Update a course

### Request

```text
PUT /api/courses/<id>
```

The `PUT` request should include all required fields:

- `name`
- `description`
- `target_date`
- `status`

The `id` and `created_at` values are not changed by an update.

### Example request

```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "REST API Fundamentals - Updated",
    "description": "Learn HTTP methods, status codes, REST principles, and API testing.",
    "target_date": "2026-11-30",
    "status": "In Progress"
  }'
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
    "id": 1,
    "name": "REST API Fundamentals - Updated",
    "description": "Learn HTTP methods, status codes, REST principles, and API testing.",
    "target_date": "2026-11-30",
    "status": "In Progress",
    "created_at": "2026-10-20T12:30:45.123456+00:00"
}
```

---

## Delete a course

### Request

```text
DELETE /api/courses/<id>
```

### Example using course ID `1`

```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

### Successful response

Status:

```text
200 OK
```

Response:

```json
{
    "message": "Course with ID 1 was deleted successfully."
}
```

---

# HTTP status codes

The API uses standard HTTP status codes.

| Status code | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | A new course was created |
| `400 Bad Request` | The request contains invalid data |
| `404 Not Found` | The course or endpoint does not exist |
| `405 Method Not Allowed` | The HTTP method is not supported |
| `500 Internal Server Error` | A server or file storage error occurred |

---

# Error responses

## Missing required fields

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

Response:

```text
400 Bad Request
```

```json
{
    "error": "Missing required fields: description, status, target_date"
}
```

---

## Invalid status

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Status Course",
    "description": "This course uses an invalid status.",
    "target_date": "2026-12-15",
    "status": "Started"
  }'
```

Response:

```text
400 Bad Request
```

```json
{
    "error": "Invalid status. Status must be one of: Completed, In Progress, Not Started"
}
```

Only these values are accepted:

```text
Not Started
In Progress
Completed
```

---

## Invalid target date format

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Invalid Date Course",
    "description": "This course uses an invalid date format.",
    "target_date": "15-12-2026",
    "status": "Not Started"
  }'
```

Response:

```text
400 Bad Request
```

```json
{
    "error": "target_date must use YYYY-MM-DD format."
}
```

The correct format is:

```text
2026-12-15
```

---

## Invalid calendar date

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Impossible Date Course",
    "description": "This course uses a date that does not exist.",
    "target_date": "2026-02-31",
    "status": "Not Started"
  }'
```

Response:

```text
400 Bad Request
```

```json
{
    "error": "target_date must be a valid calendar date."
}
```

---

## Course not found

Request:

```bash
curl http://127.0.0.1:5000/api/courses/9999
```

Response:

```text
404 Not Found
```

```json
{
    "error": "Course with ID 9999 was not found."
}
```

The same type of error occurs when updating or deleting a course that does not exist.

---

## Invalid JSON

Request:

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{"name": "Incomplete JSON"'
```

Response:

```text
400 Bad Request
```

```json
{
    "error": "Request body must contain valid JSON."
}
```

---

# Testing the API

## Basic test sequence

Start the application:

```bash
python app.py
```

Then open another terminal window and run the following commands.

### 1. Create a course

```bash
curl -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn variables, functions, and Python data structures.",
    "target_date": "2026-12-01",
    "status": "Not Started"
  }'
```

### 2. Get all courses

```bash
curl http://127.0.0.1:5000/api/courses
```

### 3. Get course ID `1`

```bash
curl http://127.0.0.1:5000/api/courses/1
```

### 4. Update course ID `1`

```bash
curl -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Basics",
    "description": "Learn Python variables, functions, classes, and data structures.",
    "target_date": "2026-11-15",
    "status": "In Progress"
  }'
```

### 5. Delete course ID `1`

```bash
curl -X DELETE http://127.0.0.1:5000/api/courses/1
```

### 6. Confirm the course was deleted

```bash
curl http://127.0.0.1:5000/api/courses/1
```

Expected result:

```json
{
    "error": "Course with ID 1 was not found."
}
```

---

## Showing response status codes

Add `-i` to a `curl` command to display the HTTP status code and response headers:

```bash
curl -i http://127.0.0.1:5000/api/courses
```

For a successful course creation, use:

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask Testing",
    "description": "Learn how to test Flask APIs.",
    "target_date": "2027-01-15",
    "status": "Not Started"
  }'
```

You should see a response beginning with something similar to:

```text
HTTP/1.1 201 CREATED
Content-Type: application/json
```

---

## Testing with a web browser

You can open `GET` endpoints in a browser:

```text
http://127.0.0.1:5000/api/courses
```

You can also open a specific course:

```text
http://127.0.0.1:5000/api/courses/1
```

Browsers are useful for `GET` requests. To test `POST`, `PUT`, and `DELETE`, use `curl`, Postman, Insomnia, or another API client.

---

# Data storage

CodeCraftHub stores data in a local JSON file instead of a database.

The file is named:

```text
courses.json
```

The file contains a JSON array:

```json
[]
```

When a course is added, it becomes:

```json
[
    {
        "id": 1,
        "name": "Python Basics",
        "description": "Learn Python programming.",
        "target_date": "2026-12-01",
        "status": "Not Started",
        "created_at": "2026-10-20T12:30:45.123456+00:00"
    }
]
```

When the API receives a request, it:

1. Reads the JSON file.
2. Converts the JSON into Python data.
3. Adds, updates, or removes a course.
4. Writes the updated data back to the file.

This approach is simple and useful for learning. For a large or multi-user production application, a database would be more appropriate.

---

# Troubleshooting

## `python` command is not recognized

Try:

```bash
python3 --version
```

If that works, run the application with:

```bash
python3 app.py
```

On Windows, reinstall Python and make sure you select:

```text
Add Python to PATH
```

during installation.

---

## Flask is not installed

If you see an error such as:

```text
ModuleNotFoundError: No module named 'flask'
```

Activate your virtual environment and install Flask:

```bash
pip install Flask
```

Then try again:

```bash
python app.py
```

---

## The virtual environment is not activated

You can activate it again with:

### Windows Command Prompt

```bash
venv\Scripts\activate
```

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
source venv/bin/activate
```

---

## PowerShell does not allow activation scripts

PowerShell may display an execution policy error. Open PowerShell as an administrator and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try:

```powershell
venv\Scripts\Activate.ps1
```

---

## Connection refused

If `curl` displays a connection error, make sure the Flask application is running:

```bash
python app.py
```

Also verify that you are using the correct URL:

```text
http://127.0.0.1:5000
```

---

## Port 5000 is already in use

Another application may already be using port `5000`.

You can change the port in `app.py`:

```python
app.run(
    host="127.0.0.1",
    port=5001,
    debug=True
)
```

Then use:

```text
http://127.0.0.1:5001
```

For example:

```bash
curl http://127.0.0.1:5001/api/courses
```

---

## `courses.json` contains invalid JSON

If the file was manually edited and contains invalid JSON, the API may return a file error.

For a development project, stop the application and replace the contents of `courses.json` with:

```json
[]
```

Then restart the application.

Be aware that this removes the existing course data.

---

## Permission denied when writing `courses.json`

Make sure:

- You have permission to write to the project directory.
- `courses.json` is not read-only.
- The application is running from the expected project folder.

On macOS or Linux, check the file permissions with:

```bash
ls -l courses.json
```

On Windows, check the file properties and make sure it is not marked as read-only.

---

## `curl` is not available

On many macOS and Linux systems, `curl` is already installed.

On Windows, try using:

- Windows Terminal
- PowerShell
- Git Bash
- Postman
- Insomnia

PowerShell also supports commands such as:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/courses
```

---

## JSON payload errors on Windows

Shell quoting rules can differ on Windows. If a multi-line `curl` command does not work, place the JSON on one line:

```bash
curl -X POST http://127.0.0.1:5000/api/courses -H "Content-Type: application/json" -d "{\"name\":\"Python Basics\",\"description\":\"Learn Python programming.\",\"target_date\":\"2026-12-01\",\"status\":\"Not Started\"}"
```

Using Postman or Insomnia can also make JSON requests easier on Windows.

---

# Learning REST API concepts

CodeCraftHub demonstrates the basic REST pattern:

```text
Resource: courses
```

The resource is accessed through URLs:

```text
/api/courses
/api/courses/1
```

Different HTTP methods perform different actions:

| Action | HTTP method | URL |
|---|---|---|
| Create a course | `POST` | `/api/courses` |
| Read all courses | `GET` | `/api/courses` |
| Read one course | `GET` | `/api/courses/1` |
| Update a course | `PUT` | `/api/courses/1` |
| Delete a course | `DELETE` | `/api/courses/1` |

The API sends and receives JSON data using the following header:

```text
Content-Type: application/json
```

---

# Limitations

This project intentionally uses a JSON file to keep the code easy to understand.

It is not designed for:

- Multiple users
- Authentication
- Concurrent writes from many users
- Large amounts of data
- Production deployment
- Advanced searching or filtering
- Database transactions

For a larger application, consider using:

- SQLite
- PostgreSQL
- MySQL
- User authentication
- Automated tests
- A production WSGI server

---

# Future improvements

Possible improvements include:

- Add a web-based frontend
- Add filtering by status
- Add search by course name
- Add course categories
- Add progress percentages
- Add user accounts
- Replace the JSON file with SQLite
- Add automated unit tests
- Add API documentation using Swagger or OpenAPI
- Deploy the API to a cloud platform

---

# License

This project is intended for learning and educational purposes.
