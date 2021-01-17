import sys
import os
from datetime import date, timedelta

from twitter_bot import today_prediction, yesterday_summary
from update_data import update_all, scrape_game_nums, update_summaries

def tweet_all():
    """
    This function updates and tweets both summaries and predictions
    """
    today = date.today() - timedelta(days = 1)
    d1 = today.strftime("%Y%m%d")
    game_id_list, prediction_id_list = update_all(d1)
    yesterday_summary(game_id_list)
    today_prediction(prediction_id_list)

def tweet_update_summaries():
    """
    This function updates and tweets summaries.
    """
    today = date.today() - timedelta(days = 1)
    d1 = today.strftime("%Y%m%d")
    game_id_list = scrape_game_nums(d1)
    print(game_id_list)
    os.chdir(os.path.join(os.getcwd(), "backend"))
    update_summaries(game_id_list)
    os.chdir('../')
    yesterday_summary(game_id_list)

def tweet():
    """
    This is the main function that updates and tweets information
    """
    if len(sys.argv) == 2:
        if sys.argv[1] == "tus":
            print("Updating and tweeting summaries")
            tweet_update_summaries()
    else:
        tweet_all()

tweet()
