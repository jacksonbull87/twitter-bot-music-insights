#This bot collects data on the top 100 trending tracks of 
#the week and finds the record with the highest velocity (most viral track)

import tweepy
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

#collects title, artist, velocity, and artist id for most viral shazam track
title, artist, velocity, artist_id = get_shazam_most_viral_track(api_token,date, country_code='US')
hashtitle = title.replace(" ", "",)
hashartist = artist.replace(" ", "",)

handle = generate_twitter_handle(api_token, artist_id)

#get spotify url for artist
spot_url = get_spotify_url(api_token, artist_id)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

if handle:
    message = "'#{}' by {} is catching alot of people's attention this past week on #shazam\nSo much so that its average change in rank over 7-days is {}\n#dataanalysis #velocity #viral Powered by @Chartmetric\n{}".format(hashtitle, handle, round(velocity, 2), spot_url)
else:
    message = "'#{}' by #{} is catching alot of people's attention this past week on #shazam\nSo much so that its average change in rank over 7-days is {}\n#dataanalysis #velocity #viral Powered by @Chartmetric\n{}".format(hashtitle, hashartist, round(velocity, 2), spot_url)

bot.update_status("'{}' by #{} is catching alot of people's attention this past week on #shazam\nSo much so that its average change in rank over 7-days is {}\n#dataanalysis #velocity #viral Powered by @Chartmetric\n{}".format(title, hashartist, round(velocity, 2), spot_url))