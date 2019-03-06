import praw
import variables
import time
import re
from datetime import datetime, timedelta, timezone
import db
def isRemoved(submission):
    if submission.banned_by is not None:
        return True
    else:
        return False
def getTag(title):
    return re.findall('\[(.*?)\]', title)[0]
def getThreadInfo(submission):
    ret = {}
    ret['game'] = getTag(submission.title)
    ret['title'] = submission.title
    ret['time'] = submission.created_utc
    ret['url'] = submission.url
    submission.comments.replace_more(limit = None)
    comments = submission.comments.list()
    ret['comments'] = len(comments)
    return ret

def validThreads(threads, reddit):
    threads = reddit.info(fullnames = threads)
    valid = []
    for thread in threads:
        if isRemoved(thread) or 'Daily Discussion' in thread.title or 'Free Talk' in thread.title or 'META' == getTag(thread.title):
            continue
        valid.append(thread)
    return valid

def generateTable(threads):
    if len(threads) == 0:
        return 'No recent match threads.' + '\n'
    else:
        table = 'Game|Thread|Comments' + '\n'
        table += ':-:|-|:-:' + '\n'
        for thread in threads:
            s = variables.spriteMappings[thread['game']] + '|[' + thread['title'] + '](' + thread['url']  + ')|' + str(thread['comments']) + '\n'
            table += s
        return table
        
def main(reddit):
    print('Getting recent matchthreads.')
    threads = db.getMatchThreads()
    threads = validThreads(threads, reddit)
    threadInfo = []
    for thread in threads:
        threadInfo.append(getThreadInfo(thread))
    return generateTable(sorted(threadInfo, key = lambda k: k['time'], reverse = True))

