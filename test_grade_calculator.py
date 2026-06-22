import unittest
import os
import grade_calculator
grade_calculator.DATA_FILE = "test_students.json"

from grade_calculator import (
    add_student, record_grade, calculate_average, get_letter_grade,
    get_class_rank, get_top_students, find_failing_students, get_subject_stats,
)

def make_students():
    return [
        {"name": "Ali Hassan",    "student_id": "S001",
         "grades": {"Math": 85, "English": 78, "Science": 90, "Computer": 88}, "attendance": 95.0},
        {"name": "Sara Khan",     "student_id": "S002",
         "grades": {"Math": 72, "English": 80, "Science": 68, "Computer": 75}, "attendance": 90.0},
        {"name": "Bilal Ahmed",   "student_id": "S003",
         "grades": {"Math": 35, "English": 40, "Science": 30, "Computer": 38}, "attendance": 70.0},
        {"name": "Tariq Mehmood", "student_id": "S004",
         "grades": {"Math": 25, "English": 30, "Science": 28, "Computer": 22}, "attendance": 60.0},
    ]

class TestAddStudent(unittest.TestCase):
    def test_add_new_student(self):
        students = make_students()
        result = add_student(students, "New Student", "S999")
        self.assertIn("added successfully", result)
        self.assertIn("S999", [s["student_id"] for s in students])

    def test_add_duplicate_student(self):
        students = make_students()
        result = add_student(students, "Duplicate", "S001")
        self.assertIn("already exists", result)

class TestRecordGrade(unittest.TestCase):
    def test_record_valid_grade(self):
        students = make_students()
        result = record_grade(students, "S001", "Math", 95)
        self.assertIn("recorded", result)
        student = next(s for s in students if s["student_id"] == "S001")
        self.assertEqual(student["grades"]["Math"], 95)

    def test_record_invalid_subject(self):
        students = make_students()
        result = record_grade(students, "S001", "History", 80)
        self.assertIn("Error", result)

    def test_record_grade_out_of_range(self):
        students = make_students()
        result = record_grade(students, "S001", "Math", 110)
        self.assertIn("Error", result)

class TestCalculateAverage(unittest.TestCase):
    def test_correct_average(self):
        students = make_students()
        avg = calculate_average(students, "S001")
        self.assertEqual(avg, round((85 + 78 + 90 + 88) / 4, 2))

    def test_nonexistent_student(self):
        students = make_students()
        self.assertIsNone(calculate_average(students, "ZZZZ"))

class TestGetLetterGrade(unittest.TestCase):
    def test_grade_a(self): self.assertEqual(get_letter_grade(85), "A")
    def test_grade_b(self): self.assertEqual(get_letter_grade(70), "B")
    def test_grade_c(self): self.assertEqual(get_letter_grade(55), "C")
    def test_grade_d(self): self.assertEqual(get_letter_grade(42), "D")
    def test_grade_f(self): self.assertEqual(get_letter_grade(30), "F")

class TestGetClassRank(unittest.TestCase):
    def test_top_student_is_rank_1(self):
        students = make_students()
        self.assertEqual(get_class_rank(students, "S001"), 1)

    def test_last_student_rank(self):
        students = make_students()
        self.assertEqual(get_class_rank(students, "S004"), len(students))

class TestGetTopStudents(unittest.TestCase):
    def test_top_2_students(self):
        students = make_students()
        top = get_top_students(students, 2)
        self.assertEqual(len(top), 2)
        self.assertGreaterEqual(top[0][2], top[1][2])

    def test_n_larger_than_class(self):
        students = make_students()
        self.assertEqual(len(get_top_students(students, 100)), len(students))

class TestFindFailingStudents(unittest.TestCase):
    def test_finds_failing(self):
        students = make_students()
        ids = [sid for _, sid, _ in find_failing_students(students)]
        self.assertIn("S003", ids)
        self.assertIn("S004", ids)

    def test_passing_not_in_failing(self):
        students = make_students()
        ids = [sid for _, sid, _ in find_failing_students(students)]
        self.assertNotIn("S001", ids)

class TestGetSubjectStats(unittest.TestCase):
    def test_math_stats(self):
        students = make_students()
        stats = get_subject_stats(students, "Math")
        scores = [85, 72, 35, 25]
        self.assertEqual(stats["min"], min(scores))
        self.assertEqual(stats["max"], max(scores))

    def test_invalid_subject_returns_none(self):
        students = make_students()
        self.assertIsNone(get_subject_stats(students, "History"))

def tearDownModule():
    if os.path.exists("test_students.json"):
        os.remove("test_students.json")

if __name__ == "__main__":
    unittest.main(verbosity=2)