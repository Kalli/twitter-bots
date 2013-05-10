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

    # Forecasts come at three hour intervals from midnight find the closest one
    forecasttimes = range(3, 25, 3)
    closestforecast = forecasttimes[min(range(len(forecasttimes)), key=lambda i: abs(forecasttimes[i]-now.hour))]

    # Get the cloud cover image
    imgstring = "http://en.vedur.is/photos/ecm0125_island_tcc/"+now.strftime("%y%m%d_0000_")+str(closestforecast)+".png"

    # Find the index javascript
    soup = BeautifulSoup(r.text.encode('utf-8'))
    indexes = soup.findAll("script", text=re.compile("VI.data.aurora.idx"))
    index_re = re.compile(datestring + ".*act:\s(\d)")
    index = index_re.findall("".join(indexes))

    tweettext = ""
    if len(index) == 1:
        tweettext = "Aurora activity in Iceland: %s/9\nDetails: %s\nCloud cover: %s\n%s" % (index[0], url, imgstring, timestring)
    if len(tweettext) > 0:
        auth = tweepy.OAuthHandler(credentials.AURORA_CONSUMER_KEY, credentials.AURORA_CONSUMER_SECRET)
        auth.set_access_token(credentials.AURORA_ACCESS_TOKEN, credentials.AURORA_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(tweettext)

tweetauroraforecast()
import cloud
cloud.cron.register(tweetauroraforecast, 'auroraforecast_tweetauroraforecast', '0 1,7,19,22 * * *', _type='s1', _max_runtime=10)
