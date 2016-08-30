import streamBot
import dailyThread
import freetalk
import praw
import sys
from time import sleep
streamTable = ''
months = dailyThread.months
ddt = ''
day = 0
sleepTime = 1 ##in minutes
##sleepTime = 0 ## debug mode
while True:
    print('')
    try :
        streamTable = streamBot.main()
        ddt = dailyThread.main(streamTable, ddt)
        day = freetalk.main(day)
    except praw.errors.InvalidCaptcha:
        ## This error is thrown everytime, doesn't effect functionality.
        pass
    except Exception :
        print("Unexpected error:", sys.exc_info()[0])
    print('Sleeping for ' + str(sleepTime) +' Minutes...')
    i = sleepTime
    while i > 0:
        sleep(60)
        i -= 1
        print(str(i) + ' minutes left.')
    
