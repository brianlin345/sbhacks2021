from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
#app.config["DEBUG"] = True

DATABASE = 'nbatweets.db'

@app.route('/summary', methods = ['GET'])
def get_summary():
    index = (request.args.get('gameId'),)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM game_summaries WHERE game_num=?', index)
    summary_raw = c.fetchone()
    conn.close()
    summary = {"index": summary_raw[0], "summary": summary_raw[1]}
    return jsonify(summary)

@app.route('/prediction', methods = ['GET'])
def get_predictions():
    index = request.args.get('gameId')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT rowid, * FROM game_predictions WHERE rowid=?', (index, ))
    prediction_raw = c.fetchone()
    conn.close()
    prediction = {"index": prediction_raw[0], "prediction": prediction_raw[1]}
    return jsonify(prediction)
