

# 🍊 Local Sales Database System (MySQL)

A structured SQL-based system for tracking fruit purchases by customers, analyzing seasonal trends, gender-based buying patterns, and fruit combinations. Designed for retail analysts, data engineers, or small business owners seeking actionable insights from transactional data.

---

## 📦 Features

- ✅ Relational schema with foreign key constraints  
- 📥 Manual or CSV-based data entry for fruit purchases  
- 📊 Aggregate analytics: top buyers, fruit popularity, seasonal trends  
- 🔍 Query flexibility: by customer, fruit combo, day, or month  
- 🧮 Stored procedure `view_table_sales()` for reusable reporting  
- 👁 View `local_sales_view` for dashboard integration  
- 🧑‍🤝‍🧑 Gender-based segmentation via foreign key join  

---

## 🗂 Schema Overview

### `Local_Sales` Table

| Column             | Type         | Description                          |
|--------------------|--------------|--------------------------------------|
| Customer           | VARCHAR(20)  | Name of the buyer                    |
| Fruit_1 to Fruit_4 | VARCHAR(20)  | Fruits purchased                     |
| Total_Fruits       | INT          | Total quantity bought                |
| Date_of_Purchase   | DATE         | Purchase date                        |
| Day                | VARCHAR(10)  | Day of the week                      |
| Purchase_Id        | INT (PK)     | Unique transaction ID                |

### `gender` Table

| Column         | Type         | Description                          |
|----------------|--------------|--------------------------------------|
| Customer_Name  | VARCHAR(20)  | Primary Key                          |
| Gender         | VARCHAR(20)  | Male or Female                       |

---

## 🧮 Stored Procedure: `view_table_sales()`

```sql
DELIMITER //

CREATE PROCEDURE view_table_sales()
BEGIN
  SELECT * FROM Local_Sales;
END //

DELIMITER ;
```

### 📊 How to Use

```sql
CALL view_table_sales();
```

---

## 📊 Aggregate Queries

### Top Buyer

```sql
SELECT Customer, SUM(Total_Fruits) AS Total_Fruits
FROM Local_Sales
GROUP BY Customer
ORDER BY Total_Fruits DESC
LIMIT 1;
```

### Unique Customers

```sql
SELECT COUNT(DISTINCT Customer) AS unique_customer
FROM Local_Sales;
```

### Most Popular Fruit

```sql
SELECT Fruit_1, SUM(Total_Fruits) AS Total_Fruits
FROM Local_Sales
GROUP BY Fruit_1
ORDER BY Total_Fruits DESC
LIMIT 1;
```

### Fruit Combo Frequency

```sql
SELECT Fruit_1, Fruit_2, COUNT(*) AS Combo_Count
FROM Local_Sales
GROUP BY Fruit_1, Fruit_2
ORDER BY Combo_Count DESC
LIMIT 1;
```

---

## 📅 Seasonal & Daily Trends

### Top Day for Sales

```sql
SELECT Day, SUM(Total_Fruits) AS Total_Fruits
FROM Local_Sales
GROUP BY Day
ORDER BY Total_Fruits DESC
LIMIT 1;
```

### Top Fruits in Q4

```sql
SELECT Fruit_3, SUM(Total_Fruits) AS Total_Fruits
FROM Local_Sales
WHERE MONTH(Date_of_Purchase) IN (10, 11, 12)
GROUP BY Fruit_3
ORDER BY Total_Fruits DESC
LIMIT 2;
```

### Lowest Sales Month

```sql
SELECT MONTH(Date_of_Purchase) AS Month, SUM(Total_Fruits) AS Total_Fruits
FROM Local_Sales
GROUP BY Month
ORDER BY Total_Fruits
LIMIT 1;
```

---

## 🍎 Fruit-Specific Insights

### Apple Mentions

```sql
SELECT COUNT(*) AS Total_Apple_Appearance
FROM Local_Sales
WHERE Fruit_1 LIKE '%apple%' OR Fruit_2 LIKE '%apple%' 
   OR Fruit_3 LIKE '%apple%' OR Fruit_4 LIKE '%apple%';
```

### Average Daily Sales

```sql
SELECT FORMAT(SUM(Total_Fruits)/42, 'N0') AS average_daily_sales
FROM Local_Sales;
```

---

## 🧑‍🤝‍🧑 Gender-Based Analysis

### Frequency of Purchase by Gender

```sql
SELECT Gender, COUNT(*) AS Frequency_Of_Purchase
FROM gender
GROUP BY Gender
ORDER BY Frequency_Of_Purchase DESC;
```

### Total Fruits by Gender (Tuesday Only)

```sql
SELECT Gender, SUM(Total_Fruits)
FROM Local_Sales
INNER JOIN gender ON Customer = gender.Customer_Name
WHERE Day = 'Tue'
GROUP BY Gender;
```

---

## 👁 Views & Segmentation

### View: `local_sales_view`

```sql
CREATE VIEW local_sales_view AS
SELECT * FROM Local_Sales;
```

### Foreign Key Constraint

```sql
ALTER TABLE Local_Sales
ADD CONSTRAINT Customer_Gender
FOREIGN KEY (Customer) REFERENCES gender(Customer_Name);
```

---

## 👤 Author

Built by Abiola Ajao  
🎓 Master’s in Collective Intelligence @ UM6P  
💼 Data Analyst → Product Manager  
📍 Morocco & Nigeria  
🔗 [LinkedIn](https://www.linkedin.com/in/abiola-ajao/) | 📧 ajaoabiola0812@gmail.com

---
