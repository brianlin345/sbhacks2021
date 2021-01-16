# getDailyMatchups.py - Finds the daily NBA games

from nba_api.stats.endpoints import leaguegamelog, scoreboard
from teamIds import teams
from customHeaders import customHeaders

# Function to get you the games on a specified date (Home vs. Away)
# Used for dates in the present or future
# Return value is a list where index 0 is a dict holding the games  {Home:Away}
# Enter a date in the format mm/dd/yyyy
def dailyMatchupsPresent(date):

    # Obtains all games that are set to occur on specified date
    dailyMatchups = scoreboard.Scoreboard(league_id='00', game_date=date, headers=customHeaders, timeout=120)
    dailyMatchupsDict = dailyMatchups.get_normalized_dict()
    listOfGames = dailyMatchupsDict['GameHeader']

    homeAwayDict = {}

    for game in listOfGames:  # Loops through each game on date

        homeTeamID = game['HOME_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the home team that corresponds with teamID
            if teamID == homeTeamID:
                homeTeamName = team

        awayTeamID = game['VISITOR_TEAM_ID']

        for team, teamID in teams.items():  # Finds name of the away team that corresponds with teamID
            if teamID == awayTeamID:
                awayTeamName = team

        homeAwayDict.update({homeTeamName:awayTeamName})

    return homeAwayDict
