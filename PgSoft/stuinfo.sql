CREATE DATABASE IF NOT EXISTS MyDB;

CREATE TABLE IF NOT EXISTS Stu
(
	Sno CHAR(4) PRIMARY KEY,
	Sname VARCHAR(10),
	Gender CHAR(2),
	Age INT,
	Birthday DATE,
	theClass CHAR(10) 
);

CREATE TABLE IF NOT EXISTS Course
(
	Cno CHAR(2) PRIMARY KEY,
	Cname VARCHAR(10),
	Chour INT
);

CREATE TABLE IF NOT EXISTS Score
(
	Sno CHAR(4),
	Cno CHAR(2),
	Grade INT,
	PRIMARY KEY(Sno, Cno)
);

USE MyDB;

-- 向stu中插入数据
INSERT INTO Stu(Sno, Sname, Gender, Age, Birthday, theClass)
	VALUES	('0101', '张强', '男', 20, '2000-2-20', '电子01班'),
			('0102', '李红', '女', 20, '2000-8-10', '电子01班'),
			('0103', '王涛', '男', 21, '1999-5-18', '电子01班'),
			('0104', '刘丽', '女', 19, '2001-3-5', 	'电子01班'),
			('0105', '孙东', '男', 21, '1999-12-17', '电子01班'),
			('0106', '王平', '男', 22, '1998-11-30', '电子01班'),
			('0201', '欧阳燕', '女', 20, '2000-4-11', '自动化05班'),
			('0202', '杨锐', '男', 20, '2000-5-13', '自动化05班'),
			('0203', '刘艳', '女', 18, '2002-1-21', '自动化05班'),
			('0204', '李昱棋', '男', 19, '2000-7-29', '自动化05班');
			
-- 向course中插入数据
INSERT INTO Course(Cno, Cname, Chour)
	VALUES	('01', '计算机软件技术基础', 48),
			('02', 'Java程序设计', 32);
			
-- 向Score中插入数据
INSERT INTO Score(Sno, Cno, Grade)
	VALUES	('0101', '01', 84),
			('0102', '01', 92),
			('0103', '01', 79),
			('0104', '01', 89),
			('0105', '01', 58),
			('0106', '01', 77),
			('0201', '01', 95),
			('0202', '01', 82),
			('0203', '01', 76),
			('0204', '01', 70),
			('0101', '02', 91),
			('0102', '02', 88),
			('0103', '02', 75),
			('0104', '02', 91),
			('0105', '02', 78),
			('0106', '02', 76),
			('0201', '02', 90),
			('0202', '02', 84),
			('0203', '02', 83),
			('0204', '02', 57);
			
SHOW TABLES;

-- 查看数据表
SELECT * FROM Stu;
SELECT * FROM Course;
SELECT * FROM Score;

-- 查询学生出生日期
SELECT 	Sno, Sname, BirthDay 
FROM 	Stu;

-- 按学号顺序查询标记为本人班级的所有学生
SELECT 	* 
FROM 	Stu 
WHERE 	theClass = '自动化05班' 
ORDER BY Sno;

-- 列出学生选择各门课程的成绩
SELECT Stu.Sname, Course.Cname, Score.Sno, Score.Grade
FROM Stu, Course, Score
WHERE Stu.Sno = Score.Sno 
	AND Score.Cno = Course.Cno;
	
-- 列出有过不及格成绩的学生名单
SELECT Score.Sno, Stu.Sname, Stu.theClass
FROM Score, Stu
WHERE Score.Sno = Stu.Sno
	AND Score.Grade < 60;

-- 求学生的平均成绩和总成绩
SELECT stu.Sname, PJCJ, ZCJ
FROM
	(SELECT score.Sno, AVG(score.Grade) as PJCJ, SUM(score.Grade) as ZCJ
	FROM score
	GROUP BY score.Sno) as pr, stu
WHERE stu.Sno = pr.Sno;

-- 查找各科成绩都 >= 85 分的学生
SELECT stu.Sname, stu.theClass
FROM
	(SELECT score.Sno, score.Grade
	FROM score
	WHERE score.Cno = '01') AS mtb1,
	(SELECT score.Sno, score.Grade
	FROM score
	WHERE score.Cno = '01') AS mtb2,
	stu
WHERE
	mtb1.Sno = stu.Sno
	AND stu.Sno = mtb2.Sno
	AND mtb1.Grade >= 85
	AND mtb2.Grade >= 85;

-- 将课程号为“01”的课程名称修改为“软件技术”；
UPDATE Course
SET Course.Cname = '软件技术'
WHERE Course.Cno = '01';

SELECT *
FROM Course;

-- 将标记为本人姓名的学生的姓名数据修改为本人学号；
UPDATE Stu
SET Stu.Sname = '20184023'
WHERE Stu.Sname = '李昱棋';

SELECT *
FROM Stu;

-- 将成绩为55~59分的男生的成绩修改为60分；
UPDATE Score, Stu
SET SCore.Grade = 60
WHERE Stu.Sno = Score.Sno
	AND Stu.Gender = '男'
	AND Score.Grade >= 55
	AND Score.Grade <= 59;

SELECT Stu.Sname, Course.Cname, Score.Sno, Score.Grade
FROM Stu, Course, Score
WHERE Stu.Sno = Score.Sno 
	AND Score.Cno = Course.Cno;


-- 删除01年以后、99年以前出生的学生的所有信息(包括选课和成绩)；
DELETE
FROM stu
WHERE stu.Birthday NOT BETWEEN '1999-01-01' AND '2000-12-31'; 

-- 删除一个班级的所有学生；
DELETE 
FROM 	Stu;

-- 删除数据表
DROP TABLE Stu, Course, Score;
SHOW TABLES;

-- 删除数据库
DROP DATABASE MyDB;
SHOW DATABASES;
			


