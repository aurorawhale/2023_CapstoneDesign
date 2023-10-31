USE courseDB;
CREATE TABLE course
(
	ID integer NOT NULL auto_increment,
	campus char(15) NOT NULL,
    courseID char(8) NOT NULL,
    subID char(4) NOT NULL,
    division char(15) NOT NULL,
    department char(100) NOT NULL,
    courseName char(200) NOT NULL,
    professor char(100),
    primary key (ID)
);

CREATE TABLE book
(
	bookID integer NOT NULL auto_increment,
	bookname char(200) NOT NULL,
    author char(100) NOT NULL,
    published integer NOT NULL,
    primary key (bookID)
);

CREATE TABLE course_book 
(
	relation_id integer NOT NULL auto_increment,
	bookID integer,
    courseID integer,
    primary key(relation_id),
    foreign key (courseID) references course(ID) ON DELETE CASCADE,
    foreign key (bookID) references book(bookID) ON DELETE CASCADE
);