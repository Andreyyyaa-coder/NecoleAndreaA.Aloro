
import sqlite3
import requests
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

DATABASE = "students.db"

# Classmate's deployed API
CLASSMATE_API_URL = (
    "https://balcenajessicaann-2axr.onrender.com/api/students"
)


# DATABASE CONNECTION
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# VALIDATE STUDENT DATA
def get_student_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return None, "Valid JSON data is required."

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if field not in data:
            return None, f"Missing required field: {field}"

        if data[field] is None or str(data[field]).strip() == "":
            return None, f"{field} cannot be empty."

    try:
        year = int(data["year"])
    except (TypeError, ValueError):
        return None, "Year must be a whole number."

    if year < 1 or year > 6:
        return None, "Year must be between 1 and 6."

    return {
        "student_id": str(data["student_id"]).strip(),
        "name": str(data["name"]).strip(),
        "program": str(data["program"]).strip(),
        "year": year,
        "section": str(data["section"]).strip()
    }, None


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# ORIGINAL STUDENT INFORMATION
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00286",
        "name": "Necole Andrea Aloro",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# GREETING ENDPOINT
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Necole")
    return jsonify({"message": f"Hello, {name}!"})


# COURSE INFORMATION
@app.route("/course")
def say_course():
    return jsonify({
        "course_code": "IT3120",
        "course_title": "System Integration",
        "instructor": "Dr. Rene Arduo",
        "semester": "First Semester",
        "academic_year": "AY 2026-2027"
    })


# CUSTOM GREETING
@app.route("/greet")
def greet():
    name = request.args.get("name", "Necole Andrea Aloro")
    program = request.args.get("program", "BSIT")
    year = request.args.get("year", "3")
    section = request.args.get("section", "A")

    return jsonify({
        "message": f"Hello {name} from {program} {year} {section}!"
    })


# PROFILE
@app.route("/profile")
def get_profile():
    return jsonify({
        "student_id": "24-00286",
        "name": "Necole Andrea Aloro",
        "program": "BSIT",
        "year": 3,
        "section": "A",
        "gmail": "aloronecoleandrea@isufst.edu.ph",
        "skills": "Mobile gaming, editing"
    })


# ENTERTAINMENT
@app.route("/entertainment")
def get_entertainment():
    return jsonify({
        "favorite_movie": "Avengers: Endgame",
        "favorite_song": "Die With A Smile",
        "favorite_game": "Mobile Legends",
        "hobby": "Watching movies and playing mobile games"
    })


# GET ALL STUDENTS
@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve students")
        return jsonify({"error": "Unable to retrieve students."}), 500
    finally:
        conn.close()


# GET ONE STUDENT BY DATABASE ID
@app.route("/students/<int:id>", methods=["GET"])
def get_student_by_id(id):
    conn = get_db_connection()
    try:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?", (id,)
        ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve student")
        return jsonify({"error": "Unable to retrieve student."}), 500
    finally:
        conn.close()


# FILTER STUDENTS BY PROGRAM
@app.route("/students/program/<string:program>", methods=["GET"])
def get_students_by_program(program):
    conn = get_db_connection()
    try:
        rows = conn.execute(
            """SELECT * FROM students
               WHERE LOWER(program) = LOWER(?)
               ORDER BY id""",
            (program,)
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    except sqlite3.Error:
        app.logger.exception("Unable to filter students")
        return jsonify({"error": "Unable to filter students."}), 500
    finally:
        conn.close()


# GET ALL STUDENTS THROUGH CRUD API
@app.route("/api/students", methods=["GET"])
def api_students():
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()
        return jsonify([dict(row) for row in rows])
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve API records")
        return jsonify({"error": "Unable to retrieve records."}), 500
    finally:
        conn.close()


# CREATE STUDENT / RECEIVE EXTERNAL RECORD
@app.route("/api/students", methods=["POST"])
def add_student():
    data, error = get_student_data()

    if error:
        return jsonify({"error": error}), 400

    raw_data = request.get_json(silent=True) or {}
    source = raw_data.get("source", "External API")

    if not isinstance(source, str) or not source.strip():
        source = "External API"

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO students
               (student_id, name, program, year, section, source)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                source.strip()
            )
        )
        conn.commit()

        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify({
            "message": "Student added successfully.",
            "student": dict(student)
        }), 201

    except sqlite3.Error:
        conn.rollback()
        app.logger.exception("Unable to add student")
        return jsonify({"error": "Unable to add student."}), 500
    finally:
        conn.close()


# GET ONE STUDENT THROUGH CRUD API
@app.route("/api/students/<int:id>", methods=["GET"])
def api_get_student(id):
    conn = get_db_connection()
    try:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?", (id,)
        ).fetchone()

        if student is None:
            return jsonify({"error": "Student not found"}), 404

        return jsonify(dict(student))
    except sqlite3.Error:
        app.logger.exception("Unable to retrieve API student")
        return jsonify({"error": "Unable to retrieve student."}), 500
    finally:
        conn.close()


# UPDATE STUDENT
@app.route("/api/students/<int:id>", methods=["PUT"])
def update_student(id):
    data, error = get_student_data()

    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?", (id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Student not found"}), 404

        conn.execute(
            """UPDATE students
               SET student_id = ?, name = ?, program = ?,
                   year = ?, section = ?
               WHERE id = ?""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                id
            )
        )
        conn.commit()

        updated_student = conn.execute(
            "SELECT * FROM students WHERE id = ?", (id,)
        ).fetchone()

        return jsonify({
            "message": "Student updated successfully.",
            "student": dict(updated_student)
        })
    except sqlite3.Error:
        conn.rollback()
        app.logger.exception("Unable to update student")
        return jsonify({"error": "Unable to update student."}), 500
    finally:
        conn.close()


# DELETE STUDENT
@app.route("/api/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    conn = get_db_connection()
    try:
        existing = conn.execute(
            "SELECT id FROM students WHERE id = ?", (id,)
        ).fetchone()

        if existing is None:
            return jsonify({"error": "Student not found"}), 404

        conn.execute("DELETE FROM students WHERE id = ?", (id,))
        conn.commit()

        return jsonify({"message": "Student deleted successfully."})
    except sqlite3.Error:
        conn.rollback()
        app.logger.exception("Unable to delete student")
        return jsonify({"error": "Unable to delete student."}), 500
    finally:
        conn.close()


# RETRIEVE PARTNER RECORDS
@app.route("/partner-records", methods=["GET"])
def partner_records():
    try:
        response = requests.get(CLASSMATE_API_URL, timeout=15)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            for key in ("students", "data", "results"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break

        if not isinstance(data, list):
            return jsonify({
                "error": "Partner API did not return a student list."
            }), 502

        return jsonify(data)

    except requests.Timeout:
        return jsonify({"error": "Partner API request timed out."}), 504
    except (requests.RequestException, ValueError):
        app.logger.exception("Partner API request failed")
        return jsonify({
            "error": "Unable to retrieve partner data."
        }), 502


# CLASSMATE API PROXY (EXISTING ROUTE)
@app.route("/classmate-students", methods=["GET"])
def get_classmate_students():
    try:
        response = requests.get(CLASSMATE_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict):
            for key in ("students", "data", "results"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break

        if not isinstance(data, list):
            return jsonify({
                "error": "The classmate API did not return a student list."
            }), 502

        return jsonify(data)

    except requests.Timeout:
        return jsonify({
            "error": "The classmate API took too long to respond."
        }), 504
    except (requests.RequestException, ValueError):
        app.logger.exception("Classmate API request failed")
        return jsonify({
            "error": "Could not retrieve classmate records."
        }), 502


# IMPORT A PARTNER RECORD INTO MY DATABASE
@app.route("/import-student", methods=["POST"])
def import_student():
    data, error = get_student_data()

    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO students
               (student_id, name, program, year, section, source)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"],
                "Classmate API"
            )
        )
        conn.commit()

        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return jsonify({
            "message": "Remote record saved successfully!",
            "student": dict(student)
        }), 201

    except sqlite3.Error:
        conn.rollback()
        app.logger.exception("Partner record import failed")
        return jsonify({
            "error": "Could not save the partner record."
        }), 500
    finally:
        conn.close()


# SEND A STUDENT RECORD TO THE PARTNER API
@app.route("/send-to-partner", methods=["POST"])
def send_to_partner():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "message": "No student data received."
        }), 400

    required_fields = [
        "student_id", "name", "program", "year", "section"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({
                "success": False,
                "message": f"Missing required field: {field}"
            }), 400

    try:
        payload = {
            "student_id": str(data["student_id"]).strip(),
            "name": str(data["name"]).strip(),
            "program": str(data["program"]).strip(),
            "year": int(data["year"]),
            "section": str(data["section"]).strip(),
            "source": "Partner API"
        }

        response = requests.post(
            CLASSMATE_API_URL,
            json=payload,
            timeout=30
        )

        try:
            partner_result = response.json()
        except ValueError:
            partner_result = {"response": response.text[:500]}

        if response.status_code not in (200, 201):
            return jsonify({
                "success": False,
                "message": "Partner API rejected the record.",
                "partner_status": response.status_code,
                "partner_response": partner_result
            }), 502

        return jsonify({
            "success": True,
            "message": "Student record sent successfully!",
            "partner_status": response.status_code,
            "partner_response": partner_result
        }), 200

    except (requests.RequestException, ValueError) as error:
        return jsonify({
            "success": False,
            "message": "Could not send the record to the Partner API.",
            "error": str(error)
        }), 502

# RUN FLASK
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
