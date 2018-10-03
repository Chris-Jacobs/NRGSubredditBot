import praw
import variables
from datetime import datetime, timedelta
import cloud
import mysql.connector
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from imgurpython import ImgurClient
import re

reddit = praw.Reddit(client_id=variables.client_id,
        client_secret=variables.client_secret,
        user_agent=variables.user_agent,
        username=variables.username,
        password=variables.password)
db = True
conn = mysql.connector.connect(host = variables.localIP, user = variables.dbUser, password=variables.dbPassword,database = 'optic_reddit')
conn.set_charset_collation('utf8mb4', 'utf8mb4_general_ci')
cur = conn.cursor()


def upload(path):
    try:
        client = ImgurClient(variables.imgurID, variables.imgurSecret)
        upload = client.upload_from_path(path, anon=True)
        return upload['link']
    except Exception:
        return None
def hour(hours):
    for h in hours:
        t = datetime.fromtimestamp(h[0])
        sql = ''' INSERT INTO traffic_hour (hour, uniques, pageviews) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews)'''
        data = (t, h[1], h[2])
        if t.minute == 0:
            cur.execute(sql, data)
    conn.commit()
def day(days):
    for d in days:
        t = datetime.utcfromtimestamp(d[0])
        sql = ''' INSERT INTO traffic_day (day, uniques, pageviews, subscriptions) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews), subscriptions = VALUES(subscriptions)'''
        data = (t, d[1], d[2], d[3])
        cur.execute(sql, data)
    conn.commit()
def month(months):
    for m in months:
        t = datetime.utcfromtimestamp(m[0])
        sql = ''' INSERT INTO traffic_month (month, uniques, pageviews) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews)'''
        data = (t ,m[1], m[2])
        cur.execute(sql, data)
    conn.commit()    
def traffic():
    try:
        print('Getting Traffic...')
        t = reddit.subreddit('OpTicGaming').traffic()
        try:
            print('Hour...')
            hour(t['hour'])
        except Exception as e:
            print('Error with Hourly Traffic')
            print(e)
        try:
            print('Day...')
            day(t['day'])
        except Exception as e:
            print('Error with Daily Traffic')
            print(e)
        try:
            print('Month...')
            month(t['month'])
        except Exception as e:
            print('Error with Monthly Traffic')
            print(e)
    except Exception:
        print('Error with traffic')

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
        now = datetime.now()
        n = now.replace(hour = 0, minute = 0, second = 0, microsecond= 0)
        lastWeek = n - timedelta(days = days)
        sql = 'SELECT day(utc) as day, count(*) from comments where date >= "{date}" and date < "{current}" group by day'''.format(date = lastWeek.strftime("%Y-%m-%d %H:%M"), current = n.strftime("%Y-%m-%d %H:%M"))
        cur.execute(sql)
        commentData = cur.fetchall()
        sql = 'SELECT day, day(day), uniques, pageviews from traffic_day where day >= "{date}" and day < "{current}"'.format(date = lastWeek.strftime("%Y-%m-%d %H:%M"), current = n.strftime("%Y-%m-%d %H:%M"))
        cur.execute(sql)
        trafficData = cur.fetchall()
        return upload(makeGraph(commentData, trafficData, "Day", 'week.png'))
    except:
        return None

def hourlyHistory():
    now = datetime.now()
    now = now.replace(minute = 0, second = 0, microsecond= 0)
    last =  now- timedelta(days = 1)
    try:
        sql = 'SELECT hour(UTC) as hour, count(*) from comments where date >= "{date}" and date < "{current}" group by hour'''.format(date = last.strftime("%Y-%m-%d %H:%M"), current = now.strftime("%Y-%m-%d %H:%M"))
        cur.execute(sql)
        commentData = cur.fetchall()
        sql = 'SELECT hour,hour(hour), uniques, pageviews from traffic_hour where hour >= "{date}" and hour < "{current}"'.format(date = last.strftime("%Y-%m-%d %H:%M"), current = now.strftime("%Y-%m-%d %H:%M"))
        cur.execute(sql)
        trafficData = cur.fetchall()
        return upload(makeGraph(commentData, trafficData, "Hour (EDT)", 'day.png', True, 24))
    except:
        return None

def oldDaily():
    regex = re.compile("(Stream.*Discussion)|(Daily Discussion)")
    now = datetime.now()
    try:
        sql = 'SELECT year(date), id, title, author from posts where month(date) = {month} and day(date) = {day} and year(date) < {year} order by date asc'.format(month = now.month, day = now.day, year = now.year)
        cur.execute(sql)
        threads = cur.fetchall()
        dailys = []
        for thread in threads:
            print(thread)
            title = thread[2]
            result = regex.search(title)
            if result is not None:
                dailys.append(thread)
        s = "Old Daily Discussion Threads: "
        for daily in dailys:
            s += "[{year}]({link}) ".format(year = daily[0], link = "https://redd.it/" + daily[1])
        return s
    except:
        return ""
    
def main():
    traffic()
    now = datetime.now()
    now = now.replace(minute = 0, second = 0, microsecond= 0)
    last =  now- timedelta(days = 1)
    highestComment = None
    score = 0
    counter = 0
    txt = ""
    sql = 'SELECT id from comments where date >= "{date}"'.format(date = last.strftime("%Y-%m-%d %H:%M"))
    cur.execute(sql)
    temp = cur.fetchall()
    comments = []
    for c in temp:
        comments.append("t1_" + c[0])
    counter = len(comments)
    s = reddit.info(fullnames=comments)
    for comment in s:
        txt += comment.body + " "
        cScore = comment.score
        if cScore > score:
            highestComment = comment
            score = cScore

    link = 'https://www.reddit.com' + highestComment.permalink
    s= "**Summary of Yesterday** \n\n"
    s += str(counter) +" comments \n\n"
    s += "[Highest Scoring Comment](" + link + ") from /u/" + str(highestComment.author) + "\n\n"
    wc = cloud.wordcloud(txt = txt)
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

