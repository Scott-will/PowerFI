-- Database: PowerFI

-- DROP DATABASE IF EXISTS "PowerFI";

CREATE DATABASE "PowerFI"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_Canada.1252'
    LC_CTYPE = 'English_Canada.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    position VARCHAR(50),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    player_id INTEGER,
    team VARCHAR(50),
    picture INTEGER,
    picture_url VARCHAR(250)
);
CREATE INDEX idx_player_id ON players(player_id);

CREATE TABLE player_images (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL,
    image_data BYTEA,
    content_type VARCHAR(255),
    CONSTRAINT fk_player_id FOREIGN KEY (player_id)
    REFERENCES players(id)
    ON DELETE CASCADE
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR(50) NOT NULL,
    timestamp INTEGER,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    added_players VARCHAR(100) NOT NULL,
    removed_players VARCHAR(100) NOT NULL,
    team_key_added VARCHAR(25) NOT NULL,
    team_key_removed VARCHAR(25) NOT NULL
);
CREATE INDEX idx_transaction_id ON transactions(transaction_id);

CREATE TABLE fantasy_teams (
    id SERIAL PRIMARY KEY,
    team_id INTEGER NOT NULL,
    name VARCHAR(250) NOT NULL,
    manager_name VARCHAR(250) NOT NULL,
    team_key VARCHAR(25),
    picture INTEGER,
    picture_url VARCHAR(250)
);
CREATE INDEX idx_team_id ON fantasy_teams(team_id);
CREATE INDEX idx_team_key ON fantasy_teams(team_key);

CREATE TABLE fantasy_team_image (
    id SERIAL PRIMARY KEY,
    fantasy_team_id INT NOT NULL,
    image_data BYTEA,
    content_type VARCHAR(255),
    CONSTRAINT fk_fantasy_team_id FOREIGN KEY (fantasy_team_id)
    REFERENCES fantasy_teams(id)
    ON DELETE CASCADE
);

INSERT INTO public.fantasy_teams(
	team_id, name, manager_name, team_key)
	VALUES (1, 'Waiver', 'Waiver', 'Waiver');