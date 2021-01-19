#this program gerates a post that contains the song with the highest velocity for the past 7-days on tiktok...most viral track
import json
import logging
from cm_config import  config
from cm_api import *
from helper_funct import *
from helper_funct1 import *
from twitter_bot import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def tweet(event, context):
    #################################################

    rt = config['refresh_token']
    api_token = get_api_token(rt)
    ################################################

    #generate today's date to make api call with
    date = generate_yesterday_date()

    #collects data from today's top 100 tracks on tiktok for the week
    data = get_tiktok_chart_data(api_token, 'tracks', date, 'weekly')

    title, artist, velocity, cm_id = parse_viral(data)
    hashartist = artist.replace(" ", "",)

    #get chartmetric artist id
    artist_id = get_track_metadata(api_token, cm_id)['artists'][0]['id']

    #get twitter handle
    handle = generate_twitter_handle(api_token, artist_id)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()


    if handle:
        # create message
        message = "'{}' by {} has a velocity metric of {},\nmaking it the most viral song this week on #tiktok #dataanalytics Powered by @Chartmetric\n{}".format(title, handle, round(velocity, 2), spot_url)


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
    else:
        # create message
        message = "'{}' by #{} has a velocity metric of {},\nmaking it the most viral song this week on #tiktok #dataanalytics Powered by @Chartmetric\n{}".format(title, hashartist, round(velocity, 2), spot_url)


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


