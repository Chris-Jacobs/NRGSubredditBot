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
streamList = {

 }
streamTable = ''
mlgList = {
    'Scump':'mlg22'
 }
 
YTList = {
    'J':'OpTicJ',
    'H3CZ':'h3czplay'
 }
    
def stream_online(stream):
    global numberOnline
    response = ""
    response = urllib.request.urlopen('https://api.twitch.tv/kraken/streams?channel=' + streamList[stream] + '&client_id=' + twitchKey)
    html = response.read()
    html = str(html)

    if 'viewer' in html:
        index = html.index('viewer') +  9
        index2 = html.index('created_at') - 2
        index3 = html.index('video_height') - 2
        if index2 > index3:
            index2 = index3
        numberOnline += 1
        return stream + "|[](http://www.twitch.tv/" + streamList[stream] +")|" + html[index:index2] + "\n"
    else:
        return ''
     
def create_sidebar():
    global streamTable
    global streamList
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
    streamTable += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EDT" + "\n" + "\n"
    streamTable += 'Name|Stream|Viewers' + "\n"
    streamTable += ':-:|:-:|:-:'
    streamTable += '\n'
    ## Twitch Streams
    for i in streamList:
        s = stream_online(i)
        sidebar += s
        streamTable += s
    response = ""
    ## MLG Streams
    try:
        response = urllib.request.urlopen('http://streamapi.majorleaguegaming.com/service/streams/all')
        html1 = response.read()
        html1 = str(html1)
        
        for i in mlgList:
            try:
                index = html1.index(mlgList[i]) + 16
                index2 = html1.index('channel_id' , index) - 2
                status = html1[index:index2]
                if status == '1':
                    j = html1.index('}', index2)
                    try:
                        k = html1.index('viewers', index2,j) + 9
                        viewers = html1[k:j]
                    except ValueError:
                        viewers = 'N/A'
                    sidebar += i +'|[](http://www.mlg.tv/' + i + ')|' + viewers + '\n'
                    streamTable += i +'|[](http://www.mlg.tv/' + i + ')|' + viewers + '\n'
                    numberOnline += 1
            except ValueError:
                pass
    except Exception:
        print("Couldn't Retrieve MLG Streams")
    ## YT Streams
    for i in YTList:
        try:
            response = urllib.request.urlopen('https://youtube.com/user/' + YTList[i])  
            html1 = response.read()
            html1 = str(html1)
            if 'Live now' in html1:
                index = html1.index("yt-lockup-meta-info") + 27
                index2 = html1.index('watching') - 1
                viewers = html1[index:index2]
                sidebar += i + '|[](http://gaming.youtube.com/user/' + YTList[i] + ')|' + viewers + '\n'
                streamTable += i + '|[](http://gaming.youtube.com/user/' + YTList[i] + ')|' + viewers + '\n'
                numberOnline += 1 
        except: print(i + "'s channel had an error.")
    sidebar += "Streams Updated at: " + str(now.month).zfill(2) + "/" + str(now.day).zfill(2) + " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + " EDT" + "\n" + "\n"
    
    sidebar += sidebar_list[2]
    sidebar = html.unescape(sidebar)
    return sidebar
    
def generate_stream_list():
    global streamList
    temp = {
    }
    print("Getting Streams from Wiki...")
    r = praw.Reddit(user_agent='self.userAgent')
    r.login(username,password,disable_warning=True)
    streams = r.get_subreddit(subreddit).get_wiki_page ('streams').content_md
    streamers =  streams.split('\n')
    for i in streamers:
        pair = i.split(',')
        try:
            pair[1] = pair[1].strip('\r')
            temp[pair[0]] = pair[1]
        except IndexError:
            pass
    streamList = temp
        
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
    global streamTable, numberOnline, username, password, subreddit, userAgent, twitchKey
    username = variables.username
    password = variables.password
    subreddit = variables.subreddit
    userAgent = variables.userAgent
    twitchKey = variables.twitchKey 
    streamTable = ''
    numberOnline = 0
    generate_stream_list()
    sidebar = create_sidebar()
    print(str(numberOnline) + ' streams online.')
    log(datetime.datetime.now())   
    try:
        update_reddit(sidebar)
    except praw.errors.InvalidCaptcha:
        pass
    return streamTable
