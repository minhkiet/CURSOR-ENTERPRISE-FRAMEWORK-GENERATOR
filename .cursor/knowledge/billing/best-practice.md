# Billing Knowledge - Best Practices

## Payment Security
- Never store raw payment card data (use PCI-DSS compliant providers)
- Verify all webhook signatures before processing
- Use idempotency keys on every payment request
- Store transaction history immutably (append-only ledger)
- Encrypt sensitive billing data at rest

## Vietnam Payment Best Practices
- Support multiple providers (MoMo, SePay, PayOS, VietQR)
- Implement fallback: if primary fails, show secondary options
- Handle payment timeout gracefully (15-minute expiry)
- Support both synchronous (card) and asynchronous (bank transfer) flows
- Implement auto-reconciliation for SePay/ VietQR banking transfers
- Handle currency formatting (VND, no decimals)

## Subscription Management
- Always calculate prorated amounts on plan changes
- Handle mid-cycle upgrades/downgrades correctly
- Implement trial-to-paid conversion tracking
- Handle failed payments with dunning workflow
- Support annual and monthly billing cycles

## Invoice Best Practices
- Generate invoices with sequential numbering
- Include line items with descriptions
- Support both VND and multi-currency
- Store invoice PDF in object storage
- Send invoice via email automatically
- Support invoice voiding (not deletion)

## Dunning Best Practices
- Day 1: Payment failed notification
- Day 3: Second retry with notification
- Day 7: Third retry with warning
- Day 14: Suspend account, final notice
- Day 21: Account termination (configurable)
- Always preserve data during dunning period

## Refund Best Practices
- Implement refund policy window (7/14/30 days)
- Always refund to original payment method
- Track refund reasons for analytics
- Send refund confirmation email
- Handle partial refunds correctly
