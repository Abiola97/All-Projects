-- 📁 Create and select the result management database
CREATE DATABASE result_management_system;
USE result_management_system;

-- 👨‍🎓 Create Student table and adjust admission_number type
CREATE TABLE Student_Table (
    admission_number INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(30),
    lastname VARCHAR(30)
);
ALTER TABLE Student_Table MODIFY admission_number VARCHAR(10);

-- 👤 Create Student Profile table with foreign key to Student_Table
CREATE TABLE Student_Profile_Table (
    sit_number INT PRIMARY KEY,
    admission_number VARCHAR(10),
    age INT,
    date_of_birth DATE,
    gender CHAR(10),
    grade VARCHAR(10),
    email VARCHAR(50),
    phone_number VARCHAR(20),
    address VARCHAR(100),
    parent_name CHAR(50),
    parent_contact VARCHAR(20),
    FOREIGN KEY (admission_number) REFERENCES Student_Table(admission_number)
);

-- 📚 Create Course table
CREATE TABLE Course_Table (
    course_code VARCHAR(10) PRIMARY KEY,
    course_name VARCHAR(20)
);

-- 📥 Create unified view combining all subject result tables
CREATE VIEW All_Results AS
SELECT * FROM english
UNION ALL SELECT * FROM maths
UNION ALL SELECT * FROM physics
UNION ALL SELECT * FROM compt
UNION ALL SELECT * FROM chem
UNION ALL SELECT * FROM lit
UNION ALL SELECT * FROM td
UNION ALL SELECT * FROM geo
UNION ALL SELECT * FROM bio
UNION ALL SELECT * FROM agric;

-- 🔧 Normalize agric table for consistency
ALTER TABLE agric 
    MODIFY course_code VARCHAR(10),
    MODIFY student VARCHAR(10),
    MODIFY `ï»¿id` INT PRIMARY KEY,
    RENAME COLUMN `ï»¿id` TO id,
    ADD CONSTRAINT fk_course FOREIGN KEY (course_code) REFERENCES Course_Table(course_code);

-- 🛠 Standardize student column type and fix corrupted id column in other result tables
ALTER TABLE compt MODIFY student VARCHAR(10), RENAME COLUMN `ï»¿id` TO id;
ALTER TABLE bio MODIFY student VARCHAR(10), RENAME COLUMN `ï»¿id` TO id;
ALTER TABLE chem MODIFY student VARCHAR(10), RENAME COLUMN `ï»¿id` TO id;
ALTER TABLE maths MODIFY student VARCHAR(10), MODIFY course_code VARCHAR(10), RENAME COLUMN `ï»¿id` TO id;

-- 🔗 Join Student and Profile tables
SELECT 
    s.admission_number, 
    s.firstname, 
    s.lastname, 
    p.grade, 
    p.email
FROM Student_Table s
JOIN Student_Profile_Table p ON s.admission_number = p.admission_number;

-- 📊 View student results by admission number
SELECT 
    s.firstname, 
    s.lastname, 
    c.course_name, 
    r.first_ca, 
    r.second_ca, 
    r.exam
FROM All_Results r
JOIN Student_Table s ON r.student = s.admission_number
JOIN Course_Table c ON r.course_code = c.course_code
WHERE s.admission_number = 'SS2-24-101';

-- 📊 View results by course code
SELECT 
    s.firstname, 
    s.lastname, 
    c.course_name, 
    r.first_ca, 
    r.second_ca, 
    r.exam
FROM All_Results r
JOIN Student_Table s ON r.student = s.admission_number
JOIN Course_Table c ON r.course_code = c.course_code
WHERE c.course_code = 'agric-s2';

-- 📊 View results by student name
SELECT 
    s.firstname, 
    s.lastname, 
    c.course_name, 
    r.first_ca, 
    r.second_ca, 
    r.exam
FROM All_Results r
JOIN Student_Table s ON r.student = s.admission_number
JOIN Course_Table c ON r.course_code = c.course_code
WHERE s.firstname = 'Michael' AND s.lastname = 'Smith';