import tweepy
import schedule
from datetime import date
from twitter_bot_auth import *
from nbaPredict import makeInterpretPredictions
import math
import time

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET);
api = tweepy.API(auth)
manualTweetFlag = False

def today_prediction():
    # message = api_call
    global manualTweetFlag
    if not (manualTweetFlag):
        today = date.today()
        d1 = today.strftime("%m/%d/%Y")
        prediction_list = makeInterpretPredictions(d1, '2020-21', '12/22/2020')
        tweet_count = math.ceil(len(prediction_list) / 4)

        for i in range(tweet_count):
            header = 'Predictions for ' + d1 + ': ('+ str(i+1) + '/' + str(tweet_count) + ')\n'
            for j in range(i * 4, (i+1) * 4):
                if(j < len(prediction_list)):
                    header += prediction_list[j]
            #api.update_status(header)
            print(header)
    else:
        manualTweetFlag = False

def manual_tweet():
    global manualTweetFlag
    manualTweetFlag = True

schedule.every().day.at("08:00").do(today_prediction)
today_prediction()
# while True:
#     schedule.run_pending()
#     time.sleep(600)

