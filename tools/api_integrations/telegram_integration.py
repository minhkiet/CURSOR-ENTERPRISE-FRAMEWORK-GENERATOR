#!/usr/bin/env python
"""
Telegram Bot Integration Tool

Provides Telegram Bot API integration for:
- Sending messages
- Managing groups
- Handling updates
- Bot commands
- Inline queries

Usage:
    python telegram_integration.py send --token BOT_TOKEN --chat_id CHAT_ID --text "Hello"
    python telegram_integration.py send-photo --token BOT_TOKEN --chat_id ID --photo URL
    python telegram_integration.py get-updates --token BOT_TOKEN
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Optional, List

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class TelegramConfig:
    """Telegram API configuration."""
    api_base_url: str = "https://api.telegram.org"


class TelegramBot:
    """Telegram Bot API client."""
    
    def __init__(self, bot_token: str, config: Optional[TelegramConfig] = None):
        self.bot_token = bot_token
        self.config = config or TelegramConfig()
        self.base_url = f"{self.config.api_base_url}/bot{bot_token}"
        self.session = requests.Session()
    
    def _request(self, method: str, data: dict = None, files: dict = None) -> dict:
        """Make API request."""
        url = f"{self.base_url}/{method}"
        response = self.session.post(url, json=data, files=files)
        response.raise_for_status()
        result = response.json()
        if not result.get("ok"):
            raise Exception(f"API Error: {result.get('description', 'Unknown error')}")
        return result.get("result", {})
    
    def get_me(self) -> dict:
        """Get bot information."""
        return self._request("getMe")
    
    def send_message(self, chat_id: int, text: str, parse_mode: str = "Markdown", 
                     reply_to_message_id: Optional[int] = None) -> dict:
        """Send text message."""
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode
        }
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        return self._request("sendMessage", data)
    
    def send_photo(self, chat_id: int, photo: str, caption: Optional[str] = None) -> dict:
        """Send photo."""
        data = {
            "chat_id": chat_id,
            "photo": photo
        }
        if caption:
            data["caption"] = caption
        return self._request("sendPhoto", data)
    
    def send_document(self, chat_id: int, document: str, caption: Optional[str] = None) -> dict:
        """Send document."""
        data = {
            "chat_id": chat_id,
            "document": document
        }
        if caption:
            data["caption"] = caption
        return self._request("sendDocument", data)
    
    def send_audio(self, chat_id: int, audio: str, caption: Optional[str] = None) -> dict:
        """Send audio."""
        data = {
            "chat_id": chat_id,
            "audio": audio
        }
        if caption:
            data["caption"] = caption
        return self._request("sendAudio", data)
    
    def send_video(self, chat_id: int, video: str, caption: Optional[str] = None) -> dict:
        """Send video."""
        data = {
            "chat_id": chat_id,
            "video": video
        }
        if caption:
            data["caption"] = caption
        return self._request("sendVideo", data)
    
    def send_location(self, chat_id: int, latitude: float, longitude: float) -> dict:
        """Send location."""
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude
        }
        return self._request("sendLocation", data)
    
    def send_contact(self, chat_id: int, phone_number: str, first_name: str, 
                     last_name: Optional[str] = None) -> dict:
        """Send contact."""
        data = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name
        }
        if last_name:
            data["last_name"] = last_name
        return self._request("sendContact", data)
    
    def send_sticker(self, chat_id: int, sticker: str) -> dict:
        """Send sticker."""
        return self._request("sendSticker", {"chat_id": chat_id, "sticker": sticker})
    
    def send_venue(self, chat_id: int, latitude: float, longitude: float,
                   title: str, address: str) -> dict:
        """Send venue."""
        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "title": title,
            "address": address
        }
        return self._request("sendVenue", data)
    
    def send_media_group(self, chat_id: int, media: List[dict]) -> dict:
        """Send media group (album)."""
        data = {
            "chat_id": chat_id,
            "media": json.dumps(media)
        }
        return self._request("sendMediaGroup", data)
    
    def edit_message_text(self, chat_id: int, message_id: int, text: str) -> dict:
        """Edit message text."""
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }
        return self._request("editMessageText", data)
    
    def delete_message(self, chat_id: int, message_id: int) -> bool:
        """Delete message."""
        return self._request("deleteMessage", {"chat_id": chat_id, "message_id": message_id})
    
    def get_updates(self, offset: Optional[int] = None, limit: int = 100) -> List[dict]:
        """Get updates."""
        data = {"limit": limit}
        if offset:
            data["offset"] = offset
        return self._request("getUpdates", data)
    
    def set_webhook(self, url: str, certificate: Optional[str] = None) -> bool:
        """Set webhook URL."""
        data = {"url": url}
        if certificate:
            files = {"certificate": open(certificate, "rb")}
            result = self._request("setWebhook", data, files)
            files["certificate"].close()
            return result
        return self._request("setWebhook", data)
    
    def get_file(self, file_id: str) -> dict:
        """Get file information."""
        return self._request("getFile", {"file_id": file_id})
    
    def download_file(self, file_path: str, destination: str) -> str:
        """Download file to destination."""
        url = f"{self.config.api_base_url}/file/bot{self.bot_token}/{file_path}"
        response = self.session.get(url, stream=True)
        response.raise_for_status()
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return destination


def main():
    parser = argparse.ArgumentParser(
        description="Telegram Bot Integration Tool"
    )
    
    parser.add_argument("--token", "-t", required=True, help="Telegram Bot Token")
    
    sub = parser.add_subparsers(dest="cmd", help="Commands")
    
    # me
    sub.add_parser("me", help="Get bot information")
    
    # send
    send = sub.add_parser("send", help="Send message")
    send.add_argument("--chat-id", "-c", type=int, required=True, help="Chat ID")
    send.add_argument("--text", required=True, help="Message text")
    send.add_argument("--parse-mode", default="Markdown", choices=["Markdown", "HTML"], help="Parse mode")
    
    # send-photo
    photo = sub.add_parser("send-photo", help="Send photo")
    photo.add_argument("--chat-id", "-c", type=int, required=True, help="Chat ID")
    photo.add_argument("--photo", "-p", required=True, help="Photo URL or file path")
    photo.add_argument("--caption", help="Photo caption")
    
    # send-document
    doc = sub.add_parser("send-document", help="Send document")
    doc.add_argument("--chat-id", "-c", type=int, required=True, help="Chat ID")
    doc.add_argument("--document", "-d", required=True, help="Document path or URL")
    doc.add_argument("--caption", help="Document caption")
    
    # send-location
    loc = sub.add_parser("send-location", help="Send location")
    loc.add_argument("--chat-id", "-c", type=int, required=True, help="Chat ID")
    loc.add_argument("--lat", type=float, required=True, help="Latitude")
    loc.add_argument("--lon", type=float, required=True, help="Longitude")
    
    # get-updates
    updates = sub.add_parser("get-updates", help="Get updates")
    updates.add_argument("--offset", type=int, help="Update offset")
    updates.add_argument("--limit", type=int, default=100, help="Update limit")
    
    args = parser.parse_args()
    bot = TelegramBot(args.token)
    
    try:
        if args.cmd == "me":
            result = bot.get_me()
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send":
            result = bot.send_message(
                args.chat_id, args.text, 
                parse_mode=args.parse_mode
            )
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-photo":
            result = bot.send_photo(args.chat_id, args.photo, args.caption)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-document":
            result = bot.send_document(args.chat_id, args.document, args.caption)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-location":
            result = bot.send_location(args.chat_id, args.lat, args.lon)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "get-updates":
            result = bot.get_updates(args.offset, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
