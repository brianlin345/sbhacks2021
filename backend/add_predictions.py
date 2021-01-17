import sqlite3

DATABASE = 'nbatweets.db'

def insert_prediction(game_id, prediction_string):
    """
    This function inserts a summary into the database.
    Args:
        game_index (int): index for the given game summary in database
        prediction (string): summary of a game including final score, individual performance, and team performance.
    """
    summary_query = (game_id, prediction_string)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO game_predictions VALUES (?, ?)', summary_query)
    conn.commit()
    conn.close()

def get_index():
    
