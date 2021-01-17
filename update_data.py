import requests
import os

from nbaPredict import makeInterpretPredictions
from backend.generate_summaries import create_summary
from backend.add_predictions import insert_prediction


nba_scoreboard = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20210115'
score_elem_exclude = "STATUS_POSTPONED"

def update_all():
    """
    This is the main function that adds rows into the backend database for predictions and summaries
    """
    game_id_list = scrape_game_nums()
    print(game_id_list)
    os.chdir(os.path.join(os.getcwd(), "backend"))
    #update_predictions()
    update_summaries(game_id_list)
    os.chdir('../')

def update_predictions():
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")
    prediction_list = makeInterpretPredictions(d1, '2020-21', '12/22/2020')

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
