create table users (
    username text,
    password text,
    type text,
    primary key (username)
);

create table marks(
    student text,
    assignment text,
    mark real
);

create table feedback(
    instructor text,
    q1 text,
    q2 text,
    q3 text,
    q4 text
);

create table requests(
    markid int,
    comment text
);

create table ships (
    instructor text,
    student text,
    primary key (instructor, student)
);

insert into
users (username, password, type)
Values
('student1', 'student1', 'student'),
('student2', 'student2', 'student'),
('instructor1', 'instructor1', 'instructor'),
('instructor2', 'instructor2', 'instructor');

insert into
ships (instructor, student)
values
('instructor1', 'student1'),
('instructor2', 'student2');

insert into
marks ('student', 'assignment', 'mark')
values
('student1', 'assignment1', '69'),
('student1', 'test1', '420'),
('student2', 'assignment1', '100'),
('student2', 'assignment2', '1');

insert into
feedback ('instructor', 'q1', 'q2', 'q3', 'q4')
values
('instructor1', 'ravioli', 'ravioli', 'give me', 'the formuoli'),
('instructor1', 'clean up, clean up', 'we all had fun today', 'now its time to clean up and', 'put everything away'),
('instructor2', 'political power', 'comes from', 'the barrel', 'of apple juice'),
('instructor2', 'it is of', 'there is nothing', 'more important than', 'appearing to be', 'secular');

insert into
requests ()
