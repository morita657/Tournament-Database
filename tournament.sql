-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- tournament table contains every playes' information. Each players have id, name, wins, matches.
-- The id should be unique id,
-- name is players' name,
-- wins is the number of the matches players won
-- matches is the number of matches players played
-- CREATE TABLE tournament (
--   id SERIAL,
--   name TEXT,-- In this case, name means players' full name
--   wins integer,--
--   matches integer--
-- );

CREATE TABLE players (
  player_id SERIAL PRIMARY KEY,
  name text,
  wins integer,
  matches integer
);


-- match table stores the result of each fights with winner and loser.
-- winner is player's id and name and loser as well.
CREATE TABLE match (
  match_id SERIAL PRIMARY KEY,
  winner_id integer REFERENCES players(player_id),
  loser_id integer REFERENCES players(player_id)
);

-- CREATE TABLE swiss_paring {
--   id1,
--   name1,
--   id2,
--   name2
-- }
