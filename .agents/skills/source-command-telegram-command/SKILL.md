# Telegram Bot Integration Skill

> **Version:** 1.0.0  
> **Platform:** Telegram Bot API  
> **Use case:** Bot development, group management, notifications

## Overview

Telegram Bot API cung cấp platform mạnh mẽ để xây dựng bot cho Telegram. Skill này hỗ trợ đầy đủ các tính năng: messaging, media, inline queries, payments, và webhook integration.

## API Capabilities

### Core Features

| Feature | Method | Description |
|----------|--------|-------------|
| Send Message | `sendMessage` | Gửi text với Markdown/HTML |
| Send Photo | `sendPhoto` | Gửi ảnh với caption |
| Send Document | `sendDocument` | Gửi file (PDF, DOC, etc.) |
| Send Media Group | `sendMediaGroup` | Gửi album (10 items max) |
| Send Location | `sendLocation` | Gửi GPS coordinates |
| Send Contact | `sendContact` | Gửi contact card |
| Send Sticker | `sendSticker` | Gửi sticker |

### Advanced Features

| Feature | Method | Description |
|---------|--------|-------------|
| Inline Mode | `answerInlineQuery` | Search & select interface |
| Payments | `sendInvoice` | Telegram Payments 5.0 |
| Games | `sendGame` | HTML5 games in chat |
| Passport | `setPassportDataRequest` | KYC integration |
| Quiz Bot | `sendQuiz` | Interactive quizzes |

## Quick Start

### 1. Create Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Follow prompts to set name and username
4. Copy the **Bot Token** (e.g., `123456789:ABCdefGHIjklMNOpqrSTUvwxyz`)

### 2. Python Integration

```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot(bot_token="YOUR_BOT_TOKEN")

# Get bot info
me = bot.get_me()
print(f"Bot: {me['username']}")

# Send message
bot.send_message(chat_id=123456789, text="Hello! 👋")

# Send with HTML formatting
bot.send_message(
    chat_id=123456789,
    text="<b>Bold</b> and <i>italic</i> text",
    parse_mode="HTML"
)

# Send photo
bot.send_photo(
    chat_id=123456789,
    photo="https://example.com/image.jpg",
    caption="Check this out!"
)
```

### 3. CLI Usage

```bash
# Get bot info
python tools/api_integrations/telegram_integration.py me --token TOKEN

# Send message
python tools/api_integrations/telegram_integration.py send --token TOKEN --chat-id 123 --text "Hello"

# Send photo
python tools/api_integrations/telegram_integration.py send-photo --token TOKEN --chat-id 123 --photo URL

# Send location
python tools/api_integrations/telegram_integration.py send-location --token TOKEN --chat-id 123 --lat 10.8231 --lon 106.6297
```

## Bot Development Patterns

### 1. Webhook Server (Flask)

```python
from flask import Flask, request, jsonify
from tools.api_integrations.telegram_integration import TelegramBot
import os

app = Flask(__name__)
bot = TelegramBot(os.environ["BOT_TOKEN"])

@app.route(f"/webhook/{os.environ['WEBHOOK_SECRET']}", methods=["POST"])
def webhook():
    update = request.get_json()
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        
        # Echo bot
        if text == "/start":
            bot.send_message(chat_id, "Welcome! 👋")
        elif text == "/help":
            bot.send_message(chat_id, "Commands:\n/start - Start\n/help - Help")
        else:
            bot.send_message(chat_id, f"You said: {text}")
    
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(port=5000)
```

### 2. Long Polling (for development)

```python
import time
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot("BOT_TOKEN")
offset = 0

print("Bot started. Press Ctrl+C to stop.")

while True:
    updates = bot.get_updates(offset=offset)
    
    for update in updates:
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "")
            
            bot.send_message(chat_id, f"Echo: {text}")
            offset = update["update_id"] + 1
    
    time.sleep(1)  # Poll every second
```

### 3. Inline Query Handler

```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot("BOT_TOKEN")

def handle_inline_query(query_id, query):
    results = [
        {
            "type": "article",
            "id": "1",
            "title": "Search Result 1",
            "input_message_content": {
                "message_text": "Result 1 selected"
            },
            "description": "Description for result 1"
        },
        {
            "type": "photo",
            "id": "2",
            "photo_url": "https://example.com/photo.jpg",
            "thumb_url": "https://example.com/thumb.jpg",
            "title": "Photo Result",
            "caption": "Photo with caption"
        }
    ]
    
    bot.answer_inline_query(query_id, results)

# Note: Use polling or webhook to receive inline queries
```

## Rich Media Messages

### 1. Inline Keyboard Buttons

```python
from tools.api_integrations.telegram_integration import TelegramBot

bot = TelegramBot("TOKEN")

# With reply markup
bot.send_message(
    chat_id=123,
    text="Choose an option:",
    reply_markup={
        "inline_keyboard": [
            [
                {"text": "✅ Yes", "callback_data": "yes"},
                {"text": "❌ No", "callback_data": "no"}
            ],
            [{"text": "🌐 Website", "url": "https://example.com"}]
        ]
    }
)
```

### 2. Media Group (Album)

```python
media = [
    {"type": "photo", "media": "https://example.com/photo1.jpg"},
    {"type": "photo", "media": "https://example.com/photo2.jpg"},
    {"type": "photo", "media": "https://example.com/photo3.jpg"}
]

bot.send_media_group(chat_id=123, media=media)
```

### 3. Poll Message

```python
bot.send_poll(
    chat_id=123,
    question="What's your favorite language?",
    options=["Python", "JavaScript", "Go", "Rust"],
    is_anonymous=False,
    type="regular"
)
```

## Best Practices

### 1. Error Handling

```python
from tools.api_integrations.telegram_integration import TelegramBot
import requests

bot = TelegramBot("TOKEN")

try:
    result = bot.send_message(123456789, "Hello!")
except requests.exceptions.HTTPError as e:
    error = e.response.json()
    error_code = error.get("error_code")
    
    if error_code == 400:
        print("Bad request - invalid chat_id or message")
    elif error_code == 401:
        print("Unauthorized - invalid bot token")
    elif error_code == 403:
        print("Forbidden - bot blocked by user")
    elif error_code == 429:
        print("Too many requests - implement backoff")
        # Retry-After header contains seconds to wait
        retry_after = int(e.response.headers.get("Retry-After", 60))
```

### 2. Rate Limiting

Telegram limits:
- Messages to chats: ~30 msg/sec, ~20 msg/min
- Groups: ~20 msg/min per group
- Broadcast: 30 msg/sec

```python
import time
import requests

def send_with_backoff(bot, chat_id, text, max_retries=5):
    for attempt in range(max_retries):
        try:
            return bot.send_message(chat_id, text)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("Retry-After", 5))
                print(f"Rate limited. Waiting {retry_after}s...")
                time.sleep(retry_after)
            else:
                raise
    raise Exception("Failed after max retries")
```

### 3. Message Formatting

```python
# Markdown (default)
bot.send_message(chat_id, """
*Bold text*
_Italic text_
__Underline__
~Strikethrough~
`Inline code`
```code block```
[Link text](https://example.com)
""", parse_mode="Markdown")

# HTML (more tags supported)
bot.send_message(chat_id, """
<b>Bold</b>
<i>Italic</i>
<u>Underline</u>
<s>Strikethrough</s>
<code>Code</code>
<pre>Code block</pre>
<a href="https://example.com">Link</a>
<span class="tg-spoiler">Spoiler</span>
""", parse_mode="HTML")
```

## Integration with Cursor Framework

### Slash Command

```
/telegram send "123456789" "Hello from Cursor!"
```

### Workflow Example

```yaml
# .cursor/workflows/telegram-alert.yaml
name: Telegram Alert Workflow
trigger:
  type: webhook
  source: monitoring-system

steps:
  - name: Format alert
    action: template.render
    template: |
      🚨 *Alert: {{ alert_type }}*
      
      {{ message }}
      
      Server: {{ server }}
      Time: {{ timestamp }}

  - name: Send to Telegram
    action: telegram.send_message
    params:
      chat_id: "{{ secrets.telegram_chat_id }}"
      text: "{{ rendered_template }}"
      parse_mode: Markdown
```

## Security

### 1. Bot Token Protection

```python
import os

# ✅ Good: Environment variable
bot = TelegramBot(os.environ["TELEGRAM_BOT_TOKEN"])

# ❌ Bad: Hardcoded token
bot = TelegramBot("123456:ABCdefGHI...")  # Never do this!
```

### 2. Webhook Verification

```python
from flask import Flask, request
import hmac

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    
    # Verify secret token (recommended)
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != os.environ["WEBHOOK_SECRET"]:
        return "Unauthorized", 401
    
    # Process update...
    return "OK"
```

## References

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [BotFather Guide](https://core.telegram.org/bots#botfather)
- [Bot Features Overview](https://core.telegram.org/bots/features)
- [Telegram Bot SDK (Python)](https://github.com/python-telegram-bot/python-telegram-bot)
