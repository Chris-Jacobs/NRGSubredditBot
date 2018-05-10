import urllib.request, urllib.error, urllib.parse
import html.parser
import requests
import praw
import datetime
import variables
import json
import widgets
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
        return ("[" + stream + "](http://www.twitch.tv/" + twitchList[stream] + ")", viewers, game)
    else:
        return None
def getSchedule(sidebar):
    s = sidebar.index("- [")
    e = sidebar.index("> [](#sep)")
    schedule = sidebar[s:e - 3]
    return (schedule, e)
def getResults(sidebar):
    s = sidebar.index("### Results")
    s = sidebar.index(">", s)
    e = sidebar.index(">", s+1)
    return sidebar[s+1:e]
def duplicateSchedule(sidebar, schedule, e):
    schedule, e = getSchedule(sidebar)
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
    schedule, index = getSchedule(sidebar)
    results = getResults(sidebar)
    try:
        accessToken = widgets.getAccessToken()
        widgets.editTextWidget("widget_10mu02x5o8oyz", "Schedule", schedule, accessToken)
        widgets.editTextWidget("widget_10sc9m3wf9td9", "Results", results, accessToken)
    except Exception:
        print('Widgets Error')
        pass
    sidebar = duplicateSchedule(sidebar,schedule, index)
    sidebar_list = sidebar.split('***')
    sidebar = sidebar_list[0]
    now = datetime.datetime.now()
    sidebar += 'Stream|Viewers' + "\n"
    sidebar += '-|:-:'
    sidebar += '\n'
    streamTable += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EDT" + "\n" + "\n"
    streamTable += 'Stream|Viewers|Game' + "\n"
    streamTable += '-|:-:|---'
    streamTable += '\n'
    streams = []
    ## Twitch Streams
    for i in twitchList:
        tuple = twitchStream(i)
        if tuple is not None:
            streams.append(tuple)
    streams.sort(key=lambda x:x[1], reverse = True)
    sum = 0
    for stream in streams:
        sidebar += stream[0] + '|' + str(stream[1]) + '\n'
        streamTable += stream[0] + '|' + str(stream[1]) + '|' + stream[2] + '\n'
        sum += stream[1]
    if sum > 0:
        streamTable += "**Total:**|**" + str(sum) + "**"
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
