---
name: "source-command-payos"
description: "PayOS - Tích hợp cổng thanh toán VietQR PayOS (Open Banking Gateway, Payment Links, Webhook Checksum)"
---

# source-command-payos

Use this skill when the user asks to run the migrated source command `payos`.

## Command Template

# Command: /payos

Tích hợp, cấu hình, kiểm tra và gỡ lỗi cổng thanh toán mở PayOS (tạo payment link, sinh mã VietQR, xác thực chữ ký Webhook HMAC-SHA256 bằng Checksum Key, xử lý Idempotency và hoàn tất đơn hàng).

## Chi tiết workflow và hướng dẫn
Xem file chi tiết tại [command.md](./payos/command.md) hoặc kỹ năng [payos](../skills/payos/SKILL.md).
