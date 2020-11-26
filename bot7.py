#This bot find the most viral song of the month on tiktok
#and top 5 cities by monthly spotify listeners for that artist


import tweepy
from cm_config import  config
from cm_api import *
from helper_funct import *
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
        track_tuple = (track['added_at'], track['name'], track['tiktok_artist_names'][0], track['isrc'], track['velocity'], track['cm_track'],
                      track['weekly_posts'])
        data_bucket.append(track_tuple)
df = pd.DataFrame(data_bucket, columns=['add date', 'title', 'artist', 'isrc', 'velocity', 'cm_id', 'number of posts'])
#drop tracks with no isrc code
df.dropna(subset=['isrc'], inplace=True)

df.sort_values('velocity', ascending=False, inplace=True)

# drop duplicate artists except for first occurence
df.drop_duplicates(subset=['artist'], keep='first', inplace=True)

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

#retreive title, artist, velocity
add_date, title, artist, velocity, cm_artist_id = most_viral_tiktoktrack(complete_data)
hashartist = artist.replace(" ", "",)
hashtitle = title.replace(" ", "",)

#get spotify url
spot_url = get_spotify_url(api_token, cm_artist_id)

#get top cities for artist
data_object = monthly_listen(api_token, cm_artist_id, add_date)

#save top five cities as variables
first, second, third, fourth, fifth = top_5_cities(data_object)

#create message
message = "Most Viral Tiktik Song of the Month: #{} by #{}\nVelocity = {} on {}\nTop 5 Cities by Spotify Monthly Listeners\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n{}".format(hashtitle,hashartist,round(velocity, 2),add_date,first,second, third, fourth, fifth,spot_url)

#instantiate twitter bot
bot = instantiate_twitter_bot()

#update status with message
bot.update_status(message)