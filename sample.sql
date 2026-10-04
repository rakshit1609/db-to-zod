
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    full_name TEXT,
    created_at DATETIME NOT NULL
);

CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    plan TEXT NOT NULL,
    active BOOLEAN NOT NULL
);
