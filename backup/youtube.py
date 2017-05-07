import untangle
import datetime
import praw
import variables
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
    index = parts[1].index("+")
    clock = parts[1][0:index]
    times = clock.split(":")
    return datetime.datetime(int(date[0]), int(date[1]), int(date[2]),int(times[0]), int(times[1]), int(times[2]))

def processUser(user):
    global videoList
    ret = ""
    url = "https://www.youtube.com/feeds/videos.xml?channel_id=" + ytToID[user]
    videos = untangle.parse(url)
    entries = videos.feed.entry
    if type(entries) is not list:
        entry = entries
        entries = []
        entries.append(entry)
    lastDay = True;
    counter = 0;
    while lastDay is True:
        entry = entries[counter]
        counter += 1
        time = parseTime(entry.published.cdata)
        yesterday = datetime.datetime.utcnow() - datetime.timedelta(days = 1)
        if time < yesterday:
            lastDay = False
        if lastDay is True:
            title = entry.title.cdata
            title = title.replace("|", "-")
            videoList.append((nameToYT[user] + "|[" + title + "](" + entry.link['href'] + ")|" + entry.media_group.media_community.media_statistics['views'] + "\n", time))
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
    ret += "All YouTube videos from OpTic members in the past 24 hours."+ "\n" + "\n"
    ret += 'Name|Video|Views' + "\n"
    ret += ':-:|-|:-:' + "\n"
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




