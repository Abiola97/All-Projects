
# 🏥 Healthcare Database System (MySQL)

A structured SQL-based system for managing patient records, hospital admissions, billing, and insurance data. Built for healthcare analysts, data engineers, or institutions seeking normalized, query-optimized databases with aggregate insights and reporting capabilities.

---

## 📦 Features

- ✅ Relational schema with clean column types and healthcare-specific attributes  
- 📥 Manual or CSV-based data entry for patient records  
- 📊 Aggregate analytics: billing totals, averages, gender proportions, insurance usage  
- 🔍 Query flexibility: by gender, insurance provider, admission type, or medical condition  
- 🧮 Derived metrics using `SUM`, `AVG`, `COUNT`, `MAX`, `MIN`, and subqueries  
- 👁 Views and temporary tables for insurance provider segmentation  

---

## 🗂 Schema Overview

### `healthcare` Table

| Column              | Type         | Description                          |
|---------------------|--------------|--------------------------------------|
| Patient_Name        | VARCHAR(50)  | Full name of the patient             |
| Age                 | INT          | Patient age                          |
| Gender              | VARCHAR(10)  | Male or Female                       |
| Blood_Type          | VARCHAR(5)   | Blood group                          |
| Medical_Condition   | VARCHAR(10)  | Diagnosis                            |
| Date_of_Admission   | DATE         | Admission date                       |
| Doctor              | VARCHAR(50)  | Attending physician                  |
| Hospital            | VARCHAR(50)  | Hospital name                        |
| Insurance_Provider  | VARCHAR(20)  | Insurance company                    |
| Billing_Amount      | FLOAT        | Total bill                           |
| Room_Number         | INT          | Assigned room                        |
| Admission_Type      | VARCHAR(10)  | Emergency, Urgent, Elective          |
| Discharge_Date      | DATE         | Date of discharge                    |
| Medication          | VARCHAR(30)  | Prescribed medication                |
| Test_Results        | VARCHAR(20)  | Lab result summary                   |

---

## 🧮 Aggregate Queries

### Total Billing Amount

```sql
SELECT FORMAT(SUM(billing_amount), 'N0') AS total_billing_amount
FROM healthcare;
```

### Average Billing Amount

```sql
SELECT FORMAT(AVG(billing_amount), 'N0') AS average_billing_amount
FROM healthcare;
```

### Highest & Lowest Billing

```sql
SELECT FORMAT(MAX(billing_amount), 'N0') AS highest_billing_amount
FROM healthcare;

SELECT FORMAT(MIN(billing_amount), 'N0') AS lowest_billing_amount
FROM healthcare;
```

### Entry Count & Column Count

```sql
SELECT FORMAT(COUNT(*), 'N0') AS number_of_data_entry
FROM healthcare;

SELECT COUNT(*) AS number_of_columns
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'healthcare';
```

---

## 📊 Insurance & Gender Analytics

### Insurance Usage & Spend

```sql
SELECT insurance_provider, COUNT(*) AS number_of_times,
FORMAT(SUM(billing_amount), 'N0') AS total_billing_amount
FROM healthcare
GROUP BY insurance_provider;
```

### Gender Proportion

```sql
SELECT gender, COUNT(*) AS gender_proportion
FROM healthcare
GROUP BY gender
ORDER BY gender_proportion DESC
LIMIT 1;
```

### Gender Difference (Max vs Min)

```sql
SELECT
  (SELECT COUNT(*) FROM healthcare WHERE gender = 'Female') -
  (SELECT COUNT(*) FROM healthcare WHERE gender = 'Male') AS gender_difference;
```

---

## 🧾 Insurance Provider Segmentation

### Permanent Table

```sql
CREATE TABLE HMOs AS
SELECT DISTINCT insurance_provider
FROM healthcare;
```

### Temporary Table

```sql
CREATE TEMPORARY TABLE hmo AS
SELECT DISTINCT insurance_provider
FROM healthcare;
```

### View

```sql
CREATE VIEW hmo_view AS
SELECT DISTINCT insurance_provider
FROM healthcare;
```

---

## 🔍 Sample Query

```sql
SELECT Patient_Name, Medical_Condition, Billing_Amount
FROM healthcare
WHERE Admission_Type = 'Emergency' AND Test_Results = 'Abnormal';
```

## 👤 Author

Built by Abiola Ajao  
🎓 Master’s in Collective Intelligence @ UM6P  
💼 Data Analyst → Product Manager  
📍 Morocco & Nigeria  
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 ajaoabiola0812@gmail.com




