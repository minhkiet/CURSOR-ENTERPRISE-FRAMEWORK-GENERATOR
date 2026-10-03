# Telegram Bot Integration Skill

**Version:** 1.0.0  
**Author:** Cursor Enterprise Framework  
**Triggers:** telegram, telegram bot, telegram api, telegram integration

## Overview

This skill provides Telegram Bot API integration for Cursor Enterprise Framework. It enables building chatbots, automating messaging, managing groups, and more.

## Capabilities

- **Messaging**: Send text, photos, documents, audio, video, stickers
- **Location & Contact**: Share locations and contact cards
- **Inline Queries**: Handle inline query bots
- **Commands**: Support for bot commands and keyboard
- **Groups**: Manage group chats and permissions

## Installation

```bash
pip install requests
```

Or use the bundled tool:
```bash
python tools/api_integrations/telegram_integration.py --help
```

## Configuration

### Environment Variables

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

### Bot Setup

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram
2. Get your bot token
3. Configure webhook or polling for updates

## Usage

### CLI Tool

```bash
# Get bot info
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN me

# Send message
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN send --chat-id 123456 --text "Hello"

# Send photo
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN send-photo --chat-id 123456 --photo URL --caption "Caption"

# Send document
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN send-document --chat-id 123456 --document /path/to/file

# Send location
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN send-location --chat-id 123456 --lat 10.8231 --lon 106.6297

# Get updates
python tools/api_integrations/telegram_integration.py --token BOT_TOKEN get-updates
```

### Python API

```python
from tools.api_integrations.telegram_integration import TelegramBot

# Initialize bot
bot = TelegramBot(bot_token="BOT_TOKEN")

# Get bot info
me = bot.get_me()
print(me)

# Send message
result = bot.send_message(chat_id=123456, text="Hello!")
print(result)

# Send photo
result = bot.send_photo(chat_id=123456, photo="https://example.com/image.jpg", caption="Caption")

# Send location
result = bot.send_location(chat_id=123456, latitude=10.8231, longitude=106.6297)
```

## Message Types

### Text Message
```python
bot.send_message(chat_id=123456, text="Hello, World!")
```

### Photo
```python
bot.send_photo(
    chat_id=123456,
    photo="https://example.com/image.jpg",
    caption="Image caption"
)
```

### Document
```python
bot.send_document(
    chat_id=123456,
    document="/path/to/file.pdf",
    caption="Document caption"
)
```

### Location
```python
bot.send_location(chat_id=123456, latitude=10.8231, longitude=106.6297)
```

### Venue
```python
bot.send_venue(
    chat_id=123456,
    latitude=10.8231,
    longitude=106.6297,
    title="Location Name",
    address="123 Street, City"
)
```

### Contact
```python
bot.send_contact(
    chat_id=123456,
    phone_number="+84912345678",
    first_name="John",
    last_name="Doe"
)
```

### Sticker
```python
bot.send_sticker(chat_id=123456, sticker="CAACAgIAAxk...")
```

## Inline Keyboards

```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot(bot_token="BOT_TOKEN")

# Create inline keyboard
reply_markup = {
    "inline_keyboard": [
        [
            {"text": "Option 1", "callback_data": "opt1"},
            {"text": "Option 2", "callback_data": "opt2"}
        ],
        [{"text": "Link", "url": "https://example.com"}]
    ]
}

bot.send_message(
    chat_id=123456,
    text="Choose an option:",
    reply_markup=json.dumps(reply_markup)
)
```

## Examples

### Simple Chatbot
```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot(bot_token="BOT_TOKEN")

def handle_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        
        if text == "/start":
            bot.send_message(chat_id, "Welcome! Type /help for commands.")
        elif text == "/help":
            bot.send_message(chat_id, "Available commands:\n/start - Start\n/help - Help")
        else:
            bot.send_message(chat_id, f"You said: {text}")

# Poll for updates
while True:
    updates = bot.get_updates()
    for update in updates:
        handle_update(update)
```

### Broadcast System
```python
def broadcast(bot, chat_ids, message):
    results = []
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id, message)
            results.append({"chat_id": chat_id, "success": True})
        except Exception as e:
            results.append({"chat_id": chat_id, "success": False, "error": str(e)})
    return results
```

## Best Practices

1. **Error Handling**: Implement proper exception handling
2. **Rate Limiting**: Respect Telegram's rate limits (30 msg/sec)
3. **Security**: Validate all incoming data
4. **Privacy**: Don't store sensitive user data unnecessarily
5. **UX**: Use appropriate message types for content

## Troubleshooting

### Bot Not Responding
- Verify bot token is correct
- Check if bot is blocked by user
- Ensure webhook/polling is configured

### Rate Limit Exceeded
- Implement delays between messages
- Use batch operations when possible
- Consider using supergroups for bulk messaging

### File Upload Issues
- Check file size limits (50MB for documents)
- Ensure file URL is publicly accessible
- Use correct MIME types

## References

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [BotFather](https://t.me/BotFather)
- [Bot Examples](https://core.telegram.org/bots/examples)

## License

MIT License - See bundled LICENSE file
