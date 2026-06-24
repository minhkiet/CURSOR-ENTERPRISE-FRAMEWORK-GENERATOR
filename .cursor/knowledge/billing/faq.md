# Billing Knowledge - FAQ

**Q: How do we handle currency for Vietnam payments?**
A: All amounts in VND (no decimals). Payment gateways use `amount` in cents/minor units. MoMo uses `amount`, SePay uses `amount`, PayOS uses `amount`.

**Q: How do we prevent duplicate charges on webhook retry?**
A: Generate unique `requestId` on payment creation. Store processed `requestId` in ledger. On webhook, check if `requestId` already processed before updating.

**Q: How do we reconcile banking transfers (SePay)?**
A: Match transfers by amount + bank account number in transfer content. Handle multiple matches (split payments). Flag suspicious matches for review.

**Q: How do we handle subscription cancellation?**
A: Access continues until end of billing period. No refund (unless legal requirement). Mark subscription as cancelled, not deleted. After period ends, suspend access.

**Q: How do we handle annual vs monthly billing?**
A: Both create subscription records. Annual = 12x monthly price. Annual has discount incentive. Both renew automatically unless cancelled.
