# BallerB0t
BallerB0t is a bot, coded in Python, that tweets predictions on today's NBA games as well as summaries on the results of yesterday's games. BallerB0t uses a Random Forest Classifier to make its predictions. It uses Flask and a SQL database. <br />
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
