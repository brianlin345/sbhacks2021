import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

#from ESPN_scraper import scrape_game

DATABASE = 'nbatweets.db'

summary_table = 'game_summaries'

TEAM_AVGS = [101.5455556, 17.62888889, 12.73555556, 22.56777778, 77.40666667, 49.98, 52.46, 56.00222222, 107.3333333, 107.3966667]


def game_score(team_stat_df):
    """
    This function returns the overall scoreline of a game.
    Args:
        team_stat_df (DataFrame): two-row dataframe containing overall team statistics for a game.
    Returns:
        score_string (string): formatted string of the game final score and teams.
    """
    scores = team_stat_df.loc[:,["PTS", "Team"]].values.tolist()
    score_string = ""
    score_string += scores[0][1] + " " + scores[0][0] + " : "
    score_string += scores[1][1] + " " + scores[1][0] + ". "
    return score_string

def individual_highlight(box_score_df):
    """
    This function generates a highlight denoting a player who had a good individual performance.
    It first returns the highest-scoring player, then checks for players who had a double-double or triple-double.
    In the case of these performances, the player with the highest sum across pts, rebounds, assists is selected.
    Args:
        box_score_df (Dataframe): dataframe containing cleaned box score table.
    Returns:
        individual_highlight_string (string): preset sentence describing a notable individual performance.
    """
    individual_highlight_string = ""
    individual_highlight_string_start = "The high impact player was "
    highlight_player = get_highest_pts(box_score_df)
    double_digit_sum = -1
    double_digit_type = 0
    for index, row in box_score_df.iterrows():
        curr_double_digit, curr_double_type = is_double_digit(row)
        if curr_double_type > double_digit_type:
            double_digit_sum = curr_double_digit
            double_digit_type = curr_double_type
            highlight_player = get_player_stats(row)
        elif curr_double_digit > double_digit_sum:
            double_digit_sum = curr_double_digit
            highlight_player = get_player_stats(row)

    individual_highlight_string += individual_highlight_string_start
    key_index = 0
    num_attributes = len(highlight_player)
    for player_attribute in highlight_player:
        if key_index == 0:
            individual_highlight_string += highlight_player[player_attribute]
            if double_digit_type > 0:
                if double_digit_type == 1:
                    individual_highlight_string += ", who recorded a double-double"
                elif double_digit_type == 2:
                    individual_highlight_string += ", who recorded a triple-double"
            individual_highlight_string += " with "
        else:
            if key_index == num_attributes - 1:
                individual_highlight_string += "and "
            individual_highlight_string += highlight_player[player_attribute] + " " + player_attribute
            if key_index < num_attributes - 1:
                individual_highlight_string += ", "
        key_index += 1

    individual_highlight_string += ". "

    return individual_highlight_string


def get_highest_pts(box_score_df):
    """
    This function returns the statistics of the player with the highest scored points in a game.
    Creates a new column for the score as integers and calls get_player_stats for formatted result.
    Args:
        box_score_df (Dataframe): dataframe containing cleaned box score table
    """
    box_score_df['PTS_int'] = pd.to_numeric(box_score_df['PTS'])
    highest_pts = box_score_df.loc[box_score_df['PTS_int'].idxmax()]
    return get_player_stats(highest_pts)

def get_player_stats(box_score_row):
    """
    This function returns the statistics for a given player as a formatted dictionary.
    Args:
        box_score_row (Dataframe): DataFrame row from the box score DataFrame representing a single player.
    Returns:
        dictionary: statistic name as key, name or statistic number as value.
    """
    name = box_score_row['Starters']
    points = box_score_row['PTS']
    rebounds = box_score_row['REB']
    assists = box_score_row['AST']
    return {"name": name, "points": points, "rebounds": rebounds, "assists": assists}

def is_double_digit(box_score_row):
    """
    This function checks if a player performance from the box score was a triple-double or double-double.
    Args:
        box_score_row (Dataframe): DataFrame row from the box score DataFrame representing a single player.
    Returns:
        pair: sum of relevant statistics, and type of double statistic (2 for triple-double, 1 for double-double, 0 for neither).
    """
    points = box_score_row['PTS_int']
    rebounds = int(box_score_row['REB'])
    assists = int(box_score_row['AST'])
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
    """
    This function generates a highlight denoting either team's best statistic compared to seasonal averages.
    Chosen statistics include: assist ratio (AST), offensive rebound ratio (OREB), defensive rebound ratio (DREB), and field goal percentage (FG).
    Args:
        team_stat_df (Dataframe): dataframe containing cleaned team statistics table.
    Returns:
        team_highlight_string (string): preset sentence describing most notable team performance.
    """
    avgStats = [17.6, 22.6, 77.4, 52.5]
    statsDict = {0: 'AST', 1: 'OREB', 2: 'DREB', 3: 'FG%'}

    team_highlight_string = ""

    homeTeamValues = team_stat_df.iloc[0][['AST', 'OREB', 'DREB', 'FG']].tolist()
    homeTeamValues[3] = homeTeamValues[3].split("-")
    homeTeamValues[3] = (float(homeTeamValues[3][0]) / float(homeTeamValues[3][1])) * 100

    awayTeamValues = team_stat_df.iloc[1][['AST', 'OREB', 'DREB', 'FG']].tolist()
    awayTeamValues[3] = awayTeamValues[3].split("-")
    awayTeamValues[3] = (float(awayTeamValues[3][0]) / float(awayTeamValues[3][1])) * 100

    for i in range(4):
        homeTeamValues[i] = round(float(homeTeamValues[i]) - avgStats[i], 1)
        awayTeamValues[i] = round(float(awayTeamValues[i]) - avgStats[i], 1)

    max_home_diff = max(homeTeamValues)
    max_away_diff = max(awayTeamValues)

    if max_home_diff >= max_away_diff:
        team_highlight_string = team_stat_df.iloc[0]['Team'] + " had the most notable " + statsDict[homeTeamValues.index(max_home_diff)] + " performance with value " + str(max_home_diff)
    else:
        team_highlight_string = team_stat_df.iloc[1]['Team'] + " had the most notable " + statsDict[awayTeamValues.index(max_away_diff)] + " performance with value " + str(max_away_diff)
    team_highlight_string += "."
    
    return team_highlight_string

def generate_summary(game_id):
    """
    This function returns a game summary given a game_id for the ESPN website.
    Args:
        game_id (int): number corresponding to a given game on ESPN website
    Returns:
        summary (str): summary of a game including final score, individual performance, and team performance.
    """
    box_score_df, team_stat_df = scrape_game(game_id)
    game_score_string = game_score(team_stat_df)
    individual_highlight_string = individual_highlight(box_score_df)
    team_highlight_string = team_highlight(team_stat_df)
    summary = game_score_string + individual_highlight_string + team_highlight_string
    return str(game_id), summary

def insert_summary(game_id, summary_string):
    """
    This function inserts a summary into the database.
    Args:
        table_name (string): name of table to insert into
        game_index (int): index for the given game summary in database
        summary_string (string): summary of a game including final score, individual performance, and team performance.
    """
    summary_query = (game_id, summary_string)
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO game_summaries VALUES (?, ?)', summary_query)
    conn.commit()
    conn.close()


def scrape_game(game_id):
    nba_root = "https://www.espn.com/nba/boxscore"
    box_score_params = {"gameId": game_id}

    page = requests.get(nba_root, params = box_score_params)
    soup = BeautifulSoup(page.content, 'html.parser')

    tables = soup.find_all("table", "mod-data", limit = 2)
    team_divs = soup.find_all("div", "team-name", limit = 2)
    teams = []
    for team in team_divs:
        teams.append(team.text)

    box_score_dict = {}
    box_score_cols = []
    team_stat_dict = {}
    row_index = 0
    team_row_index = 0
    dnp = False

    team_stat_exclude  = ["name", "min", "plusminus"]

    team_num = 0
    team_col = []

    team_stat_found = False

    for table in tables:
        if row_index == 0:
            header = table.find("thead")
            categories = header.find_all("th")
            for category in categories:
                box_score_cols.append(category.text)

        body = table.find_all("tbody", limit = 2)
        for body_table in body:
            rows = body_table.find_all("tr")
            for row in rows:
                curr_row = []
                data = row.find_all("td")
                if row.has_attr("class") and row["class"][0] == "highlight":
                    if team_stat_found:
                        continue

                    for val in data:
                        if val.has_attr("class") and val["class"][0] in team_stat_exclude:
                            curr_row.append('')
                        else:
                            curr_row.append(val.text)
                    team_stat_dict[team_row_index] = curr_row
                    team_row_index += 1
                    team_stat_found = True
                    continue

                for val in data:
                    if val.has_attr("class") and val["class"][0] == "dnp":
                        dnp = True
                        continue
                    if dnp:
                        break
                    if val.has_attr("class") and val["class"][0] == "name":
                        link_text = val.find("span").text
                        curr_row.append(link_text)
                    else:
                        curr_row.append(val.text)
                if not dnp:
                    box_score_dict[row_index] = curr_row
                    row_index += 1
                    team_col.append(teams[team_num])
                dnp = False
        team_num += 1
        team_stat_found = False

    box_score_df = pd.DataFrame.from_dict(box_score_dict, orient = 'index', columns = box_score_cols)
    team_stat_df = pd.DataFrame.from_dict(team_stat_dict, orient = 'index', columns = box_score_cols)
    box_score_df["Team"] = team_col
    team_stat_df["Team"] = teams

    return box_score_df, team_stat_df

def create_summary(game_id):
    id, summ = generate_summary(game_id)
    insert_summary(id, summ)
