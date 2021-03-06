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
import scheduler

mid = '<OFFICE>'
pfolder = '/home/pi/talkingtweet/'
wstatus = 'Command Done OK'
timerevent = scheduler.Scheduler()
wdt = 0

def incWDT():
    global wdt
    wdt += 1
    
def decWDT():
    global wdt
    if wdt > 0:
        wdt -= 1
        
def checkWDT(maxv):
    global wdt
    if wdt >= maxv:
        return 1
    else:
        return 0
    
def printWDT():
    global wdt
    print wdt
    
def getNowTime():
    now = time.time()
    nowlog = datetime.datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    return nowlog

def tweetStatus(msg):
    wstatus = msg+' '+ getNowTime() +' in ' +mid
    try:
        api.update_status(status = wstatus)
    except:
        pass

def minLCDUpdate():
    now = time.localtime(time.time())
    year, month, day, hour, minute, second, weekday, yearday, daylight = now

    lcdShowMessage('RPiTalkingTweet',5)
    if checkWDT(3) == 1:
        reboot()
    if ((minute % 10) == 0):
    	print 'System Tweet'
    	incWDT()
    	tweetStatus('take: by myself')      
    
def hourlyStatusUpdate():
    print 'System Tweet'
    incWDT()
    tweetStatus('take: by myself')

def reboot():
    print 'Reboot'
    pid = subprocess.call(["sudo", "reboot"])


def lcdShowMessage(mymsg,dur):
    nowlog = getNowTime()
    lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
    lcd.backlight(lcd.ON)
    lcd.clear()
    message = nowlog + '\n' + mymsg
    lcd.message(message)
    
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
            wstatus = 'TalkZH OK'
            try:
                speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
                googlespeech.speakSpeechFromTextZH(speaktext)
                print speaktext
            except:
                wstatus = "Error talkZH"
                tweetStatus(wstatus)
                
        if tweetcommand == 'talkjp:':
            wstatus = 'TalkJP OK'
            try:
                speaktext = tweetprocess.processUnicodeforJPZH(tweettext)
                googlespeech.speakSpeechFromTextJP(speaktext)
                print speaktext
            except:
                wstatus = "Error talkjp"
                tweetStatus(wstatus)  
                
        if tweetcommand == 'talk:':
            wstatus = 'Talk OK'
            try:
                speaktext = tweetprocess.processUnicodeforEN(tweettext)
                googlespeech.speakSpeechFromTextEN(speaktext)
                print speaktext
            except:
                wstatus = "Error talk:"
                tweetStatus(wstatus)
                
        if tweetcommand == 'take:':
            wstatus = 'Take OK'
            try:
                nowlog = getNowTime()
                ##api = tweepy.API(auth)
                fname = pfolder +'DCIM/'+nowlog+'.jpg'
                pid = subprocess.call(["fswebcam","-r","640x480",fname])
                api.status_update_with_media(fname,status=nowlog)
                lcdShowMessage('Take Picture!',5)
                decWDT()
            except:
                wstatus = "Error take Picture"
                tweetStatus(wstatus)
            
        if tweetcommand == 'show:':
            wstatus = 'Show OK'
            try:
                showtext = tweetprocess.processUnicodeforEN(tweettext)
                nowlog = getNowTime()
                lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
                lcd.backlight(lcd.ON)
                lcd.clear()
                message = nowlog + '\n'+showtext
                lcd.message(message)
            except:
                wstatus = "Error Show Text on LCD"
                tweetStatus(wstatus)   

        if tweetcommand == 'showoff:':
            lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
            lcd.backlight(lcd.OFF)
            
        if tweetcommand == 'showon:':
            lcd = Adafruit_CharLCDPlate.Adafruit_CharLCDPlate(busnum = 1)
            lcd.backlight(lcd.ON)
            lcd.clear()
            lcd.message("Aloha !\nRPiTalkingTweet")

        if tweetcommand == 'reboot:':
            print 'Reboot'
            pid = subprocess.call(["sudo","reboot"])
            
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

### StartUp Procedure
    wdt = 0
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
    
### Setup Timer Event
    #timerevent.AddTask( hourlyStatusUpdate,3600,30)
    timerevent.AddTask( minLCDUpdate,60,5)
    print timerevent
    timerevent.StartAllTasks()
    
### Setup Twitter Stream'''    
    
    l = StdOutListener()
    auth = OAuthHandler(tweetkey.consumer_key, tweetkey.consumer_secret)
    auth.set_access_token(tweetkey.access_token, tweetkey.access_token_secret)
    
    api = tweepy.API(auth)
    stream = Stream(auth, l)	
    stream.userstream()

