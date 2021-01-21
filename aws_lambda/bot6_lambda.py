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


    #get artist id for each artist
    id_bucket = []
    for track_id in df['cm_id']:
        artist_id = get_track_metadata(api_token, track_id)['artists'][0]['id']
        id_bucket.append(artist_id)

    # #create artist ID feature to dataframe
    df['cm_artist_id'] = id_bucket

    #total wikipedia views for each artist and add to dataframe as new feature
    wiki_bucket = []
    for artist in df['cm_artist_id']:
        views = get_fan_metrics(api_token, artist, 'wikipedia', one_month_ago, current_date, field='views')['views']
        total_views = count_wiki_views(views)
        wiki_bucket.append(total_views)
    complete_data = df.join(pd.DataFrame(wiki_bucket, columns=['wiki views']))
    #sort dataframe by wiki views, desceninding order, reset index
    reset = complete_data.sort_values('wiki views', ascending=False).reset_index()

    #get title, artist, artist id, and wiki views for top artist
    title, artist, artist_id, wiki_views = get_topwiki_artist(reset)

    wiki_views = insert_thousands_commas(wiki_views)
    
    hashartist = artist.replace(" ", "",)

    #get spotify url for artist
    spot_url = get_spotify_url(api_token, artist_id)

    #get artist twitter handle
    handle = generate_twitter_handle(api_token, artist_id)

    #instantiatiate twitter bot object
    bot = instantiate_twitter_bot()

    if handle:
        #create message
        message = "Out of all the artists having tracks on TikTok's Top 100 weekly chart,\n{} had the most views on #wikipedia\nTotal Views: {} since {}\n#DataAnalytics #MusicDiscovery\nPowered by @Chartmetric\n{}".format(handle, wiki_views, one_month_ago, spot_url)

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
    else:
        #create message
        message = "Out of all the artists having tracks on TikTok's Top 100 weekly chart,\n{} had the most views on #wikipedia\nTotal Views: {} since {}\n#DataAnalytics #MusicDiscovery\nPowered by @Chartmetric\n{}".format(artist, wiki_views, one_month_ago, spot_url)

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