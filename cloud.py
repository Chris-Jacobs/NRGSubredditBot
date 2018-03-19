import time
import datetime
import variables
import praw
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import numpy as np
from PIL import Image
from imgurpython import ImgurClient
reddit = praw.Reddit(client_id=variables.client_id, client_secret=variables.client_secret, user_agent=variables.user_agent)
subreddit = reddit.subreddit('opticgaming')
output = 'cloud.jpg'
def getDailyComments():
    txt = ""
    t = time.time() - 86400 #yesterday
    for comment in subreddit.comments(limit=5000):
        if (comment.created_utc < t): #timezone taken into account
            break
        txt += comment.body + " "

    return txt
def getThreadComments(threadid):
    submission = reddit.submission(id = threadid)
    submission.comments.replace_more(limit=None)    
    comments = submission.comments.list()
    txt = ''
    for comment in comments:
        txt += comment.body + " "
    return txt
def upload(path):
    try:
        client = ImgurClient(variables.imgurID, variables.imgurSecret)
        upload = client.upload_from_path('cloud.jpg', anon=True)
        return upload['link']
    except Exception:
        return None
def wordcloud(txt = None):
    try:
        imgmask = np.array(Image.open('mask.png'))
        colors = ImageColorGenerator(np.array(Image.open('whitemask.png')))
        stopwords = STOPWORDS
        stopwords.add('http')
        stopwords.add('https')
        if txt == None:
            txt = getDailyComments()
        wordcloud = WordCloud(background_color='black',mask=imgmask, color_func=colors, stopwords=stopwords).generate(txt)
        image = wordcloud.to_image()
        image.save(output)
        return upload(output)
    except Exception:
        return None
def main():
    return wordcloud()

