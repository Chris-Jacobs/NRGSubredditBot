import praw
import variables
import time
import re
from datetime import datetime, timedelta, timezone
def isRemoved(submission):
    if submission.banned_by is not None:
        return True
    else:
        return False
def getThreadInfo(submission):
    if isRemoved(submission):
        return None
    ret = {}
    game = re.findall('\[(.*?)\]', submission.title)[0]
    if (game != 'META'):
        ret['game'] = game
    else:
        return None
    ret['locked'] = submission.locked
    ret['title'] = submission.title
    ret['time'] = submission.created_utc
    ret['views'] = submission.view_count
    ret['url'] = submission.url
    submission.comments.replace_more(limit = None)
    comments = submission.comments.list()
    ret['comments'] = len(comments)
    return ret
    
def checkUser(user):
    t  = datetime.utcnow() + timedelta(hours = -40)
    t = t.replace(tzinfo=timezone.utc).timestamp()
    threads = []
    #print(t)
    for submission in r.redditor(user).submissions.new():
        if submission.created_utc >= t:
            if submission.subreddit == 'OpTicGaming':
                thread = getThreadInfo(submission)
                if thread is not None:
                    threads.append(getThreadInfo(submission))
        else:
            break
    return threads
def checkUsers():
    threads = []
    for user in variables.postUsers:
        threads.extend(checkUser(user))
    threads = sorted(threads, key = lambda k: k['time'], reverse = True)
    return generateTable(threads)
def generateTable(threads):
    if len(threads) == 0:
        return 'No recent match threads.'
    else:
        table = 'Game|Thread|Comments|Views|Locked' + '\n'
        table += ':-:|-|:-:|:-:|:-:' + '\n'
        for thread in threads:
            s = variables.spriteMappings[thread['game']] + '|[' + thread['title'] + '](' + thread['url']  + ')|' + str(thread['comments']) + '|' + str(thread['views']) + '|' + str(thread['locked']) + '\n'
            table += s
        return table
        
def main():
    return checkUsers()

r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
#submission = r.submission(url = submission)
#print(time.gmtime(time.time()))
#print(time.gmtime(submission.created_utc))
#print(dir(submission))
