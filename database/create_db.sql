create database business_db;

use business_db;

create table owners(
	id int not null primary key auto_increment,
    name varchar(255),
    email varchar(255),
    phone varchar(50),
    categories varchar(255),
    img_url varchar(255),
    info varchar(255)
);

create table images(
	id int not null primary key auto_increment,
	owner_id int,
    img_url varchar(255),
	foreign key (owner_id) references owners(id)
);

create table items(
	id int not null primary key auto_increment,
	img_id int,
    owner_id int,
    name varchar(255),
    price int,
    info varchar(255),
    foreign key (owner_id) references owners(id),
    foreign key (img_id) references images(id)
);
