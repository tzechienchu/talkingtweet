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
wstatus = 'Command Done OK'
def getNowTime():
    now = time.time()
    nowlog = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    return nowlog

class StdOutListener(StreamListener):
    """ A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_status(self, status):
        '''print (u"{text}".format(text=status.text))
        print (u"{name}({screen})\n{created} via {src}\n".format(
                name = status.author.name,screen=status.author.screen_name,
                created=status.created_at,src=status.source))
        '''
        
        userid = status.author.screen_name

        tweettext = tweetprocess.removeHTTPURL(status.text)
        tweetcommand = tweetprocess.getTweetCommand(tweettext)
        if (len(tweetcommand) > 2):
            tweetcommand = tweetcommand.lower()
            print tweetcommand

        if tweetcommand == 'talkzh:':
            wstatus = 'TalkZH OK' + getNowTime()
            try:
                speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
                googlespeech.speakSpeechFromTextZH(speaktext)
                print speaktext
            except:
                wstatus = "Error talkZH"
            api.update_status(status = wstatus)
                
        if tweetcommand == 'talkjp:':
            wstatus = 'TalkJP OK' + getNowTime()
            try:
                speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
                googlespeech.speakSpeechFromTextJP(speaktext)
                print speaktext
            except:
                wstatus = "Error talkjp"
            api.update_status(status = wstatus)    
                
        if tweetcommand == 'talk:':
            wstatus = 'Talk OK' + getNowTime()
            try:
                speaktext = tweetprocess.processUnicodeforEN(tweettext)
                googlespeech.speakSpeechFromTextEN(speaktext)
                print speaktext
            except:
                wstatus = "Error talk:"
            api.update_status(status = wstatus)
                
        if tweetcommand == 'take:':
            wstatus = 'Take OK' + getNowTime()
            try:
                nowlog = getNowTime()
                ##api = tweepy.API(auth)
                fname = pfolder +'DCIM/'+nowlog+'.jpg'
                pid = subprocess.call(["fswebcam",fname])
                api.status_update_with_media(fname,status=nowlog)
            except:
                wstatus = "Error take Picture"
            api.update_status(status = wstatus)
            
        if tweetcommand == 'show:':
            wstatus = 'Show OK' + getNowTime()
            try:
                showtext = tweetprocess.processUnicodeforEN(tweettext)
                nowlog = getNowTime()
                lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
                lcd.clear()
                message = nowlog + '\n'+showtext
                lcd.message(message)
            except:
                wstatus = "Error Show Text on LCD"
            api.update_status(status = wstatus)    
            
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
    
    api = tweepy.API(auth)
    stream = Stream(auth, l)	
    stream.userstream()
    
