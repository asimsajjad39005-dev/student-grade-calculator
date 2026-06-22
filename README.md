```markdown
# Student Grade Calculator

A command-line Python application to manage student grades. Built with plain Python standard library only.

---

## Project Structure

```
student_grade_calculator/
├── grade_calculator.py
├── test_grade_calculator.py
├── students.json
└── README.md
```

---

## How to Run

```bash
# Start the app
python grade_calculator.py

# Run tests
python -m unittest test_grade_calculator.py -v
```

---

## Menu Options

```
=========================================
       STUDENT GRADE CALCULATOR
=========================================
 1. List all students
 2. Add a new student
 3. Record / update a grade
 4. Set attendance
 5. View student details
 6. Show top N students
 7. Show failing students (avg < 40)
 8. Show subject statistics
 9. Exit
=========================================
```

---

## Grade Boundaries

| Letter | Range    |
|--------|----------|
| A      | 80 – 100 |
| B      | 65 – 79  |
| C      | 50 – 64  |
| D      | 40 – 49  |
| F      | 0  – 39  |

---

## Functions

| Function | Description |
|----------|-------------|
| `add_student` | Add new student, reject duplicate ID |
| `record_grade` | Save grade, validate subject and range |
| `calculate_average` | Mean of all subject grades |
| `get_letter_grade` | Convert number to A/B/C/D/F |
| `get_class_rank` | Rank 1 (best) to N |
| `get_top_students` | Top N sorted by average |
| `find_failing_students` | Average below 40 |
| `get_subject_stats` | Min, max, average, median |

---

## Test Results

```
test_add_duplicate_student ... ok
test_add_new_student ... ok
test_correct_average ... ok
test_nonexistent_student ... ok
test_finds_failing ... ok
test_passing_not_in_failing ... ok
test_last_student_rank ... ok
test_top_student_is_rank_1 ... ok
test_grade_a ... ok
test_grade_b ... ok
test_grade_c ... ok
test_grade_d ... ok
test_grade_f ... ok
test_invalid_subject_returns_none ... ok
test_math_stats ... ok
test_n_larger_than_class ... ok
test_top_2_students ... ok
test_record_grade_out_of_range ... ok
test_record_invalid_subject ... ok
test_record_valid_grade ... ok

Ran 20 tests in 0.004s — OK
```

---

## Default Students

| Rank | Name          | ID   | Average | Grade |
|------|---------------|------|---------|-------|
| 1    | Ayesha Malik  | S004 | 91.5    | A     |
| 2    | Maryam Javed  | S010 | 89.75   | A     |
| 3    | Ali Hassan    | S001 | 85.25   | A     |
| 4    | Fatima Noor   | S008 | 81.25   | A     |
| 5    | Sara Khan     | S002 | 73.75   | B     |
| 6    | Zara Siddiqui | S006 | 68.75   | B     |
| 7    | Umar Farooq   | S003 | 55.75   | C     |
| 8    | Hamza Raza    | S007 | 48.75   | D     |
| 9    | Bilal Ahmed   | S005 | 35.75   | F     |
| 10   | Tariq Mehmood | S009 | 26.25   | F     |

---

## GitHub Setup

```bash
git init
git add .
git commit -m "Student Grade Calculator"
git remote add origin https://github.com/asimsajjad39005-dev/student-grade-calculator.git
git push -u origin main
```

```
