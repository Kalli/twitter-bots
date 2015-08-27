# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import re
import time
import tweepy
import os

CONSUMER_KEY = os.environ.get('AURORA_BOT_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('AURORA_BOT_CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('AURORA_BOT_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('AURORA_BOT_ACCESS_TOKEN_SECRET')


def tweetauroraforecast():
    url = "http://en.vedur.is/weather/forecasts/aurora/"
    r = requests.get(url)
    r.encoding

    now = time.gmtime()
    datestring = time.strftime("%y%m%d", now)
    timestring = time.strftime("%H:00 - %d.%m.%y", now)

    # Forecasts come at three hour intervals from midnight find the closest one
    forecasttimes = range(3, 25, 3)
    closestforecast = forecasttimes[min(range(len(forecasttimes)), key=lambda i: abs(forecasttimes[i]-now.tm_hour))]

    # Get the cloud cover image
    imgstring = "http://en.vedur.is/photos/ecm0125_island_tcc/"+time.strftime("%y%m%d_0000_", now)+str(closestforecast)+".png"

    # Find the index javascript
    soup = BeautifulSoup(r.text.encode('utf-8'))
    indexes = soup.findAll("script", text=re.compile("VI.data.aurora.idx"))
    index_re = re.compile(datestring + ".*act:\s(\d)")
    index = index_re.findall("".join(indexes))

    tweettext = ""
    if len(index) == 1:
        tweettext = "Aurora activity in Iceland: %s/9\nDetails: %s\nCloud cover: %s\n%s" % (index[0], url, imgstring, timestring)
    if len(tweettext) > 0:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.update_status(tweettext)

tweetauroraforecast()

while True:
    time.sleep(60* 60)
    if time.gmtime().tm_hour in [0, 6, 12, 18]:
        try:
            tweetauroraforecast()
        except Exception:
            print(traceback.format_exc())