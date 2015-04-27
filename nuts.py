# -*- coding: utf-8 -*-
__author__ = 'cohalz'

from twitter import *
import configparser
import random
import re

def tweet(string,tweet_id):
    try:
        tw.statuses.update(status=string,in_reply_to_status_id=tweet_id)
    except:
        tweet(string+"!",tweet_id)

def update(_id,tweet_user,message,reply):
    tweet_user = msg['user']['screen_name']     
    string = "@"+ tweet_user + " " + message
    tweet(string,_id)
    tw.favorites.create(_id=_id)
    print(tweet_user+": "+reply)

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
image = [
    "https://twitter.com/yuya_b_c_d/status/587468014779367424/photo/1",
    "https://twitter.com/yuya_b_c_d/status/587468383827861504/photo/1",
    "https://twitter.com/pachitamao/status/587468907402768384/photo/1",
    "https://twitter.com/sugino_souta/status/587468974994010112/photo/1",
    "https://twitter.com/zakosuka/status/587470532146151427/photo/1",
    "https://twitter.com/kureha0226/status/587490861451083776/photo/1",
    "https://twitter.com/yuya_b_c_d/status/587490950320037888/photo/1",
    "https://twitter.com/pachitamao/status/587491294231969792/photo/1",
    "https://twitter.com/yuya_b_c_d/status/587491331947102208/photo/1",
    "https://twitter.com/pachitamao/status/587491654539448322/photo/1",
    "https://twitter.com/yuya_b_c_d/status/587491674152009729/photo/1",
    "https://twitter.com/sugino_souta/status/587493043873284096/photo/1",
    "https://twitter.com/kts_tdu_bot/status/587493915923591169/photo/1",
    "https://twitter.com/yuya_b_c_d/status/587954787569631232/photo/1",
    "https://twitter.com/kirotgsche/status/590903763939897344/photo/1",
    "https://twitter.com/sorenuts_nuts/status/590903369943756801/photo/1",
    "https://twitter.com/sorenuts_nuts/status/590904484240314368/photo/1",
    "https://twitter.com/sorenuts_nuts/status/590501001892798465/photo/1",
    "http://t.co/GljHE6tLSU",
    "http://t.co/zCOjIw2FSv",
    "https://twitter.com/kirotgsche/status/587976953820360704/photo/1"
    ]
start_message="それナッツ!"
message="それナッツ"
end_message="ナッツナッツ"
pettern = re.compile("@[a-zA-Z0-9_]*\sそれナッツ")
egosa = re.compile(".*(そ.*れ.*ナ.*ッ.*ツ.*)")
tweet(start_message,0)
linkprefix = re.compile(".*http://t.co/.*")
prob = 800
print(my_name+": "+start_message)

tw_us = TwitterStream(auth=oauth, domain='userstream.twitter.com')
try:
    for msg in tw_us.user():
        if "text" in msg:
            matchstr = pettern.match(msg['text'])
            matchego = egosa.match(msg['text'])
            matchlink = linkprefix.match(msg['text'])
            tweet_user = msg['user']['screen_name'] 
            if tweet_user != my_name and not(msg['text'].startswith("RT")):
                if msg['id'] % prob == prob / 2 or msg['text'].count("それナッツ？"):
                    tweet(image[random.randint(0,len(image) - 1)],0)
                    print(tweet_user+": "+msg['text'])

                elif matchstr:
                    update(msg['id'],tweet_user,matchstr.group(),msg['text'])
                elif msg['id'] % prob == 0:
                    update(msg['id'],tweet_user,message,msg['text'])
                elif matchego:
                    update(msg['id'],tweet_user,matchego.group(1),msg['text'])
                elif msg['text'].startswith("@"+my_name):
                    update(msg['id'],tweet_user,message,msg['text'])
                    if matchlink:
                        fp = open('image.log','a')
                        fp.write(matchlink.group()+"\n")
                        fp.close()
except:
    tweet(end_message,0)
    print(my_name+": "+end_message)
    fp.close()
