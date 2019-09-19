import praw
def processWikipage(reddit):
    wikiPage  = reddit.subreddit('OpTicGaming').wiki['verification'].content_md
    lines = wikiPage.split("\n")
    users = []
    for line in lines:
        users.append(line.split(","))
    return users
def generateFlairs(users):
    userFlairs = []
    for user in users:
        userFlair = {}
        userFlair['user'] = user[0].strip()
        flair = ":checkmark: {name} - {role}".format(name = user[1].strip(), role = user[2].strip())
        userFlair['flair_text'] = flair
        userFlairs.append(userFlair)
    return userFlairs
def assignFlairs(flairs, reddit):
    css = 'verify'
    reddit.subreddit('OpTicGaming').flair.update(flair_list = flairs, css_class = css)
def main(reddit):
    users = processWikipage(reddit)
    flairs = generateFlairs(users)
    assignFlairs(flairs, reddit)