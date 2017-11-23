import praw
import variables
from datetime import datetime
import time
r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
subreddit = r.subreddit(variables.subreddit)
ow = 'HoustonOutlaws'
ow = r.subreddit(ow)
def isRemoved(submission):
    s = r.submission(url = submission)
    #print(s.title)
    if s.banned_by is not None:
        return True
    else:
        return False
def crosspost(submission):
    try:
        if submission.title.startswith('[OW]'):
            newTitle = submission.title.replace('[OW]', '').lstrip()
            thread = ow.submit(newTitle, url = submission.url, resubmit = False)
            thread.mod.lock()
            return True
        return False
    except Exception:
        return False
#t = time.time()
#print(t)
#for submission in subreddit.new(limit=10):
    #print(submission.title)
    #print(submission.created_utc)
#for submission in subreddit.submissions(start = 1509417110.0):
#    print(submission.title)
while True:
    print('Getting Time')
    with open('time.txt', 'r') as f:
        t = float(f.read())
    print('Getting /r/OpTicGaming Submissions')
    for submission in subreddit.submissions(start = t):
        crosspost(submission)
    t = time.time()
    print('Saving Time')
    with open('time.txt', 'w') as f:
        f.write(str(t))
    print('Checking for Removed Posts')
    for submission in ow.new(limit=10):
        if isRemoved(submission.url):
            submission.mod.remove()
    print('Sleeping...')
    time.sleep(5 * 60)
