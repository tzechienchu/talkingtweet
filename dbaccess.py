#
# SQLite 3 DB Access Class
#
import sqlite3 as lite
import sys

class TWdbaccess:
    def __init__(self,dbfile):
        self.con = lite.connect(dbfile)
        self.cur = self.con.cursor() 
    def dbConnect(self,dbfile):
        self.con = lite.connect(dbfile)
        self.cur = self.con.cursor()        
    def reCreateAllTable(self):
        with self.con:
            sqlcmd = """
                DROP TABLE IF EXISTS Tweets;
                DROP TABLE IF EXISTS UserState;
                DROP TABLE IF EXISTS CommandSet;
                CREATE TABLE Tweets(Id INT,User TEXT,DTime TEXT,Tweet TEXT,URL TEXT);
                CREATE TABLE UserState(Id INT,User TEXT,Language TEXT);
                CREATE TABLE CommandSet(Id INT,Command TEXT,Parameters TEXT,Functio TEXT);      
            """
            self.cur.executescript(sqlcmd)
            
    def reCreateTweetTable(self):
        with self.con:
            sqlcmd = """
                DROP TABLE IF EXISTS Tweets;
                CREATE TABLE Tweets(Id INT,User TEXT,DTime TEXT,Tweet TEXT,URL TEXT);             
            """
            self.cur.executescript(sqlcmd)
            
    def reCreateUserTable(self):
        with self.con:
            sqlcmd = """
                DROP TABLE IF EXISTS UserState;
                CREATE TABLE UserState(Id INT,User TEXT,Language TEXT);     
            """
            self.cur.executescript(sqlcmd)
            
    def reCreateCommandTable(self):
        with self.con:
            sqlcmd = """
                DROP TABLE IF EXISTS CommandSet;
                CREATE TABLE CommandSet(Id INT,Command TEXT,Parameters TEXT,Functio TEXT);      
            """
            self.cur.executescript(sqlcmd)            
            
    def insertTweet(self,idx,username,datatime,tweet,url):
        with self.con:
            self.cur.execute("INSERT INTO Tweets (Id,User,DTime,Tweet,URL) values (?,?,?,?,?)",(idx,username,datatime,tweet,url))

    def insertUserState(self,idx,username,language):
        with self.con:
            self.cur.execute("INSERT INTO UserState (Id,User,Language) values (?,?,?)",(idx,username,language))

    def readUserState(self):
        userlang = {}
        with self.con:
            self.cur.execute("SELECT * FROM UserState")
            users = self.cur.fetchall()
            for row in users:
                userlang[row[1]]=row[2]
            return userlang
        
    def printTweetAll(self):
        with self.con:
            self.cur.execute("SELECT * FROM Tweets")
            rows = self.cur.fetchall()
            for row in rows:
                print row

if __name__ == "__main__":
    mytweetdb = TWdbaccess("tweetdb.db")
    mytweetdb.reCreateAllTable()
    mytweetdb.insertUserState(1,"cafe_kyoto","ja")
    mytweetdb.insertUserState(2,"Kyoto_Shop","ja")
    mytweetdb.printTweetAll()
    
    
        
