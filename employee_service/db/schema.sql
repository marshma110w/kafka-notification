DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    department VARCHAR(128) NOT NULL,
    notification_type VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL
);

DROP TABLE IF EXISTS outbox_events;

CREATE TABLE outbox_events (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP NOT NULL,
    type VARCHAR(128) NOT NULL,
    data JSONB NOT NULL,
    processed BOOLEAN DEFAULT FALSE
);
