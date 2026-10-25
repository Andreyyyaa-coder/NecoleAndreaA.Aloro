
import sqlite3

DATABASE = "students.db"

students = [
    ("2026-00123", "JM Abordaje", "BSIT", 3, "A"),
    ("2026-00124", "Katrina Pauleen Rivas", "BSN", 3, "B"),
    ("2026-00125", "Jessica Ann Balcena", "BSIT", 3, "A"),
    ("2026-00126", "Alyanna Daniella Joy Betoya", "BSN", 3, "C"),
    ("2026-00127", "Joshua Porras", "BSN", 3, "A")
]

conn = sqlite3.connect(DATABASE)
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

# Add sample records only if the table is empty.
# This prevents existing records from being deleted.
cursor.execute("SELECT COUNT(*) FROM students")
count = cursor.fetchone()[0]

if count == 0:
    cursor.executemany("""
        INSERT INTO students
            (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)
    """, students)
    print("Database created with five sample records.")
else:
    print(f"Database already contains {count} records. Existing records preserved.")

conn.commit()
conn.close()
