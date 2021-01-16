import flask
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATABASE = 'nbatweets.db'

@app.route('/summary', methods = ['GET'])
def get_summary():

@app.route('/predictions', methods = ['GET'])
def get_predictions():
