#!/usr/bin/env python
"""
Facebook Graph API Integration Tool

Provides Facebook Graph API integration for:
- Page management
- Post creation
- Messenger bot
- Analytics
- Ad management

Usage:
    python facebook_integration.py post --token TOKEN --page-id PAGE_ID --message "Hello"
    python facebook_integration.py page-info --token TOKEN --page-id PAGE_ID
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
class FacebookConfig:
    """Facebook API configuration."""
    api_version: str = "v18.0"
    graph_url: str = "https://graph.facebook.com"
    messaging_url: str = "https://graph.facebook.com/me/messages"


class FacebookClient:
    """Facebook Graph API client."""
    
    def __init__(self, access_token: str, config: Optional[FacebookConfig] = None):
        self.access_token = access_token
        self.config = config or FacebookConfig()
        self.base_url = self.config.graph_url
        self.session = requests.Session()
        self.session.params = {"access_token": access_token}
    
    def _request(self, method: str, endpoint: str, data: dict = None, files: dict = None) -> dict:
        """Make API request."""
        url = f"{self.base_url}/{endpoint}"
        response = self.session.request(method, url, json=data, files=files)
        response.raise_for_status()
        return response.json()
    
    def get_page_info(self, page_id: str) -> dict:
        """Get page information."""
        return self._request("GET", f"/{self.config.api_version}/{page_id}")
    
    def post_to_page(self, page_id: str, message: str, link: Optional[str] = None,
                     image: Optional[str] = None) -> dict:
        """Create a post on the page."""
        endpoint = f"/{self.config.api_version}/{page_id}/feed"
        data = {"message": message}
        
        if link:
            data["link"] = link
        if image:
            files = {"source": open(image, "rb")} if isinstance(image, str) else image
            return self._request("POST", endpoint, data, files)
        
        return self._request("POST", endpoint, data)
    
    def get_posts(self, page_id: str, limit: int = 25) -> List[dict]:
        """Get page posts."""
        endpoint = f"/{self.config.api_version}/{page_id}/posts"
        params = {"limit": limit}
        response = self._request("GET", endpoint, params)
        return response.get("data", [])
    
    def send_message(self, recipient_id: str, message: str) -> dict:
        """Send message via Messenger."""
        endpoint = f"/{self.config.api_version}/me/messages"
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message}
        }
        return self._request("POST", endpoint, data)
    
    def send_attachment(self, recipient_id: str, attachment_type: str, url: str) -> dict:
        """Send attachment via Messenger."""
        endpoint = f"/{self.config.api_version}/me/messages"
        data = {
            "recipient": {"id": recipient_id},
            "message": {
                "attachment": {
                    "type": attachment_type,
                    "payload": {"url": url, "is_reusable": True}
                }
            }
        }
        return self._request("POST", endpoint, data)
    
    def get_comments(self, post_id: str, limit: int = 50) -> List[dict]:
        """Get comments on a post."""
        endpoint = f"/{self.config.api_version}/{post_id}/comments"
        params = {"limit": limit}
        response = self._request("GET", endpoint, params)
        return response.get("data", [])
    
    def post_comment(self, post_id: str, message: str) -> dict:
        """Post a comment on a post."""
        endpoint = f"/{self.config.api_version}/{post_id}/comments"
        data = {"message": message}
        return self._request("POST", endpoint, data)
    
    def get_page_insights(self, page_id: str, metrics: List[str]) -> dict:
        """Get page insights/metrics."""
        endpoint = f"/{self.config.api_version}/{page_id}/insights"
        params = {"metric": ",".join(metrics)}
        return self._request("GET", endpoint, params)
    
    def get_conversations(self, page_id: str, limit: int = 50) -> List[dict]:
        """Get page conversations."""
        endpoint = f"/{self.config.api_version}/{page_id}/conversations"
        params = {"limit": limit}
        response = self._request("GET", endpoint, params)
        return response.get("data", [])
    
    def upload_photo(self, page_id: str, image_path: str, caption: Optional[str] = None) -> dict:
        """Upload photo to page."""
        endpoint = f"/{self.config.api_version}/{page_id}/photos"
        data = {}
        if caption:
            data["caption"] = caption
        files = {"source": open(image_path, "rb")}
        return self._request("POST", endpoint, data, files)


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Graph API Integration Tool"
    )
    
    parser.add_argument("--token", "-t", required=True, help="Facebook Access Token")
    
    sub = parser.add_subparsers(dest="cmd", help="Commands")
    
    # page-info
    info = sub.add_parser("page-info", help="Get page information")
    info.add_argument("--page-id", "-p", required=True, help="Page ID")
    
    # post
    post = sub.add_parser("post", help="Create a post")
    post.add_argument("--page-id", "-p", required=True, help="Page ID")
    post.add_argument("--message", "-m", required=True, help="Post message")
    post.add_argument("--link", "-l", help="Link to include")
    post.add_argument("--image", "-i", help="Image path")
    
    # posts
    posts = sub.add_parser("posts", help="Get page posts")
    posts.add_argument("--page-id", "-p", required=True, help="Page ID")
    posts.add_argument("--limit", type=int, default=25, help="Number of posts")
    
    # send-message
    msg = sub.add_parser("send-message", help="Send Messenger message")
    msg.add_argument("--recipient", "-r", required=True, help="Recipient ID")
    msg.add_argument("--message", "-m", required=True, help="Message text")
    
    # comments
    comments = sub.add_parser("comments", help="Get post comments")
    comments.add_argument("--post-id", required=True, help="Post ID")
    comments.add_argument("--limit", type=int, default=50, help="Number of comments")
    
    # insights
    insights = sub.add_parser("insights", help="Get page insights")
    insights.add_argument("--page-id", "-p", required=True, help="Page ID")
    insights.add_argument("--metrics", nargs="+", default=["page_impressions"], help="Metrics")
    
    args = parser.parse_args()
    client = FacebookClient(args.token)
    
    try:
        if args.cmd == "page-info":
            result = client.get_page_info(args.page_id)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "post":
            result = client.post_to_page(args.page_id, args.message, args.link, args.image)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "posts":
            result = client.get_posts(args.page_id, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "send-message":
            result = client.send_message(args.recipient, args.message)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "comments":
            result = client.get_comments(args.post_id, args.limit)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif args.cmd == "insights":
            result = client.get_page_insights(args.page_id, args.metrics)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        return 0
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
