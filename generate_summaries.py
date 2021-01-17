import sqlite3
import pandas as pd

from ESPN_scraper import scrape_game

DATABASE = 'nbatweets.db'

TEAM_AVGS = [101.5455556, 17.62888889, 12.73555556, 22.56777778, 77.40666667, 49.98, 52.46, 56.00222222, 107.3333333, 107.3966667]


def game_score(team_stat_df):
    scores = team_stat_df.loc[:,["PTS", "Team"]].values.tolist()
    score_string = ""
    score_string += scores[0][1] + " " + scores[0][0] + " : "
    score_string += scores[1][1] + " " + scores[1][0]
    return score_string

def individual_highlight(box_score_df):
    individual_highlight_string = ""
    individual_highlight_string_start = "The high impact player was "
    highlight_player = get_highest_pts(box_score_df)
    double_digit_sum = -1
    double_digit_type = 0
    for index, row in df.iterrrows():
        curr_double_digit, curr_double_type = is_double_digit(row)
        if double_type > double_digit_type:
            double_digit_sum = curr_double_digit
            highlight_player = get_player_stats(row)
        elif curr_double_digit > double_digit_sum:
            double_digit_sum = curr_double_digit
            highlight_player = get_player_stats(row)

    individual_highlight_string += individual_highlight_string_start
    key_index = 0
    for player_attribute in highlight_player:
        if key_index == 0:
            individual_highlight_string += highlight_player[player_attribute]
            individual_highlight_string += " with "
        key_index += 1
    if double_digit_type > 0:

    #return individual_highlight_string


def get_highest_pts(box_score_df):
    box_score_df['PTS'] = pd.to_numeric(box_score_df['PTS'])
    highest_pts = box_score_df.loc[box_score_df['PTS'].idxmax()]
    return get_player_stats(highest_pts)

def get_player_stats(box_score_row):
    name = box_score_row['Starters']
    points = box_score_row['PTS']
    rebounds = box_score_row['REB']
    assists = box_score_row['AST']
    return {"name": name, "points": points, "rebounds": rebounds, "assists": assists}

def is_double_digit(box_score_row):
    points = box_score_row['PTS']
    rebounds = box_score_row['REB']
    assists = box_score_row['AST']
    if points >= 10 and rebounds >= 10 and assists >= 10:
        return points + rebounds + assists, 2
    if points >= 10 and rebounds >= 10:
        return points + rebounds, 1
    elif points >= 10 and assists >= 10:
        return points + assists, 1
    elif rebounds >= 10 and assists >= 10:
        return rebounds + assists, 1
    return 0, 0


def team_highlight(team_stat_df):
    return 0


def generate_summary(game_id):
    box_score_df, team_stat_df = scrape_game(game_id)
    game_score_string = game_score(team_stat_df)
    individual_highlight(box_score_df)
    summary = game_score_string
    return summary


generate_summary(401267342)
