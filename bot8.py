#This bot collects data on top 100 trending tracks on Tiktok
#for the current week. Then it finds the artist with the 
#largest total playlist reach on Spotify

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

current_date = generate_yesterday_date()

before_date = generate_one_week_prior_date()

data = get_tiktok_chart_data(api_token, 'tracks', current_date, 'weekly', limit=100)

#parse data into dataframe (columns=['rank', 'added_at', 'title', 'artist', 'isrc', 'velocity', 'cm_id', 'time_on_chart', 'release_dates'])
parsed_data = parse_tiktok_data(data)

#get artist id for each artist
id_bucket = []
for track_id in parsed_data['cm_id']:
    artist_id = get_track_metadata(api_token, track_id)['artists'][0]['id']
    id_bucket.append(artist_id)
    
# #create artist ID feature to dataframe
parsed_data['cm_artist_id'] = id_bucket

parsed_data = parsed_data.dropna(subset=['artist'])

reach_list = []
for row in parsed_data.iterrows():
    track_id = row[1]['cm_id']
    reach = get_playlist_reach(api_token, before_date,current_date, track_id, 'spotify', status='current')
    reach_list.append(reach)
    
# create new feature for total playlist reach by map reach track id's
parsed_data['total playlist reach'] = reach_list

#sort dataset by total playlist reach
complete_data = parsed_data.sort_values('total playlist reach', ascending=False).reset_index(drop='index')

#assign values of the top playlist reach to variables
title = complete_data['title'][0].replace(" ", "",)
artist = complete_data['artist'][0].replace(" ", "",)
reach = insert_thousands_commas(complete_data['total playlist reach'][0])
artist_id = complete_data['cm_artist_id'][0]
#get artist twitter handle
handle = generate_twitter_handle(api_token, artist_id)

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

if twitter_handle:
    message = "Out of all the top trending tracks on TikTok this past week,\nthe song #{} by {}\nhad the largest playlist reach on Spotify\nreaching {} potential followers\n#DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(title,handle,reach, spot_url)

    bot.update_status(message)
else:
    message = "Out of all the top trending tracks on TikTok this past week,\nthe song #{} by {}\nhad the largest playlist reach on Spotify\nreaching {} potential followers\n#DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(title,artist,reach, spot_url)
    bot.update_status(message)