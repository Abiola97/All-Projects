Create database Local_Sales_db;
Use Local_sales_db;
Create Table Local_Sales (
	Customer VarChar(20),
    Fruit_1 varchar(20),
    Fruit_2 varchar(20),
    Fruit_3 Varchar(20),
    Fruit_4 varchar(20),
    Total_Fruits int,
    Date_of_Purchase date,
    Day varchar(10), 
    Purchase_Id int Primary key
);

Select Customer, sum(Total_Fruits) as Total_Fruits
From Local_Sales
Group By Customer
Order By Total_Fruits Desc
Limit 1;

Select Count(distinctrow(customer)) as unique_customer
from Local_Sales;

Select Distinct(Fruit_4)
From local_sales
Where Fruit_4 NOT IN (
	Select Fruit_1 from local_sales
    Union Select Fruit_2 from local_sales
    union Select Fruit_3 from local_sales
    );
use local_sales_db;
Create view local_sales_view as
Select *
from Local_sales as view_table;

Select *
From local_sales_view;
Delimiter //
Create procedure view_table_sales()
Begin
Select *
from Local_sales;
End //
Delimiter ;

Call view_table_sales;

Select Fruit_1, Sum(Total_Fruits) as Total_Fruits
from local_sales
group by Fruit_1
order by Total_Fruits Desc
Limit 1;

call view_table_sales;

select Customer, sum(Total_Fruits) as Total_Fruits
from local_sales
Where Customer = 'Jamie';

Select Day, Sum(Total_Fruits) as Total_Fruits
from local_sales
group by Day
order by Total_Fruits Desc
Limit 1;


SELECT Fruit_1, Fruit_2, COUNT(*) AS Combo_Count
FROM Local_sales
GROUP BY Fruit_1, Fruit_2
ORDER BY Combo_Count DESC
LIMIT 1;

SELECT Fruit_3, Fruit_4, COUNT(*) AS Combo_Count
From local_sales
Group by Fruit_3, Fruit_4
Order By Combo_Count asC
LIMIT 1;

SELECT Fruit_3, Fruit_4, COUNT(*) AS Combo_Count
From local_sales
Group by Fruit_3, Fruit_4
Order By Combo_Count asC
LIMIT 1;

SELECT Fruit_3, Fruit_4, COUNT(*) AS Combo_Count
From local_sales
Group by Fruit_3, Fruit_4
Order By Combo_Count asC
LIMIT 1;

call view_table_sales;
SELECT Fruit_3, Sum(Total_Fruits) as Total_Fruits
From local_sales
WHERE MONTH(Date_of_Purchase) IN (10, 11, 12)
Group by Fruit_3
Order By Total_Fruits DESC
LIMIT 2;

Select month(Date_of_Purchase)as Month,
sum(Total_Fruits) as Total_Fruits
From local_sales
group by Month
Order by Total_Fruits
Limit 1;

SELECT COUNT(*) as Total_Apple_Appearance
FROM local_sales
WHERE Fruit_1 LIKE '%apple%' OR Fruit_2 LIKE '%apple%' 
OR Fruit_3 LIKE '%apple%' OR Fruit_4 LIKE '%apple%';

SELECT Customer, SUM(Total_Fruits) AS Total_Weekend_Q1_Purchase
FROM Local_Sales
WHERE Customer IN ('Jamie', 'Ralph')
  AND DAY IN ('Sat', 'Sun')
  AND MONTH(Date_of_Purchase) IN (1, 2, 3)
GROUP BY Customer
ORDER BY Customer DESC;

Select Format((sum(Total_Fruits)/42),'NO') as average_daily_sales
from Local_sales;

CREATE TABLE gender (

    Customer_Name VARCHAR(20) PRIMARY KEY,

    Gender VARCHAR(20)

);



INSERT INTO gender



VALUES

    ("Esther","Female"),

    ('Hauwa','Female'),

    ('Isaac','Male'),

    ('Jamie','Male'),

    ('Jerry','Male'),

    ('Joe','Male'),

    ('Juliet','Female'),

    ('Pauline','Female'),

    ('Philip','Male'),

    ('Ralph','Male'),

    ('Sm','Mle');

SELECT * FROM gender

UPDATE gender
SET Customer_Name = "Sam", Gender="Male"
WHERE Customer_Name= "Sm";

Select *
From gender;

Select Gender, count(*) as Frequency_Of_Purchase
From gender
Group By gender
Order By gender Desc;

alter table local_sales
add constraint Customer_Gender
Foreign Key (Customer) References gender(Customer_Name);

Select Gender, Sum(Total_Fruits)
from local_sales Inner Join gender
on Customer = gender.Customer_Name
Where Day = 'Tue'
Group By Gender;