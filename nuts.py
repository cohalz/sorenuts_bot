# -*- coding: utf-8 -*-
__author__ = 'cohalz'

from twitter import *
import configparser
import random

def tweet(string,tweet_id):
    try:
        tw.statuses.update(status=string,in_reply_to_status_id=tweet_id)
    except:
        tweet(string+"!",tweet_id)

config = configparser.ConfigParser()
config.read('nuts.ini')
oauth_config = config['oauth']

oauth = OAuth(
    consumer_key=oauth_config['consumer'],
    consumer_secret=oauth_config['consumer_secret'],
    token=oauth_config['token'],
    token_secret=oauth_config['token_secret']
)

tw = Twitter(
    auth=OAuth(
        oauth_config['token'],
        oauth_config['token_secret'],
        oauth_config['consumer'],
        oauth_config['consumer_secret'])
)


my_name = tw.account.settings()['screen_name']
start_message="それナッツ!"
message="それナッツ"
end_message="ナッツナッツ"

tweet(start_message,0)
print(my_name+": "+start_message)

tw_us = TwitterStream(auth=oauth, domain='userstream.twitter.com')
try:
    for msg in tw_us.user():
        if "text" in msg:
            tweet_user = msg['user']['screen_name'] 
            if (msg['text'].startswith("@"+my_name) or msg['text'].count(message)) and tweet_user != my_name :
                string = "@"+ tweet_user + " " + message
                tweet(string,msg['id'])
                tw.favorites.create(_id=msg['id'])
                print(tweet_user+": "+msg['text'])
except:
    tweet(end_message,0)
    print(my_name+": "+end_message)

