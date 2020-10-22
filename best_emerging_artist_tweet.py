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

current_date = generate_today_date()

before_date = generate_one_week_prior_date()

#collect top200 chart data for current date
data = get_spotify_charts(api_token, current_date, 'US', 'regional', 'weekly')

#parse data and get title, artist, artists ids, and current spotify popularity 
parsed_data = parse_top200_popularity(data)

df2 = add_popularity_before_after(before_date, current_date, parsed_data)

title, artist,artist_id, before_pop, after_pop, pop_change = get_most_successful_artist(df2)
hashartist = artist.replace(" ", "",)

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

bot.update_status("This week the artist known as {} earned the biggest increase in @spotify popularity with their song {}\nTheir popularity increased by {}% in just 7 days\n#dataanalysis #music powered by @Chartmetric\n{}".format(hashartist, title, round(pop_change/before_pop *100, 2), spot_url))

