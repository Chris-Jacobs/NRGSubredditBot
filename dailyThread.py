import praw
import datetime
import stats
import variables
import db
def getDate(submission):
    time = submission.created
    return datetime.datetime.fromtimestamp(time)
def statsComment(ddt, reddit):
    try:
        statComment = stats.main(reddit)
        ddt.reply(statComment)
    except Exception:
        pass
def createBody(streamTable, matchTable, reddit):
    wikiDdt = reddit.subreddit('OpTicGaming').wiki['ddt'].content_md
    ddtSections = wikiDdt.split("******")
    ddtBody = ddtSections[0]
    ddtBody += "\n\n"
    ddtBody += matchTable
    ddtBody += "*****"
    ddtBody += "\n\n"
    ddtBody += streamTable
    ddtBody += "\n"
    ddtBody += "****"
    ddtBody += ddtSections[2]
    return ddtBody
def createThread(streamTable, matchTable, reddit):
    ddtBody = createBody(streamTable, matchTable, reddit)
    now = datetime.datetime.now()
    dateString = now.strftime("%B %d, %Y")
    title = '[MISC] Daily Discussion and Match Thread Hub ({date})'.format(date =  dateString)
    ddt = reddit.subreddit(variables.subreddit).submit(title = title , selftext = ddtBody, send_replies=False)
    ddt.comment_sort = "new"
    ddt.mod.sticky(state=True, bottom = True)
    statsComment(ddt, reddit)
    return ddt.id

def editThread(thread, streamTable, matchTable, reddit):
    ddtBody = createBody(streamTable, matchTable, reddit)
    thread.edit(ddtBody)
    return thread.id
def getThread(id, reddit):
    if id is None and variables.subreddit == "OpTicGaming":
        id = db.lastDaily()
    if id is None:
        for submission in reddit.subreddit(variables.subreddit).new():
            if "Daily Discussion" in submission.title and str(submission.author) == "Crim_Bot":
                return submission.id
    return id
def main(thread, streamTable, matches, reddit):
    print('Getting recent DDT.')
    thread = getThread(thread, reddit)
    if thread is None:
        print('Thread not found. Creating new one.')
        thread = createThread(streamTable, matches, reddit)
    thread = reddit.submission(id = thread)
    old = getDate(thread)
    now = datetime.datetime.now()
    if now.hour == variables.ddthour and (old.day < now.day or old.month < now.month or old.year < now.year):
        thread.mod.sticky(False)
        print('Time for new DDT. Creating new one.')
        return createThread(streamTable, matches, reddit)
    else:
        print('Editing DDT.')
        return editThread(thread, streamTable, matches, reddit)