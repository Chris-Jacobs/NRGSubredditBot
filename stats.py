import praw
import variables
import time
import cloud
reddit = praw.Reddit(client_id=variables.client_id,
        client_secret=variables.client_secret,
        user_agent=variables.user_agent,
        username=variables.username,
        password=variables.password)
def main(lastDDT):
    subreddit = reddit.subreddit(variables.subreddit)
    highestComment = None
    score = 0
    counter = 0
    txt = ""
    for submission in subreddit.submissions(start = lastDDT.created_utc - 10):
        print(submission.title)
        submission.comments.replace_more(limit=None)
        comments = submission.comments.list()
        for comment in comments:
            txt += comment.body + " "
            counter += 1
            cScore = comment.score
            if cScore > score:
                highestComment = comment
                score = cScore
    link = 'https://www.reddit.com' + highestComment.permalink
    s= "**Summary of Yesterday** \n\n"
    s += str(counter) +" comments \n\n"
    s += "[Highest Scoring Comment](" + link + ") from /u/" + str(highestComment.author) + "\n\n"
    wc = cloud.wordcloud(txt = txt)
    wc = None
    if wc is not None:
        s += "[Yesterday's Word Cloud](" + wc + ")"
    return s


