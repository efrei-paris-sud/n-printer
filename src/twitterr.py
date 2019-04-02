#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import print_function
import base64, HTMLParser, httplib, json, sys, urllib, zlib, textwrap
from unidecode import unidecode
from Adafruit_Thermal import *
import tweepy

consumer_key    = '5qwNg96PL5cBteeDy856HuorR'
consumer_secret = 't8Q7meg4DmkwWND6S341y4A0CaChDb1LLHio3XqvBJ0YknVXU0'

access_token = '1274835308-TziMunJqwQLNugn4STN37UoKtJK1asHPvRLp5ss'
access_token_secret = 'OofO8gqrwBs7pXZNqNumzQgLgqp4n5mrm83BNnj73JqQc'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)