# Billing Knowledge - Architecture

## Billing System Architecture
```
[Frontend] --> [Billing API] --> [Subscription Engine]
                              |--> [Payment Gateway] --> [MoMo/SePay/PayOS/ZaloPay/VNPay]
                              |--> [Invoice Generator]
                              |--> [Webhook Handler]
                              |--> [Dunning Service]
                              |--> [Ledger]
```

## Vietnam Payment Integration Architecture

### MoMo Integration
```
[App] --> [Create payment] --> [MoMo API: /v2/gateway/api/create]
                                        |
                                        v
                              [Return payment URL/QR]
                                        |
                                        v
                              [User pays via MoMo app]
                                        |
                                        v
                              [MoMo Webhook] --> [Verify signature] --> [Update order]
```

### SePay Integration
```
[App] --> [Monitor transfers] --> [SePay API: /banking]
                                        |
                                        v
                              [Auto-match by amount + content]
                                        |
                                        v
                              [Update payment status]
```

### PayOS Integration
```
[App] --> [Create payment] --> [PayOS API]
                                        |
                                        v
                              [Return checkout URL]
                                        |
                                        v
                              [User pays via VietQR]
                                        |
                                        v
                              [PayOS Webhook] --> [Verify checksum] --> [Update order]
```

## Key Design Patterns

### Idempotency
- Every payment request must have unique idempotency key
- Store idempotency keys to prevent duplicate charges
- Handle webhook retries safely

### Webhook Security
- Always verify webhook signatures/checksums
- Use timestamp validation to prevent replay attacks
- Implement idempotent webhook handlers

### Reconciliation
- Daily reconciliation between payment provider and ledger
- Automated alert for mismatches
- Manual review queue for edge cases
