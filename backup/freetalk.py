import datetime
import praw
import variables
import random
sayings = {}

def getSaying():
    global sayings
    print("Getting Phrases from Wiki...")
    r = praw.Reddit(client_id=variables.client_id,
                    client_secret=variables.client_secret,
                    user_agent=variables.user_agent,
                    username=variables.username,
                    password=variables.password)
    wiki = r.subreddit(variables.subreddit).wiki['freetalk'].content_md
    sayings =  wiki.split('\n')
    return random.choice(sayings)
def postThread():
 
    r = praw.Reddit(client_id=variables.client_id,
                    client_secret=variables.client_secret,
                    user_agent=variables.user_agent,
                    username=variables.username,
                    password=variables.password)
    body = getSaying().strip() + ", have a great Friday!"
    print("Posting Free Talk Friday...")
    now = datetime.datetime.now()
    ret = r.subreddit(variables.subreddit).submit(title = '[MISC] Free Talk Friday ('  + variables.months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')' , selftext = body, send_replies=False)
    ret.mod.sticky(state=True, bottom=True)

def main(day):
    now = datetime.datetime.today()
    if now.weekday() == 4 and day != now.day and now.hour == variables.ftfhour:
        postThread()
        return now.day
    else:
        print('Not Time for Free Talk Friday.')
        return day

