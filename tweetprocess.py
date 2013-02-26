#
#Twitter Data Process
#

import re
import unicodedata

def getTweetCommand(text):
    rtext = ""
    if isinstance(text,str):
        print text
        text = unicode(text,'unicode-escape')
    for chr in text:
        chrtype = unicodedata.category(chr)
        if chrtype == 'Ll':
            rtext = rtext + chr
        if chrtype == 'Lu':
            rtext = rtext + chr            
        if chr == ':':
            return rtext+':'

def processUnicodeforEN(text):
    rtext = ""
    if isinstance(text,str):
        print text
        text = unicode(text,'unicode-escape')    
    for chr in text:
        chrtype = unicodedata.category(chr)
        if chrtype == 'Ll' :
            rtext = rtext + chr
        if chrtype == 'Lu' :
            rtext = rtext + chr
        if chrtype == 'Nd' :
            rtext = rtext + chr            
        if chrtype == 'Zs' :
            rtext = rtext + ' '
        if chr == ':' :
            rtext = rtext + ':'            
            
    if "show:" in rtext:
        rtext = rtext.replace("show:","")
        
    return rtext
        
def processUnicodeforJPZH(text):
    rtext = u""
    for chr in text:
        chrtype = unicodedata.category(chr)
        #print chrtype
        if chrtype == 'Lo' :
            rtext = rtext + chr
        if chrtype == 'Nd' :
            rtext = rtext + chr             
        if chrtype == 'Zs' :
            rtext = rtext + chr
            
    return rtext
        
def getHTTPURL(subject):
    t = ""
    t = subject[subject.find("http://"):]
    t = t[0:20]
    if len(t) < 5:
        return ""
    else:
        return t

def removeHTTPURL(subject):
    t = ""
    t = subject[subject.find("http://"):]
    t = t[0:20]
    if len(t) < 5:
        return subject
    else:
        return subject.replace(t,'')    
    
def getCommand(subject):
    t = ""
    t = subject[subject.find("#RPiTTC"):]
    #print len(t)
    if len(t) < 5 :
        return ""
    else:
        return t

def parseCommand(command):
    t = command[command.find(":")+1:]
    commands = t.split(',')
    return commands
