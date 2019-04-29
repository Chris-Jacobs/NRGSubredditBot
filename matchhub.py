import praw
import variables
import time
import re
from datetime import datetime, timedelta, timezone
import db
from reddittable import RedditColumn, RedditTable

def isRemoved(submission):
    """
    Checks if Submission has been removed by moderators
    Args:
        submission: praw.models.Submission Object
    Returns:
        True if submission's been removed, False otherwise
    """
    if submission.banned_by is not None:
        return True
    else:
        return False
def getTag(title):
    """
    Pulls the tag from the Title
    Args:
        title: Title of the thread as a String
    Returns:
        A String with the tag or an empty string if no tag is present. 
        Example: 
            "[COD] Match Thread" returns COD
    """
    try:
        return re.findall('\[(.*?)\]', title)[0]
    except IndexError:
        return ""
    
def getThreadInfo(submission):
    """
    Creates Dictionary with the information for the table for a thread
    Args:
        submission: praw.models.Submission Object
    Returns:
        A dictionary of the thread information
        Example:
        {
            'game': 'COD',
            'comments': 311,
            'time': 1554154218.0,
            'url': 'https://www.reddit.com/r/OpTicGaming/comments/b89fp9/cod_cod_is_back_appreciation_post_match_thread/',
            'title': '[COD] CoD Is Back Appreciation Post - Match Thread (OpTic Gaming vs Enigma6)'
        }
    """
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
    """
    Removes DDT's, FTF's and Removed Threads from the list of threads for the table and retreives the submissions
    Args:
        threads: List of threads in the Reddit fullname format - see https://www.reddit.com/dev/api/
            Example: ['t3_b8092f', 't3_b80rrv', 't3_b89fp9']
        reddit: Authorized praw.Reddit object
    Returns:
        List of submission objects from the passed in fullnames without DDT's, FTF's and removed threads
    """
    threads = reddit.info(fullnames = threads)
    valid = []
    for thread in threads:
        if isRemoved(thread) or 'Daily Discussion' in thread.title or 'Free Talk' in thread.title or 'META' == getTag(thread.title):
            continue
        valid.append(thread)
    return valid

def generateTable(threads):
    """
    Generates Match Thread Table for the DDT
    Args:
        threads: List of dictionaries returned by getThreadInfo()
            Should be pre sorted already
    Returns:
        RedditTable Object with Game, Thread, and Comments column or String if no recent threads
    """
    if len(threads) == 0:
        return 'No recent match threads.' + '\n'
    else:
        table = RedditTable([
                RedditColumn("Game", centered= True),
                RedditColumn("Thread"),
                RedditColumn("Comments", centered = True)
            ])
        for thread in threads:
            row = [
                variables.spriteMappings.get(thread['game'], 'MISC'),
                "[{title}]({url})".format(title = thread['title'], url = thread['url']),
                str(thread['comments'])
            ]
            table.addRow(row)
        return table
        
def main(reddit):
    """
    Builds the Match Thread Table to be inserted into the DDT
    Args:
        reddit: Authorized praw.Reddit object
    Returns:
        Match Thread Table String
    """
    print('Getting recent matchthreads.')
    threads = db.getMatchThreads()
    threads = validThreads(threads, reddit)
    threadInfo = []
    for thread in threads:
        threadInfo.append(getThreadInfo(thread))
    return generateTable(sorted(threadInfo, key = lambda k: k['time'], reverse = True))

