
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

    cleaned = {
        "student_id": str(data["student_id"]).strip(),
        "name": str(data["name"]).strip(),
        "program": str(data["program"]).strip(),
        "year": year,
        "section": str(data["section"]).strip()
    }

    return cleaned, None


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
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        conn.close()


# CREATE STUDENT
@app.route("/api/students", methods=["POST"])
def add_student():
    data, error = get_student_data()

    if error:
        return jsonify({"error": error}), 400

    conn = get_db_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO students
               (student_id, name, program, year, section)
               VALUES (?, ?, ?, ?, ?)""",
            (
                data["student_id"],
                data["name"],
                data["program"],
                data["year"],
                data["section"]
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

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Could not add the student. Check for duplicate values."
        }), 409
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Could not update the student. Check for duplicate values."
        }), 409
    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
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

        conn.execute(
            "DELETE FROM students WHERE id = ?", (id,)
        )
        conn.commit()

        return jsonify({
            "message": "Student deleted successfully."
        })

    except sqlite3.Error as error:
        return jsonify({"error": str(error)}), 500
    finally:
        conn.close()


# CLASSMATE API PROXY
# The browser calls this local endpoint instead of Jessica's API directly.
@app.route("/classmate-students", methods=["GET"])
def get_classmate_students():
    try:
        response = requests.get(
            CLASSMATE_API_URL,
            timeout=30
        )

        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            return jsonify({
                "error": "The classmate API did not return valid JSON."
            }), 502

        # Accept a list directly or a list wrapped in a dictionary.
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

    except requests.RequestException as error:
        app.logger.error("Classmate API request failed: %s", error)

        return jsonify({
            "error": "Could not retrieve classmate records.",
            "details": str(error)
        }), 502


# KEEP THIS BLOCK AT THE VERY BOTTOM
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
