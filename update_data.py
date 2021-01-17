import requests
import os
from datetime import date

from nbaPredict import makeInterpretPredictions
from backend.generate_summaries import create_summary
from backend.add_predictions import insert_prediction, get_prediction_index


nba_scoreboard = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20210115'
score_elem_exclude = "STATUS_POSTPONED"

def update_all():
    """
    This is the main function that adds rows into the backend database for predictions and summaries.
    """
    game_id_list = scrape_game_nums()
    os.chdir(os.path.join(os.getcwd(), "backend"))
    prediction_id_list = update_predictions()
    update_summaries(game_id_list)
    os.chdir('../')

def update_predictions():
    """
    This function generates the prediction for each game in the given day.
    Returns:
        row_indices (list): list of rowids used by database to access prediction strings
    """
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")
    #prediction_list = makeInterpretPredictions(d1, '2020-21', '12/22/2020')
    prediction_list = ['aqecr', 'bcqrv', 'cqcqr', 'dcqrv']
    curr_row = get_prediction_index()
    row_indices = []
    for prediction in prediction_list:
        insert_prediction(prediction)
        row_indices.append(curr_row)
        curr_row += 1
    return row_indices

def update_summaries(game_id_list):
    """
    This function creates a summary for each game in the given day.
    Args:
        game_id_list (list): list of game ids used by ESPN to access box score tables
    """
    for game_id in game_id_list:
        create_summary(game_id)

def scrape_game_nums():
    """
    This function gets the game ids for the current day using the ESPN api endpoint
    Returns:
        game_id_list (list): list of game ids used by ESPN to access box score tables
    """
    game_id_list = []
    page = requests.get(nba_scoreboard)
    games = page.json()["events"]
    for game in games:
        if game["status"]["type"]["name"] == score_elem_exclude:
            continue
        game_id_list.append(game["id"])
    return game_id_list

update_all()