#this bot collects data on the top 100 trending tracks of the
#week on Tiktok and outputs the track with the high velocity 
#(most viral track)

from cm_config import  config
from cm_api import *
from helper_funct import *
from helper_funct1 import *
from twitter_bot import *


#################################################

rt = config['refresh_token']
api_token = get_api_token(rt)
################################################

#generate today's date to make api call with
date = generate_today_date()

#collects data from today's top 100 tracks on tiktok for the week
data = get_tiktok_chart_data(api_token, 'tracks', date, 'weekly')

title, artist, velocity, cm_id = parse_viral(data)
hashartist = artist.replace(" ", "",)

#get chartmetric artist id
artist_id = get_track_metadata(api_token, cm_id)['artists'][0]['id']

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

bot.update_status("'{}' by #{} has a velocity metric of {},\nmaking it the most viral song this week on #tiktok #dataanalytics Powered by @Chartmetric\n{}".format(title, hashartist, round(velocity, 2), spot_url))