Create Database healthcare_db; 
Use healthcare_db;
Create Table healthcare (
	Patient_Name Varchar (50),
	Age	Int,
	Gender Varchar(10),
	Blood_Type Varchar(5),
	Medical_Condition Varchar(10),
	Date_of_Admission Date,	
	Doctor Varchar(50),
	Hospital Varchar(50),
	Insurance_Provider Varchar(20),
	Billing_Amount float,
    Room_Number INT,
    Admission_Type Varchar(10),
	Discharge_Date Date,
	Medication	Varchar(30),
    Test_Results varchar(20)
    );

Select * 
from healthcare;

USE healthcare;

SELECT * 
FROM healthcare_db;
-- TOTAl BILLING AMOUNT USING SUM AGGREGATE

-- SELECT *
-- FROM database_name.table_name;

-- SELECT *
-- FROM rms.student;

-- TOTAL BILLING AMOUNT USING SUM AGGREGATE

SELECT FORMAT(SUM(billing_amount),'N0') AS total_billing_amount
FROM healthcare;

-- NUMBER OF ENTRIES IN MY HEALTHCARE DATABASE USING COUNT AGGREGATE

SELECT FORMAT(COUNT(*),'N0') as number_of_data_entry
FROM healthcare;

-- NUMBER OF COLUMN OF THE HEALTHCARE_DB TABLE
SELECT COUNT(*) as number_of_columns
FROM INFORMATION_SCHEMA.COLUMNS;


-- AVERAGE BILLING AMOUNT

SELECT FORMAT(AVG(billing_amount),'N0') AS average_billing_amount
FROM healthcare;

-- HIGHEST BILLING AMOUNT
SELECT FORMAT(MAX(billing_amount),'N0') AS highest_billing_amount
FROM healthcare;


-- LOWEST BILLING AMOUNT
SELECT FORMAT(MIN(billing_amount),'N0') AS lowest_billing_amount
FROM healthcare;

-- number times patient use an insurance provider

SELECT insurance_provider, COUNT(insurance_provider) AS number_of_times, 
FORMAT(SUM(billing_amount),'N0') AS total_billing_amount
FROM healthcare
GROUP BY insurance_provider
;

SELECT gender, COUNT(gender) as gender_proportion
FROM healthcare
GROUP BY gender
ORDER BY gender_proportion DESC
LIMIT 1;

SELECT gender, COUNT(gender) as gender_proportion
FROM healthcare_db
GROUP BY gender
ORDER BY gender_proportion
LIMIT 1;

SELECT
(SELECT COUNT(gender) as gender_proportion
FROM healthcare
GROUP BY gender
ORDER BY gender_proportion DESC
LIMIT 1) - (SELECT COUNT(gender) as gender_proportion
FROM healthcare
GROUP BY gender
ORDER BY gender_proportion
LIMIT 1) AS gender_difference;


SELECT COUNT(DISTINCT insurance_provider)
FROM healthcare;

USE healthcare_db;
CREATE TABLE HMOs AS
SELECT DISTINCT insurance_provider
FROM healthcare;

SELECT *
FROM hmos;

CREATE TEMPORARY TABLE hmo AS
SELECT DISTINCT insurance_provider FROM healthcare;

SELECT *
FROM hmo;

CREATE VIEW hmo_view AS 
SELECT DISTINCT insurance_provider
FROM healthcare;

SELECT *
FROM hmo_view;
