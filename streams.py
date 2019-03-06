import requests
import variables
import json
import time
import datetime
url = variables.keys['StreamsBase']

def get_live():
    r = requests.get(url + '/live').json()
    return r


def get_timezone():
    return "EST" if time.localtime().tm_isdst == 0 else "EDT"
def format_time(timeString):
    time = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:S")
    return "Streams Updated at: {month}/{day} {hour}:{minute} {timezone}".format(month = str(time.month).zfill(2), day = str(time.day).zfill(2), hour = str(time.hour).zfill(2), minute = str(time.minute).zfill(2), timezone = get_timezone())

def ddt_table(streams, timeString):
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
def sidebar_table(streams, timeString):
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
    print("Getting livestreams.")
    streamList = get_live()
    timeString = format_time(streamList['time'])
    ddtTable = ddt_table(streamList, timeString)
    sidebarTable = sidebar_table(streamList, timeString)
    return (ddtTable, sidebarTable)