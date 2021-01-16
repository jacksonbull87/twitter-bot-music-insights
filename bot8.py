
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

current_date = generate_today_date()

before_date = generate_one_week_prior_date()

data = get_tiktok_chart_data(api_token, 'tracks', '2021-01-15', 'weekly', limit=100)

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

reach_list = []
for row in parsed_data2.iterrows():
    track_tup = ()
    track_id = row[1]['cm_id']
    reach = get_playlist_reach(api_token, before_date,current_date, track_id, 'spotify', status='current')
    track_tup = (track_id, reach)
    reach_list.append(track_tup)
    
#create a dictionary from a list of tuples
di = {}
total_reach = Convert(reach_list, di)

# create new feature for total playlist reach by map reach track id's
parsed_data2['total playlist reach'] = parsed_data2['cm_id'].map(total_reach)


complete_data = parsed_data2.join(pd.DataFrame(listener_bucket, columns=['before', 'after']))
complete_data['listener_diff'] = complete_data['after'] - complete_data['before']

complete_data.drop(axis=1, columns=['level_0', 'index'], inplace=True)

#sort dataset by total playlist reach
complete_data = complete_data.sort_values('total playlist reach', ascending=False).reset_index(drop='index')

#assign values of the top playlist reach to variables
title = complete_data['title'][0].replace(" ", "",)
artist = complete_data['artist'][0].replace(" ", "",)
reach = insert_thousands_commas(complete_data['total playlist reach'][0])
artist_id = complete_data['cm_artist_id'][0]

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()
message = "Out of all the top trending tracks on TikTok this past week,\nthe song #{} by #{}\nhad the largest playlist reach on Spotify\nreaching {} potential followers\n#DataAnalytics #MusicDiscovery\nPower by @Chartmetric\n{}".format(title,artist,reach, spot_url)

bot.update_status(message)