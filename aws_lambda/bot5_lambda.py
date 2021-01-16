import json
import logging
from cm_config import config
from cm_api import *
from helper_funct import *
from helper_funct1 import *
from twitter_bot import *
import time
import random
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def tweet(event, context):
    # ################################################
    # generate api token for chartmetric api access
    rt = config['refresh_token']
    api_token = get_api_token(rt)
    ################################################

    current_date = generate_today_date()

    before_date = generate_one_week_prior_date()

    data = get_tiktok_chart_data(api_token, 'tracks', current_date, 'weekly', limit=100)
    #parse data into dataframe (columns='title', 'artist', 'isrc', 'velocity', 'cm_id')
    parsed_data = parse_tiktok_data(data)

    #get artist id for each artist
    id_bucket = []
    for artist in parsed_data['artist']:
        artist_id = get_artist_id(api_token, artist, 'artists')
        id_bucket.append(artist_id)
        time.sleep(1.5)
        
    # #create artist ID feature to dataframe
    parsed_data['cm_artist_id'] = id_bucket

    # #drop rows with no ID
    parsed_data2 = parsed_data.dropna(subset=['cm_artist_id'])
    parsed_data2.reset_index(inplace=True)
    parsed_data2 = parsed_data2[~parsed_data2['cm_artist_id'].isin( ['None'])].reset_index()
    # # #collect before and after listener values for each artist
    listener_bucket = []
    for artist in parsed_data2['cm_artist_id']:
        listeners = get_fan_metrics(api_token, artist, 'spotify', before_date, current_date, field='listeners')['listeners']
        if len(listeners) > 0:
            follow_tuple = (listeners[0]['value'], listeners[-1]['value'])
            listener_bucket.append(follow_tuple)
        else:
            follow_tuple = (None, None)
            listener_bucket.append(follow_tuple)

    complete_data = parsed_data2.join(pd.DataFrame(listener_bucket, columns=['before', 'after']))
    complete_data['listener_diff'] = complete_data['after'] - complete_data['before']

    complete_data.drop(axis=1, columns=['level_0', 'index'], inplace=True)

    title, artist, artist_id, before, listener_diff = get_most_listener_gain(complete_data)
    hashartist = artist.replace(" ", "",)
    hashtitle = title.replace(" ", "",)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)

    #get artist twitter handle
    handle = generate_twitter_handle(api_token, artist_id)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    if handle:
        
        message = "Out of all the artists trending on this week's top 100 Tiktok tracks,\n{} had the biggest gain in Spotify listeners\nUp {}% since last week\n#{} #{} #DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(handle, round(listener_diff/before *100, 2),hashtitle, hashartist,spot_url)

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
        message = "Out of all the artists trending on this week's top 100 Tiktok tracks,\n{} had the biggest gain in Spotify listeners\nUp {}% since last week\n#{} #{} #DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(artist, round(listener_diff/before *100, 2),hashtitle, hashartist,spot_url)

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