import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import urllib

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def makeConfig(app):
    return({
        "web": {
            "client_id": app.config['G_CLIENT_ID'],
            "project_id": app.config['G_PROJECT_ID'],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": app.config['G_CLIENT_SECRET'],
            "redirect_uris": [
                "https://slate.csh.rit.edu",
                "https://profiles.csh.rit.edu",
                "https://slate.cs.house"
            ]
        }
    })


def getURL(app):
    """
    Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            return creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(makeConfig(app), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        calendar = service.calendars()
        calendar = calendar.get(calendarId='primary').execute()

        return ("https://calendar.google.com/calendar/ical/" + urllib.parse.quote(calendar['id'], safe='') + "/public/basic.ics")
    except HttpError as err:
        return(err)


if __name__ == '__main__':
    getURL()
