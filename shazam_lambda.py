
import tweepy
import json
import logging
from cm_config import  config
from cm_api import *
from helper_funct import *
from twitter_bot import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def tweet(event, context):
    #################################################

    rt = config['refresh_token']
    api_token = get_api_token(rt)
    ################################################

    #generate today's date to make api call with

    date = generate_today_date()

    #collects title, artist, velocity, and artist id for most viral shazam track
    title, artist, velocity, artist_id = get_shazam_most_viral_track(api_token,date, country_code='US')
    hashartist = artist.replace(" ", "",)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)
    
    message = "'{}' by #{} is catching alot of people's attention this past week on #shazam\nSo much so that its average change in rank over 7-days is {}\n#dataanalysis #velocity #viral Powered by @Chartmetric\n{}".format(title, hashartist, round(velocity, 2), spot_url)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    bot.update_status(message)



    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    bot.update_status(message)


    
   

    body = {
        "message": message,
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    logger.info(message)

    return response