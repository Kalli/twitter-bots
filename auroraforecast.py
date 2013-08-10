# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import re
import datetime
import tweepy
import credentials

def tweetauroraforecast():
    url = "http://en.vedur.is/weather/forecasts/aurora/"
    r = requests.get(url)
    r.encoding

    now = datetime.datetime.now()
    datestring = now.strftime("%y%m%d")
    timestring = now.strftime("%H:00 - %d.%m.%y")

    # Get the cloud cover image
    description={"0":"Minimum","1":"Quiet","2":"Low","3":"Moderate","4":"Active","5":"High","6":"Very high","7":"Strong","8":"Severe","9":"Extreme"}

    # Find the index javascript
    soup = BeautifulSoup(r.text.encode('utf-8'))
    indexes = soup.findAll("script", text=re.compile("VI.data.aurora.idx"))
    index_re = re.compile(datestring + ".*act:\s(\d)")
    index = index_re.findall("".join(indexes))
    tweettext = ""
    if len(index) == 1:
        tweettext = "Current aurora activity in Iceland: %s - %s/9\nDetails: %s\n%s" % (description[index[0]], index[0], url,  timestring)
    if len(tweettext) > 0:
        auth = tweepy.OAuthHandler(credentials.AURORA_CONSUMER_KEY, credentials.AURORA_CONSUMER_SECRET)
        auth.set_access_token(credentials.AURORA_ACCESS_TOKEN, credentials.AURORA_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(tweettext)

tweetauroraforecast()
import cloud
cloud.cron.register(tweetauroraforecast, 'auroraforecast_tweetauroraforecast', '0 1,7,19,22 * * *', _type='s1', _max_runtime=10)
