from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome Student!"


@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00286",
        "name": "Necole Andrea Aloro",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })


@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Necole Andrea')
    return jsonify({
        "message": f"Hello, {name}!"
    })


@app.route('/course')
def say_course():
    return jsonify({
        "course_code": "IT3120",
        "course_title": "System Integration",
        "instructor": "Dr. Rene Arduo",
        "semester": "First Semester",
        "academic_year": "AY 2026-2027"
    })


@app.route('/greet')
def greet():
    name = request.args.get('name', 'Necole Andrea Aloro')
    program = request.args.get('program', 'BSIT')
    year = request.args.get('year', '3')
    section = request.args.get('section', 'A')

    return jsonify({
        "message": f"Hello {name} from {program} {year} {section}!"
    })

@app.route('/profile')
def get_profile():
    return jsonify({
        "student_id": "24-00286",
        "name": "Necole Andrea Aloro",
        "program": "BSIT",
        "year": 3,
        "section": "A",
        "gmail": "aloronecoleandrea@isufst.edu.ph",
        "skills": "mobile gaming, editing"
    })

@app.route('/entertainment')
def get_entertainment():
    return jsonify({
        "favorite_movie": "Avengers: Endgame",
        "favorite_song": "Die With A Smile",
        "favorite_game": "Mobile Legends",
        "hobby": "Watching movies and playing mobile games"
    })
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

