import urllib.request, urllib.error, urllib.parse
import html.parser
import praw
import datetime
import variables
username = ''
password = ''
subreddit = ''
userAgent = ''
twitchKey = ''
numberOnline = 0
twitchList = {}
mlgList = {}
YTList = {}
streamMap = {}
streamTable = ''
def specialTupleAdd(tuple1, tuple2):
    url1 = tuple1[0]
    url2 = tuple2[0]
    view1 = int(tuple1[1])
    view2 = int(tuple2[1])
    return (url1 + ' ' + url2, str(view1 + view2))

def twitchStream(stream):
    global numberOnline
    try:
        response = urllib.request.urlopen('https://api.twitch.tv/kraken/streams?channel=' + twitchList[stream] + '&client_id=' + twitchKey)
    except Exception:
        return None;
    html = response.read()
    html = str(html)

    if 'viewer' in html:
        index = html.index('viewer') +  9
        index2 = html.index('created_at') - 2
        index3 = html.index('video_height') - 2
        if index2 > index3:
            index2 = index3
        viewers = html[index:index2]
        return ("[](http://www.twitch.tv/" + twitchList[stream] + ")", viewers)
    else:
        return None
def youtubeStream(stream):
    global numberOnline
    try:
        response = urllib.request.urlopen('https://youtube.com/user/' + YTList[stream])
    except Exception:
        return None;
    html1 = response.read()
    html1 = str(html1)
    if 'Live now' in html1:
        index = html1.index("yt-lockup-meta-info") + 27
        index2 = html1.index('watching') - 1
        viewers = html1[index:index2]
        viewers = viewers.replace(",", "")
        return ("[](http://gaming.youtube.com/user/" + YTList[stream] + ')', viewers)
    else:
        return None
def mlgStream(stream):
    try:
        response = urllib.request.urlopen('http://streamapi.majorleaguegaming.com/service/streams/all')
    except Exception:
        return None;
    html1 = response.read()
    html1 = str(html1)
    index = html1.index(mlgList[stream]) + 16
    index2 = html1.index('channel_id', index) - 2
    status = html1[index:index2]
    if status == '1':
        j = html1.index('}', index2)
        try:
            k = html1.index('viewers', index2, j) + 9
            viewers = html1[k:j]
        except ValueError:
            viewers = 'N/A'
        return ("[](http://www.mlg.tv/" + stream + ')', viewers)
    else:
        return None
def create_sidebar():
    global streamTable
    global twitchList
    global numberOnline
    print('Creating Sidebar...')
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password,disable_warning=True)
    sidebar = r.get_subreddit(subreddit).get_wiki_page ('edit_sidebar').content_md
    sidebar_list = sidebar.split('***')
    sidebar = sidebar_list[0]
    now = datetime.datetime.now()
    sidebar += 'Name|Stream|Viewers' + "\n"
    sidebar += ':-:|:-:|:-:'
    sidebar += '\n'
    streamTable += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EST" + "\n" + "\n"
    streamTable += 'Name|Stream|Viewers' + "\n"
    streamTable += ':-:|:-:|:-:'
    streamTable += '\n'
    ## Twitch Streams
    for i in twitchList:
        s = twitchStream(i)
        if s is not None:
            previous = streamMap[i]
            if previous is None:
                streamMap[i] = s
            else:
                streamMap[i] = specialTupleAdd(previous, s)
    response = ""
    ## MLG Streams
    for i in mlgList:
        s = mlgStream(i)
        if s is not None:
            previous = streamMap[i]
            if previous is None:
                streamMap[i] = s
            else:
                streamMap[i] = specialTupleAdd(previous, s)
    ## YT Streams
    for i in YTList:
        s = youtubeStream(i)
        if s is not None:
            previous = streamMap[i]
            if previous is None:
                streamMap[i] = s
            else:
                streamMap[i] = specialTupleAdd(previous, s)
    ##Create Stream List
    for stream in streamMap:
        tuple = streamMap[stream]
        if tuple is not None:
            sidebar += stream + '|' + tuple[0] + '|' + tuple[1] + '\n'
            streamTable += stream + '|' + tuple[0] + '|' + tuple[1] + '\n'
    sidebar += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EDT" + "\n" + "\n"
    sidebar += sidebar_list[2]
    sidebar = html.unescape(sidebar)
    return sidebar
    
def generate_stream_lists():
    global twitchList
    global mlgList
    global YTList
    global streamMap
    print("Getting Streams from Wiki...")
    r = praw.Reddit(user_agent=variables.userAgent)
    r.login(username,password,disable_warning=True)
    streams = r.get_subreddit(subreddit).get_wiki_page ('streams').content_md
    streamers = streams.split('\n')
    for i in streamers:
        pair = i.split(',')
        try:
            pair[1] = pair[1].strip('\r')
            parts = pair[0].split(':')
            temp = parts[0]
            streamMap[parts[1]] = None
            if temp == "YT":
                YTList[parts[1]] = pair[1]
            elif temp == "TW":
                twitchList[parts[1]] = pair[1]
            elif temp == "ML":
                mlgList[parts[1]] = pair[1]

        except IndexError:
            pass
        
def update_reddit(sidebar):
    print('Updating Sidebar...')
    r = praw.Reddit(user_agent=userAgent)
    r.login(username,password, disable_warning = True)
    settings = r.get_subreddit(subreddit).get_settings()
    settings['description'] = sidebar
    settings = r.get_subreddit(subreddit).update_settings(description=settings['description'])
   
    
def log(logmessage):
    print('Updating Log...')
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password,disable_warning=True)
    r.get_subreddit(subreddit).edit_wiki_page ('log', logmessage)

def main():
    global streamTable, numberOnline, username, password, subreddit, userAgent, twitchKey, streamMap
    username = variables.username
    password = variables.password
    subreddit = variables.subreddit
    userAgent = variables.userAgent
    twitchKey = variables.twitchKey 
    streamTable = ''
    numberOnline = 0
    generate_stream_lists()
    sidebar = create_sidebar()
    log(datetime.datetime.now())
    try:
        update_reddit(sidebar)
    except praw.errors.InvalidCaptcha:
        pass
    return streamTable
