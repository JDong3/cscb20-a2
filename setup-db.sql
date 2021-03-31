create table users (
    username text,
    password text,
    type text,
    primary key (username)
);

insert into
users (username, password, type)
Values
('student1', 'student1', 'student'),
('student2', 'student2', 'student'),
('instructor1', 'instructor1', 'instructor'),
('instructor2', 'instructor2', 'instructor');
