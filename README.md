# BallerB0t
BallerB0t is a bot, coded in Python, that tweets predictions on today's NBA games as well as summaries on the results of yesterday's games. BallerB0t uses a Random Forest Classifier to make its predictions. It uses Flask and a SQL database. <br />
Twitter Link: https://twitter.com/BallerB0t
<br />
## Main Dependencies
- nba-api
- tweepy
- pandas
- numpy
- scikit-learn
- Flask <br />
<p>Rest in requirements.txt, which can be ran with:</p>
<code> pip install -r requirements.txt </code> <br>

## Twitter Bot
- Uses tweepy API to generate certs for authentication.
- Uses a schedule API in order to queue jobs to run daily before the first game. 
- Pulls and tweets the predictions on the current day's games from the database.
- Pulls and tweets the summaries of the previous day's games.

## Random Forest Model
- Predictions are generated using a Random Forest Classifier with 75 estimators and a max-depth of 8. 
- Trained using statistics, per 100 posessions, across three seasons: 2016-2017, 2017-2018, and 2018-2019.
- Features: Home team, win percentage, rebounds, turnovers, plus-minus, offensive rating, defensive rating, true shooting percentage.
- Accuracy of 65%.

## Backend API/Database
- Box score tables are scraped from the NBA section of ESPN using requests and BeautifulSoup.
- Pandas is used to extract key statistics like triple-doubles and create formatted highlights in text format.
- Sqlite database stores finalized game summaries and predictions, indexed by game id provided by ESPN and generation id.
- Flask server returns information from the database with endpoints for game summaries and predictions.
- Twitter bot makes a GET request to the API with the specific game ids needed to receive the final text it will tweet.
