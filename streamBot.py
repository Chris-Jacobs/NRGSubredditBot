import urllib.request, urllib.error, urllib.parse
import html.parser
import requests
import praw
import datetime
import variables
import json
numberOnline = 0
twitchList = {}
mlgList = {}
YTList = {}
streamMap = {}
streamTable = ''

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
        j = json.loads(html)
        game = j['streams'][0]['game']
        viewers = j['streams'][0]['viewers']
        return ("[](http://www.twitch.tv/" + twitchList[stream] + ")", viewers, game)
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
    sidebar += ':-:|:-:|:-:'
    sidebar += '\n'
    streamTable += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EDT" + "\n" + "\n"
    streamTable += 'Name|Stream|Viewers|Game' + "\n"
    streamTable += ':-:|:-:|:-:|---'
    streamTable += '\n'
    ## Twitch Streams
    for i in twitchList:
        tuple = twitchStream(i)
        if tuple is not None:
            sidebar += i + '|' + tuple[0] + '|' + str(tuple[1]) + '\n'
            streamTable += i + '|' + tuple[0] + '|' + str(tuple[1]) + '|' + tuple[2] + '\n'
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
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    page = r.subreddit(variables.subreddit).wiki['streams']
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
    ('Updating Sidebar...')
    r = praw.Reddit(client_id=variables.client_id,
                     client_secret=variables.client_secret,
                     user_agent=variables.user_agent,
                     username=variables.username,
                     password=variables.password)
    r.subreddit(variables.subreddit).mod.update(description = sidebar, spoilers_enabled = True)


def main():
    global streamTable, numberOnline, streamMap
    streamTable = ''
    numberOnline = 0
    generate_stream_lists()
    sidebar = create_sidebar()
    update_reddit(sidebar)
    return streamTable
