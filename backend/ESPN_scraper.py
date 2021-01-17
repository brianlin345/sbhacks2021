# this file creates finished data for the database that the bot will request from
import requests
from bs4 import BeautifulSoup
import pandas as pd

nba_root = "https://www.espn.com/nba/boxscore"
#game_id = 401267342

def scrape_game(game_id):
    nba_root = "https://www.espn.com/nba/boxscore"
    box_score_params = {"gameId": str(game_id)}

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
