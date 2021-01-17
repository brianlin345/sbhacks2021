import requests


#from nbaPredict import makeInterpretPredictions
from backend.generate_summaries import create_summary
from backend.add_predictions import insert_prediction


#nba_scoreboard = 'https://www.espn.com/nba/scoreboard/_/date/20210115'
nba_scoreboard = 'http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20210115'
score_elem_exclude = "STATUS_POSTPONED"

def update_all():
    game_id_list = scrape_game_nums()
    #update_predictions()
    update_summaries(game_id_list)

def update_predictions():
    today = date.today()
    d1 = today.strftime("%m/%d/%Y")
    prediction_list = makeInterpretPredictions(d1, '2020-21', '12/22/2020')


def update_summaries(game_id_list):
    game_id_list = scrape_game_nums()
    for game_id in game_id_list:
        create_summary(game_id)

def scrape_game_nums():
    game_id_list = []
    page = requests.get(nba_scoreboard)
    games = page.json()["events"]
    for game in games:
        if game["status"]["type"]["name"] == score_elem_exclude:
            continue
        game_id_list.append(game["id"])
    return game_id_list
    for game_id in game_id_list:
        create_summary(game_id)
