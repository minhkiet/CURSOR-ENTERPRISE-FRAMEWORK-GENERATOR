#!/usr/bin/env python
"""
Google APIs Integration Tool

Provides Google APIs integration for:
- Gmail
- Google Drive
- Google Calendar
- Google Sheets
- Google Analytics

Usage:
    python google_integration.py gmail --credentials CRED_FILE list-messages
    python google_integration.py drive --credentials CRED_FILE list-files
    python google_integration.py calendar --credentials CRED_FILE list-events
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Optional, List

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("ERROR: Google libraries required.")
    print("Install with: pip install google-api-python-client google-auth google-auth-oauthlib")
    sys.exit(1)


@dataclass
class GoogleConfig:
    """Google API configuration."""
    scopes: dict = None
    
    def __post_init__(self):
        self.scopes = {
            "gmail": ["https://www.googleapis.com/auth/gmail.readonly", 
                      "https://www.googleapis.com/auth/gmail.send"],
            "drive": ["https://www.googleapis.com/auth/drive.readonly"],
            "calendar": ["https://www.googleapis.com/auth/calendar.readonly"],
            "sheets": ["https://www.googleapis.com/auth/spreadsheets.readonly"],
        }


class GoogleClient:
    """Google APIs client."""
    
    def __init__(self, credentials_path: str, token_path: Optional[str] = None):
        self.credentials_path = credentials_path
        self.token_path = token_path or "token.json"
        self.config = GoogleConfig()
        self.creds = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.config.scopes.get("gmail", []))
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, 
                    self.config.scopes.get("gmail", [])
                )
                self.creds = flow.run_local_server(port=0)
            
            with open(self.token_path, "w") as token:
                token.write(self.creds.to_json())
    
    def get_gmail_service(self):
        """Get Gmail API service."""
        from googleapiclient.discovery import build
        return build("gmail", "v1", credentials=self.creds)
    
    def get_drive_service(self):
        """Get Drive API service."""
        from googleapiclient.discovery import build
        return build("drive", "v3", credentials=self.creds)
    
    def get_calendar_service(self):
        """Get Calendar API service."""
        from googleapiclient.discovery import build
        return build("calendar", "v3", credentials=self.creds)
    
    def gmail_list_messages(self, max_results: int = 10) -> List[dict]:
        """List Gmail messages."""
        service = self.get_gmail_service()
        results = service.users().messages().list(
            userId="me", 
            maxResults=max_results
        ).execute()
        return results.get("messages", [])
    
    def gmail_send_message(self, to: str, subject: str, body: str) -> dict:
        """Send Gmail message."""
        from base64 import urlsafe_b64encode
        import mimetypes
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        service = self.get_gmail_service()
        
        message = MIMEMultipart()
        message["to"] = to
        message["subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        raw = urlsafe_b64encode(message.as_bytes()).decode()
        return service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()
    
    def drive_list_files(self, folder_id: Optional[str] = None, max_results: int = 100) -> List[dict]:
        """List Drive files."""
        service = self.get_drive_service()
        
        query = "'me' in owners"
        if folder_id:
            query = f"'{folder_id}' in parents"
        
        results = service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, mimeType, createdTime, modifiedTime)"
        ).execute()
        return results.get("files", [])
    
    def drive_create_folder(self, name: str, parent_id: Optional[str] = None) -> dict:
        """Create Drive folder."""
        service = self.get_drive_service()
        
        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder"
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]
        
        return service.files().create(
            body=file_metadata,
            fields="id, name"
        ).execute()
    
    def calendar_list_events(self, max_results: int = 10) -> List[dict]:
        """List Calendar events."""
        service = self.get_calendar_service()
        
        events = service.events().list(
            calendarId="primary",
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return events.get("items", [])
    
    def calendar_create_event(self, summary: str, start: str, end: str, 
                             description: Optional[str] = None, location: Optional[str] = None) -> dict:
        """Create Calendar event."""
        service = self.get_calendar_service()
        
        event = {
            "summary": summary,
            "start": {"dateTime": start},
            "end": {"dateTime": end},
        }
        if description:
            event["description"] = description
        if location:
            event["location"] = location
        
        return service.events().insert(
            calendarId="primary",
            body=event
        ).execute()


def main():
    parser = argparse.ArgumentParser(
        description="Google APIs Integration Tool"
    )
    
    parser.add_argument("--credentials", "-c", required=True, help="Path to credentials.json")
    parser.add_argument("--token", "-t", help="Path to token.json (default: token.json)")
    
    subparsers = parser.add_subparsers(dest="api", help="Google API")
    
    # Gmail
    gmail = subparsers.add_parser("gmail", help="Gmail operations")
    gmail_sub = gmail.add_subparsers(dest="cmd", help="Commands")
    
    gmail_list = gmail_sub.add_parser("list-messages", help="List messages")
    gmail_list.add_argument("--max", type=int, default=10, help="Max results")
    
    gmail_send = gmail_sub.add_parser("send", help="Send message")
    gmail_send.add_argument("--to", required=True, help="Recipient email")
    gmail_send.add_argument("--subject", "-s", required=True, help="Subject")
    gmail_send.add_argument("--body", "-b", required=True, help="Body")
    
    # Drive
    drive = subparsers.add_parser("drive", help="Drive operations")
    drive_sub = drive.add_subparsers(dest="cmd", help="Commands")
    
    drive_list = drive_sub.add_parser("list-files", help="List files")
    drive_list.add_argument("--folder", help="Folder ID")
    drive_list.add_argument("--max", type=int, default=100, help="Max results")
    
    drive_mkdir = drive_sub.add_parser("mkdir", help="Create folder")
    drive_mkdir.add_argument("--name", "-n", required=True, help="Folder name")
    drive_mkdir.add_argument("--parent", help="Parent folder ID")
    
    # Calendar
    cal = subparsers.add_parser("calendar", help="Calendar operations")
    cal_sub = cal.add_subparsers(dest="cmd", help="Commands")
    
    cal_list = cal_sub.add_parser("list-events", help="List events")
    cal_list.add_argument("--max", type=int, default=10, help="Max results")
    
    cal_create = cal_sub.add_parser("create", help="Create event")
    cal_create.add_argument("--summary", "-s", required=True, help="Event title")
    cal_create.add_argument("--start", required=True, help="Start time (ISO format)")
    cal_create.add_argument("--end", required=True, help="End time (ISO format)")
    cal_create.add_argument("--desc", help="Description")
    cal_create.add_argument("--loc", help="Location")
    
    args = parser.parse_args()
    
    try:
        client = GoogleClient(args.credentials, args.token)
        
        if args.api == "gmail":
            if args.cmd == "list-messages":
                result = client.gmail_list_messages(args.max)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.cmd == "send":
                result = client.gmail_send_message(args.to, args.subject, args.body)
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.api == "drive":
            if args.cmd == "list-files":
                result = client.drive_list_files(args.folder, args.max)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.cmd == "mkdir":
                result = client.drive_create_folder(args.name, args.parent)
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.api == "calendar":
            if args.cmd == "list-events":
                result = client.calendar_list_events(args.max)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif args.cmd == "create":
                result = client.calendar_create_event(
                    args.summary, args.start, args.end, args.desc, args.loc
                )
                print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
