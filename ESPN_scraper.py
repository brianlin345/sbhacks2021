# this file creates finished data for the database that the bot will request from
import requests
from bs4 import BeautifulSoup
import pandas as pd

game_id = 401267342
nba_root = "https://www.espn.com/nba/boxscore"
box_score_params = {"gameId": str(game_id)}

page = requests.get(nba_root, params = box_score_params)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup)

tables = soup.find_all("table", "mod-data", limit = 2)

box_score_dict = {}
box_score_cols = []
row_index = 0

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
            if row.has_attr("class") and row["class"][0] == "highlight":
                continue
            data = row.find_all("td")
            for val in data:
                if val.has_attr("class") and val["class"][0] == "dnp":
                    continue
                if val.has_attr("class") and val["class"][0] == "name":
                    link_text = val.find("span").text
                    curr_row.append(link_text)
                    continue
                curr_row.append(val.text)
            box_score_dict[row_index] = curr_row
            row_index += 1

box_score_df = pd.DataFrame.from_dict(box_score_dict, orient = 'index', columns = box_score_cols)
print(box_score_df)
