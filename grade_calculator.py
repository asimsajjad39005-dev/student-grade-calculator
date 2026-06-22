"""
Student Grade Calculator
A command-line application to manage student grades for a class.
"""

import json
import os
import statistics

DATA_FILE = "students.json"

def load_students():
    """Load student data from students.json. Returns empty list if file not found."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_students(students):
    """Save the current student list to students.json immediately."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

def add_student(students, name, student_id):
    """Add a new student record to the list."""
    for s in students:
        if s["student_id"] == student_id:
            return f"Error: Student ID '{student_id}' already exists."
    students.append({
        "name": name,
        "student_id": student_id,
        "grades": {"Math": None, "English": None, "Science": None, "Computer": None},
        "attendance": 0.0
    })
    save_students(students)
    return f"Student '{name}' added successfully."

def record_grade(students, student_id, subject, grade):
    """Record or update a grade for a specific subject."""
    valid_subjects = ["Math", "English", "Science", "Computer"]
    if subject not in valid_subjects:
        return f"Error: Subject must be one of {valid_subjects}."
    if not (0 <= grade <= 100):
        return "Error: Grade must be between 0 and 100."
    for s in students:
        if s["student_id"] == student_id:
            s["grades"][subject] = grade
            save_students(students)
            return f"Grade {grade} recorded for {s['name']} in {subject}."
    return f"Error: Student ID '{student_id}' not found."

def calculate_average(students, student_id):
    """Calculate the average grade across all subjects for a student."""
    for s in students:
        if s["student_id"] == student_id:
            scores = [v for v in s["grades"].values() if v is not None]
            if not scores:
                return 0.0
            return round(sum(scores) / len(scores), 2)
    return None

def get_letter_grade(average):
    """Convert a numeric average to a letter grade."""
    if average >= 80:
        return "A"
    elif average >= 65:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"

def get_class_rank(students, student_id):
    """Return the class rank (1 = highest) of a student by average grade."""
    averages = [(s["student_id"], calculate_average(students, s["student_id"])) for s in students]
    averages.sort(key=lambda x: x[1] if x[1] is not None else -1, reverse=True)
    for rank, (sid, _) in enumerate(averages, start=1):
        if sid == student_id:
            return rank
    return None

def get_top_students(students, n):
    """Return the top N students sorted by average grade (highest first)."""
    ranked = []
    for s in students:
        avg = calculate_average(students, s["student_id"])
        ranked.append((s["name"], s["student_id"], avg if avg is not None else 0.0))
    ranked.sort(key=lambda x: x[2], reverse=True)
    return ranked[:n]

def find_failing_students(students):
    """Find all students whose average grade is below 40."""
    failing = []
    for s in students:
        avg = calculate_average(students, s["student_id"])
        if avg is not None and avg < 40:
            failing.append((s["name"], s["student_id"], avg))
    return failing

def get_subject_stats(students, subject):
    """Return statistics (min, max, average, median) for a given subject."""
    scores = [
        s["grades"][subject]
        for s in students
        if subject in s["grades"] and s["grades"][subject] is not None
    ]
    if not scores:
        return None
    return {
        "min": min(scores),
        "max": max(scores),
        "average": round(sum(scores) / len(scores), 2),
        "median": round(statistics.median(scores), 2)
    }

def set_attendance(students, student_id, attendance):
    """Set attendance percentage for a student."""
    if not (0 <= attendance <= 100):
        return "Error: Attendance must be between 0 and 100."
    for s in students:
        if s["student_id"] == student_id:
            s["attendance"] = attendance
            save_students(students)
            return f"Attendance updated for {s['name']}."
    return f"Error: Student ID '{student_id}' not found."

def display_student(students, student_id):
    """Print a full summary card for a student."""
    for s in students:
        if s["student_id"] == student_id:
            avg = calculate_average(students, student_id)
            letter = get_letter_grade(avg)
            rank = get_class_rank(students, student_id)
            print(f"\n{'='*40}")
            print(f"  Name        : {s['name']}")
            print(f"  Student ID  : {s['student_id']}")
            print(f"  Attendance  : {s['attendance']}%")
            print(f"  Grades:")
            for sub, grade in s["grades"].items():
                print(f"    {sub:<10}: {grade if grade is not None else 'N/A'}")
            print(f"  Average     : {avg}")
            print(f"  Letter Grade: {letter}")
            print(f"  Class Rank  : #{rank}")
            print(f"{'='*40}\n")
            return
    print(f"Student ID '{student_id}' not found.")

def list_all_students(students):
    """Print a summary table of all students."""
    if not students:
        print("No students on record.")
        return
    print(f"\n{'#':<5} {'Name':<20} {'ID':<10} {'Avg':<8} {'Grade':<6} {'Attend'}")
    print("-" * 60)
    for rank, s in enumerate(
        sorted(students, key=lambda x: calculate_average(students, x["student_id"]) or 0, reverse=True),
        start=1
    ):
        avg = calculate_average(students, s["student_id"])
        letter = get_letter_grade(avg)
        print(f"{rank:<5} {s['name']:<20} {s['student_id']:<10} {avg:<8} {letter:<6} {s['attendance']}%")
    print()

def seed_default_students(students):
    """Add 10 default students if the list is empty."""
    defaults = [
        ("Ali Hassan",    "S001", {"Math": 85, "English": 78, "Science": 90, "Computer": 88}, 95.0),
        ("Sara Khan",     "S002", {"Math": 72, "English": 80, "Science": 68, "Computer": 75}, 90.0),
        ("Umar Farooq",   "S003", {"Math": 55, "English": 60, "Science": 50, "Computer": 58}, 82.0),
        ("Ayesha Malik",  "S004", {"Math": 92, "English": 88, "Science": 95, "Computer": 91}, 98.0),
        ("Bilal Ahmed",   "S005", {"Math": 35, "English": 40, "Science": 30, "Computer": 38}, 70.0),
        ("Zara Siddiqui", "S006", {"Math": 65, "English": 70, "Science": 72, "Computer": 68}, 88.0),
        ("Hamza Raza",    "S007", {"Math": 48, "English": 52, "Science": 45, "Computer": 50}, 75.0),
        ("Fatima Noor",   "S008", {"Math": 78, "English": 82, "Science": 80, "Computer": 85}, 93.0),
        ("Tariq Mehmood", "S009", {"Math": 25, "English": 30, "Science": 28, "Computer": 22}, 60.0),
        ("Maryam Javed",  "S010", {"Math": 88, "English": 91, "Science": 87, "Computer": 93}, 97.0),
    ]
    for name, sid, grades, attend in defaults:
        students.append({
            "name": name, "student_id": sid,
            "grades": grades, "attendance": attend
        })
    save_students(students)
    print("Loaded 10 default students.")

def print_menu():
    print("\n" + "=" * 45)
    print("       STUDENT GRADE CALCULATOR")
    print("=" * 45)
    print(" 1. List all students")
    print(" 2. Add a new student")
    print(" 3. Record / update a grade")
    print(" 4. Set attendance")
    print(" 5. View student details")
    print(" 6. Show top N students")
    print(" 7. Show failing students (avg < 40)")
    print(" 8. Show subject statistics")
    print(" 9. Exit")
    print("=" * 45)

def main():
    students = load_students()
    if not students:
        print("No data found. Seeding 10 default students...")
        seed_default_students(students)

    while True:
        print_menu()
        choice = input("Enter option (1-9): ").strip()
        try:
            if choice == "1":
                list_all_students(students)
            elif choice == "2":
                name = input("Enter student name: ").strip()
                sid  = input("Enter student ID  : ").strip()
                if not name or not sid:
                    print("Name and ID cannot be empty.")
                else:
                    print(add_student(students, name, sid))
            elif choice == "3":
                sid     = input("Enter student ID : ").strip()
                subject = input("Subject (Math/English/Science/Computer): ").strip().capitalize()
                grade   = float(input("Enter grade (0-100): "))
                print(record_grade(students, sid, subject, grade))
            elif choice == "4":
                sid        = input("Enter student ID      : ").strip()
                attendance = float(input("Enter attendance % (0-100): "))
                print(set_attendance(students, sid, attendance))
            elif choice == "5":
                sid = input("Enter student ID: ").strip()
                display_student(students, sid)
            elif choice == "6":
                n = int(input("How many top students to show? "))
                top = get_top_students(students, n)
                print(f"\nTop {n} Students:")
                print(f"{'Rank':<6} {'Name':<20} {'ID':<10} {'Average'}")
                print("-" * 50)
                for i, (name, sid, avg) in enumerate(top, 1):
                    print(f"{i:<6} {name:<20} {sid:<10} {avg}")
            elif choice == "7":
                failing = find_failing_students(students)
                if not failing:
                    print("No failing students.")
                else:
                    print(f"\nFailing Students ({len(failing)} found):")
                    for name, sid, avg in failing:
                        print(f"  {name} ({sid}) — Average: {avg} [{get_letter_grade(avg)}]")
            elif choice == "8":
                subject = input("Enter subject (Math/English/Science/Computer): ").strip().capitalize()
                stats = get_subject_stats(students, subject)
                if stats:
                    print(f"\n{subject} Statistics:")
                    print(f"  Min    : {stats['min']}")
                    print(f"  Max    : {stats['max']}")
                    print(f"  Average: {stats['average']}")
                    print(f"  Median : {stats['median']}")
                else:
                    print("No grades recorded for that subject.")
            elif choice == "9":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()