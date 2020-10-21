#this module contains the function to instantiate an object as a twitter bot

import tweepy
from cm_config import config


#set authorization keys to variable to authorize twitter api access
consumer_key = config['consumer_key']
consumer_secret_key = config['consumer_secret_key']
access_key = config['access_token']
access_token_secret = config['access_token_secret']



def instantiate_twitter_bot():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_key, access_token_secret)

    api = tweepy.API(auth)
    return api