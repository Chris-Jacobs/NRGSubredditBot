import streamBot
import dailyThread
import freetalk
import matchthreads
import praw
import sys
import matchhub
from time import sleep
streamTable = ''
ddt = ''
day = 0
sleepTime = 2 ##in minutes
debugMode = False
if len(sys.argv) > 1:
    debugMode = True
while True:
    sleepTime = 0 if debugMode else sleepTime
    print('')
    if not debugMode:
        try :
            matchthreads.main()
            try:
                streamTable = streamBot.main()
            except Exception:
                streamTable = ""
            #yt = youtube.main()
            yt = None
            matches = matchhub.main()
            ddt = dailyThread.main(streamTable, yt, ddt, matches)
            day = freetalk.main(day)
        except Exception :
            print("Unexpected error:", sys.exc_info()[0])
    else:
        matchthreads.main()
        streamTable = streamBot.main()
        #yt = youtube.main()
        yt = None
        matches = matchhub.main()
        ddt = dailyThread.main(streamTable, yt, ddt, matches)
        day = freetalk.main(day)
    print('Sleeping for ' + str(sleepTime) +' Minutes...')
    i = sleepTime
    while i > 0:
        sleep(60)
        i -= 1
        print(str(i) + ' minutes left.')
    
