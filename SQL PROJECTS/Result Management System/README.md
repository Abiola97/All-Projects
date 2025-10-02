
# 🎓 Result Management System (MySQL)

A fully normalized SQL-based system for managing student records, profiles, courses, and subject-wise results. Designed for educational institutions and data engineers seeking scalable, query-optimized academic databases with advanced analytics and ranking logic.

---

## 📦 Features

- ✅ Relational schema with foreign key constraints
- 📥 CSV data import via MySQL Table Import Wizard
- 🔗 Joins across `Student_Table`, `Student_Profile_Table`, and `Course_Table`
- 👁 Unified view `All_Results` combining multiple subject tables
- 📊 Aggregated performance view with total, average, highest, and lowest scores
- 🏅 Ranking logic using `DENSE_RANK`, `ROW_NUMBER`, and `RANK`
- 🛠 Stored procedure `view_table_rms()` for reusable analytics

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

- 📊 [student.csv](https://docs.google.com/spreadsheets/d/1QzwxrQu6m58f6XMGY92s66ey38Dz29lnfM3TkAVAi-w/edit?usp=sharing)  
- 📊 [student profile.csv](https://docs.google.com/spreadsheets/d/1WlV-F6KoazIP9AQR_pb--WFR4aKfXQMTg6GaoEBVjJU/edit?usp=sharing)  
- 📊 [course.csv](https://docs.google.com/spreadsheets/d/1CXJU02gJJ1WyU8tpy7y9TR_tTO_FcgHRsPlxuJuzum0/edit?usp=sharing)  
- 📊 [result for different.csv](https://drive.google.com/drive/folders/1ryD-i9azSTIomBhkJF9JULIsoasdSBnT?usp=sharing)

---

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

-- Aggregate scores and rank students
SELECT *, DENSE_RANK() OVER (ORDER BY total_score DESC) AS student_rank
FROM student_results_db_view;
```
---

## 🧮 Stored Procedure: `view_table_rms()`

This procedure aggregates scores across 10 subjects for each student, calculating:

- `total_score`: Sum of all subject scores  
- `average_score`: Rounded average across subjects  
- `highest_score`: Maximum score among subjects  
- `lowest_score`: Minimum score among subjects  

### 📌 Procedure Definition

```sql
DELIMITER //

CREATE PROCEDURE view_table_rms()
BEGIN
  SELECT *,
    (agriculture + biology + chemistry + computer_sci + english + geography + literature + maths + physics + technical_drawing) AS total_score,
    ROUND((agriculture + biology + chemistry + computer_sci + english + geography + literature + maths + physics + technical_drawing) / 10.0) AS average_score,
    GREATEST(agriculture, biology, chemistry, computer_sci, english, geography, literature, maths, physics, technical_drawing) AS highest_score,
    LEAST(agriculture, biology, chemistry, computer_sci, english, geography, literature, maths, physics, technical_drawing) AS lowest_score
  FROM (
    SELECT ag.id, s.admission_number,
      CONCAT(s.firstname, ' ', s.lastname) AS student_name,
      (ag.first_ca + ag.second_ca + ag.exam) AS agriculture,
      (b.first_ca + b.second_ca + b.exam) AS biology,
      (c.first_ca + c.second_ca + c.exam) AS chemistry,
      (cs.first_ca + cs.second_ca + cs.exam) AS computer_sci,
      (e.first_ca + e.second_ca + e.exam) AS english,
      (g.first_ca + g.second_ca + g.exam) AS geography,
      (l.first_ca + l.second_ca + l.exam) AS literature,
      (m.first_ca + m.second_ca + m.exam) AS maths,
      (p.first_ca + p.second_ca + p.exam) AS physics,
      (t.first_ca + t.second_ca + t.exam) AS technical_drawing
    FROM Student_Table s
    JOIN agric ag ON s.admission_number = ag.student
    JOIN bio b ON s.admission_number = b.student
    JOIN chem c ON s.admission_number = c.student
    JOIN compt cs ON s.admission_number = cs.student
    JOIN english e ON s.admission_number = e.student
    JOIN geo g ON s.admission_number = g.student
    JOIN lit l ON s.admission_number = l.student
    JOIN maths m ON s.admission_number = m.student
    JOIN physics p ON s.admission_number = p.student
    JOIN td t ON s.admission_number = t.student
  ) AS rms_table;
END //

DELIMITER ;
```

### 📊 How to Use

```sql
CALL view_table_rms();
```

You can also rank students based on their total score:

```sql
SELECT *, DENSE_RANK() OVER (ORDER BY total_score DESC) AS student_rank
FROM student_results_db_view;
```


## 📈 Dashboard Integration

Views like `student_results_db_view` are optimized for BI tools such as Power BI, Tableau, or Metabase. Schema supports easy joins for student profiles, course performance, and institutional KPIs.

