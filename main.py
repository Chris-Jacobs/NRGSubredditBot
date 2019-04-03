import freetalk
import matchthreads
import praw
import sys
import matchhub
import praw
import variables
import streams
import sidebar
from time import sleep
import stats
import traffic
import dailyThread
import verification
from reddittable import RedditTable
ddt = None
day = 0
sleepTime = 2 ##in minutes
debugMode = False
if len(sys.argv) > 1:
    debugMode = True
while True:
    #sleepTime = 0 if debugMode else sleepTime
    print('')
    botReddit = praw.Reddit(client_id = variables.keys['RedditBotClientID'],
                    client_secret = variables.keys['RedditBotClientSecret'],
                    user_agent = variables.keys['RedditUserAgent'],
                    username = variables.keys['RedditBotUsername'],
                    password = variables.keys['RedditBotPassword'])
    modReddit = praw.Reddit(client_id = variables.keys['RedditModClientID'],
                    client_secret = variables.keys['RedditModClientSecret'],
                    user_agent = variables.keys['RedditUserAgent'],
                    username = variables.keys['RedditModUsername'],
                    password = variables.keys['RedditModPassword'])
    if debugMode:
        matchthreads.main(modReddit)
        ddtStreamTable, sidebarStreamTable = streams.main()
        sidebar.main(botReddit, sidebarStreamTable)
        matchTable = matchhub.main(botReddit)
        ddt = dailyThread.main(ddt, ddtStreamTable, matchTable, botReddit)
        freetalk.main(botReddit)
        traffic.main(botReddit)
        verification.main(botReddit)
        #exit()
    else:
        try:
            matchthreads.main(modReddit)
        except Exception:
            print('Error with Match Threads site.')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
        try:
            ddtStreamTable, sidebarStreamTable = streams.main()
        except Exception:
            print('Error with Streams.')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
            ddtStreamTable = RedditTable(None)
            sidebarStreamTable = RedditTable(None)
        try:
            sidebar.main(botReddit, sidebarStreamTable)
        except Exception:
            print('Error with Sidebar.')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
        try:
            matchTable = matchhub.main(botReddit)
        except Exception:
            print('Error with recent matches.')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
            matchTable = RedditTable(None)
        try:
            ddt = dailyThread.main(ddt, ddtStreamTable, matchTable, botReddit)
        except Exception:
            print('Error with DDT.')
            ddt = None
        try:
            freetalk.main(botReddit)
        except Exception:
            print('Error with FTF.')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
        try:
            traffic.main(botReddit)
        except Exception:
            print('Error with Traffic')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
        try:
            verification.main(botReddit)
        except Exception:
            print('Error with Verification Flairs')
            print(sys.exc_info()[0])
            print(sys.exc_info()[1])
            print("")
    print('Sleeping for ' + str(sleepTime) +' Minutes...')
    i = sleepTime
    while i > 0:
        sleep(60)
        i -= 1
        print(str(i) + ' minutes left.')
    
