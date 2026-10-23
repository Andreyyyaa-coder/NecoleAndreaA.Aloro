
import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


# Existing endpoint: original student information
@app.route("/student")
def get_student():
    return jsonify({
        "student_id": "24-00286",
        "name": "Necole Andrea Aloro",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


# Existing endpoint: greeting
@app.route("/hello")
def say_hello():
    name = request.args.get("name", "Necole")
    return jsonify({"message": f"Hello, {name}!"})


# Existing endpoint: course information
@app.route("/course")
def say_course():
    return jsonify({
        "course_code": "IT3120",
        "course_title": "System Integration",
        "instructor": "Dr. Rene Arduo",
        "semester": "First Semester",
        "academic_year": "AY 2026-2027"
    })


# Existing endpoint: custom greeting
@app.route("/greet")
def greet():
    name = request.args.get("name", "Necole Andrea Aloro")
    program = request.args.get("program", "BSIT")
    year = request.args.get("year", "3")
    section = request.args.get("section", "A")

    return jsonify({
        "message": (
            f"Hello {name} from {program} "
            f"{year} {section}!"
        )
    })


# Existing endpoint: profile
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


# Existing endpoint: entertainment
@app.route("/entertainment")
def get_entertainment():
    return jsonify({
        "favorite_movie": "Avengers: Endgame",
        "favorite_song": "Die With A Smile",
        "favorite_game": "Mobile Legends",
        "hobby": "Watching movies and playing mobile games"
    })


# NEW: Retrieve all students from SQLite
@app.route("/students")
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students ORDER BY id"
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# NEW: Retrieve one student by database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        "SELECT * FROM students WHERE id = ?",
        (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# ADDITIONAL TASK: Filter students by program
# Example: /students/program/BSIT
@app.route("/students/program/<string:program>")
def get_students_by_program(program):
    conn = get_db_connection()
    students = conn.execute(
        "SELECT * FROM students WHERE LOWER(program) = LOWER(?) ORDER BY id",
        (program,)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
