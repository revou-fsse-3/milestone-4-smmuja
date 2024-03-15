CREATE DATABASE milestone_4_smmuja;

USE milestone_4_smmuja;

CREATE TABLE user (
	id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

START TRANSACTION;
ALTER TABLE user ADD COLUMN role ENUM ('User', 'Admin') NULL DEFAULT NULL;
ALTER TABLE user ADD COLUMN role VARCHAR (255) NULL DEFAULT NULL;


ROLLBACK;
COMMIT;


CREATE TABLE account (
	id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    account_type VARCHAR(255) NOT NULL,
    account_number VARCHAR(255) NOT NULL,
    balance DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

START TRANSACTION;

ALTER TABLE  `account` ADD UNIQUE (`id` ,`account_number`);

ALTER TABLE account 
MODIFY COLUMN account_type ENUM ('Checking', 'Savings') NOT NULL;


ROLLBACK;
COMMIT;

CREATE TABLE transaction (
	id INT PRIMARY KEY AUTO_INCREMENT,
    from_account_id INT,
    to_account_id INT,
    amount DECIMAL(10,2) NOT NULL,
    type VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	
    FOREIGN KEY (from_account_id) REFERENCES account(id),
    FOREIGN KEY (to_account_id) REFERENCES account(id)
);

select * from user;

select * from transaction;

select * from account;