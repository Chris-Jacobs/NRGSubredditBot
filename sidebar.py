import praw
import html
import variables
def getSchedule(sidebar):
    """
    Extracts the Schedule section from the sidebar
    Args:
        sidebar: Sidebar Text
    Returns:
        The text of the schedule section
    """
    startIndex = sidebar.index("- [")
    endIndex = sidebar.index("> [](#sep)")
    schedule = sidebar[startIndex:endIndex - 3]
    return (schedule, endIndex)
def getResults(sidebar):
    """
    Extracts the Results section from the sidebar
    Args:
        sidebar: Sidebar Text
    Returns:
        The text of the Results section
    """
    s = sidebar.index("### Results")
    s = sidebar.index(">", s)
    e = sidebar.index(">", s+1)
    return sidebar[s+1:e]

def duplicateSchedule(sidebar, schedule, index):
    """
    Duplicates the schedule from the wiki template so scrolling is smooth
    Args:
        sidebar: Text of the Whole Sidebar
        schedule: Text of the Schedule
        index: Index to insert the duplicated schedule
    Returns:
        The complete sidebar with duplicated schedule
    """
    schedule, index = getSchedule(sidebar)
    sidebar = sidebar[:index + 15] + schedule + sidebar[index+15:]
    return sidebar

def updateWidgets(reddit, schedule, results):
    """
    Updates the New Reddit Widgets with the Schedule and Results.
    Correspond Widget ID's are in variables.
    Args:
        reddit: Authorized praw.Reddit object
        schedule: Text of the Schedule
        results: Text of the Results

    """
    sidebarWidgets = reddit.subreddit(variables.subreddit).widgets.sidebar
    for widget in sidebarWidgets:
        if widget.id == variables.scheduleWidget:
            widget.mod.update(text = schedule)
        elif widget.id == variables.resultsWidget:
            widget.mod.update(text = results)

def createSidebar(sidebar, table):
    """
    Creates the full sidebar given the template and the stream table.
    Also creates the schedule and results for the New Reddit Widgets
    Args:
        sidebar: Contents of the wiki page
        table: Stream Table to be inserted
    Returns:
        Tuple of strings.
            sidebar: Text of the Sidebar to be pushed to Subreddit Settings
            schedule: Just the text containing the schedule section of the sidebar'
            results: Just the text containing the results section of the sidebar'
    """
    schedule, index = getSchedule(sidebar)
    results = getResults(sidebar)
    sidebar = duplicateSchedule(sidebar, schedule, index)
    sidebarParts = sidebar.split("***")
    sidebar = sidebarParts[0] + table + sidebarParts[2]
    return sidebar, schedule, results
def updateSidebar(reddit, sidebar):
    """
    Updates the Sidebar with the given string
    Args:
        reddit: Authorized praw.Reddit object
        sidebar: sidebar text to push to Subreddit Settings
    """
    reddit.subreddit(variables.subreddit).mod.update(description = sidebar, spoilers_enabled = True)

def getSidebar(reddit):
    """
    Retrieves the Sidebar from the 'edit_sidebar' wiki page
    Args:
        reddit: Authorized praw.Reddit object
    Returns:
        string with the contents of the wiki page
    """
    return reddit.subreddit(variables.subreddit).wiki['edit_sidebar'].content_md
def main(reddit, table):
    """
    Builds and Edits the Sidebar along with New Reddit Widgets
    Args:
        reddit: Authorized praw.Reddit object
    """
    print('Building Sidebar.')
    wikiSidebar = getSidebar(reddit)
    sidebar, schedule, results = createSidebar(wikiSidebar, table)
    print('Updating Sidebar')
    updateWidgets(reddit, schedule, results)
    updateSidebar(reddit, sidebar)
