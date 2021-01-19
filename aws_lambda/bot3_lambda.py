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

    current_date = generate_yesterday_date()
    one_month_ago = generate_one_month_ago()

    date_list = get_date_range(one_month_ago, current_date, 'W')

    #extract data for all top 100 tracks for dates given
    data_bucket = []
    for week in date_list:
        data = get_tiktok_chart_data(api_token, 'tracks', week, 'weekly', limit=100)
        for track in data:
            track_tuple = (track['name'], track['tiktok_artist_names'][0], track['isrc'], track['velocity'], track['cm_track'])
            data_bucket.append(track_tuple)
    df = pd.DataFrame(data_bucket, columns=['title', 'artist', 'isrc', 'velocity', 'cm_id'])
    #drop tracks with no isrc code
    df.dropna(subset=['isrc'], inplace=True)

    #drop duplicate artists except for first occurence
    df.drop_duplicates(subset=['artist'], keep='last', inplace=True)

    #get artist id for each artist
    id_bucket = []
    for track_id in df['cm_id']:
        artist_id = get_track_metadata(api_token, track_id)['artists'][0]['id']
        id_bucket.append(artist_id)

        
    # #create artist ID feature to dataframe
    df['cm_artist_id'] = id_bucket


    df.reset_index(inplace=True, drop='index')
    # # # #collect before and after listener values for each artist
    listener_bucket = []
    for artist in df['cm_artist_id']:
        listeners = get_fan_metrics(api_token, artist, 'spotify', one_month_ago, current_date, field='listeners')['listeners']
        if len(listeners) > 0:
            follow_tuple = (listeners[0]['value'], listeners[-1]['value'])
            listener_bucket.append(follow_tuple)

        else:
            follow_tuple = (None, None)
            listener_bucket.append(follow_tuple)

    complete_data = df.join(pd.DataFrame(listener_bucket, columns=['before', 'after']))
    complete_data['listener_diff'] = complete_data['after'] - complete_data['before']

    title, artist, artist_id, before, listener_diff = get_most_listener_gain(complete_data)
    hashartist = artist.replace(" ", "",)
    hashtitle = title.replace(" ", "",)
    num_listener_diff = insert_thousands_commas(listener_diff)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)

    #get artist twitter handle
    handle = generate_twitter_handle(api_token, artist_id)


    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()
    if handle:
            message = "Out of all the artists having tracks on TikTok's Top 100 weekly chart,\n{} had the biggest monthly gain in Spotify listeners\nUp {}% ({} more listeners) since {}\n#{} #{} #DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(handle, round(listener_diff/before *100, 2),num_listener_diff, one_month_ago, hashtitle, hashartist,spot_url)


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
            message = "Out of all the artists having tracks on TikTok's Top 100 weekly chart,\n#{} had the biggest monthly gain in Spotify listeners\nUp {}% ({} more listeners) since {}\n#{} #{} #DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(hashartist, round(listener_diff/before *100, 2),num_listener_diff, one_month_ago, hashtitle, hashartist,spot_url)
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