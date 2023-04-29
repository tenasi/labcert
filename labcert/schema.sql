-- Initialize the database.
-- Drop any existing data and create empty tables.

-- DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS certs;

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS certs (
    cert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cert_name TEXT NOT NULL,
    cert_level INTEGER NOT NULL,
    cert_type TEXT NOT NULL,
    cert_status TEXT NOT NULL,
    cert_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cert_serial TEXT NOT NULL,
    cert_not_valid_before TIMESTAMP NOT NULL,
    cert_not_valid_after TIMESTAMP NOT NULL,
    subject_name TEXT NOT NULL,
    subject_algorithm TEXT NOT NULL,
    subject_strength TEXT NOT NULL,
    issuer_id INTEGER,
    issuer_name TEXT,
    issuer_type TEXT
);
