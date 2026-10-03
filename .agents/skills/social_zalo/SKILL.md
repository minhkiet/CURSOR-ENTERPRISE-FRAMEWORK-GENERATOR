# Zalo API Integration Skill

**Version:** 1.0.0  
**Author:** Cursor Enterprise Framework  
**Triggers:** zalo, zalo api, zalo integration, zalo messaging

## Overview

This skill provides Zalo API integration for Cursor Enterprise Framework. It enables sending messages, managing Official Accounts (OA), accessing user profiles, and more.

## Capabilities

- **Messaging**: Send text messages, images, links, and rich media
- **Official Account (OA) Management**: Create menus, manage followers
- **User Profile**: Get user information and profile data
- **Social Features**: Handle social interactions

## Installation

```bash
pip install requests
```

Or use the bundled tool:
```bash
python tools/api_integrations/zalo_integration.py --help
```

## Configuration

### Environment Variables

```bash
export ZALO_ACCESS_TOKEN="your_access_token"
export ZALO_OA_ID="your_oa_id"
```

### Token Setup

1. Register at [Zalo Developers](https://developers.zalo.me/)
2. Create an application
3. Get your access token from the developer dashboard
4. Configure OAuth for your application

## Usage

### CLI Tool

```bash
# Get user profile
python tools/api_integrations/zalo_integration.py --token TOKEN profile --uid USER_ID

# Send message
python tools/api_integrations/zalo_integration.py --token TOKEN send --uid USER_ID --message "Hello"

# Send image
python tools/api_integrations/zalo_integration.py --token TOKEN send-image --uid USER_ID --image URL --caption "Caption"

# Send link
python tools/api_integrations/zalo_integration.py --token TOKEN send-link --uid USER_ID --url https://example.com --title "Title"

# Get followers
python tools/api_integrations/zalo_integration.py --token TOKEN followers --offset 0 --limit 100
```

### Python API

```python
from tools.api_integrations.zalo_integration import ZaloClient

# Initialize client
client = ZaloClient(access_token="YOUR_TOKEN")

# Get user profile
profile = client.get_user_profile(user_id="USER_ID")
print(profile)

# Send message
result = client.send_message(user_id="USER_ID", message="Hello!")
print(result)

# Send image
result = client.send_image(user_id="USER_ID", image_url="https://example.com/image.jpg", caption="Caption")
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v2.0/me` | GET | Get user profile |
| `/v2.0/me/sendmsg` | POST | Send message |
| `/v2.0/me/followers` | GET | Get followers |
| `/v2.0/me/createMenu` | POST | Create OA menu |

## Message Types

### Text Message
```python
client.send_message(user_id="USER_ID", message="Hello, World!")
```

### Image Message
```python
client.send_image(
    user_id="USER_ID",
    image_url="https://example.com/image.jpg",
    caption="Image caption"
)
```

### Link Message
```python
client.send_link(
    user_id="USER_ID",
    link_url="https://example.com",
    link_title="Example Link",
    link_desc="Link description"
)
```

## Best Practices

1. **Token Management**: Store tokens securely, rotate periodically
2. **Rate Limiting**: Respect Zalo's API rate limits
3. **Error Handling**: Implement retry logic for failed requests
4. **User Privacy**: Only request necessary permissions

## Troubleshooting

### Authentication Errors
- Verify your access token is valid
- Check token expiration
- Ensure OAuth is properly configured

### Message Delivery Issues
- Verify user ID is correct
- Check if user has blocked your OA
- Ensure message content complies with Zalo policies

### Rate Limiting
- Implement exponential backoff
- Cache frequently accessed data
- Batch requests when possible

## Examples

### Automated Response System
```python
from tools.api_integrations.zalo_integration import ZaloClient

client = ZaloClient(access_token="TOKEN")

def handle_message(user_id, message):
    responses = {
        "hello": "Chào bạn!",
        "help": "Gõ 'products' để xem sản phẩm",
        "products": "Danh sách sản phẩm: ...",
    }
    
    reply = responses.get(message.lower(), "Cảm ơn bạn đã nhắn tin!")
    client.send_message(user_id, reply)
```

### Broadcast Messages
```python
def broadcast(client, user_ids, message):
    results = []
    for user_id in user_ids:
        try:
            result = client.send_message(user_id, message)
            results.append({"user_id": user_id, "success": True})
        except Exception as e:
            results.append({"user_id": user_id, "success": False, "error": str(e)})
    return results
```

## References

- [Zalo Developers](https://developers.zalo.me/)
- [Zalo API Documentation](https://developers.zalo.me/docs/)
- [Zalo SDK](https://github.com/zalo/zalo-sdk-python)

## License

MIT License - See bundled LICENSE file
