import praw
import datetime
import variables
import stats
username = ""
password = ""
subreddit = ""
userAgent = ""
def getDate(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)

def getFileText():
    target = open('link.txt', 'a+')
    target.seek(0)
    link = target.read()
    print(link)
    target.close()
    return link
def createThread(streamTable, yt, matches):
    print('Creating Daily Thread...')
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    ddt = createBody(streamTable, yt, matches)
    now = datetime.datetime.now()
    ret = r.subreddit(variables.subreddit).submit(title = '[MISC] Daily Discussion and Match Thread Hub ('  + variables.months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')' , selftext = ddt, send_replies=False)
    ret.comment_sort = "new"
    ret.mod.sticky(state=True, bottom = True)
    #link = cloud.main()
    try:
        stat = stats.main()
    except Exception:
        stat = None
    if stat is not None:
        statComment = ret.reply(stat)
        if "Crim_Bot" in stat:
            statComment.reply("Oh shit that's me! ^(P.S. You guys need to stop)")
    target = open('link.txt', 'w')
    target.truncate()
    target.write(ret.url)
    target.close()
    return ret
def createBody(streamTable, yt, matches):
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
    ddt += matches
    ddt += '***** \n \n'
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

def editThread(streamTable, yt,  thread, matches):
    print('Editing Daily Thread...')
    ddt = createBody(streamTable, yt, matches)
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    thread.edit(ddt)
    
    
    return thread

def getThread():
    link = getFileText()
    if link == '':
        return ''
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    return r.submission(url = link)
def main(streamTable, yt, thread, matches):
    if thread == '':
        thread = getThread()
    if thread == '': ##nothing in file
        return createThread(streamTable, yt,matches)
    now = datetime.datetime.now()
    if now.hour == variables.ddthour:
        old = getDate(thread)
        if (old.day < now.day or old.month < now.month or old.year < now.year):
            thread.mod.sticky(False)
            return createThread(streamTable, yt, matches)
        else:
            return editThread(streamTable, yt,  thread, matches)
            

    else:
        return editThread(streamTable, yt,  thread, matches)
