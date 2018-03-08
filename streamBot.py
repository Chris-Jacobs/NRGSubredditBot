import urllib.request, urllib.error, urllib.parse
import html.parser
import requests
import praw
import datetime
import variables
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
        headers = {'Accept' : 'application/vnd.twitchtv.v3+json', 'Client-ID' : str(variables.twitchKey)}
        response = requests.get('https://api.twitch.tv/kraken/streams?channel=' + twitchList[stream], headers = headers)
        #response = urllib.request.urlopen('https://api.twitch.tv/kraken/streams?channel=' + twitchList[stream] + '&client_id=' + twitchKey)
    except Exception:
        return None

    html = response.text
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
        return None
    html1 = response.read()
    response.close()
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
    response.close()
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
def duplicateSchedule(sidebar):
    s = sidebar.index("- [")
    e = sidebar.index("> [](#sep)")
    schedule = sidebar[s:e - 3]
    sidebar = sidebar[:e + 15] + schedule + sidebar[e+15:]
    return sidebar
def create_sidebar():
    global streamTable
    global twitchList
    global numberOnline
    print('Creating Sidebar...')
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    sidebar = r.subreddit(variables.subreddit).wiki['edit_sidebar'].content_md
    sidebar = duplicateSchedule(sidebar)
    sidebar_list = sidebar.split('***')
    sidebar = sidebar_list[0]
    now = datetime.datetime.now()
    sidebar += 'Name|Stream|Viewers' + "\n"
    sidebar += ':-:|--:|--:'
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
    sidebar += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EST" + "\n" + "\n"
    sidebar += sidebar_list[2]
    sidebar = html.unescape(sidebar)
    return sidebar
    
def generate_stream_lists():
    global twitchList
    global mlgList
    global YTList
    global streamMap
    print("Getting Streams from Wiki...")
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    page = r.subreddit(variables.subreddit).wiki['streams']
    print(page.content_md)
    streams = r.subreddit(variables.subreddit).wiki['streams'].content_md
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
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    r.subreddit(variables.subreddit).mod.update(description = sidebar, spoilers_enabled = True)

    
def log(logmessage):
    print('Updating Log...')
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    r.subreddit(variables.subreddit).wiki['log'].edit(logmessage)

def main():
    global streamTable, numberOnline, streamMap
    streamTable = ''
    numberOnline = 0
    generate_stream_lists()
    sidebar = create_sidebar()
    update_reddit(sidebar)
    return streamTable
