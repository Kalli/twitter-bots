# -*- coding: utf-8 -*-
import tweepy
import random
import time
import os
import traceback

'''
the @thorskastridin cod tweet bot spreads awareness about the cod wars (https://en.wikipedia.org/wiki/Cod_Wars) 
by asking people tweeting about the cold war and cod 4 whether they meant to tweet about the cod wars
'''
tweets = ["{0}? Are you sure you didn't mean the cod wars? {1}", 
    "I haven't heard about {0} but I do know about the cod wars {1}",
    "ok ok, {0} is pretty cool but nothing compared to the cod wars {1}",
    "{0}? Is that a typo? Surely you meant the cod wars {1}",
    "the cod wars > {0}, everybody knows that {1}"
    ]

WIKILINK = 'https://en.wikipedia.org/wiki/Cod_Wars'
CONSUMER_KEY = os.environ.get('COD_BOT_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('COD_BOT_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('COD_BOT_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('COD_BOT_ACCESS_TOKEN_SECRET')

def spreadawareness():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    search_term = random.choice(['"the cold war"', '"cod4"'])
    search_results = api.search(search_term + " since:"+time.strftime("%Y-%m-%d"))
    selectedtweet = random.choice(search_results)
    tweettext = "@"+selectedtweet.user.screen_name + " " 
    tweettext += random.choice(tweets).format(search_term, WIKILINK)
    api.update_status(tweettext, selectedtweet.id_str)

while True:
    try: 
        spreadawareness()
    except Exception:
        print(traceback.format_exc())
    time.sleep(30 * 60) # the codbot sleeps with the fishes for 30 minutes


