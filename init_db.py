
import sqlite3

DATABASE = "students.db"

students = [
    ("2026-00123", "JM Abordaje", "BSIT", 3, "A"),
    ("2026-00124", "Katrina Pauleen Rivas", "BSN", 3, "B"),
    ("2026-00125", "Jessica Ann Balcena", "BSIT", 3, "A"),
    ("2026-00126", "Alyanna Daniella Joy Betoya", "BSN", 3, "C"),
    ("2026-00127", "Joshua Porras", "BSN", 3, "A")
]


def create_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    try:
        # Create the students table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                program TEXT NOT NULL,
                year INTEGER NOT NULL,
                section TEXT NOT NULL,
                source TEXT DEFAULT 'Local'
            )
        """)

        # Add the source column if an older table does not have it.
        cursor.execute("PRAGMA table_info(students)")
        columns = [column[1] for column in cursor.fetchall()]

        if "source" not in columns:
            cursor.execute("""
                ALTER TABLE students
                ADD COLUMN source TEXT DEFAULT 'Local'
            """)
            print("Source column added successfully.")

        # Insert sample records only if the table is empty.
        cursor.execute("SELECT COUNT(*) FROM students")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.executemany("""
                INSERT INTO students
                    (student_id, name, program, year, section, source)
                VALUES (?, ?, ?, ?, ?, 'Local')
            """, students)

            print("Database created with five sample records.")
        else:
            print(f"Database already contains {count} records.")
            print("Existing records preserved.")

        # Create the exchange attempts table.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                student_name TEXT,
                direction TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        print("Exchange attempts table is ready.")
        print("Database setup completed successfully.")

    except sqlite3.Error as error:
        conn.rollback()
        print("Database setup error:", error)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
