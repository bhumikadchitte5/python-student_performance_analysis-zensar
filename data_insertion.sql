INSERT INTO STUDENT VALUES  
    (3101, 'Pooja', 'Patil', '2004-05-15', 'p.patil@gmail.com'), 
    (3102, 'Samir', 'Thakur', '2003-08-20', 'samir@gmail.com'), 
    (3204, 'Meena', 'Nikam', '2004-09-10', 'meena@gmail.com'), 
    (3205, 'Ishan', 'Hire', '2003-02-25', 'isha@example.com'), 
    (3115, 'Robert', 'Johnson', '2004-11-30', 'robert@gmail.com'), 
    (3106, 'Lalit', 'Desale', '2002-03-18', 'l.desale@gmail.com'), 
    (3107, 'David', 'Clark', '2003-06-05', 'david@gmail.com'), 
    (3208, 'Sophia', 'John', '2004-10-12', 'sophia@gmail.com'), 
    (3219, 'James', 'Lee', '2003-12-21', 'james@gmail.com'), 
    (3110, 'Olivia', 'Gite', '2004-01-29', 'olivia@gmail.com');
    
INSERT INTO COURSES VALUES 
(212101, 'PYTHON', '2024-01-10', '2024-05-20', 4),
(212102, 'JAVA', '2024-01-12', '2024-05-22', 5),
(212103, 'JAVASCRIPT', '2024-01-15', '2024-05-25', 3),
(212104, 'CPP', '2024-01-18', '2024-05-28', 5),
(212105, 'DATA STRUCTURE', '2024-01-20', '2024-05-30', 4);

INSERT INTO GRADES(STUDENT_ID,COURSE_ID,MARKS,GRADE) VALUES 
(3101, 212101, 85, 'A'),
(3101, 212102, 78, 'B'),
(3102, 212101, 88, 'A'),
(3102, 212103, 92, 'A'),
(3204, 212104, 65, 'C'),
(3205, 212105, 72, 'B'),
(3115, 212101, 90, 'A'),
(3106, 212102, 84, 'B'),
(3107, 212103, 76, 'B'),
(3208, 212104, 80, 'B');