CREATE DATABASE IF NOT EXISTS cs353hw4db;
USE cs353hw4db;

create table User (
    id int not null auto_increment,
    password varchar(30) not null,
    username varchar(255) not null unique,
    email varchar(255) not null,
    primary key(id)
);

create table TaskType(
    type varchar(255) not null unique,
    primary key(type)
);

create table Task (
    id int not null auto_increment,
    title varchar(255) not null,
    description text not null,
    status varchar(255) not null,
    deadline datetime not null,
    creation_time datetime not null,
    done_time datetime,
    user_id int not null,
    task_type varchar(255) not null,
    primary key(id),
    foreign key (user_id) references User(id),
    foreign key (task_type) references TaskType(type) 
);

insert into User (password,username,email)
values ("pass123", "user1", "user1@example.com"), ("password","user2", "user2@example.com");

insert into TaskType (type)
values ("Health"), ("Job"), ("Lifestyle"), ("Family"), ("Hobbies");

insert into Task (title, description, status, deadline, creation_time, done_time, user_id, task_type)
values ("Go for a walk", "Walk for at least 30 mins",  "Done", "2023-03-20 17:00:00", "2023-03-15 10:00:00", "2023-03-20 10:00:00",  1 ,"Health"),
("Clean the house", "Clean the whole house",  "Done", "2023-03-18 12:00:00", "2023-03-14 09:00:00", "2023-03-18 17:00:00", 1 ,"Lifestyle"),
("Submit report", "Submit quarterly report",  "Todo", "2023-04-12 17:00:00", "2023-03-21 13:00:00" ,null, 1 , "Job"),
("Call Mom", "Call Mom and wish her",  "Todo", "2023-04-06 11:00:00", "2023-03-23 12:00:00", null, 1 ,"Family"),
("Gym workout", "Do weight training for an hour",  "Done", "2023-03-19 14:00:00", "2023-03-12 10:00:00", "2023-03-19 11:00:00", 1 , "Health"),
("Play guitar", "Learn new song for an hour",  "Todo", "2023-04-05 20:00:00", "2023-03-20 14:00:00", null, 2, "Hobbies"),
("Book flights", "Book flights for summer vacation", "Done", "2023-03-16 09:00:00", "2023-03-13 13:00:00", "2023-03-16 11:00:00", 2 , "Lifestyle"),
("Write a blog post", "Write about recent project", "Todo", "2023-04-11 17:00:00", "2023-03-22 09:00:00", null, 2, "Job"),
("Grocery shopping", "Buy groceries for the week", "Todo", "2023-04-05 18:00:00", "2023-03-31 10:00:00", null, 2, "Family"),
("Painting", "Paint a landscape for 2 hours", "Done", "2023-03-23 15:00:00", "2023-03-18 14:00:00", "2023-03-23 16:00:00", 2, "Hobbies");

