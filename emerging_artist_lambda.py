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
    #generate api token for chartmetric api access
    rt = config['refresh_token']
    api_token = get_api_token(rt)
    ################################################

    current_date = generate_today_date()

    before_date = generate_one_week_prior_date()

    #collect top200 chart data for current date
    data = get_spotify_charts(api_token, current_date, 'US', 'regional', 'daily')

    #parse data and get title, artist, artists ids, and current spotify popularity 
    parsed_data = parse_top200_popularity(data)

    df2 = add_popularity_before_after(api_token, before_date, current_date, parsed_data)

    title, artist,artist_id, before_pop, after_pop, pop_change = get_most_successful_artist(df2)
    hashartist = artist.replace(" ", "",)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    message = "This week the artist known as #{} gained the biggest increase in @spotify popularity with their song '{}'\nTheir popularity increased by {}% in just 7 days\n#dataanalysis #musicdiscovery powered by @Chartmetric\n{}".format(hashartist, title, round(pop_change/before_pop *100, 2), spot_url)

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