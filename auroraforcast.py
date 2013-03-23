# -*- coding: utf-8 -*-
import requests
from BeautifulSoup import BeautifulSoup
import re
import datetime
import tweepy
import credentials

def tweetauroraforcast():
    url = "http://en.vedur.is/weather/forecasts/aurora/"
    r = requests.get(url)
    r.encoding
    soup = BeautifulSoup(r.text.encode('utf-8'))
    indexes = soup.findAll("script", text=re.compile("VI.data.aurora.idx"))
    texts = soup.findAll("script", text=re.compile("VI.data.aurora.text"))

    now = datetime.datetime.now()
    datestring = now.strftime("%y%m%d")
    timestring = now.strftime("%H:00 - %d.%m.%y")

    text_re = re.compile("txt: \'(.*)\'")
    textforecast = text_re.findall("".join(texts))

    index_re = re.compile(datestring + ".*act:\s(\d)")
    index = index_re.findall("".join(indexes))

    tweettext = ""
    if len(textforecast) == 1 and len(index) == 1:
        if len(textforecast[0]) > 35:
            textforecast[0] = textforecast[0][0:40] + "..."
        tweettext = "Aurora activity in Iceland: %s/9\n\"%s\"\n%s\n%s" % (index[0], textforecast[0], url, timestring)

    if len(tweettext) > 0:
        auth = tweepy.OAuthHandler(credentials.AURORA_CONSUMER_KEY, credentials.AURORA_CONSUMER_SECRET)
        auth.set_access_token(credentials.AURORA_ACCESS_TOKEN, credentials.AURORA_ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(tweettext)
        user = api.me()
        print user.name

#tweetauroraforcast()
import cloud
cloud.cron.register(tweetauroraforcast, 'auroraforcast_tweetauroraforcast', '1 */8 * * *', _type='s1', _max_runtime=10)
