-- Active: 1682796954254@@phase2-team13.c4lq3dlivano.us-east-1.rds.amazonaws.com@3306@university

USE university;
-- Table for storing student information

-- Create user table
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    uid INT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(32),
    fname VARCHAR(32),
    lname VARCHAR(32),
    address VARCHAR(128),
    email VARCHAR(50),
    ssn INT
);

-- Create student table with foreign key reference to user table

DROP TABLE IF EXISTS student;
CREATE TABLE student (
    studentid INT PRIMARY KEY,
    program VARCHAR(10),
    rdygrad INT,
    advisorid int NULL,
    FOREIGN KEY (studentid) REFERENCES user(uid) ON DELETE CASCADE
);

-- Create alumni table with foreign key reference to user table

DROP TABLE IF EXISTS alumni;
CREATE TABLE alumni (
    alumnid INT PRIMARY KEY,
    FOREIGN KEY (alumnid) REFERENCES user(uid) ON DELETE CASCADE
);

-- Create faculty table with foreign key reference to user table

DROP TABLE IF EXISTS faculty;
CREATE TABLE faculty (
    facultyID INT PRIMARY KEY,
    facultyRole VARCHAR(32), -- 1 for grad sec, 2 for advisor, 3 for admin, 4 for FR, 5 for Chair, 6 for SA
    FOREIGN KEY (facultyID) REFERENCES user(uid) ON DELETE CASCADE
);

-- Create applicant table with foreign key reference to user table

DROP TABLE IF EXISTS applicant;
CREATE TABLE applicant (
    applicantID INT PRIMARY KEY,
    applicantStatus VARCHAR(55),
    FOREIGN KEY (applicantID) REFERENCES user(uid) ON DELETE CASCADE
);


-- Create course table
DROP TABLE IF EXISTS course;
CREATE TABLE course (
    cid INT,
    dept VARCHAR(4),
    courseNumber INT,
    title VARCHAR(64),
    credits INT,
    instructorID INT,
    day VARCHAR(1),
    course_start INT,
    course_end INT, 
    PRIMARY KEY (cid), 
    FOREIGN KEY (instructorID) REFERENCES faculty(facultyID),
    CONSTRAINT unique_course UNIQUE(dept, courseNumber)
);

DROP TABLE IF EXISTS preq;
CREATE TABLE preq (
    courseID INT,
    preqID INT,
    Primary Key (courseID, preqID),
    FOREIGN KEY (courseID) REFERENCES course(cid)
);
DROP TABLE IF EXISTS transcript;
CREATE TABLE transcript(
  tuid INT,
  cid INT,
  grade varchar(4),
  semester varchar(20),
  year varchar(20),
  Foreign Key (tuid) REFERENCES user(uid),
  FOREIGN KEY (cid) REFERENCES course(cid) ON DELETE CASCADE,
  PRIMARY KEY (tuid, cid, semester, year)
);

DROP TABLE IF EXISTS form1;
CREATE TABLE form1(
  id          int(15),
  courseDept  varchar(4),
  courseNum  varchar(50) not null, 
  holding int,
  primary key(id, courseDept, courseNum),
  foreign key(id) references student(studentid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS thesis;
CREATE TABLE thesis(
  thesis LONGTEXT,
  uid INT,
  decision int NULL,
  FOREIGN KEY (uid) REFERENCES student(studentid) ON DELETE CASCADE
);

DROP TABLE IF EXISTS ApplicationForm;
CREATE TABLE ApplicationForm (
    studentID INT(8) NOT NULL,
    degreeSeeking VARCHAR(32) NOT NULL,
    MScheck VARCHAR(32),
    MSmajor VARCHAR(32),
    MSyear INT(4),
    MSuniversity VARCHAR(32),
    MSgpa DECIMAL(3,2),
    BAcheck VARCHAR(32) NOT NULL,
    BAmajor VARCHAR(32) NOT NULL,
    BAyear INT(4) NOT NULL,
    BAuniversity VARCHAR(32) NOT NULL,
    BAgpa DECIMAL(3,2) NOT NULL,
    GREverbal INT(3),
    GREquantitative INT(3),
    GREyear INT(4),
    GREadvancedScore INT(4),
    GREadvancedSubject VARCHAR(32),
    TOEFLscore INT(4),
    TOEFLdate VARCHAR(32),
    priorWork VARCHAR(300) NOT NULL,
    startDate VARCHAR(32) NOT NULL,
    transcriptStatus VARCHAR(32),
    r1status VARCHAR(32),
    r1writer VARCHAR(32) NOT NULL,
    r1email VARCHAR(32) NOT NULL,
    r1title VARCHAR(32) NOT NULL,
    r1affiliation VARCHAR(32) NOT NULL,
    r1letter VARCHAR(500) NOT NULL,
    r2status VARCHAR(32),
    r2writer VARCHAR(32),
    r2email VARCHAR(32),
    r2title VARCHAR(32),
    r2affiliation VARCHAR(32),
    r2letter VARCHAR(500),
    r3status VARCHAR(32),
    r3writer VARCHAR(32),
    r3email VARCHAR(32),
    r3title VARCHAR(32),
    r3affiliation VARCHAR(32),
    r3letter VARCHAR(500),
    PRIMARY KEY(startDate, studentID)
);

DROP TABLE IF EXISTS ReviewForm;
CREATE TABLE ReviewForm (
  studentID INT(8) NOT NULL,
  reviewer VARCHAR(32) NOT NULL,
  r1rating INT(1) NOT NULL,
  r1generic VARCHAR(1) NOT NULL,
  r1credible VARCHAR(1) NOT NULL,
  r1from VARCHAR(10) NOT NULL,
  r2rating INT(1),
  r2generic VARCHAR(1),
  r2credible VARCHAR(1),
  r2from VARCHAR(10),
  r3rating INT(1),
  r3generic VARCHAR(1),
  r3credible VARCHAR(1),
  r3from VARCHAR(1),
  GASrating INT(1) NOT NULL,
  deficiencies VARCHAR(40),
  rejectReason VARCHAR(40),
  thoughts VARCHAR(40),
  semesterApplied VARCHAR(10) NOT NULL,
  decision VARCHAR(32) NOT NULL,
  PRIMARY KEY (studentID, reviewer),
  FOREIGN KEY (studentID) REFERENCES applicant(applicantID) ON DELETE CASCADE
);


INSERT INTO user (uid, username, password, fname, lname, address, email, ssn)
VALUES (12312312, 'JohnLennon', 'Jonny', 'John', 'Lennon', 'SEH', 'johnLennon@example.com', '111111111');
INSERT INTO applicant (applicantID, applicantStatus) VALUES (12312312, 'Application Recieved and Decision Pending');
INSERT INTO ApplicationForm (studentID, degreeSeeking, MScheck, BAcheck, BAmajor,
                              BAyear, BAuniversity, BAgpa, GREverbal, GREquantitative, 
                              GREyear, priorWork, startDate, r1writer, r1email, r1title, r1affiliation)

VALUES (12312312, 'masters', 'no', 'yes', 'CS', 2021, 'GW', 3.47, 165, 134, 2022, 'worked at a startup', 'soon', 'Professor', 'prof@gmail.com', 'Professor rec letter', 'Professor');


INSERT INTO user (uid, username, password, fname, lname, address, email, ssn)
VALUES (66666666, 'RingoStarr', 'ringy', 'Ringo', 'Starr', 'SEH', 'ringoStarr@example.com', '222111111');
INSERT INTO applicant (applicantID, applicantStatus) VALUES (66666666, 'Application Materials Missing');


INSERT INTO user VALUES (55555555, 'pm', 'pm', 'Paul', 'McCartney', '123 Main St, Anytown USA', 'pm@email.com', 322879319);
INSERT INTO student VALUES (55555555, 'masters', 0, 13333333);

INSERT INTO user VALUES (66666665, 'gh', 'gh', 'George', 'Harrison', '456 Elm St, Anytown USA', 'gh@email.com', 918152720);
INSERT INTO student VALUES (66666665, 'masters', 0, 14444444);

INSERT INTO user VALUES (00000003, 'rs', 'rs', 'Ringo', 'Starr', '789 Oak St, Anytown USA', 'rs@email.com', 159720131);
INSERT INTO student VALUES (00000003, 'phd', 0, 14444444);

INSERT INTO user VALUES (00000004, 'sarahlee', 'password4', 'Sarah', 'Lee', '321 Cedar St, Anytown USA', 'sarahlee@email.com', 798066266);
INSERT INTO student VALUES (00000004, 'phd', 0, NULL);

INSERT INTO user VALUES (88888888, 'b_holiday', 'pass', 'Billie', 'Holiday', '1776 Hamilton St, New York USA', 'billie@email.com', 936687952);
INSERT INTO student VALUES (88888888, 'masters', 0, NULL);

INSERT INTO user VALUES (99999999, 'd_krall', 'pass', 'Diana', 'Krall', '1821 Canada St, DC USA', 'dkrall@email.com', 625758829);
INSERT INTO student VALUES (99999999, 'masters', 0, NULL);

INSERT INTO user VALUES (77777777, 'ec', 'ec', 'Eric', 'Clapton', '321 Cedar St, Anytown USA', 'ec@email.com', 754209585
);
INSERT INTO alumni VALUES (77777777);



INSERT INTO user VALUES (13333333, 'bh', 'bh', 'Bhagi', 'Narahari', '123 Main St, Anytown USA', 'bh@university.edu', 761943655);
INSERT INTO faculty VALUES (13333333, 'instructor');
INSERT INTO user VALUES (15151515, 'choi', 'choi', 'Hyeong', 'Choi', '123 Main St, Anytown USA', 'hchoi@university.edu', 753982455);
INSERT INTO faculty VALUES (15151515, 'instructor');
INSERT INTO user VALUES (14444444, 'gp', 'gp', 'Gabe', 'Parmer','123 Main St, Anytown USA', 'gp@university.edu', 811261598);
INSERT INTO faculty VALUES (14444444, 'instructor');
INSERT INTO user VALUES (16666666, 'jt', 'jt', 'James', 'Taylor','123 Main St, Anytown USA', 'jt@university.edu', 681323400);
INSERT INTO faculty VALUES (16666666, 'chair');
INSERT INTO user VALUES (12222222, 'my', 'my', 'Michael', 'Yoo', '123 Main St, Anytown USA','prof1@university.edu', 168155586);
INSERT INTO faculty VALUES (12222222, 'gsec');
INSERT INTO user VALUES (15555555, 'admin', 'admin', 'admin', 'three', '123 Main St, Anytown USA', 'admin@university.edu', 165301167);
INSERT INTO faculty VALUES (15555555, 'admin');
INSERT INTO user VALUES (89898989, 'fr', 'fr', 'for', 'real', '123 Main St, fr USA', 'fr@university.edu', 557539292);
INSERT INTO faculty VALUES (89898989, 'faculty reviewer');





INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (1, 'CSCI', 6221, 'SW Paradigms', 3, NULL, 'M', 1500, 1730);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (2, 'CSCI', 6461, 'Computer Architecture', 3, 13333333, 'T', 1500, 1730); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (3, 'CSCI', 6212, 'Algorithms', 3, 15151515, 'W', 1500, 1730); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (4, 'CSCI', 6220, 'Machine Learning', 3, NULL, 'F', 1500, 1730); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (5, 'CSCI', 6232, 'Networks 1', 3, 13333333, 'M', 1800, 2030);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (6, 'CSCI', 6233, 'Networks 2', 3, NULL, 'M', 1800, 2030);
INSERT INTO preq (courseID, preqID) VALUES (6, 5);

INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (7, 'CSCI', 6241, 'Database 1', 3, NULL, 'W', 1800, 2030); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (8, 'CSCI', 6242, 'Database 2', 3, NULL, 'R', 1800, 2030); 
INSERT INTO preq (courseID, preqID) VALUES (8, 7);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (9, 'CSCI', 6246, 'Compilers', 3, NULL, 'T', 1500, 1730);
INSERT INTO preq (courseID, preqID) VALUES (9, 2);
INSERT INTO preq (courseID, preqID) VALUES (9, 3);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (10, 'CSCI', 6260, 'Multimedia', 3, NULL, 'R', 1800, 2030); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (11, 'CSCI', 6251, 'Cloud Computing', 3, NULL, 'M', 1800, 2030);
INSERT INTO preq (courseID, preqID) VALUES (11, 2);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (12, 'CSCI', 6254, 'SW Engineering', 3, NULL, 'M', 1530, 1800); 
INSERT INTO preq (courseID, preqID) VALUES (12, 1);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (13, 'CSCI', 6262, 'Graphics 1', 3, NULL, 'W', 1800, 2030); 
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (14, 'CSCI', 6283, 'Security 1', 3, NULL, 'T', 1800, 2030); 
INSERT INTO preq (courseID, preqID) VALUES (14, 3);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (15, 'CSCI', 6284, 'Cryptography', 3, NULL, 'M', 1800, 2030); 
INSERT INTO preq (courseID, preqID) VALUES (15, 3);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (16, 'CSCI', 6286, 'Network Security', 3, NULL, 'W', 1800, 2030); 
INSERT INTO preq (courseID, preqID) VALUES (16, 5);
INSERT INTO preq (courseID, preqID) VALUES (16, 14);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (17, 'CSCI', 6325, 'Algorithms 2', 3, NULL, 'M', 1600, 1830);
INSERT INTO preq (courseID, preqID) VALUES (17, 3);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (18, 'CSCI', 6339, 'Embedded Systems', 3, NULL, 'R', 1600, 1830);
INSERT INTO preq (courseID, preqID) VALUES (18, 2);
INSERT INTO preq (courseID, preqID) VALUES (18, 3);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (19, 'CSCI', 6384, 'Cryptography 2', 3, NULL, 'W', 1500, 1730);
INSERT INTO preq (courseID, preqID) VALUES (19, 15);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (20, 'ECE', 6241, 'Communication Theory', 3, NULL, 'M', 1800, 2030);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (21, 'ECE', 6242, 'Information Theory', 2, NULL, 'T', 1800, 2030);
INSERT INTO course (cid, dept, courseNumber, title, credits, instructorID, day, course_start, course_end) VALUES (22, 'MATH', 6210, 'Logic', 2, NULL, 'W', 1800, 2030);

INSERT INTO transcript (tuid, cid, grade, semester, year)
VALUES
(55555555, 1, 'A', 'Fall', '2021'),
(55555555, 2, 'A', 'Fall', '2021'),
(55555555, 3, 'A', 'Spring', '2021'),
(55555555, 5, 'A', 'Spring', '2021'),
(55555555, 6, 'A', 'Fall', '2022'),
(55555555, 7, 'B', 'Spring', '2022'),
(55555555, 8, 'B', 'Fall', '2022'),
(55555555, 9, 'B', 'Spring', '2022'),
(55555555, 13, 'B', 'Fall', '2023'),
(55555555, 14, 'B', 'Fall', '2023');


INSERT INTO transcript (tuid, cid, grade, semester, year)
VALUES
(66666665, 21, 'C', 'Fall', '2021'),
(66666665, 1, 'B', 'Fall', '2021'),
(66666665, 2, 'B', 'Spring', '2021'),
(66666665, 3, 'B', 'Spring', '2021'),
(66666665, 5, 'B', 'Fall', '2022'),
(66666665, 6, 'B', 'Spring', '2022'),
(66666665, 7, 'B', 'Fall', '2022'),
(66666665, 8, 'B', 'Spring', '2022'),
(66666665, 14, 'B', 'Fall', '2023'),
(66666665, 15, 'B', 'Fall', '2023');


INSERT INTO transcript (tuid, cid, grade, semester, year)
VALUES
(00000003, 1, 'A', 'Fall', '2022'),
(00000003, 2, 'A', 'Fall', '2022'),
(00000003, 3, 'A', 'Spring', '2021'),
(00000003, 4, 'A', 'Spring', '2021'),
(00000003, 5, 'A', 'Fall', '2022'),
(00000003, 6, 'A', 'Fall', '2022'),
(00000003, 7, 'A', 'Spring', '2022'),
(00000003, 8, 'A', 'Spring', '2022'),
(00000003, 9, 'A', 'Spring', '2022'),
(00000003, 10, 'A', 'Fall', '2023'),
(00000003, 11, 'A', 'Fall', '2023'),
(00000003, 12, 'A', 'Fall', '2023');

INSERT INTO transcript (tuid, cid, grade, semester, year)
VALUES
(77777777, 1, 'B', 'Fall', '2023'),
(77777777, 3, 'B', 'Fall', '2023'),
(77777777, 2, 'B', 'Fall', '2023'),
(77777777, 8, 'B', 'Fall', '2023'),
(77777777, 5, 'B', 'Fall', '2023'),
(77777777, 6, 'B', 'Fall', '2023'), 
(77777777, 7, 'B', 'Fall', '2023'),
(77777777, 16, 'A', 'Fall', '2023'),
(77777777, 14, 'A', 'Fall', '2023'),
(77777777, 15, 'A', 'Fall', '2023'); 

INSERT INTO transcript (tuid, cid, grade, semester, year)
VALUES
(88888888, 1, 'IP', 'Spring', '2023'),
(88888888, 3, 'IP', 'Spring', '2023');

INSERT INTO thesis (thesis, uid, decision) VALUES ('Sample thesis text', 00000003, NULL);
