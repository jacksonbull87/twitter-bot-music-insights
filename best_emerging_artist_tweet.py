import tweepy
from cm_config import  config
from cm_api import *
from helper_funct import *
from twitter_bot import *

#################################################
#generate api token for chartmetric api access
rt = config['refresh_token']
api_token = get_api_token(rt)
################################################

current_date = generate_today_date

before_date = generate_one_week_prior_date()

data = get_tiktok_chart_data(api_token, 'tracks', current_date, 'weekly', limit=100)
#parse data into dataframe (columns='title', 'artist', 'isrc', 'velocity', 'cm_id')
parsed_data = parse_tiktok_data(data)
#get artist id for each artist
id_bucket = []
for artist in parsed_data['artist']:
    artist_id = get_artist_id(api_token, artist, 'artists')
    id_bucket.append(artist_id)
    time.sleep(4)
#create artist ID feature to dataframe
parsed_data['cm_artist_id'] = id_bucket
#drop rows with no ID
parsed_data.dropna(subset='cm_artist_id', inplace=True)
#collect before and after listener values for each artist
listener_bucket = []
for artist in parsed_data['cm_artist_id']:
    listeners = get_fan_metrics(api_token, artist, 'spotify', before_date, current_date, field='listeners')['listeners']
    if len(listeners) > 0:
        follow_tuple = (listeners[0]['value'], listeners[-1]['value'])
        listener_bucket.append(follow_tuple)
        time.sleep(4)
    else:
        follow_tuple = (None, None)
        listener_bucket.append(follow_tuple)
        time.sleep(1)

complete_data = parsed_data.join(pd.DataFrame(listener_bucket, columns=['before', 'after']))
complete_data['listener_diff'] = complete_data['after'] - complete_data['before']

title, artist, artist_id, before, listener_diff = get_most_listener_gain(complete_data)
hashartist = artist.replace(" ", "",)

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

bot.update_status("After trending on Tiktok this week, {artist} had the biggest gain in Spotify listeners\nUp {}% since last week\nPower by @Chartmetric\n{}".format(artist, round(listener_diff/before *100, 2), spot_url))

