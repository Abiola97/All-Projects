# 🎓 Result Management System (MySQL)

A structured SQL-based system for managing student records, profiles, courses, and subject-wise results. Designed for educational institutions or data engineers looking to build scalable, normalized databases.

---

## 📦 Features

- ✅ Relational schema with foreign key constraints
- 📥 CSV data import via MySQL Table Import Wizard
- 🔗 Joins across `Student_Table`, `Student_Profile_Table`, and `Course_Table`
- 👁 Unified view `All_Results` combining multiple subject tables
- 📊 Query flexibility: by student ID, course code, or name

---

## 🗂 Schema Overview

### `Student_Table`
- `admission_number` (PK)
- `firstname`
- `lastname`

### `Student_Profile_Table`
- `sit_number` (PK)
- `admission_number` (FK)
- `age`, `date_of_birth`, `gender`, `grade`, `email`, `phone_number`, `address`, `parent_name`, `parent_contact`

### `Course_Table`
- `course_code` (PK)
- `course_name`

### Subject Tables (e.g., `english`, `maths`, `physics`, etc.)
- `id` (PK)
- `course_code` (FK)
- `student` (FK)
- `first_ca`, `second_ca`, `exam`

---

📥 CSV Resources
Please download the following CSV files to populate your tables:
- 📊 [[student.csv]( https://docs.google.com/spreadsheets/d/1QzwxrQu6m58f6XMGY92s66ey38Dz29lnfM3TkAVAi-w/edit?usp=sharing)](#)


student profile csv

course csv

results for different courses csv
## 🔍 Sample Queries

```sql
-- View results for a specific student
SELECT * FROM All_Results WHERE student = 'SS2-24-104';

-- Join student and profile data
SELECT s.admission_number, s.firstname, s.lastname, p.grade, p.email
FROM Student_Table s
JOIN Student_Profile_Table p ON s.admission_number = p.admission_number;

-- View results by course
SELECT s.firstname, s.lastname, c.course_name, r.first_ca, r.second_ca, r.exam
FROM All_Results r
JOIN Student_Table s ON r.student = s.admission_number
JOIN Course_Table c ON r.course_code = c.course_code
WHERE c.course_code = 'agric-s2';

