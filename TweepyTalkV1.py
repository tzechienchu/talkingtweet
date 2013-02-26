from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import subprocess

import time
import datetime

import googlespeech
import dbaccess
import tweetprocess

from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
import smbus
import Adafruit_CharLCDPlate

consumer_key = '*'
consumer_secret = '*'
access_token = '*'
access_token_secret = '*'

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_status(self, status):
        print (u"{text}".format(text=status.text))
        print (u"{name}({screen})\n{created} via {src}\n".format(
                name = status.author.name,screen=status.author.screen_name,
                created=status.created_at,src=status.source))
            
        userid = status.author.screen_name

        tweettext = tweetprocess.removeHTTPURL(status.text)
        tweetcommand = tweetprocess.getTweetCommand(tweettext)
        print tweetcommand

        if tweetcommand == 'talkZH:':
            speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
            print speaktext
            googlespeech.speakSpeechFromTextZH(speaktext)
        if tweetcommand == 'talkJP:':
            speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
            print speaktext
            googlespeech.speakSpeechFromTextJP(speaktext)
        if tweetcommand == 'talk:':
            speaktext = tweetprocess.processUnicodeforEN(tweettext)
            print speaktext
            googlespeech.speakSpeechFromTextEN(speaktext)
            
        if tweetcommand == 'take:':
            now = time.time()
            nowlog = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
            api = tweepy.API(auth)
            pid = subprocess.call(["fswebcam","test.jpg"])
            fn = '/home/pi/talkingtweet/test.jpg'
            api.status_update_with_media(fn,status=nowlog)
            
        if tweetcommand == 'show:':
            showtext = tweetprocess.processUnicodeforEN(tweettext)
            now = time.time()
            nowlog = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')            
            lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
            lcd.clear()
            message = nowlog + '\n'+showtext
            lcd.message(message)
    
            
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
    lcd.clear()
    lcd.message("Aloha !\nRPiTalkingTweet")
    
    tdb = dbaccess.TWdbaccess("tweetdb.db")
    userlang = tdb.readUserState()
    print userlang

##
##    text = u"RT @nhk_news: 朱莉安 ABCD 不要看電視 http://t.co/wlINNXkl #nhk_news"
##    speaktext = tweetprocess.removeHTTPURL(text)
##    print speaktext
##    speaktext = tweetprocess.processUnicodeforJPZH(speaktext)
##    print speaktext
##    googlespeech.speakSpeechFromTextZH(speaktext)
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    stream = Stream(auth, l)	
    stream.userstream()
    
