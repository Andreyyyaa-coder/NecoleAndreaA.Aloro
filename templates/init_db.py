
import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Reset the sample records each time this script runs.
cursor.execute("DELETE FROM students")

students = [
    ("2026-00123", "JM Abordaje", "BSIT", 3, "A"),
    ("2026-00124", "Katrina Pauleen Rivas", "BSN", 3, "B"),
    ("2026-00125", "Jessica Ann Balcena", "BSIT", 3, "A"),
    ("2026-00126", "Alyanna Daniella Joy Betoya", "BSN", 3, "C"),
    ("2026-00127", "Joshua Porras", "BSN", 3, "A")
]

cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

conn.commit()
conn.close()

print("Database created successfully.")
