#!/usr/bin/python

from __future__ import print_function
import base64, HTMLParser, httplib, json, sys, urllib, zlib, textwrap
from unidecode import unidecode
from Adafruit_Thermal import *

import subprocess, time, Image, socket

import urllib


consumer_key    = '5qwNg96PL5cBteeDy856HuorR'
consumer_secret = 't8Q7meg4DmkwWND6S341y4A0CaChDb1LLHio3XqvBJ0YknVXU0'


#http://dev.twitter.com/docs/using-search
#https://developer.twitter.com/en/docs/tweets/search/quick-start/premium-30-day

query = sys.argv[1]
hashtag = sys.argv[2]
print(query)



printer   = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
host      = 'api.twitter.com'
authUrl   = '/oauth2/token'
searchUrl = '/1.1/search/tweets.json?'
agent     = 'Gutenbird v1.0'

if len(sys.argv) > 1: lastId = sys.argv[1]
else:                 lastId = '1'


def issueRequestAndDecodeResponse(method, url, body, headers):
  connection = httplib.HTTPSConnection(host)
  connection.request(method, url, body, headers)
  response = connection.getresponse()
  if response.status != 200:
    exit(-1)
  compressed = response.read()
  connection.close()
  return json.loads(zlib.decompress(compressed, 16+zlib.MAX_WBITS))



token = issueRequestAndDecodeResponse(
  'POST', authUrl, 'grant_type=client_credentials',
   {'Host'            : host,
    'User-Agent'      : agent,
    'Accept-Encoding' : 'gzip',
    'Content-Type'    : 'application/x-www-form-urlencoded;charset=UTF-8',
    'Authorization'   : 'Basic ' + base64.b64encode(
     urllib.quote(consumer_key) + ':' + urllib.quote(consumer_secret))}
  )['access_token']


data = issueRequestAndDecodeResponse(
  'GET',
  (searchUrl + 'count=3&since_id=%s&q=%s' %
   (lastId, urllib.quote(query+ ' ' + hashtag))),
  None,
  {'Host'            : host,
   'User-Agent'      : agent,
   'Accept-Encoding' : 'gzip',
   'Authorization'   : 'Bearer ' + token})

printer.setSize('L')
printer.print("________________")
printer.setSize('S')

for tweet in data['statuses']:

  printer.inverseOn()
  printer.setSize('L') 
  printer.print(' ' + '{:<31}'.format(tweet['user']['screen_name']))
  printer.setSize('S')
  printer.inverseOff()

  printer.underlineOn()
  printer.print('{:<32}'.format(tweet['created_at']))
  printer.underlineOff()
  
  printer.feed(3)
  
  tweettext=textwrap.wrap(unidecode(
    HTMLParser.HTMLParser().unescape(tweet['text'])),32)
  for line in tweettext:
    printer.boldOn()
    printer.print(line + "\n")
    printer.boldOff()

  printer.feed(3)
  url = "https://twitter.com/statuses/" + tweet['id_str']
  urllib.urlretrieve("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=p%C3%A7" + url, "qrcode.jpg")
  printer.printImage(Image.open('qrcode.jpg'), True)
  printer.setSize('L')
  printer.print("________________")
  printer.setSize('S')

print(data['search_metadata']['max_id_str'] + ' ' + tweet['text']) 

