import datetime
import praw
import variables
import random
username = ''
password = ''
subreddit = ''
userAgent = ''
sayings = {}
months = {
    1:'January ',
    2:'Febuary ',
    3:'March ',
    4:'April ',
    5:'May ',
    6:'June ',
    7:'July ',
    8:'August ',
    9:'September ',
    10:'October ',
    11:'November ',
    12:'December '
}
def getSaying():
    global sayings
    print("Getting Phrases from Wiki...")
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password,disable_warning=True)
    wiki = r.get_subreddit(subreddit).get_wiki_page ('freetalk').content_md 
    sayings =  wiki.split('\n')
    return random.choice(sayings)
def postThread():
 
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password, disable_warning = True)
    body = getSaying().strip() + ", have a great Friday!"
    print("Posting Free Talk Friday...")
    now = datetime.datetime.now()
    ret = r.submit(subreddit, '[MISC] Free Talk Friday ('  + months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')' , text = body)
    ret.sticky()
    
def main(day):
    global username, password, subreddit, userAgent
    username = variables.username
    password = variables.password
    subreddit = variables.subreddit
    userAgent = variables.userAgent
    now = datetime.datetime.today()
    if now.weekday() == 4 and day != now.day and now.hour == variables.ftfhour:
        postThread()
        return now.day
    else:
        print('Not Time for Free Talk Friday.')
        return day

