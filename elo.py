import json
import random

class Song:
    name = ""
    elo = 0
    def __init__(self, name, elo):
        self.name = name
        self.elo = elo
        
    def getName(self):
        return self.name
        
    def getElo(self):
        return self.elo
        
    def expectedScore(self, song):
        other_elo = song.getElo()
        R = (other_elo - self.elo)/400
        E = 1/(1+10**R)
        return E
    
    def updateScore(self, result, song):
        self.elo = (int)(self.elo + (24*(result - self.expectedScore(song))))
    
def compareSongs(song1, song2, song1Result):
    tempSong1 = song1
    tempSong2 = song2
    
    song1.updateScore(song1Result, tempSong2)
    if(song1Result == 1):
        song2.updateScore(0, tempSong1)
    else:
        song2.updateScore(1, tempSong1)

songs = []

    
def fillSongs(file):
    data = ""
    with open(file) as json_data:
        data = json.load(json_data)    
        
    for i in range(0, len(data["items"])):
        name = data["items"][i]["track"]["name"]
        songs.append(Song(name, 1200))
        
def readFile():
    with open('SongsElo.txt', "r") as f:
        lines = f.readlines()
        for i in lines:
            line = i.split(" ")
            elo = int(line[0])
            del line[0]
            line = " ".join(line)
            line = line.rstrip()
            songs.append(Song(line, elo))
   
        
def cycleSongs():
    song1 = random.choice(songs)
    song2 = random.choice(songs)
    while song1.getName() == song2.getName():
        song2 = random.choice(songs)
        
    result = input("1: " + song1.getName() + " <=> 2: " + song2.getName() + " ------ any other key: Exit\n")
       
    if result == "1":
        compareSongs(song1, song2, 1)
    elif (result == "2"):
        compareSongs(song1, song2, 0)
        
    return result
        
def printSongs():
    songs.sort(key=lambda x: x.getElo(), reverse=True)
    for i in range(0,len(songs)):
        print("%50s  ::  %10s" % (songs[i].getName(), str(songs[i].getElo())))
        
    with open('SongsElo.txt', 'w') as out:
        out.write("")
    with open('SongsElo.txt', 'a') as out:
        for i in range(0, len(songs)):
            out.write(str(songs[i].getElo()) + " " + songs[i].getName() + "\n")
            
            
#fillSongs("songs.txt")
readFile()
result = "1"
while result == "1" or result == "2":
    result = cycleSongs()
    
printSongs()