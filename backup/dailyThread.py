import praw
import datetime
import variables

username = ""
password = ""
subreddit = ""
userAgent = ""
def getDate(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def createThread(streamTable, yt):
    print('Creating Daily Thread...')
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    ddt = createBody(streamTable, yt)
    now = datetime.datetime.now()
    ret = r.subreddit(variables.subreddit).submit(title = '[MISC] Daily Discussion Thread ('  + variables.months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')' , selftext = ddt, send_replies=False)
    ret.comment_sort = "new"
    ret.mod.sticky(state=True, bottom = True)
    target = open('link.txt', 'w')
    target.truncate()
    target.write(ret.url)
    target.close()
    return ret
def createBody(streamTable, yt):
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    ddt = r.subreddit(variables.subreddit).wiki['ddt'].content_md
    ddt_list = ddt.split('******')
    ddt = ddt_list[0]
    ddt += '\n'
    ddt += '\n'
    ddt += str(streamTable)
    ddt += '\n'
    ddt += "*****"
    if yt is not None:
        ddt += '\n'
        ddt += str(yt)
        ddt += '\n'
        ddt += "*****"
    ddt += ddt_list[2]
    return ddt

def editThread(streamTable, yt,  thread):
    print('Editing Daily Thread...')
    ddt = createBody(streamTable, yt)
    ##print(streamTable)
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    thread.edit(ddt)
    
    
    return thread
def getThread():
    target = open('link.txt', 'a+')
    target.seek(0)
    link = target.read()
    print(link)
    target.close()
    if link == '':
        return ''
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    return r.submission(url = link)
def main(streamTable, yt, thread):
    if thread == '':
        thread = getThread()
    if thread == '': ##nothing in file
        return createThread(streamTable, yt)
    now = datetime.datetime.now()
    if now.hour == variables.ddthour:
        old = getDate(thread)
        if (old.day < now.day or old.month < now.month or old.year < now.year):
            thread.mod.sticky(False)
            return createThread(streamTable, yt)
        else:
            return editThread(streamTable, yt,  thread)
            

    else:
        return editThread(streamTable, yt,  thread)