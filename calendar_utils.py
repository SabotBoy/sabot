import datetime
import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    import base64

    creds = None

    # ✅ Read base64-encoded credentials from Render environment variable
    creds_encoded = os.environ.get("GOOGLE_CREDENTIALS_B64")

    if not creds_encoded:
        raise ValueError("Missing GOOGLE_CREDENTIALS_B64 environment variable.")

    creds_json = base64.b64decode(creds_encoded).decode()

    # ✅ Write to temporary file
    with open("credentials_temp.json", "w") as f:
        f.write(creds_json)

    # ✅ Use the temp file to authenticate
    flow = InstalledAppFlow.from_client_secrets_file("credentials_temp.json", SCOPES)
    creds = flow.run_local_server(port=0)

    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)



def create_event(summary, start_datetime, end_datetime):
    service = get_calendar_service()

    event = {
        'summary': summary,
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'America/Jamaica',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'America/Jamaica',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event.get('htmlLink')
