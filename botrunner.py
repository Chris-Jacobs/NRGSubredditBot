import streamBot
import dailyThread
import freetalk
import matchthreads
import praw
import sys
import youtube
from time import sleep
streamTable = ''
ddt = ''
day = 0
sleepTime = 5 ##in minutes
debugMode = False
while True:
    sleepTime = 0 if debugMode else 5
    print('')
    if not debugMode:
        try :
            matchthreads.main()
            streamTable = streamBot.main()
            yt = youtube.main()
            ddt = dailyThread.main(streamTable, yt, ddt)
            day = freetalk.main(day)
        except Exception :
            print("Unexpected error:", sys.exc_info()[0])
            try:
                streamBot.log(sys.exc_info()[0])
            except Exception:
                 pass
    else:
        matchthreads.main()
        streamTable = streamBot.main()
        yt = youtube.main()
        #yt = None
        ddt = dailyThread.main(streamTable, yt, ddt)
        day = freetalk.main(day)
    print('Sleeping for ' + str(sleepTime) +' Minutes...')
    i = sleepTime
    while i > 0:
        sleep(60)
        i -= 1
        print(str(i) + ' minutes left.')
    
