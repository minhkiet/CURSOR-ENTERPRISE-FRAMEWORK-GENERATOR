# Billing Knowledge - Checklist

## Setup
- [ ] Payment gateway integration (MoMo, SePay, PayOS)
- [ ] Webhook handler with signature verification
- [ ] Idempotency keys implemented
- [ ] Transaction ledger (append-only)
- [ ] Currency handling (VND)

## Subscription Management
- [ ] Subscription model with plan/tier
- [ ] Trial period management
- [ ] Plan upgrade/downgrade logic
- [ ] Prorated billing on changes
- [ ] Subscription renewal automation
- [ ] Grace period for failed payments

## Payment Processing
- [ ] Create payment request flow
- [ ] Handle async payment status updates
- [ ] Webhook retry handling (idempotent)
- [ ] Payment timeout handling
- [ ] Refund capability
- [ ] Payment method management

## Reconciliation
- [ ] Daily reconciliation job
- [ ] Auto-match SePay transfers
- [ ] Mismatch alerting
- [ ] Manual review queue
- [ ] Failed payment retry

## Invoice & Reporting
- [ ] Invoice generation with sequential numbering
- [ ] Invoice PDF storage
- [ ] Revenue reporting (MRR, ARR)
- [ ] Churn tracking
- [ ] Payment method expiry tracking
