import praw
import datetime
import variables
username = ''
password = ''
subreddit = ''
userAgent = ''
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
username = ""
password = ""
subreddit = ""
userAgent = ""
def getDate(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)
    
def createThread(streamTable):
    print('Creating Daily Thread...')
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password, disable_warning = True)
    ddt = createBody(streamTable)
    now = datetime.datetime.now()
    ret = r.submit(subreddit, '[MISC] Daily Discussion Thread ('  + months[now.month] + str(now.day).zfill(2) + ', ' + str(now.year) + ')' , text = ddt)
    ret.set_suggested_sort(sort = 'new')
    ret.sticky(bottom = True)
    target = open('link.txt', 'w')
    target.truncate()
    target.write(ret.permalink)
    target.close()
    return ret
def createBody(streamTable):
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password, disable_warning = True)
    ddt = r.get_subreddit(subreddit).get_wiki_page ('ddt').content_md
    ddt_list = ddt.split('******')
    ddt = ddt_list[0]
    ddt += '\n'
    ddt += '\n'
    ddt += str(streamTable)
    ddt += '\n'
    ddt += "*****"
    ddt += ddt_list[2]
    return ddt

def editThread(streamTable, thread):
    print('Editing Daily Thread...')
    ddt = createBody(streamTable)
    ##print(streamTable)
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password, disable_warning = True)
    thread.edit(ddt)
    
    
    return thread
def getThread():
    target = open('link.txt', 'r')
    link = target.read()
    target.close()
    if link == '':
        return ''
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password, disable_warning = True)
    return r.get_submission(link)
def main(streamTable, thread):
    global username, password, subreddit, userAgent
    username = variables.username
    password = variables.password
    subreddit = variables.subreddit
    userAgent = variables.userAgent
    if thread == '':
        thread = getThread()
    if thread == '': ##nothing in file
        return createThread(streamTable)
    now = datetime.datetime.now()
    if now.hour == variables.ddthour:
        old = getDate(thread)
        if (old.day < now.day or old.month < now.month or old.year < now.year):
            return createThread(streamTable)
        else:
            return editThread(streamTable, thread) 
            

    else:
        return editThread(streamTable, thread)    