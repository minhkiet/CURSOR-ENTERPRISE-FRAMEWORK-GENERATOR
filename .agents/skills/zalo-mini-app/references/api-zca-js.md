# ZCA-JS - Unofficial Zalo API for JavaScript

> [!WARNING]
> This is an **unofficial** Zalo API cho tài khoản cá nhân. Hoạt động bằng cách simulate browser để tương tác với Zalo Web.
> **Cảnh báo:** Sử dụng API này có thể khiến tài khoản bị khóa hoặc banned. Sử dụng tại rủi ro của bạn.

## Installation

```bash
bun add zca-js # or npm install zca-js
```

### V2 Migration (Image Support)

Since v2.0.0, `zca-js` đã loại bỏ sharp dependency. Cần provide `imageMetadataGetter` function để gửi ảnh/GIF:

```bash
bun add sharp # or npm install sharp
```

```javascript
import { Zalo } from "zca-js";
import sharp from "sharp";
import fs from "node:fs";

async function imageMetadataGetter(filePath) {
    const data = await fs.promises.readFile(filePath);
    const metadata = await sharp(data).metadata();
    return {
        height: metadata.height,
        width: metadata.width,
        size: metadata.size || data.length,
    };
}

const zalo = new Zalo({ imageMetadataGetter });
```

## Core Features

| Feature | Description |
|---------|-------------|
| **QR Login** | Đăng nhập bằng QR code |
| **Message Listener** | Lắng nghe tin nhắn real-time |
| **Send Messages** | Gửi text, sticker, hình ảnh |
| **Thread Support** | Hỗ trợ User DM và Group |
| **Quote Reply** | Trả lời tin nhắn có trích dẫn |

## Quick Start

### 1. Login với QR Code

```javascript
import { Zalo } from "zca-js";

const zalo = new Zalo();
const api = await zalo.loginQR();
```

### 2. Listen for Messages

```javascript
import { Zalo, ThreadType } from "zca-js";

const zalo = new Zalo();
const api = await zalo.loginQR();

api.listener.on("message", (message) => {
    const isPlainText = typeof message.data.content === "string";

    switch (message.type) {
        case ThreadType.User: {
            // Tin nhắn riêng từ user
            if (isPlainText) {
                console.log("User DM:", message.data.content);
            }
            break;
        }
        case ThreadType.Group: {
            // Tin nhắn trong group
            if (isPlainText) {
                console.log("Group msg:", message.data.content);
            }
            break;
        }
    }
});

api.listener.start();
```

> [!IMPORTANT]
> Chỉ một listener có thể chạy per account. Nếu mở Zalo trên browser, listener sẽ tự động dừng.

### 3. Echo Bot Example

```javascript
import { Zalo, ThreadType } from "zca-js";

const zalo = new Zalo();
const api = await zalo.loginQR();

api.listener.on("message", (message) => {
    const isPlainText = typeof message.data.content === "string";
    if (message.isSelf || !isPlainText) return;

    api.sendMessage(
        { msg: "echo: " + message.data.content },
        message.threadId,
        message.type
    );
});

api.listener.start();
```

### 4. Send Sticker

```javascript
// Tìm sticker
const stickerIds = await api.getStickers("hello");
const stickerObject = await api.getStickersDetail(stickerIds[0]);

// Gửi sticker
api.sendMessageSticker(
    stickerObject,
    message.threadId,
    message.type // ThreadType.User or ThreadType.Group
);
```

## API Reference

### Classes & Exports

| Export | Description |
|--------|-------------|
| `Zalo` | Main class, khởi tạo với options |
| `ThreadType` | Enum: `User`, `Group` |
| `EventEmitter` | Event listener base |

### Zalo Class Options

```typescript
interface ZaloOptions {
    imageMetadataGetter?: (filePath: string) => Promise<ImageMetadata>;
    cookies?: string;        // Cookie string (optional)
    imei?: string;           // Device IMEI (optional)
    userAgent?: string;      // Browser UA (optional)
}
```

### API Methods

```typescript
// Login
await zalo.loginQR(): Promise<ZaloAPI>

// Listener
api.listener.on(event: string, callback: Function)
api.listener.start()
api.listener.stop()

// Messaging
api.sendMessage(content: MessageContent, threadId: string, type: ThreadType): Promise<void>
api.sendMessageSticker(sticker: StickerObject, threadId: string, type: ThreadType): Promise<void>

// Utilities
api.getStickers(query: string): Promise<string[]>
api.getStickersDetail(stickerId: string): Promise<StickerObject>
```

## Message Types

```typescript
interface IncomingMessage {
    type: ThreadType.User | ThreadType.Group;
    threadId: string;
    isSelf: boolean;
    data: {
        msgId: string;
        content: string | object;  // string = text, object = media
        timestamp: number;
        quote?: MessageQuote;
    };
}

interface MessageContent {
    msg: string;
    quote?: MessageQuote;  // Reply với quote
}

interface MessageQuote {
    msgId: string;
    content: string;
}
```

## Use Cases

### Chatbot với AI Integration

```javascript
import { Zalo, ThreadType } from "zca-js";

const zalo = new Zalo();
const api = await zalo.loginQR();

api.listener.on("message", async (message) => {
    if (message.isSelf) return;
    
    const text = message.data.content;
    if (typeof text !== "string") return;

    // Gọi AI response
    const response = await callAI(text);
    
    api.sendMessage(
        { msg: response },
        message.threadId,
        message.type
    );
});

api.listener.start();
```

### Auto-reply với Keywords

```javascript
const keywords = {
    "hello": "Xin chào! 👋",
    "help": "Tôi có thể giúp gì cho bạn?",
    "price": "Vui lòng truy cập website để xem giá..."
};

api.listener.on("message", (message) => {
    if (message.isSelf) return;
    
    const text = (message.data.content || "").toLowerCase();
    
    for (const [key, reply] of Object.entries(keywords)) {
        if (text.includes(key)) {
            api.sendMessage({ msg: reply }, message.threadId, message.type);
            return;
        }
    }
});
```

### Multi-Account Management

Kết hợp với [MultiZlogin](https://github.com/ChickenAI/multizlogin) để quản lý nhiều tài khoản Zalo đồng thời với proxy và webhook integration.

## Ecosystem & Related Projects

| Project | Description |
|---------|-------------|
| [ZaloDataExtractor](https://github.com/JustKemForFun/ZaloDataExtractor) | Browser extension để extract IMEI, cookies, user agent từ Zalo Web |
| [MultiZlogin](https://github.com/ChickenAI/multizlogin) | Multi-account Zalo management với proxy & webhook |
| [n8n-nodes-zalo-tools](https://github.com/ChickenAI/zalo-node) | N8N node cho Zalo account cá nhân |
| [Zalo-F12](https://github.com/ElectroHeavenVN/Zalo-F12) | JavaScript snippets cho DevTools để thay đổi Zalo Web/PC |
| [Zalo-F12-Tools](https://github.com/JustKemForFun/Zalo-F12-Tools) | Toggle hidden modes cho Zalo Web |

## Security Considerations

> [!WARNING]
> - Chỉ sử dụng cho tài khoản cá nhân
> - Không dùng để spam hoặc abuse
> - Tài khoản có thể bị khóa nếu Zalo phát hiện bất thường
> - Không lưu trữ cookies/credentials không cần thiết
> - Implement rate limiting cho bot

### Best Practices

```javascript
// Rate limiting
const messageTimestamps = new Map();

function canSendMessage(threadId) {
    const now = Date.now();
    const last = messageTimestamps.get(threadId) || 0;
    if (now - last < 1000) return false; // 1 msg/giây
    messageTimestamps.set(threadId, now);
    return true;
}

api.listener.on("message", (message) => {
    if (!canSendMessage(message.threadId)) return;
    // ... process message
});
```

## Documentation

- API Docs: https://zca-js.tdung.com
- GitHub: https://github.com/RFS-ADRENO/zca-js
- License: MIT

## Comparison: ZCA-JS vs Zalo Mini App SDK

| Aspect | ZCA-JS | Zalo Mini App SDK |
|--------|--------|-------------------|
| **Loại** | Unofficial API | Official SDK |
| **Mục đích** | Tài khoản cá nhân, chatbot | Mini App trong Zalo |
| **Tài khoản** | Zalo cá nhân (cần QR login) | Tài khoản doanh nghiệp |
| **Cài đặt** | npm/bun | zmp-cli |
| **Rủi ro** | Cao (có thể banned) | Thấp (official) |

**Khi nào dùng:**
- **ZCA-JS**: Chatbot cá nhân, automation, data extraction
- **Zalo Mini App SDK**: Xây dựng ứng dụng Mini App chính thức
