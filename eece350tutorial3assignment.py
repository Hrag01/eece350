import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# this is important because foreign keys are OFF by default in SQLite
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 30)

    for row in rows:
        print(" | ".join(str(value) for value in row))

# Create tables
cursor.execute("""
CREATE TABLE student (
    studentID INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""CREATE TABLE registered_courses (
               studentID INT,
                courseID INT,
               PRIMARY KEY (studentID, courseID),
               FOREIGN KEY (studentID) REFERENCES student(studentID)
)
""")
cursor.execute("""CREATE TABLE grades (
               studentID INT,
                courseID INT,
                grade REAL,
               PRIMARY KEY (studentID, courseID),
               FOREIGN KEY (studentID, courseID) REFERENCES registered_courses(studentID, courseID)
)
""")





students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]

cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)

registered_courses = [
    (1, 101),
    (1, 102),
    (2, 102),
    (2, 201),
    (3, 201),
    (3, 202)
]

cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered_courses)

grades = [
    (1, 101, 90),
    (1, 102, 84),
    (2, 102, 92),
    (2, 201, 85),
    (3, 201, 75),
    (3, 202, 68)
]

cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades)

conn.commit()



print_table(cursor, "student")
print_table(cursor, "registered_courses")
print_table(cursor, "grades")


#Query max grade per student
print("Maximum grade per student:")
cursor.execute("""
SELECT g.studentID, g.courseID, g.grade AS max_grade
FROM grades g
JOIN (
    SELECT studentID, MAX(grade) AS max_grade
    FROM grades
    GROUP BY studentID
) mg
ON g.studentID = mg.studentID AND g.grade = mg.max_grade;
""")
for row in cursor.fetchall():
    print(row)


#Query average grade per student
print("\nAverage grade per student:")
cursor.execute("""
SELECT studentID, AVG(grade) AS avg_grade
FROM grades
GROUP BY studentID
""")
for row in cursor.fetchall():
    print(row)

conn.close()