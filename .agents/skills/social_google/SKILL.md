# Google APIs Integration Skill

**Version:** 1.0.0  
**Author:** Cursor Enterprise Framework  
**Triggers:** google, google api, google drive, gmail, google calendar, google sheets

## Overview

This skill provides Google APIs integration for Cursor Enterprise Framework. It supports Gmail, Google Drive, Google Calendar, and more.

## Capabilities

- **Gmail**: Send/receive emails, manage labels
- **Google Drive**: List files, upload, download, share
- **Google Calendar**: Create events, list calendars
- **Google Sheets**: Read/write spreadsheets
- **Google Analytics**: Get analytics data

## Installation

```bash
pip install google-api-python-client google-auth google-auth-oauthlib
```

Or use the bundled tool:
```bash
python tools/api_integrations/google_integration.py --help
```

## Configuration

### Google Cloud Console Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable required APIs (Gmail, Drive, Calendar, Sheets)
4. Create OAuth 2.0 credentials
5. Download credentials.json

### Environment Variables

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

## OAuth Flow

The first time you run, you'll be prompted to authorize via browser:

```python
client = GoogleClient(credentials_path="credentials.json")
# Browser will open for OAuth authorization
# Token will be saved to token.json
```

## Usage

### CLI Tool

```bash
# List Gmail messages
python tools/api_integrations/google_integration.py --credentials creds.json gmail list-messages --max 10

# Send Gmail
python tools/api_integrations/google_integration.py --credentials creds.json gmail send --to user@example.com --subject "Hello" --body "Message body"

# List Drive files
python tools/api_integrations/google_integration.py --credentials creds.json drive list-files

# Create Drive folder
python tools/api_integrations/google_integration.py --credentials creds.json drive mkdir --name "New Folder"

# List Calendar events
python tools/api_integrations/google_integration.py --credentials creds.json calendar list-events --max 10

# Create Calendar event
python tools/api_integrations/google_integration.py --credentials creds.json calendar create --summary "Meeting" --start "2024-01-15T09:00:00" --end "2024-01-15T10:00:00"
```

### Python API

```python
from tools.api_integrations.google_integration import GoogleClient

# Initialize client (first run: browser opens for OAuth)
client = GoogleClient(credentials_path="credentials.json")

# Gmail
messages = client.gmail_list_messages(max_results=10)
client.gmail_send_message(to="user@example.com", subject="Hello", body="Message")

# Drive
files = client.drive_list_files()
folder = client.drive_create_folder(name="New Folder")

# Calendar
events = client.calendar_list_events()
client.calendar_create_event(
    summary="Meeting",
    start="2024-01-15T09:00:00",
    end="2024-01-15T10:00:00"
)
```

## Gmail Operations

### List Messages
```python
messages = client.gmail_list_messages(max_results=20)
for msg in messages:
    print(msg["id"])
```

### Send Message
```python
result = client.gmail_send_message(
    to="recipient@example.com",
    subject="Subject Line",
    body="Email body content"
)
print(result)
```

## Google Drive Operations

### List Files
```python
# All files
files = client.drive_list_files()

# Files in folder
files = client.drive_list_files(folder_id="FOLDER_ID")

# Search files
files = client.drive_list_files()
python_files = [f for f in files if f["name"].endswith(".py")]
```

### Create Folder
```python
folder = client.drive_create_folder(name="Project Files")
print(f"Created folder: {folder['id']}")
```

### Upload File
```python
from googleapiclient.http import MediaFileUpload

def upload_file(client, name, path, folder_id=None):
    service = client.get_drive_service()
    
    file_metadata = {"name": name}
    if folder_id:
        file_metadata["parents"] = [folder_id]
    
    media = MediaFileUpload(path)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name"
    ).execute()
    return file

file = upload_file(client, "document.pdf", "/path/to/file.pdf")
```

## Calendar Operations

### List Events
```python
events = client.calendar_list_events(max_results=50)
for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    print(f"{start}: {event['summary']}")
```

### Create Event
```python
event = client.calendar_create_event(
    summary="Team Meeting",
    start="2024-01-15T14:00:00",
    end="2024-01-15T15:00:00",
    description="Weekly team sync",
    location="Conference Room"
)
print(f"Created event: {event['id']}")
```

### Create Recurring Event
```python
event = {
    "summary": "Weekly Sync",
    "start": {"dateTime": "2024-01-15T14:00:00", "timeZone": "Asia/Ho_Chi_Minh"},
    "end": {"dateTime": "2024-01-15T15:00:00", "timeZone": "Asia/Ho_Chi_Minh"},
    "recurrence": ["RRULE:FREQ=WEEKLY;COUNT=12"]
}
```

## Examples

### Email Automation
```python
from tools.api_integrations.google_integration import GoogleClient
from datetime import datetime, timedelta

client = GoogleClient(credentials_path="credentials.json")

def send_daily_report(recipients, report_content):
    subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
    for recipient in recipients:
        client.gmail_send_message(
            to=recipient,
            subject=subject,
            body=report_content
        )

# Send weekly digest
send_daily_report(
    recipients=["team@example.com"],
    report_content="Weekly digest content..."
)
```

### Calendar Booking System
```python
def book_slot(client, attendee_email, start_time, end_time, title):
    try:
        event = client.calendar_create_event(
            summary=title,
            start=start_time,
            end=end_time,
            description=f"Meeting with {attendee_email}"
        )
        
        # Send invite
        client.gmail_send_message(
            to=attendee_email,
            subject=f"Meeting Invitation: {title}",
            body=f"You've been invited to: {title}\nTime: {start_time}"
        )
        
        return event
    except Exception as e:
        print(f"Booking failed: {e}")
        return None
```

### Backup Drive Files
```python
def backup_to_local(client, output_dir):
    import os
    
    files = client.drive_list_files()
    for file in files:
        if file["mimeType"] != "application/vnd.google-apps.folder":
            # Download file
            print(f"Backing up: {file['name']}")
            # Implementation for file download
```

## Best Practices

1. **Token Security**: Keep credentials.json secure, don't commit to git
2. **Token Refresh**: Tokens auto-refresh, but handle expiration gracefully
3. **Rate Limiting**: Respect Google API rate limits
4. **Scopes**: Request only necessary permissions
5. **Error Handling**: Implement retry logic for transient errors

## Troubleshooting

### OAuth Error
- Verify credentials.json is valid
- Check if redirect URIs are configured correctly
- Ensure required APIs are enabled

### Token Issues
- Delete token.json and re-authenticate
- Check if OAuth consent screen is configured

### API Errors
- Verify API is enabled in Cloud Console
- Check quota limits
- Implement exponential backoff

## References

- [Google APIs](https://developers.google.com/api-client-library)
- [Gmail API](https://developers.google.com/gmail/api)
- [Drive API](https://developers.google.com/drive/api)
- [Calendar API](https://developers.google.com/calendar/api)

## License

MIT License - See bundled LICENSE file
