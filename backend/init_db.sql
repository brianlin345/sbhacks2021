/* clears the database */
/* sqlite3 nbatweets.db */
/* .read init_db.sql */
DROP TABLE IF EXISTS game_summaries;
CREATE TABLE IF NOT EXISTS game_summaries (
  game_num INTEGER,
  game_summary TEXT
);

DROP TABLE IF EXISTS game_predictions;
CREATE TABLE IF NOT EXISTS game_predictions (
  game_num TEXT,
  game_prediction TEXT
);
