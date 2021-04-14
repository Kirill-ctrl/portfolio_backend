DROP SEQUENCE IF EXISTS account_main_id_seq CASCADE;

CREATE SEQUENCE account_main_id_seq START 1;

DROP TABLE IF EXISTS account_main CASCADE;

CREATE TABLE account_main(
    id INTEGER PRIMARY KEY DEFAULT nextval('account_main_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    email VARCHAR(100) NOT NULL CONSTRAINT unique_account_email UNIQUE,
    name VARCHAR(100) NOT NULL,
    hash_password VARCHAR(300),
    is_confirmed BOOLEAN NOT NULL DEFAULT FALSE
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS auth_code_seq CASCADE;

CREATE SEQUENCE auth_code_seq START 1;

DROP TABLE IF EXISTS auth_code CASCADE;

CREATE TABLE auth_code(
    id BIGINT DEFAULT nextval('auth_code_seq') PRIMARY KEY,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    edited_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER UNIQUE NOT NULL REFERENCES account_main(id) ON DELETE CASCADE,
    code VARCHAR(6) NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS account_session_id_seq CASCADE;

CREATE SEQUENCE account_session_id_seq START 1;

DROP TABLE IF EXISTS account_session CASCADE;

CREATE TABLE account_session(
    id BIGINT DEFAULT nextval('account_session_id_seq') PRIMARY KEY,
    created_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    edited_at timestamp with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER NOT NULL REFERENCES account_main(id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS organisation_id_seq CASCADE;

CREATE SEQUENCE organisation_id_seq START 1;

DROP TABLE IF EXISTS organisation CASCADE;

CREATE TABLE organisation(
    id SMALLINT PRIMARY KEY DEFAULT nextval('organisation_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER REFERENCES account_main(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    login VARCHAR(50) CONSTRAINT unique_place_login UNIQUE,
    photo_link VARCHAR (500),
    description VARCHAR (2000)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS parents_id_seq CASCADE;

CREATE SEQUENCE parents_id_seq START 1;

DROP TABLE IF EXISTS parents CASCADE;

CREATE TABLE parents(
    id SMALLINT PRIMARY KEY DEFAULT nextval('parents_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    account_main_id INTEGER REFERENCES account_main(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS children_id_seq CASCADE;

CREATE SEQUENCE children_id_seq START 1;

DROP TABLE IF EXISTS children CASCADE;

CREATE TABLE children(
    id SMALLINT PRIMARY KEY DEFAULT nextval('children_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    parents_id INTEGER REFERENCES parents(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    surname VARCHAR(150) NOT NULL,
    date_born DATE NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS events_id_seq CASCADE;

CREATE SEQUENCE events_id_seq START 1;

DROP TABLE IF EXISTS events CASCADE;

CREATE TABLE events(
    id SMALLINT PRIMARY KEY DEFAULT nextval('events_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    type VARCHAR(200) NOT NULL,
    name VARCHAR(200) NOT NULL,
    date_event DATE NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS event_hours_id_seq CASCADE;

CREATE SEQUENCE event_hours_id_seq START 1;

DROP TABLE IF EXISTS event_hours CASCADE;

CREATE TABLE event_hours(
    id SMALLINT PRIMARY KEY DEFAULT nextval('event_hours_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    hours INTEGER NOT NULL
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS achievements_id_seq CASCADE;

CREATE SEQUENCE achievements_id_seq START 1;

DROP TABLE IF EXISTS achievements CASCADE;

CREATE TABLE achievements(
    id SMALLINT PRIMARY KEY DEFAULT nextval('achievements_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    point INTEGER NOT NULL,
    nomination VARCHAR(150)
);

-- -----------------------------------------------------------------------------

DROP SEQUENCE IF EXISTS events_child_id_seq CASCADE;

CREATE SEQUENCE events_child_id_seq START 1;

DROP TABLE IF EXISTS events_child CASCADE;

CREATE TABLE events_child(
    id SMALLINT PRIMARY KEY DEFAULT nextval('events_child_id_seq'),
    created_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    edited_at TIMESTAMP with time zone NOT NULL DEFAULT current_timestamp,
    children_id INTEGER REFERENCES children(id) ON DELETE CASCADE,
    events_id INTEGER REFERENCES events(id) ON DELETE CASCADE
);
