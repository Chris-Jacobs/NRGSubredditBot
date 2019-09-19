import db
import praw
def main(reddit):
    try:
        print('Getting Traffic...')
        t = reddit.subreddit('OpTicGaming').traffic()
        try:
            db.hourTraffic(t['hour'])
        except Exception as e:
            print('Error with Hourly Traffic')
            print(e)
        try:
            db.dayTraffic(t['day'])
        except Exception as e:
            print('Error with Daily Traffic')
            print(e)
        try:
            db.monthTraffic(t['month'])
        except Exception as e:
            print('Error with Monthly Traffic')
            print(e)
    except Exception:
        print('Error with traffic')