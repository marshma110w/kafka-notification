DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    department VARCHAR(128) NOT NULL,
    notification_type VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL
);
