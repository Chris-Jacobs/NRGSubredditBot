import requests
import variables
import json
import time
import datetime
url = variables.keys['StreamsBase']

def getLive():
    """ 
    Fetches JSON of livestreams from Twitch Service
    Returns:
        A dictionary of livestream data.
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
    time = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:S")
    return "Streams Updated at: {month}/{day} {hour}:{minute} {timezone}".format(month = str(time.month).zfill(2), day = str(time.day).zfill(2), hour = str(time.hour).zfill(2), minute = str(time.minute).zfill(2), timezone = getTimezone())

def ddtTable(streams, timeString):
    """
    Builds the Stream Table for the DDT
    Args:
        streams: Dictionary returned from getLive()
        timeString: Time String created in formatTime, added directly to DDT
    Returns:
        timeString and then a markdown table with 3 columns, Stream, Viewers, and Game. 
        Stream Column has a markdown link of the format [Username](LinkToStream)
    """
    table = timeString + "\n\n"
    viewers = streams['total_viewers']
    streams = streams['streams']
    table += "Stream|Viewers|Game" + "\n"
    table += '-|:-:|---' + "\n"
    for stream in streams:
        link = "https://twitch.tv/" + stream['name']
        table += "[{name}]({url})|{viewers}|{game}".format(name = stream['name'], url = link, viewers = stream['viewers'], game = stream['game'])
        table += "\n"
    table += "**Total**|**{total}**".format(total = str(viewers))
    return table
def sidebarTable(streams, timeString):
    """
    Builds the Stream Table for the Sidebar
    Args:
        streams: Dictionary returned from getLive()
        timeString: Time String created in formatTime, added directly to Sidebar
    Returns:
        A markdown table with 2 columns, Stream and Viewers followed by the timeString. 
        Stream Column has a markdown link of the format [Username](LinkToStream)
    """
    table = "Streams|Viewers" + "\n"
    table += '-|:-:' + "\n"
    streams = streams['streams']
    for stream in streams:
        link = "https://twitch.tv/" + stream['name']
        table += "[{name}]({url})|{viewers}".format(name = stream['name'], url = link, viewers = stream['viewers'])
        table += "\n"
    
    table += timeString + "\n\n" 
    return table


def main():
    """
    Handles all Livestream functionality
    Returns:
        A tuple of strings. First is the table for the DDT, second is the table for the Sidebar.
    """
    print("Getting livestreams.")
    streamList = getLive()
    timeString = formatTime(streamList['time'])
    ddt = ddtTable(streamList, timeString)
    sidebar = sidebarTable(streamList, timeString)
    return (ddt, sidebar)