CREATE TABLE users(id serial, name varchar(64), password varchar(64), email varchar(128), role int, balance int, purse varchar(64));

INSERT INTO users (name, password, email, role, balance, purse) VALUES ('Diller', 'D1ll3r_P@5Sw0rd', 'diller_email@casic.ru', 1, 0, '<None>');
