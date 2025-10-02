Create database join_db;
Use join_db;

alter table course
modify course_id varchar(10),
modify course_name char(30);

alter table course
modify student_id varchar(6),
modify course_name char(150);

alter table student
modify student_id varchar(10) Primary key;

alter table course
add constraint
foreign key(student_id) references student(student_id),
modify course_id varchar(6) primary key
;

Select *
from student;

Select *
from course;

-- INNER JOIN OUTER JOIN RIGHT JOIN
Select *
From student s
inner Join course c
on s.student_id = c.student_id;

insert into course(course_id, course_name)
values(106, 'Literature');

Select *
From student s
left join course c
on s.student_id = c.student_id;

Select *
From student s
right join course c
on s.student_id = c.student_id;

use join_db;
Select *
From emp_salary1;

Select Department, AVG(Salary)
From join_db.emp_salary1
Group BY Department;

-- USING WINDOW FUNCTION
Select *, AVG(Salary) over(partition by Department) AS average_salary
From join_db.emp_salary1;

Select *, Dense_Rank() Over(order by Salary DEsc) as ranking
from join_db.emp_salary1;

Select *, Dense_Rank() Over(Partition by Department order by Salary DEsc) as ranking
from join_db.emp_salary1;

Select Department, Avg(Salary) as avg_salary
from join_db.emp_salary1
group by Department
Having avg_salary >=35000;
	