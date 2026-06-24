# Billing Knowledge - Decision Tree

## Which payment provider to support?
- MoMo: Large user base, QR payments, good for consumer apps
- SePay: Banking auto-reconciliation, best for subscription billing
- PayOS/VietQR: Bank-agnostic QR, good for B2B
- ZaloPay: If strong Zalo user base
- VNPay: Maximum coverage, but complex integration
- Recommendation: Support SePay + PayOS as primary for subscriptions

## How to handle payment failures?
1. Check if retryable (network error) -> retry immediately
2. Check if card expired -> notify user to update
3. Check if insufficient funds -> notify user
4. Non-retryable -> add to dunning queue
5. After max retries -> suspend account

## How to calculate prorated billing?
- New plan price: $50/month (30 days = $1.67/day)
- Old plan price: $30/month ($1.00/day)
- Days remaining in billing cycle: 15 days
- Credit: 15 x $1.00 = $15
- Charge: 15 x $1.67 = $25
- Net charge: $25 - $15 = $10

## What to do on webhook failure?
1. Log the failure with full payload
2. Return 200 to provider (prevent retries)
3. Queue for async processing
4. Process with idempotency check
5. Alert if processing fails
