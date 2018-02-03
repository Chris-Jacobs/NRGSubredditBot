import praw
import datetime
import variables
import requests

def getMatches():
	return requests.get(variables.schedulerbase + "getMatches.php")

def deleteScheduledMatch(id):
	return requests.get(variables.schedulerbase + "deleteMatch.php?id=" + id)

def postMatch(r, match):
	match_title = match['Title']
	match_post = match['Post']
	match_flair = match['Flair']
	try:
		thread = r.subreddit(variables.subreddit).submit(title=match_title, selftext=match_post, send_replies=False)

		deleteScheduledMatch(match['ID'])

		#loop through the subreddit's link flairs and try to match the supplied flair with either a flair_text for flair_css
		choices = thread.flair.choices()
		for flair in choices :
			if(match_flair in flair['flair_css_class'] or match_flair in flair['flair_text']):
				thread.flair.select(flair['flair_template_id'])
				break
	except:
		pass


def main():
	print("Checking for scheduled matchthreads.")
	matches = getMatches().json()
	match_count = len(matches)

	r = praw.Reddit(client_id=variables.mod_client_id,
                     client_secret=variables.mod_client_secret,
                     user_agent=variables.user_agent,
                     username=variables.mod_username,
                     password=variables.mod_password)

	for match in matches:
		print("Posting matchthread: " + match['Title'])
		postMatch(r, match)
