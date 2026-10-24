#!/usr/bin/env python
"""
Zalo Integration MCP Tool

MCP tool for Zalo API integration.
Provides tools for sending messages, managing OA, and Mini App development.

Usage:
    python zalo_mcp_tool.py --help
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
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests


@dataclass
class ZaloConfig:
    """Zalo API configuration."""
    api_base_url: str = "https://graph.zalo.me"
    official_api_url: str = "https://openapi.zalo.me"


class ZaloMCPClient:
    """Zalo API client for MCP tool."""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.config = ZaloConfig()
        self.session = requests.Session()
        self.session.headers.update({
            "access_token": access_token,
            "Content-Type": "application/json"
        })
    
    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile information."""
        url = f"{self.config.api_base_url}/v2.0/me"
        params = {"fields": "id,name,picture"}
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": str(e)}
    
    def send_message(self, user_id: str, message: str) -> dict:
        """Send text message to user."""
        url = f"{self.config.official_api_url}/v2.0/me/sendmsg"
        payload = {
            "recipient": {"user_id": user_id},
            "message": {"text": message}
        }
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": str(e)}
    
    def send_image(self, user_id: str, image_url: str, caption: Optional[str] = None) -> dict:
        """Send image message to user."""
        url = f"{self.config.official_api_url}/v2.0/me/sendmsg"
        payload = {
            "recipient": {"user_id": user_id},
            "message": {
                "attachment": {
                    "type": "image",
                    "payload": {"url": image_url}
                }
            }
        }
        if caption:
            payload["message"]["text"] = caption
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": str(e)}
    
    def get_followers(self, offset: int = 0, limit: int = 100) -> dict:
        """Get list of followers."""
        url = f"{self.config.api_base_url}/v2.0/me/followers"
        params = {"offset": offset, "limit": limit}
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Zalo MCP Tool")
    parser.add_argument("--token", required=True, help="Zalo access token")
    parser.add_argument("--action", choices=["profile", "send", "send-image", "followers"], 
                       required=True, help="Action to perform")
    parser.add_argument("--uid", help="User ID")
    parser.add_argument("--message", help="Message text")
    parser.add_argument("--image", help="Image URL")
    parser.add_argument("--caption", help="Image caption")
    
    args = parser.parse_args()
    
    client = ZaloMCPClient(args.token)
    
    result = None
    if args.action == "profile":
        result = client.get_user_profile(args.uid)
    elif args.action == "send":
        result = client.send_message(args.uid, args.message)
    elif args.action == "send-image":
        result = client.send_image(args.uid, args.image, args.caption)
    elif args.action == "followers":
        result = client.get_followers()
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
