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


import tweetkey

pfolder = '/home/pi/talkingtweet/'
def getNowTime():
    now = time.time()
    nowlog = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    return nowlog

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
            nowlog = getNowTime()
            api = tweepy.API(auth)
            fname = pfolder +'DCIM/'+nowlog+'.jpg'
            pid = subprocess.call(["fswebcam",fname])
            api.status_update_with_media(fname,status=nowlog)
            
        if tweetcommand == 'show:':
            showtext = tweetprocess.processUnicodeforEN(tweettext)
            nowlog = getNowTime()
            lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
            lcd.clear()
            message = nowlog + '\n'+showtext
            lcd.message(message)
    
            
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

### StartUp Procedure
    
    lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
    lcd.clear()
    lcd.message("Aloha !\nRPiTalkingTweet")
    
    tdb = dbaccess.TWdbaccess("tweetdb.db")
    userlang = tdb.readUserState()
    print userlang

### 1st Pircure sometimes will goes wrong
    
    pid = subprocess.call(["fswebcam","test.jpg"])

### Test Speaker Output
    
    text = u"Talking Tweet Turn On"
    speaktext = tweetprocess.removeHTTPURL(text)
    print speaktext
    speaktext = tweetprocess.processUnicodeforEN(speaktext)
    print speaktext
    googlespeech.speakSpeechFromTextEN(speaktext)

### Setup Twitter Stream'''    
    
    l = StdOutListener()
    auth = OAuthHandler(tweetkey.consumer_key, tweetkey.consumer_secret)
    auth.set_access_token(tweetkey.access_token, tweetkey.access_token_secret)
    
    stream = Stream(auth, l)	
    stream.userstream()
    
