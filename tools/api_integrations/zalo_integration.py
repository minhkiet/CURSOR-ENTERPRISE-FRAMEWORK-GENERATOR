#!/usr/bin/env python
"""
Zalo API Integration Tool

Provides Zalo API integration for:
- Sending messages
- Managing Official Accounts (OA)
- User profile access
- Rich media messages
- Social features

Usage:
    python zalo_integration.py send --token TOKEN --uid UID --message "Hello"
    python zalo_integration.py profile --token TOKEN --uid UID
    python zalo_integration.py send-image --token TOKEN --uid UID --image path/to/image.jpg
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


@dataclass
class ZaloConfig:
    """Zalo API configuration."""
    api_base_url: str = "https://graph.zalo.me"
    official_api_url: str = "https://openapi.zalo.me"


class ZaloClient:
    """Zalo API client."""
    
    def __init__(self, access_token: str, config: Optional[ZaloConfig] = None):
        self.access_token = access_token
        self.config = config or ZaloConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "access_token": access_token,
            "Content-Type": "application/json"
        })
    
    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile information."""
        url = f"{self.config.api_base_url}/v2.0/me"
        params = {"fields": "id,name,picture"}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def send_message(self, user_id: str, message: str) -> dict:
        """Send text message to user."""
        url = f"{self.config.official_api_url}/v2.0/me/sendmsg"
        payload = {
            "recipient": {"user_id": user_id},
            "message": {"text": message}
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def send_image(self, user_id: str, image_url: str, caption: Optional[str] = None) -> dict:
        """Send image message to user."""
        url = f"{self.config.official_api_url}/v2.0/me/sendmsg"
        payload = {
            "recipient": {"user_id": user_id},
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": image_url
                    }
                }
            }
        }
        if caption:
            payload["message"]["text"] = caption
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def send_link(self, user_id: str, link_url: str, link_title: str, link_desc: Optional[str] = None) -> dict:
        """Send link/message with URL."""
        url = f"{self.config.official_api_url}/v2.0/me/sendmsg"
        payload = {
            "recipient": {"user_id": user_id},
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "elements": [{
                            "title": link_title,
                            "subtitle": link_desc or "",
                            "default_action": {
                                "type": "web_url",
                                "url": link_url
                            }
                        }]
                    }
                }
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def create_menu(self, menu_data: dict) -> dict:
        """Create OA menu."""
        url = f"{self.config.official_api_url}/v2.0/me/createMenu"
        response = self.session.post(url, json=menu_data)
        response.raise_for_status()
        return response.json()
    
    def get_followers(self, offset: int = 0, limit: int = 100) -> dict:
        """Get list of followers."""
        url = f"{self.config.api_base_url}/v2.0/me/followers"
        params = {"offset": offset, "limit": limit}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Zalo API Integration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--token", "-t", required=True, help="Zalo access token")
    
    sub = parser.add_parser("profile", help="Get user profile")
    sub.add_argument("--uid", "-u", required=True, help="User ID")
    
    msg = sub.add_parser("send", help="Send message")
    msg.add_argument("--uid", "-u", required=True, help="User ID")
    msg.add_argument("--message", "-m", required=True, help="Message text")
    
    img = sub.add_parser("send-image", help="Send image")
    img.add_argument("--uid", "-u", required=True, help="User ID")
    img.add_argument("--image", "-i", required=True, help="Image URL or path")
    img.add_argument("--caption", "-c", help="Image caption")
    
    link = sub.add_parser("send-link", help="Send link")
    link.add_argument("--uid", "-u", required=True, help="User ID")
    link.add_argument("--url", "-u", dest="link_url", required=True, help="Link URL")
    link.add_argument("--title", required=True, help="Link title")
    link.add_argument("--desc", help="Link description")
    
    followers = sub.add_parser("followers", help="Get followers")
    followers.add_argument("--offset", type=int, default=0, help="Offset")
    followers.add_argument("--limit", type=int, default=100, help="Limit")
    
    args = parser.parse_args()
    client = ZaloClient(args.token)
    
    try:
        if args.cmd == "profile":
            result = client.get_user_profile(args.uid)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send":
            result = client.send_message(args.uid, args.message)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-image":
            result = client.send_image(args.uid, args.image, args.caption)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-link":
            result = client.send_link(args.uid, args.link_url, args.title, args.desc)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "followers":
            result = client.get_followers(args.offset, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
