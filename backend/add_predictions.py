import sqlite3
import os

DATABASE = 'nbatweets.db'

def insert_prediction(prediction_string):
    """
    This function inserts a summary into the database.
    Args:
        prediction_string (string): prediction of game result with percent chance.
    """
    prediction_query = (prediction_string,)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO game_predictions VALUES (?)', prediction_query)
    conn.commit()
    conn.close()

def get_prediction_index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT MAX(rowid) FROM game_predictions')
    max_row = c.fetchone()[0]
    conn.close()
    if max_row is None:
        return 1
    else:
        return max_row + 1
