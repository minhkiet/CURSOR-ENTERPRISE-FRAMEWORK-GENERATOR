---
name: "source-command-payment-command"
description: "Payment - Review payment integration Việt Nam (MoMo, SePay, PayOS, ZaloPay, VNPay, VietQR)"
---

# source-command-payment-command

Use this skill when the user asks to run the migrated source command `payment-command`.

## Command Template

# Command: /payment

## Mục tiêu
Review payment integration cho các payment provider phổ biến tại Việt Nam.

## Trigger Keywords
- payment
- thanh toán
- momo
- sepay
- payos
- zalo pay
- zalo pay integration
- vnpay
- vietqr
- payment integration
- webhook payment
- thanh toán momo
- thanh toán vn
- payment gateway
- payment provider
- refund
- refund payment
- payment reconciliation
- payment flow

## Supported Providers

### MoMo (MoMo Payment)
- [ ] API integration review
- [ ] Webhook security (signature validation)
- [ ] Payment flow (create, confirm, refund)
- [ ] Error handling
- [ ] Idempotency
- [ ] Reconciliation

### SePay (SePay Banking)
- [ ] API integration review
- [ ] Webhook security
- [ ] Account linking
- [ ] Transaction monitoring
- [ ] Error handling

### PayOS
- [ ] API integration review
- [ ] Webhook security (checksum validation)
- [ ] Payment flow
- [ ] Error handling
- [ ] Idempotency

### ZaloPay
- [ ] API integration review
- [ ] App-based payment
- [ ] Webhook security
- [ ] Error handling

### VNPay
- [ ] Gateway integration review
- [ ] Payment flow
- [ ] Return URL handling
- [ ] Security checks
- [ ] Error handling

### VietQR
- [ ] QR payment integration
- [ ] Bank account validation
- [ ] Transaction verification
- [ ] Error handling

## Liên kết
- [[../skills/vietnam-payment-review]] - Vietnam Payment Review Skill
- [[../rules/billing]] - Billing Rules
- [[../rules/security]] - Security Rules
- [[../rules/web-security]] - Web Security Rules
