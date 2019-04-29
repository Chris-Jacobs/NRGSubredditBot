import praw
import variables
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from imgurpython import ImgurClient
import db
from wordcloud import ImageColorGenerator,STOPWORDS, WordCloud
import numpy as np
from PIL import Image
import traffic
def upload(path):
    try:
        client = ImgurClient(variables.keys['ImgurClientID'], variables.keys['ImgurSecret'])
        upload = client.upload_from_path(path, anon=True)
        return upload['link']
    except Exception:
        return None

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
def makeGraph(commentData, trafficData, xLabel, fileName, setLength = False, length = 24):
    commentMap = {}
    if setLength:
        for x in range(length):
            commentMap[x] = 0
    for cd in commentData:
        t = cd[0]
        num = cd[1]
        commentMap[t] = num
    data = []
    for td in trafficData:
        d = (td[0].timestamp(), commentMap[td[1]], td[2], td[3], td[1])
        data.append(d)
    data = np.asarray(data)
    fig, ax1 = plt.subplots(figsize = (18,9))
    color = 'tab:red'
    ax1.set_xlabel(xLabel)
    ax1.set_ylabel('# of Comments', color = color)
    x = data[:,0]
    y = data[:,1]
    xTick = data[:,4]
    ax1.plot(x,y, color = color, markersize = 12, marker = ".")
    ax1.tick_params(axis = 'y', labelcolor = color)
    ax1.set_xticks(x)
    ax1.set_xticklabels(xTick)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Pageviews', color = color)
    y = data[:,3]
    ax2.plot(x, y, color = color, markersize = 12, marker = ".")
    ax2.tick_params(axis = 'y', labelcolor = color)

    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.05))
    make_patch_spines_invisible(ax3)
    ax3.spines["right"].set_visible(True)
    color = 'tab:green'
    ax3.set_ylabel('Uniques', color = color)
    y = data[:,2]
    ax3.plot(x, y, color = color, markersize = 12, marker = ".")
    ax3.tick_params(axis = 'y', labelcolor = color)
    fig.tight_layout()
    plt.savefig(fileName)
    return fileName
def dailyHistory(days = 8):
    try:
        commentData, trafficData = db.dailyHistory(days)
        return upload(makeGraph(commentData, trafficData, "Day", 'week.png'))
    except:
        return None

def hourlyHistory():
    try:
        commentData, trafficData = db.hourlyHistory()
        return upload(makeGraph(commentData, trafficData, "Hour (EDT)", 'day.png', True, 24))
    except:
        return None

def oldDaily():
    try:
        dailys = db.oldDailys()
        s = "Old Daily Discussion Threads: "
        for daily in dailys:
            s += "[{year}]({link}) ".format(year = daily[0], link = "https://redd.it/" + daily[1])
        return s
    except:
        return ""

def wordcloud(txt):
    output = 'cloud.jpg'
    try:
        imgmask = np.array(Image.open('mask.png'))
        colors = ImageColorGenerator(np.array(Image.open('whitemask.png')))
        stopwords = STOPWORDS
        stopwords.add('http')
        stopwords.add('https')
        wordcloud = WordCloud(background_color='black',mask=imgmask, color_func=colors, stopwords=stopwords).generate(txt)
        image = wordcloud.to_image()
        image.save(output)
        return upload(output)
    except Exception:
        return None

def processComments(comments, reddit):
    txt = ""
    score = 0
    highestComment = None
    s = reddit.info(fullnames = comments)
    for comment in s:
        txt += comment.body + " "
        cScore = comment.score
        if cScore > score:
            highestComment = comment
            score = cScore
    return highestComment, txt

def main(reddit):
    traffic.main(reddit)
    highestComment = None
    txt = ""
    comments = db.getComments()
    counter = len(comments)
    highestComment, txt = processComments(comments, reddit)

    link = 'https://www.reddit.com' + highestComment.permalink
    s= "**Summary of Yesterday** \n\n"
    s += str(counter) +" comments \n\n"
    s += "[Highest Scoring Comment](" + link + ") from /u/" + str(highestComment.author)
    if highestComment.author == "Crim_Bot":
        s+= " (what a handsome ~~guy~~ bot)"
    s += "\n\n"
    wc = wordcloud(txt = txt)
    if wc is not None:
        s += "[Yesterday's Word Cloud](" + wc + ")" + "\n\n"
    day = hourlyHistory()
    if day is not None:
        s += "[Traffic per hour for Last 24 Hours](" + day + ")" + "\n\n"
    week = dailyHistory()
    if week is not None:
        s += "[Traffic per day for Last 7 Days](" + week + ")" + "\n\n"
    s += oldDaily() + "\n\n"
    return s

