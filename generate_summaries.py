import sqlite3
import pandas as pd

from ESPN_scraper import scrape_game

DATABASE = 'nbatweets.db'


def game_score(team_stat_df):
    scores = team_stat_df.loc[:,["PTS", "Team"]].values.tolist()
    score_string = ""
    if int(scores[0][0]) > int(scores[1][0]):
        score_string += scores[0][1] + " " + scores[0][0] + " : "
        score_string += scores[1][1] + " " + scores[1][0]
    else:
        score_string += scores[1][1] + " " + scores[1][0] + " : "
        score_string += scores[0][1] + " " + scores[0][0]
    return score_string

def individual_highlight():
    return 0

def team_highlight():
    return 0

def generate_summary(game_id):
    box_score_df, team_stat_df = scrape_game(game_id)
    print(game_score(team_stat_df))


generate_summary(401267342)
