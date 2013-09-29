# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import re
import datetime
import tweepy
import metadata
import random


def get_aurora_description(descriptions, rating):
    return random.choice(descriptions[rating])


def get_aurora_activity_rating():
    url = "http://en.vedur.is/weather/forecasts/aurora/"
    r = requests.get(url)
    r.encoding

    now = datetime.datetime.now()
    datestring = now.strftime("%y%m%d")

    # Find the index javascript
    soup = BeautifulSoup(r.text.encode('utf-8'))
    indexes = soup.findAll("script", text=re.compile("VI.data.aurora.idx"))
    index_re = re.compile(datestring + ".*act:\s(\d)")
    index = index_re.findall("".join(indexes))
    return index


def tweetauroraforecast():
    index = get_aurora_activity_rating()
    tweettext = ""
    if len(index) == 1:
        now = datetime.datetime.now()
        timestring = now.strftime("%y%m%d-%H")
        tweettext = get_aurora_description(metadata.descriptions, index[0]) + " http://en.vedur.is/weather/forecasts/aurora/?t="+timestring
    if len(tweettext) > 0:
        auth = tweepy.OAuthHandler(metadata.AURORA_CONSUMER_KEY, metadata.AURORA_CONSUMER_SECRET)
        auth.set_access_token(metadata.AURORA_ACCESS_TOKEN, metadata.AURORA_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(tweettext)

tweetauroraforecast()
import cloud
cloud.cron.register(tweetauroraforecast, 'itaurorahunt_tweetauroraforecast', '0 7,19,22 * * *', _type='s1', _max_runtime=10)
