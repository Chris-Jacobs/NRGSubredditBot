import requests
import requests.auth
import variables

def getAccessToken():
    client_auth = requests.auth.HTTPBasicAuth(variables.client_id, variables.client_secret)
    post_data = {"grant_type": "password", "username": variables.username, "password": variables.password}
    headers = {"User-Agent": variables.user_agent}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    access_token = response.json()['access_token']
    return access_token
def editTextWidget(widgetID, widgetName, text, access_token = None):
    if access_token is None:
        access_token = getAccessToken()
    bearer = "bearer " + access_token
    headers = {
        "Authorization": bearer,
        "User-Agent":variables.user_agent
    }
    data = {
        "id": widgetID,
        "kind": "textarea",
        "shortName": widgetName,
        "text": text
    }
    url = "https://oauth.reddit.com/r/OpTicGaming/api/widget/" + widgetID + "?raw_json=1"
    r = requests.put(url, json = data, headers = headers)
    print(r.raise_for_status())
