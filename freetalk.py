import datetime
import praw
import variables
import random
import db
def getSaying(reddit):
    print("Getting Phrases from Wiki...")
    wiki = reddit.subreddit(variables.subreddit).wiki['freetalk'].content_md
    sayings =  wiki.split('\n')
    return random.choice(sayings)
def postThread(reddit):
 
    body = getSaying(reddit).strip() + ", have a great Friday!"
    print("Posting Free Talk Friday...")
    now = datetime.datetime.now()
    dateString = now.strftime("%B %d, %Y")
    title = '[MISC] Free Talk Friday ({date})'.format(date = dateString)
    ret = reddit.subreddit(variables.subreddit).submit(title = title, selftext = body, send_replies=False)
    ret.mod.sticky(state=True, bottom=True)

def main(reddit):
    now = datetime.datetime.today()
    lastId, lastDate = db.lastFTF()
    if now.weekday() == 4 and now.hour == variables.ftfhour and now.day != lastDate.day:
        print('Posting Free Talk Friday.')
        postThread(reddit)
    else:
        print('Not Time for Free Talk Friday.')

