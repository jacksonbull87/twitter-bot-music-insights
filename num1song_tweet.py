#this python program gernates a post that contains the number 1 song on the the spotifh top 200 one year prior to today
#runs every thursday

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

#generates the date one year prior to make api call
date = generate_date_one_year_ago()

#extracks data for SPotify Top 200 chart for date generated above
data = get_spotify_charts(api_token, date, 'US', 'regional', 'daily')

#parses data and save title and artist as two variables
title, artist = parse_data(data)
hashartist = artist.replace(" ", "",)

#instantiatiate twitter bot object
bot = instantiate_twitter_bot()

bot.update_status("One Year Ago on {}: \nThe #1 song was '{}' by #{}\n@spotify #top200 #throwbackthursday Powered by @Chartmetric".format(date, title, hashartist))

