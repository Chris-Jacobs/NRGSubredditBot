import praw
import html
import variables
def get_schedule(sidebar):
    startIndex = sidebar.index("- [")
    endIndex = sidebar.index("> [](#sep)")
    schedule = sidebar[startIndex:endIndex - 3]
    return (schedule, endIndex)
def get_results(sidebar):
    s = sidebar.index("### Results")
    s = sidebar.index(">", s)
    e = sidebar.index(">", s+1)
    return sidebar[s+1:e]

def duplicate_schedule(sidebar, schedule, index):
    schedule, index = get_schedule(sidebar)
    sidebar = sidebar[:index + 15] + schedule + sidebar[index+15:]
    return sidebar

def update_widgets(reddit, schedule, results):
    sidebarWidgets = reddit.subreddit(variables.subreddit).widgets.sidebar
    for widget in sidebarWidgets:
        if widget.id == variables.scheduleWidget:
            widget.mod.update(text = schedule)
        elif widget.id == variables.resultsWidget:
            widget.mod.update(text = results)

def create_sidebar(sidebar, table):
    schedule, index = get_schedule(sidebar)
    results = get_results(sidebar)
    sidebar = duplicate_schedule(sidebar, schedule, index)
    sidebarParts = sidebar.split("***")
    sidebar = sidebarParts[0] + table + sidebarParts[2]
    return sidebar, schedule, results
def update_sidebar(reddit, sidebar):
    reddit.subreddit(variables.subreddit).mod.update(description = sidebar, spoilers_enabled = True)

def get_sidebar(reddit):
    return reddit.subreddit(variables.subreddit).wiki['edit_sidebar'].content_md
def main(reddit, table):
    print('Building Sidebar.')
    wikiSidebar = get_sidebar(reddit)
    sidebar, schedule, results = create_sidebar(wikiSidebar, table)
    update_widgets(reddit, schedule, results)
    update_sidebar(reddit, sidebar)
