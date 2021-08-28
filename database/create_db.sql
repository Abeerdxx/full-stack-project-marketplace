create database business_db;

use business_db;

create table owners(
	id int not null primary key auto_increment,
    categories varchar(255),
    info varchar(255)
);

create table users(
	id int not null primary key auto_increment,
    name varchar(255),
    email varchar(255) UNIQUE,
    city varchar(255),
    zip_code varchar(255),
    phone varchar(50),
    img_url varchar(255),
    pass_hash varchar(255),
    type BIT,
    foreign key (id) references owners(id)
);

create table images(
	owner_id int,
    img_url varchar(500) primary key,
	foreign key (owner_id) references owners(id)
);

create table items(
	id int not null primary key auto_increment,
	img_url varchar(255),
    owner_id int,
    name varchar(255),
    price int,
    info varchar(255),
    foreign key (owner_id) references owners(id),
    foreign key (img_url) references images(img_url)
);

create table Messages(
    receiver int,
    sender varchar(255),
    msg varchar(255),
    foreign key (receiver) references users(email)
);
