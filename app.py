"""
CodeCraftHub - Course Tracking REST API

This Flask application provides CRUD operations for courses and stores
course data in a local JSON file named "courses.json".

Run the application with:

    python app.py

The API will be available at:

    http://127.0.0.1:5000
"""

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request


# -------------------------------------------------------------------
# Flask application setup
# -------------------------------------------------------------------

app = Flask(__name__)


# Store courses.json in the same directory as this app.py file.
DATA_FILE = Path(__file__).parent / "courses.json"


# These are the only valid course statuses.
VALID_STATUSES = {
    "Not Started",
    "In Progress",
    "Completed",
}


# This regular expression ensures the date has exactly YYYY-MM-DD format.
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# -------------------------------------------------------------------
# Custom error class
# -------------------------------------------------------------------

class StorageError(Exception):
    """
    Custom exception used when there is a problem reading or writing
    the courses.json file.
    """

    pass


# -------------------------------------------------------------------
# JSON file helper functions
# -------------------------------------------------------------------

def ensure_data_file():
    """
    Create courses.json automatically if it does not already exist.

    The initial file contains an empty JSON list because courses will
    be stored as a list of objects.
    """

    if not DATA_FILE.exists():
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)
        except OSError as error:
            raise StorageError(
                f"Unable to create the data file: {error}"
            ) from error


def load_courses():
    """
    Read and return all courses from courses.json.

    Returns:
        list: A list of course dictionaries.

    Raises:
        StorageError: If the file cannot be read or contains invalid JSON.
    """

    # Make sure the file exists before trying to read it.
    ensure_data_file()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            courses = json.load(file)

    except OSError as error:
        raise StorageError(
            f"Unable to read the data file: {error}"
        ) from error

    except json.JSONDecodeError as error:
        raise StorageError(
            "The data file contains invalid JSON."
        ) from error

    # The JSON file should contain a list of courses.
    if not isinstance(courses, list):
        raise StorageError(
            "The data file must contain a JSON list."
        )

    return courses


def save_courses(courses):
    """
    Save all courses to courses.json.

    Args:
        courses (list): The list of course dictionaries.

    Raises:
        StorageError: If the file cannot be written.
    """

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(courses, file, indent=4)

    except OSError as error:
        raise StorageError(
            f"Unable to write to the data file: {error}"
        ) from error


def get_next_course_id(courses):
    """
    Generate the next course ID.

    IDs start at 1. The next ID is one greater than the highest
    existing ID. Deleted IDs are not reused.
    """

    if not courses:
        return 1

    highest_id = max(course.get("id", 0) for course in courses)
    return highest_id + 1


def get_current_timestamp():
    """
    Return the current UTC time as an ISO 8601 timestamp.

    Example:
        2026-10-20T12:30:45.123456+00:00
    """

    return datetime.now(timezone.utc).isoformat()


# -------------------------------------------------------------------
# Validation helper functions
# -------------------------------------------------------------------

def validate_course_data(data):
    """
    Validate the data sent by the client when creating or updating
    a course.

    Returns:
        str or None:
        An error message if validation fails, otherwise None.
    """

    # These fields must be supplied by the client.
    required_fields = {
        "name",
        "description",
        "target_date",
        "status",
    }

    # Check for missing fields.
    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return (
            "Missing required fields: "
            + ", ".join(sorted(missing_fields))
        )

    # name must be a non-empty string.
    if not isinstance(data["name"], str) or not data["name"].strip():
        return "name is required and must be a non-empty string."

    # description must be a non-empty string.
    if (
        not isinstance(data["description"], str)
        or not data["description"].strip()
    ):
        return (
            "description is required and must be "
            "a non-empty string."
        )

    # status must be one of the allowed values.
    if data["status"] not in VALID_STATUSES:
        return (
            "Invalid status. Status must be one of: "
            + ", ".join(sorted(VALID_STATUSES))
        )

    # Validate the target date.
    target_date = data["target_date"]

    if not isinstance(target_date, str):
        return "target_date must be a string in YYYY-MM-DD format."

    if not DATE_PATTERN.fullmatch(target_date):
        return "target_date must use YYYY-MM-DD format."

    try:
        # This catches invalid dates such as 2026-02-31.
        date.fromisoformat(target_date)
    except ValueError:
        return "target_date must be a valid calendar date."

    return None


def find_course_by_id(courses, course_id):
    """
    Find a course by its numeric ID.

    Returns:
        dict or None: The matching course, if found.
    """

    for course in courses:
        if course.get("id") == course_id:
            return course

    return None


# -------------------------------------------------------------------
# Error handlers
# -------------------------------------------------------------------

@app.errorhandler(StorageError)
def handle_storage_error(error):
    """
    Return a helpful JSON response when a file read or write fails.
    """

    return jsonify({
        "error": str(error)
    }), 500


@app.errorhandler(404)
def handle_not_found(error):
    """
    Handle requests sent to an endpoint that does not exist.
    """

    return jsonify({
        "error": "The requested endpoint was not found."
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    """
    Handle requests using an unsupported HTTP method.
    """

    return jsonify({
        "error": "The HTTP method is not allowed for this endpoint."
    }), 405


# -------------------------------------------------------------------
# REST API routes
# -------------------------------------------------------------------

@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Add a new course.

    Endpoint:
        POST /api/courses
    """

    # silent=True prevents Flask from raising an exception for invalid
    # JSON. Instead, it returns None, which we handle below.
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    # Validate all required course fields.
    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    # Read existing courses.
    courses = load_courses()

    # Build the new course object.
    new_course = {
        "id": get_next_course_id(courses),
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "target_date": data["target_date"],
        "status": data["status"],
        "created_at": get_current_timestamp(),
    }

    # Add and save the new course.
    courses.append(new_course)
    save_courses(courses)

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
def get_all_courses():
    """
    Return all courses.

    Endpoint:
        GET /api/courses
    """

    courses = load_courses()

    return jsonify(courses), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    Return statistics about all courses.

    Endpoint:
        GET /api/courses/stats
    """

    # Load all courses from courses.json.
    courses = load_courses()

    # Start every status at zero so the response includes statuses
    # even when no courses currently use them.
    courses_by_status = {
        "Not Started": 0,
        "In Progress": 0,
        "Completed": 0,
    }

    # Count each course according to its status.
    for course in courses:
        status = course.get("status")

        if status in courses_by_status:
            courses_by_status[status] += 1

    # Return the total and the status breakdown.
    return jsonify({
        "total_courses": len(courses),
        "courses_by_status": courses_by_status,
    }), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Return one course by ID.

    Endpoint:
        GET /api/courses/<id>
    """

    courses = load_courses()
    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Update an existing course.

    The request must include all required course fields.

    Endpoint:
        PUT /api/courses/<id>
    """

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must contain valid JSON."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object."
        }), 400

    # Validate the incoming course data.
    validation_error = validate_course_data(data)

    if validation_error:
        return jsonify({
            "error": validation_error
        }), 400

    courses = load_courses()
    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Update only fields that the client is allowed to change.
    # The ID and created_at timestamp remain unchanged.
    course["name"] = data["name"].strip()
    course["description"] = data["description"].strip()
    course["target_date"] = data["target_date"]
    course["status"] = data["status"]

    save_courses(courses)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.

    Endpoint:
        DELETE /api/courses/<id>
    """

    courses = load_courses()
    course = find_course_by_id(courses, course_id)

    if course is None:
        return jsonify({
            "error": f"Course with ID {course_id} was not found."
        }), 404

    # Remove the course from the list and save the updated list.
    courses.remove(course)
    save_courses(courses)

    return jsonify({
        "message": f"Course with ID {course_id} was deleted successfully."
    }), 200


# -------------------------------------------------------------------
# Start the application
# -------------------------------------------------------------------

if __name__ == "__main__":
    # Create courses.json before starting the development server.
    # If creation fails, the error is displayed clearly.
    try:
        ensure_data_file()
    except StorageError as error:
        print(f"Startup error: {error}")
        raise SystemExit(1)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )