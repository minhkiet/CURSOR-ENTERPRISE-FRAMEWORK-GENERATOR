# Facebook Graph API Integration Skill

> **Version:** 1.0.0  
> **Platform:** Facebook Graph API  
> **Use case:** Page management, messaging, marketing automation

## Overview

Facebook Graph API cung cấp interface để tương tác với Facebook Pages, Groups, Users, và Ads. Skill này hỗ trợ Page management, messaging, post scheduling, và analytics.

## API Capabilities

### 1. Page Management

| Feature | Endpoint | Description |
|----------|----------|-------------|
| Get Page Info | `/me` | Thông tin Page |
| Get Posts | `/me/posts` | Danh sách bài viết |
| Create Post | `/me/feed` | Tạo bài viết mới |
| Get Comments | `/{post-id}/comments` | Lấy comments |
| Get Insights | `/{post-id}/insights` | Metrics của bài viết |

### 2. Messenger Platform

| Feature | Endpoint | Description |
|----------|----------|-------------|
| Send Message | `/me/messages` | Gửi message |
| Set Webhook | Webhook | Nhận incoming messages |
| Get Conversations | `/me/conversations` | Danh sách conversations |
| Send Template | `/me/messages` | Gửi rich template |

### 3. Media & Stories

| Feature | Endpoint | Description |
|----------|----------|-------------|
| Upload Photo | `/me/photos` | Upload ảnh lên Page |
| Upload Video | `/me/videos` | Upload video |
| Create Album | `/me/albums` | Tạo album ảnh |

## Quick Start

### 1. Setup Facebook App

1. Go to [Facebook Developer Console](https://developers.facebook.com)
2. Create new App → Choose "Business" or "Other"
3. Add products: **Facebook Login**, **Messenger**, **Pages**
4. Configure App Settings

### 2. Get Access Token

```bash
# 1. Get User Access Token via Graph API Explorer
# https://developers.facebook.com/tools/explorer/

# 2. Request permissions:
# - pages_manage_metadata
# - pages_read_engagement
# - pages_manage_posts
# - messenger_management

# 3. Exchange for Long-Lived Token (60 days)
curl -i -X GET \
  "https://graph.facebook.com/v18.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id=APP_ID&\
client_secret=APP_SECRET&\
fb_exchange_token=SHORT_LIVED_TOKEN"
```

### 3. Python Integration

```python
from tools.api_integrations.facebook_integration import FacebookClient

# Initialize with Page access token
client = FacebookClient(
    page_access_token="PAGE_ACCESS_TOKEN",
    app_id="APP_ID",
    app_secret="APP_SECRET"
)

# Get page info
page = client.get_page_info()
print(f"Page: {page['name']}")
print(f"Followers: {page['followers_count']}")

# Create post
post = client.create_post(
    message="Hello from Facebook API! 👋",
    link="https://example.com"
)
print(f"Post ID: {post['id']}")

# Get recent posts
posts = client.get_posts(limit=10)
for post in posts['data']:
    print(f"- {post['message'][:50]}...")
```

## Message Templates

### 1. Text Message

```python
client.send_message(
    recipient_id="USER_PSID",
    message={"text": "Hello! How can I help you?"}
)
```

### 2. Generic Template (Carousel)

```python
client.send_message(
    recipient_id="USER_PSID",
    message={
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Product 1",
                        "subtitle": "$99.99",
                        "image_url": "https://example.com/product1.jpg",
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "https://shop.example.com/p1",
                                "title": "View"
                            },
                            {
                                "type": "postback",
                                "title": "Add to Cart",
                                "payload": "ADD_TO_CART_1"
                            }
                        ]
                    },
                    {
                        "title": "Product 2",
                        "subtitle": "$149.99",
                        "image_url": "https://example.com/product2.jpg",
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "https://shop.example.com/p2",
                                "title": "View"
                            }
                        ]
                    }
                ]
            }
        }
    }
)
```

### 3. Button Template

```python
client.send_message(
    recipient_id="USER_PSID",
    message={
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": "What would you like to do?",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "View Products",
                        "payload": "VIEW_PRODUCTS"
                    },
                    {
                        "type": "web_url",
                        "url": "https://shop.example.com",
                        "title": "Visit Store"
                    }
                ]
            }
        }
    }
)
```

### 4. List Template

```python
client.send_message(
    recipient_id="USER_PSID",
    message={
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "elements": [
                    {
                        "title": "Category: Electronics",
                        "image_url": "https://example.com/electronics.jpg",
                        "subtitle": "View our electronics",
                        "default_action": {
                            "type": "web_url",
                            "url": "https://shop.example.com/electronics"
                        }
                    },
                    {
                        "title": "Category: Fashion",
                        "image_url": "https://example.com/fashion.jpg",
                        "subtitle": "Shop fashion items",
                        "default_action": {
                            "type": "web_url",
                            "url": "https://shop.example.com/fashion"
                        }
                    }
                ],
                "buttons": [
                    {
                        "type": "web_url",
                        "url": "https://shop.example.com",
                        "title": "View All"
                    }
                ]
            }
        }
    }
)
```

## Webhook Integration

### Flask Webhook Server

```python
from flask import Flask, request, jsonify
from tools.api_integrations.facebook_integration import FacebookClient
import os
import hmac
import hashlib

app = Flask(__name__)
client = FacebookClient(
    page_access_token=os.environ["PAGE_TOKEN"],
    app_secret=os.environ["APP_SECRET"]
)

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """Webhook verification for Facebook."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == os.environ["VERIFY_TOKEN"]:
        return challenge, 200
    return "Verification failed", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    """Handle incoming webhook events."""
    body = request.get_json()
    
    if body.get("object") == "page":
        for entry in body.get("entry", []):
            for event in entry.get("messaging", []):
                if "message" in event:
                    sender_id = event["sender"]["id"]
                    message_text = event["message"].get("text", "")
                    
                    # Echo back
                    client.send_message(
                        recipient_id=sender_id,
                        message={"text": f"You said: {message_text}"}
                    )
                
                elif "postback" in event:
                    sender_id = event["sender"]["id"]
                    payload = event["postback"]["payload"]
                    
                    # Handle postback
                    client.send_message(
                        recipient_id=sender_id,
                        message={"text": f"Received payload: {payload}"}
                    )
    
    return "OK", 200

if __name__ == "__main__":
    app.run(port=5000)
```

## Page Management

### 1. Schedule Post

```python
from datetime import datetime, timedelta

# Schedule for 2 hours from now
publish_time = datetime.now() + timedelta(hours=2)

post = client.create_post(
    message="Scheduled post! ⏰",
    scheduled_publish_time=int(publish_time.timestamp()),
    unpublished_content_type="SCHEDULED"
)
print(f"Scheduled Post ID: {post['id']}")
```

### 2. Upload Photo Album

```python
# Create album
album = client.create_album(
    name="Product Launch 2024",
    message="New products coming soon!"
)

# Upload photos
photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
for photo in photos:
    client.upload_photo(
        url=photo,
        caption=f"Product photo: {photo}",
        album_id=album['id']
    )
```

### 3. Get Page Insights

```python
# Get page metrics
insights = client.get_page_insights(
    metrics=[
        "page_impressions",
        "page_reach",
        "page_views",
        "page_fan_count",
        "page_post_engagements"
    ],
    period="day"
)

for metric in insights['data']:
    print(f"{metric['name']}: {metric['values'][0]['value']}")
```

## Best Practices

### 1. Error Handling

```python
from tools.api_integrations.facebook_integration import FacebookClient
import requests

client = FacebookClient(page_access_token="TOKEN")

try:
    result = client.send_message("PSID", {"text": "Hello"})
except requests.exceptions.HTTPError as e:
    error = e.response.json()
    error_code = error.get("error", {}).get("code")
    error_msg = error.get("error", {}).get("message")
    
    if error_code == 190:  # Token expired
        print("Access token expired, need to refresh")
    elif error_code == 100:  # Invalid parameter
        print(f"Invalid request: {error_msg}")
    elif error_code == 10:  # Permission denied
        print("Insufficient permissions")
    elif error_code == 368:  # Blocked by user
        print("User blocked the page")
```

### 2. Rate Limiting

Facebook has strict rate limits:
- API calls: 200/hour per Page
- Messages: 1000/hour per Page

```python
import time

def send_with_backoff(client, recipient, message, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.send_message(recipient, message)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 60 * (attempt + 1)  # Backoff
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Rate limit exceeded")
```

### 3. Token Refresh

```python
# Refresh long-lived token (extend to 60 days)
new_token = client.refresh_access_token()
print(f"New token expires at: {new_token['expires_at']}")
```

## Security

### 1. App Secret Proof

```python
# For sensitive API calls, include appsecret_proof
client = FacebookClient(
    page_access_token="TOKEN",
    app_id="APP_ID",
    app_secret="APP_SECRET"
)

# The SDK handles appsecret_proof automatically
```

### 2. Verify Webhook

```python
def verify_facebook_webhook(request, app_secret):
    """Verify webhook signature from Facebook."""
    signature = request.headers.get("X-Hub-Signature-256")
    
    if not signature:
        return False
    
    # Parse signature
    expected = hmac.new(
        app_secret.encode(),
        request.get_data(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## Integration with Cursor Framework

### Slash Command

```
/facebook post "Hello from Cursor!"
/facebook send "USER_PSID" "Hello!"
/facebook insights
```

### Workflow Example

```yaml
# .cursor/workflows/facebook-auto-reply.yaml
name: Facebook Auto Reply
trigger:
  type: webhook
  source: facebook-messenger

steps:
  - name: Parse message
    action: facebook.parse_message
    output: parsed

  - name: Generate response
    action: ai.generate
    prompt: "Customer asked: {{ parsed.text }}\nGenerate a helpful response."

  - name: Send reply
    action: facebook.send_message
    params:
      recipient_id: "{{ parsed.sender_id }}"
      message: "{{ generated_response }}"
```

## References

- [Facebook Graph API Documentation](https://developers.facebook.com/docs/graph-api)
- [Messenger Platform](https://developers.facebook.com/docs/messenger-platform)
- [Page API](https://developers.facebook.com/docs/pages)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
