import variables
import mysql.connector
from datetime import datetime, timedelta
import re
conn = mysql.connector.connect(host = variables.keys['ExternalIP'], user = variables.keys['DatabaseUser'], password = variables.keys['DatabasePassword'], database ='optic_reddit')
conn.set_charset_collation('utf8mb4', 'utf8mb4_general_ci')
cur = conn.cursor()

def hourTraffic(hours):
    for h in hours:
        t = datetime.fromtimestamp(h[0])
        sql = ''' INSERT INTO traffic_hour (hour, uniques, pageviews) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews)'''
        data = (t, h[1], h[2])
        if t.minute == 0:
            cur.execute(sql, data)
    conn.commit()
def dayTraffic(days):
    for d in days:
        t = datetime.utcfromtimestamp(d[0])
        sql = ''' INSERT INTO traffic_day (day, uniques, pageviews, subscriptions) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews), subscriptions = VALUES(subscriptions)'''
        data = (t, d[1], d[2], d[3])
        cur.execute(sql, data)
    conn.commit()

def monthTraffic(months):
    for m in months:
        t = datetime.utcfromtimestamp(m[0])
        sql = ''' INSERT INTO traffic_month (month, uniques, pageviews) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE uniques = VALUES(uniques), pageviews = VALUES(pageviews)'''
        data = (t ,m[1], m[2])
        cur.execute(sql, data)
    conn.commit()

def dailyHistory(days = 8):
    now = datetime.now()
    n = now.replae(hour = 0, minute = 0, second = 0, microsecond = 0)
    lastWeek = n - timedelta(days = days)
    sql = 'SELECT day(utc) as day, count(*) from comments where date >= "{date}" and date < "{current}" group by day'''.format(date = lastWeek.strftime("%Y-%m-%d %H:%M"), current = n.strftime("%Y-%m-%d %H:%M"))
    cur.execute(sql)
    commentData = cur.fetchall()
    sql = 'SELECT day, day(day), uniques, pageviews from traffic_day where day >= "{date}" and day < "{current}"'.format(date = lastWeek.strftime("%Y-%m-%d %H:%M"), current = n.strftime("%Y-%m-%d %H:%M"))
    cur.execute(sql)
    trafficData = cur.fetchall()
    return commentData, trafficData
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
        return commentData, trafficData
    except:
        return None
def oldDailys():
    regex = re.compile("(Stream.*Discussion)|(Daily Discussion)")
    now = datetime.now()
    try:
        sql = 'SELECT year(date), id, title, author from posts where month(date) = {month} and day(date) = {day} and year(date) < {year} order by date asc'.format(month = now.month, day = now.day, year = now.year)
        cur.execute(sql)
        threads = cur.fetchall()
        dailys = []
        for thread in threads:
            title = thread[2]
            result = regex.search(title)
            if result is not None:
                dailys.append(thread)
        return dailys
    except:
        return None
def lastDaily():
    try:
        sql = 'SELECT id from posts where author = "Crim_Bot" and title like "%Daily Discussion%" order by id desc limit 1'
        cur.execute(sql)
        thread = cur.fetchone()
        return thread[0]
    except Exception:
        return None
def lastFTF():
    try:
        sql = 'SELECT id, date from posts where author = "Crim_Bot" and title like "%Free Talk Friday%"order by id desc limit 1'
        cur.execute(sql)
        thread = cur.fetchone()
        return thread
    except Exception:
        return None
def getComments():
    now = datetime.now()
    now = now.replace(minute = 0, second = 0, microsecond= 0)
    last = now - timedelta(days = 1)

    sql = 'SELECT id from comments where date >= "{date}"'.format(date = last.strftime("%Y-%m-%d %H:%M"))
    cur.execute(sql)
    temp = cur.fetchall()
    comments = []
    for c in temp:
        comments.append("t1_" + c[0])
    return comments
def getMatchThreads(lastHours = 40):
    now = datetime.now()
    old = now + timedelta(hours = -1 * lastHours)
    authorString = str(variables.postUsers).replace("[", "(").replace("]", ")")
    sql = 'SELECT id from posts where date >= "{date}" and author in {authors}'.format(date = old.strftime("%Y-%m-%d %H:%M"), authors = authorString)
    cur.execute(sql)
    temp = cur.fetchall()
    posts = []
    for p in temp:
        posts.append("t3_" + p[0])
    return posts