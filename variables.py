import sqlite3
conn = sqlite3.connect('keys.db')
c = conn.cursor()
username, password, user_agent, twitchKey, client_secret, client_id, ytKey, imgurID, imgurSecret, schedulerbase  = c.execute("SELECT * FROM Keys").fetchone()
c.close()
subreddit = "OpTicGamingSandbox"
ddthour = 7
ftfhour = 7
postUsers = ['OpTicModerators']
months = {
    1:'January ',
    2:'February ',
    3:'March ',
    4:'April ',
    5:'May ',
    6:'June ',
    7:'July ',
    8:'August ',
    9:'September ',
    10:'October ',
    11:'November ',
    12:'December '
}
spriteMappings = {
    'COD':'[COD](#ww2)',
    'CSGO':'[CSGO](#csgo)',
    'HALO':'[HALO](#halo)',
    'LOL':'[LOL](#lol)',
    'OW':'[OW](#ow)',
    'GOW':'[GOW](#gow)',
    'PUBG':'[PUBG](#pubg)',
    'DOTA':'[DOTA](#dota)',
    'MISC':'[MISC](#optic)'
}
