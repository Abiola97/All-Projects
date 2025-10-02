

# 🔗 Join Operations & Salary Analytics (MySQL)

A relational SQL-based system designed to demonstrate join operations, foreign key constraints, and salary analytics using aggregate and window functions. Ideal for data analysts, engineers, or students mastering SQL joins and departmental insights.

---

## 📦 Features

- ✅ Relational schema with foreign key constraints  
- 🔗 Demonstrates `INNER JOIN`, `LEFT JOIN`, and `RIGHT JOIN`  
- 📊 Salary analytics using `AVG`, `DENSE_RANK`, and `PARTITION BY`  
- 🧮 Department-level insights using `GROUP BY` and `HAVING`  
- 📚 Course enrollment mapping via foreign key joins  

---

## 🗂 Schema Overview

### `student` Table

| Column       | Type         | Description              |
|--------------|--------------|--------------------------|
| student_id   | VARCHAR(10)  | Primary Key              |
| student_name | VARCHAR(50)  | Student's full name      |
| age          | INT          | Student age              |

### `course` Table

| Column       | Type         | Description                          |
|--------------|--------------|--------------------------------------|
| course_id    | VARCHAR(6)   | Primary Key                          |
| student_id   | VARCHAR(6)   | Foreign Key → `student(student_id)`  |
| course_name  | CHAR(150)    | Course title                         |

### `emp_salary1` Table

| Column     | Type         | Description              |
|------------|--------------|--------------------------|
| Name       | VARCHAR(50)  | Employee name            |
| Age        | INT          | Employee age             |
| Department | VARCHAR(50)  | Department name          |
| Salary     | INT          | Monthly salary           |

---

## 🔗 Join Operations

### Inner Join: Students with Enrolled Courses

```sql
SELECT *
FROM student s
INNER JOIN course c ON s.student_id = c.student_id;
```

### Left Join: All Students + Their Courses (if any)

```sql
SELECT *
FROM student s
LEFT JOIN course c ON s.student_id = c.student_id;
```

### Right Join: All Courses + Enrolled Students (if any)

```sql
SELECT *
FROM student s
RIGHT JOIN course c ON s.student_id = c.student_id;
```

---

## 🧮 Salary Analytics

### Average Salary by Department

```sql
SELECT Department, AVG(Salary) AS avg_salary
FROM emp_salary1
GROUP BY Department;
```

### Average Salary Using Window Function

```sql
SELECT *, AVG(Salary) OVER(PARTITION BY Department) AS average_salary
FROM emp_salary1;
```

### Ranking Employees by Salary

```sql
SELECT *, DENSE_RANK() OVER(ORDER BY Salary DESC) AS ranking
FROM emp_salary1;
```

### Departmental Ranking by Salary

```sql
SELECT *, DENSE_RANK() OVER(PARTITION BY Department ORDER BY Salary DESC) AS ranking
FROM emp_salary1;
```

### Departments with High Average Salary

```sql
SELECT Department, AVG(Salary) AS avg_salary
FROM emp_salary1
GROUP BY Department
HAVING avg_salary >= 35000;
```

---

## 👤 Author

Built by Abiola Ajao  
🎓 Master’s in Collective Intelligence @ UM6P  
💼 Data Analyst → Product Manager  
📍 Morocco & Nigeria  
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 ajaoabiola0812@gmail.com

---


