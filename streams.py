import requests
import variables
import json
import time
import datetime
from reddittable import RedditColumn, RedditTable
url = variables.keys['StreamsBase']

def getLive():
    """ 
    Fetches JSON of livestreams from Twitch Service
    Returns:
        A dictionary of livestream data
        Example:
        {
            'total_viewers':2866,
            'time': '2019-03-06 17:03:S',
            'streams': [
                {
                    'title': 'Extra Auto-aim today',
                    'name': 'TeePee',
                    'game': 'Call of Duty: Black Ops 4',
                    'viewers': 2866
                }
            ]
        }
    """ 
    r = requests.get(url + '/live').json()
    return r

def getTimezone():
    """ 
    Determines if DST is active or not
    """
    return "EST" if time.localtime().tm_isdst == 0 else "EDT"

def formatTime(timeString):
    """
    Formats time as seen on the Sidebar and DDT Body
    Args:
        timeString: the value from the 'time' key from the Twitch Service
    Returns:
        String that is added to the sidebar and DDT Table
    """
    time = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S")
    return "Streams Updated at: {month}/{day} {hour}:{minute} {timezone}".format(month = str(time.month).zfill(2), day = str(time.day).zfill(2), hour = str(time.hour).zfill(2), minute = str(time.minute).zfill(2), timezone = getTimezone())

def ddtTable(streams, timeString):
    """
    Builds the Stream Table for the DDT
    Args:
        streams: Dictionary returned from getLive()
        timeString: Time String created in formatTime, added directly to DDT
    Returns:
        RedditTable object with Stream, Viewers, and Game column with the timeString as a prefix
            Stream Column has a markdown link of the format [Username](LinkToStream)
    """
    table = RedditTable([RedditColumn("Stream"), RedditColumn("Viewers", centered = True), RedditColumn("Game")], prefix= timeString)
    viewers = streams['total_viewers']
    for stream in streams['streams']:
        link = "https://twitch.tv/" + stream['name']
        row = [
            "[{name}]({url})".format(name = stream['name'], url = link),
            stream['viewers'],
            stream['game']
        ]
        table.addRow(row)
    table.addRow(["**Total**", "**{total}**".format(total = str(viewers))])
    return table
def sidebarTable(streams, timeString):
    """
    Builds the Stream Table for the Sidebar
    Args:
        streams: Dictionary returned from getLive()
        timeString: Time String created in formatTime, added directly to Sidebar
    Returns:
        RedditTable object with Stream and Viewers column with the timeString as a suffix
            Stream Column has a markdown link of the format [Username](LinkToStream)
    """
    table = RedditTable([RedditColumn("Streams"), RedditColumn("Viewers", centered= True)], suffix = timeString)
    for stream in streams['streams']:
        link = "https://twitch.tv/" + stream['name']
        row = [
            "[{name}]({url})".format(name = stream['name'], url = link),
            stream['viewers']
        ]
        table.addRow(row)
    return table


def main():
    """
    Handles all Livestream functionality
    Returns:
        A tuple of RedditTable objects. First RedditTable is the table for the DDT, second RedditTable is the table for the Sidebar.
    """
    print("Getting livestreams.")
    streamList = getLive()
    timeString = formatTime(streamList['time'])
    ddt = ddtTable(streamList, timeString)
    sidebar = sidebarTable(streamList, timeString)
    return (ddt, sidebar)