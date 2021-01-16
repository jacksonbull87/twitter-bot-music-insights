#This bot collects data on the top trending tracks
#on Tiktok from the previous 4 weeks. For each unique artists,
#the bot will collect daily listener counts for the current day
#and the date 7-days earlier. Based on the difference between
#those two value, the bot will output metadata for the
#artist with the biggest gain in listeners

import tweepy
from cm_config import  config
from cm_api import *
from helper_funct import *
from helper_funct1 import *
from twitter_bot import *
import random
import decimal

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

#drop duplicate artists except for first occurence
df.drop_duplicates(subset=['artist'], keep='last', inplace=True)

#get artist id for each artist
id_bucket = []
for artist in df['artist']:
    artist_id = get_artist_id(api_token, artist, 'artists')
    id_bucket.append(artist_id)

    
# #create artist ID feature to dataframe
df['cm_artist_id'] = id_bucket


#drop rows with no ID
df2 = df.dropna(subset=['cm_artist_id'])
df2.reset_index(inplace=True)
df2 = df2[~df2['cm_artist_id'].isin( ['None'])].reset_index()

# # # #collect before and after listener values for each artist
listener_bucket = []
for artist in df2['cm_artist_id']:
    listeners = get_fan_metrics(api_token, artist, 'spotify', one_month_ago, current_date, field='listeners')['listeners']
    if len(listeners) > 0:
        follow_tuple = (listeners[0]['value'], listeners[-1]['value'])
        listener_bucket.append(follow_tuple)

    else:
        follow_tuple = (None, None)
        listener_bucket.append(follow_tuple)

complete_data = df2.join(pd.DataFrame(listener_bucket, columns=['before', 'after']))
complete_data['listener_diff'] = complete_data['after'] - complete_data['before']

#drop unnecessary index columns
complete_data.drop(axis=1, columns=['level_0', 'index'], inplace=True)
#find track with biggest gain in spotify listeners and return title, artist, artist id, listeners one month ago, 
#and listener difference
title, artist, artist_id, before, listener_diff = get_most_listener_gain(complete_data)
hashartist = artist.replace(" ", "",)
hashtitle = title.replace(" ", "",)

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#create message
message = "Out of all the artists having tracks on TikTok's Top 100 weekly chart,\n{} had the biggest monthly gain in Spotify listeners\nUp {}% since {}\n#{} #{} #DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(artist, round(listener_diff/before *100, 2), one_month_ago, hashtitle, hashartist,spot_url)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

bot.update_status(message)
