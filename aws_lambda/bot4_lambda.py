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
    #generate api token for chartmetric api access
    rt = config['refresh_token']
    api_token = get_api_token(rt)
    ################################################

    #generates the date one year prior to make api call
    date = generate_date_one_year_ago()

    #extracks data for SPotify Top 200 chart for date generated above
    data = get_spotify_charts(api_token, date, 'US', 'regional', 'daily')

    #parses data and save title and artist as two variables
    title, artist = parse_data(data)
    hashartist = artist.replace(" ", "",)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    message = "One Year Ago on {}: \nThe #1 song was '{}' by #{}\n@spotify #top200 #throwbackthursday Powered by @Chartmetric".format(date, title, hashartist)

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