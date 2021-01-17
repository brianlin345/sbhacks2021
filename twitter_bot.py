import tweepy
import schedule
from datetime import date, timedelta
from twitter_bot_auth import *
from nbaPredict import makeInterpretPredictions
import math
import time
import requests

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET);
api = tweepy.API(auth)
manualTweetFlag = False

API_root = 'http://127.0.0.1:5000/'

def today_prediction(prediction_id_list):
    """
    This function tweets the predictions for today's games before they occur.
    """
    # message = api_call
    global manualTweetFlag
    if not (manualTweetFlag):
        prediction_url = API_root + "prediction"
        prediction_list = []
        for prediction_id in prediction_id_list:
            predict_params = {"gameId": prediction_id}
            response = requests.get(prediction_url, params = predict_params)
            response_data = response.json()
            prediction_list.append(response_data["prediction"])
        tweet_count = math.ceil(len(prediction_list) / 4)
        today = date.today()
        d1 = today.strftime("%m/%d/%Y")

        for i in range(tweet_count):
            header = 'Predictions for ' + d1 + ': ('+ str(i+1) + '/' + str(tweet_count) + ')\n\n'
            for j in range(i * 4, (i+1) * 4):
                if(j < len(prediction_list)):
                    header += prediction_list[j]
            api.update_status(header)
            print(header)
    else:
        manualTweetFlag = False

def yesterday_summary(game_id_list):
    """
    This function tweets the summaries of yesterday's games after they finish.
    """
    # message = api_call
    global manualTweetFlag
    if not (manualTweetFlag):
        summary_url = API_root + "summary"
        summary_list = []
        for game_id in game_id_list:
            summary_params = {"gameId": game_id}
            response = requests.get(summary_url, params = summary_params)
            response_data = response.json()
            summary_list.append(response_data["summary"])

        today = date.today() - timedelta(days = 1)
        d1 = today.strftime("%m/%d/%Y")

        summary_index = 1
        num_summaries = len(summary_list)
        for summary in summary_list:
            header = 'Summaries for ' + d1 + ': ('+ str(summary_index) + '/' + str(num_summaries) + ')\n\n'
            content = header + summary
            #api.update_status(content)
            print(content)
            summary_index += 1

    else:
        manualTweetFlag = False

def manual_tweet():
    global manualTweetFlag
    manualTweetFlag = True

schedule.every().day.at("08:00").do(today_prediction)

# while True:
#     schedule.run_pending()
#     time.sleep(600)
