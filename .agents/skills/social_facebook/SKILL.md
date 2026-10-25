# Facebook Graph API Integration Skill

**Version:** 1.0.0  
**Author:** Cursor Enterprise Framework  
**Triggers:** facebook, facebook api, facebook graph, facebook integration, meta

## Overview

This skill provides Facebook Graph API integration for Cursor Enterprise Framework. It enables page management, post creation, Messenger bot functionality, and analytics.

## Capabilities

- **Page Management**: Get page info, manage settings
- **Posting**: Create posts, upload photos, share links
- **Messenger**: Send messages, handle conversations
- **Comments**: Read and post comments
- **Analytics**: Get page insights and metrics

## Installation

```bash
pip install requests
```

Or use the bundled tool:
```bash
python tools/api_integrations/facebook_integration.py --help
```

## Configuration

### Facebook App Setup

1. Create a Facebook App at [Meta Developers](https://developers.facebook.com/)
2. Configure Facebook Login or Pages API
3. Generate a Page Access Token
4. Set required permissions

### Environment Variables

```bash
export FACEBOOK_ACCESS_TOKEN="your_page_access_token"
export FACEBOOK_PAGE_ID="your_page_id"
```

## Usage

### CLI Tool

```bash
# Get page info
python tools/api_integrations/facebook_integration.py --token TOKEN page-info --page-id PAGE_ID

# Create post
python tools/api_integrations/facebook_integration.py --token TOKEN post --page-id PAGE_ID --message "Hello World"

# Post with link
python tools/api_integrations/facebook_integration.py --token TOKEN post --page-id PAGE_ID --message "Check this out!" --link https://example.com

# Get posts
python tools/api_integrations/facebook_integration.py --token TOKEN posts --page-id PAGE_ID --limit 25

# Send Messenger message
python tools/api_integrations/facebook_integration.py --token TOKEN send-message --recipient USER_ID --message "Hello!"

# Get comments
python tools/api_integrations/facebook_integration.py --token TOKEN comments --post-id POST_ID

# Get insights
python tools/api_integrations/facebook_integration.py --token TOKEN insights --page-id PAGE_ID --metrics page_impressions page_views
```

### Python API

```python
from tools.api_integrations.facebook_integration import FacebookClient

# Initialize client
client = FacebookClient(access_token="PAGE_ACCESS_TOKEN")

# Get page info
info = client.get_page_info(page_id="PAGE_ID")
print(info)

# Create post
result = client.post_to_page(page_id="PAGE_ID", message="Hello, World!")
print(result)

# Post with image
result = client.post_to_page(
    page_id="PAGE_ID",
    message="Check this image!",
    image="/path/to/image.jpg"
)
```

## Post Types

### Text Post
```python
client.post_to_page(page_id="PAGE_ID", message="Hello, World!")
```

### Link Post
```python
client.post_to_page(
    page_id="PAGE_ID",
    message="Check this out!",
    link="https://example.com/article"
)
```

### Photo Post
```python
client.post_to_page(
    page_id="PAGE_ID",
    message="Beautiful sunset",
    image="/path/to/sunset.jpg"
)
```

### Photo with Link
```python
# Use post_to_page with both image and link parameters
```

## Messenger Integration

### Send Text Message
```python
client.send_message(recipient_id="USER_PSID", message="Hello!")
```

### Send Image
```python
client.send_attachment(
    recipient_id="USER_PSID",
    attachment_type="image",
    url="https://example.com/image.jpg"
)
```

### Send File
```python
client.send_attachment(
    recipient_id="USER_PSID",
    attachment_type="file",
    url="https://example.com/document.pdf"
)
```

## Comments Management

### Get Comments
```python
comments = client.get_comments(post_id="POST_ID", limit=50)
for comment in comments:
    print(f"{comment['from']['name']}: {comment['message']}")
```

### Post Comment
```python
client.post_comment(post_id="POST_ID", message="Great post!")
```

## Analytics

### Available Metrics

| Metric | Description |
|--------|-------------|
| `page_impressions` | Total impressions |
| `page_views` | Total views |
| `page_fan_count` | Total likes |
| `page_engagement` | Engagement rate |
| `page_reach` | Reach statistics |
| `page_views_demographics` | Audience demographics |

### Get Insights
```python
metrics = [
    "page_impressions",
    "page_views",
    "page_fan_count",
    "page_engagement"
]
insights = client.get_page_insights(page_id="PAGE_ID", metrics=metrics)
print(insights)
```

## Examples

### Auto-Poster
```python
from tools.api_integrations.facebook_integration import FacebookClient
import schedule

client = FacebookClient(access_token="TOKEN")

def post_daily():
    client.post_to_page(
        page_id="PAGE_ID",
        message="Daily update!",
        link="https://example.com/latest"
    )

# Schedule daily post
schedule.every().day.at("09:00").do(post_daily)
```

### Comment Auto-Reply
```python
def auto_reply(client, page_id):
    # Get recent posts
    posts = client.get_posts(page_id, limit=5)
    
    for post in posts:
        # Get comments
        comments = client.get_comments(post["id"])
        
        for comment in comments:
            # Check if not replied
            if not has_replied(comment["id"]):
                # Auto reply
                client.post_comment(
                    post_id=post["id"],
                    message="Thanks for your comment!"
                )
```

### Messenger Bot
```python
def handle_message(sender_id, message):
    if "hello" in message.lower():
        client.send_message(sender_id, "Hello! How can I help?")
    elif "help" in message.lower():
        client.send_message(sender_id, "Type 'products' to see our products")
    elif "products" in message.lower():
        client.send_attachment(sender_id, "image", "https://example.com/products.jpg")
    else:
        client.send_message(sender_id, "Thanks for your message!")
```

## Best Practices

1. **Token Management**: Use long-lived tokens, refresh periodically
2. **Rate Limiting**: Respect Graph API rate limits
3. **Permissions**: Only request necessary permissions
4. **Privacy**: Don't store user data unnecessarily
5. **Content Policy**: Follow Facebook's content policies

## Troubleshooting

### Token Expired
- Regenerate long-lived token
- Implement token refresh logic

### Permission Denied
- Verify required permissions
- Re-authorize the app

### Rate Limited
- Implement exponential backoff
- Cache frequently accessed data

## References

- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Meta Developers](https://developers.facebook.com/)
- [Messenger Platform](https://developers.facebook.com/docs/messenger-platform)

## License

MIT License - See bundled LICENSE file
