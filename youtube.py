import untangle
import datetime
import praw
import variables
import urllib.request, urllib.error, urllib.parse
import json
nameToYT = {
}
ytToID = {
}
timeMap = {
}
videoList = []
def parseTime(time):
    parts = time.split('T')
    date = parts[0].split("-")
    times = parts[1].split(":")
    times[2] = times[2].split('.')[0]
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]),int(times[0]), int(times[1]), int(times[2]))

def processUser(user):
    global videoList
    ret = ""
    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails%2Cstatus&maxResults=10&key=" + variables.ytKey + "&playlistId=" + ytToID[user]
    r = urllib.request.urlopen(url)
    data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
    lastDay = True;
    counter = 0;
    while lastDay is True:
        entry = data['items'][counter]['snippet']
        counter += 1
        time = parseTime(entry['publishedAt'])
        yesterday = datetime.datetime.utcnow() - datetime.timedelta(days = 1)
        if time < yesterday:
            lastDay = False
        if lastDay is True:
            title = entry['title']
            title = title.replace("|", "-")
            link = "https://www.youtube.com/watch?v=" + entry['resourceId']['videoId']
            videoList.append((nameToYT[user] + "|[" + title + "](" + link + ")|" + "\n", time))
        #print (time)
        #print (yesterday)
        #print(entry.title.cdata)
        #print(entry.link['href'])
        #print(entry.media_group.media_community.media_statistics['views'])
        #print(entry.author.name.cdata)
        #print(entry.published.cdata)
    return ret

def processVideoList():
    global videoList
    videoList.sort(key = lambda x : x[1], reverse = True)
    ret = ''
    if len(videoList) > 15:
        videoList = videoList[:15]
    for video in videoList:
        ret += video[0]
    return ret

def main():
    global videoList
    videoList = []
    r = praw.Reddit(client_id=variables.client_id,
                    client_secret=variables.client_secret,
                    user_agent=variables.user_agent,
                    username=variables.username,
                    password=variables.password)
    ret = ""
    ret += "The last 15 YouTube videos from OpTic members in the past 24 hours."+ "\n" + "\n"
    ret += 'Name|Video' + "\n"
    ret += ':-:|-|' + "\n"
    channels = r.subreddit(variables.subreddit).wiki['yt'].content_md
    channels = channels.split('\n')
    print ('Getting YouTube Channels')
    for channel in channels:
        vars = channel.split(':')
        nameToYT[vars[1]] = vars[0]
        ytToID[vars[1]] = vars[2]
        processUser(vars[1])
    print('Getting List of Videos')
    ret += processVideoList()
    return ret


#url = "https://www.googleapis.com/youtube/v3/activities?part=snippet,contentDetails&key=AIzaSyBNwzKg3d_nFRKQhGy-BDiBLCea6lmpwN8&channelId=UCVhkzoReyB25jpFEeXjh3kQ"
#r = urllib.request.urlopen(url)
#html1 = response.read()
#response.close()
#html1 = str(html1)
#data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
#print(html1)
#print(data["items"][0]["snippet"]["type"])

#id= 'UCK8sQmJBp8GCxrOtXWBpyEA'
#url = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key=AIzaSyBNwzKg3d_nFRKQhGy-BDiBLCea6lmpwN8&id=" + id
#r = urllib.request.urlopen(url)
#data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
#uploadId = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#print(uploadId)
#uploadId = "UUVhkzoReyB25jpFEeXjh3kQ"
#url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails%2Cstatus&key=AIzaSyBNwzKg3d_nFRKQhGy-BDiBLCea6lmpwN8&&playlistId=" + uploadId
#r = urllib.request.urlopen(url)
#data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
#print(data['items'][0]['snippet']['resourceId']['videoId'])

#r = praw.Reddit(client_id=variables.client_id,
#                client_secret=variables.client_secret,
#                user_agent=variables.user_agent,
#                username=variables.username,
#                password=variables.password)
#channels = r.subreddit(variables.subreddit).wiki['yt'].content_md
#channels = channels.split('\n')
#for channel in channels:
    #vars = channel.split(':')
    #id = vars[2]
    #url = "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&key=" + variables.ytKey + "&id=" + id
   # r = urllib.request.urlopen(url)
  #  data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))
 #   uploadId = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#    print(vars[0]+ ":" + vars[1] + ":" + uploadId)