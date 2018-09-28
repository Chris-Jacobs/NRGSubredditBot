import sqlite3
conn = sqlite3.connect('keys.db')
c = conn.cursor()
username, password, user_agent, twitchKey, client_secret, client_id, ytKey, imgurID, imgurSecret, schedulerbase, mod_username, mod_password, mod_client_secret, mod_client_id, localIP, dbUser, dbPassword, dbIP = c.execute("SELECT * FROM Keys").fetchone()
c.close()
subreddit = "OpTicGaming"
ddthour = 7
ftfhour = 7
postUsers = ['OpTicModerators', 'Crim_Bot']
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
    'COD':'[COD](#i_ww2)',
    'CSGO':'[CSGO](#i_cs)',
    'FN':'[FN](#i_fn)',
    'LOL':'[LOL](#i_lol)',
    'OW':'[OW](#i_ow)',
    'GOW':'[GOW](#i_gow)',
    'PUBG':'[PUBG](#i_pubg)',
    'DOTA':'[DOTA](#i_dota)',
    'MISC':'[MISC](#i_optic)'
}
