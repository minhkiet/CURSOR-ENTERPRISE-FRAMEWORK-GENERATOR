# Revenue report / Báo cáo doanh thu

For owners and accountants asking about revenue on their own SePay data: one period, period over period, per point of sale or account, internal transfers set apart, and why two figures differ. Read `mcp.md` and `revenue-rules.md` first. What counts, and which view of the cash-flow report answers which question, is set only in `revenue-rules.md` (› Choosing the view); this file adds the default method, period comparisons, explaining differences and the answer shape.

## Which method

| The user asks for | Method | `basis` |
|---|---|---|
| "doanh thu" with no method named | With payment code | `with_code` |
| "tổng tiền vào", "dòng tiền", money in of the business | All money in, gateway payments included (`gateway` `include`, the default) | `all_in` |
| "sao kê", "tiền về tài khoản", money that reached one bank account | the statement view of `revenue-rules.md` › Choosing the view | `all_in`, `gateway` `exclude`, `bank_account_xid` of that account (`list_bank_accounts` first) |
| per point of sale, "qua VA" | Via VA | `via_va` |
| a method by name | that method | |

- Name the method in the answer ("tính theo giao dịch có mã thanh toán, gồm cả thẻ và NAPAS qua cổng"). When the user did not choose it, add one line that two other methods exist (all money in, via VA), without their figures unless asked: no total of another method anywhere in the answer, not even beside the items that wait for confirmation (never "theo cách tất cả tiền vào thì tổng là …").
- Never compare or add figures of different methods.

## Calls

- One period: `get_cashflow_report` with `basis`, `from_date`, `to_date`, `period` (`day` / `week` / `month` to match the question), in the view `revenue-rules.md` › Choosing the view gives for the question. Revenue and "tổng tiền vào" keep gateway payments in (`gateway` `include`, the default); leave them out (`exclude`) only for money that reached the bank, as on a statement, and read them alone (`only`) only for sales through the gateway.
- Per point of sale: `basis` `via_va`, `group_by` `va`; read `by_va[]`.
- Per bank account: `by_bank_account[]` of the same call; one account only: `bank_account_xid`.
- **Refunds, every time.** The report gives money in only, so a revenue figure is not finished until refunds of the period are looked up: call `list_transactions` with `direction` `out` for the same period (every page), check gateway voids and refunds (`list_pg_orders`), and apply `revenue-rules.md` › Refunds. Then give gross, refunds in the period and net (thực thu), even when refunds are 0 ("không có hoàn tiền trong kỳ"). When refunds cannot be read, say so and give gross only.
- Repeat every line of the report's `notes` that bears on the figure.

## Period over period

- Same method for both periods, one call each.
- **Current period not over** (e.g. "tháng này" on 10/11): the main comparison is the same number of days (01–10/11 against 01–10/10); add one line with the whole previous period for reference, and say the current period is not over.
- Give both figures, the difference in đồng and in %, and the word for it (tăng / giảm / không đổi).
- Then where the change comes from, using the figures of the same calls: per point of sale, per account, card and NAPAS through the gateway (`gateway_in`), refunds, the days with the largest change (`timeline[]`). Say only what the figures show; never guess a business reason (season, promotion).

## Why two figures differ

### Between periods
As above: break the difference down by the parts the report returns, largest first.

### Between methods
Explain with the parts that make them differ, each with its figure: internal transfers and transfers without a payment code (in all money in only), card and NAPAS through the gateway (not via VA), coded transfers that did not land on a VA, gateway money arriving at the bank (`revenue-rules.md`).

### Against the user's bank statement or books
1. Ask for what is missing to compare: their figure, which account, which period (and whether it is money in or revenue).
2. Read the same account and period in the statement view of `revenue-rules.md` › Choosing the view (`basis` `all_in`, `gateway` `exclude`, `bank_account_xid`), and the revenue figure in its own view. `bank_account_xid` is the statement's account from `list_bank_accounts`, passed in that same call even when the business has one account: a statement is one account, and the call without it adds up every account. So call `list_bank_accounts` first and wait for its result; never send the statement-view call in the same batch of parallel calls as `list_bank_accounts`. Then list each source of the gap with its figure:
   - internal transfers (on the statement, not revenue);
   - gateway money arriving at the bank (on the statement, already counted as card / NAPAS revenue);
   - card and NAPAS payments through the gateway (in revenue, never on that account's statement);
   - transfers without a payment code (on the statement, not in "with payment code");
   - refunds and other money out (a statement's balance includes them, money in does not);
   - accounts or days not connected to SePay, and data hidden by the business's settings (`hidden_fields`, `notes`).
3. Add the sources up. When they do not account for the whole gap, give the part still unexplained in đồng and say so; never stretch a source to close it.

## Answer shape

Figures first: method, period, gross, refunds, net, then the breakdown asked for, in the user's language, money written 7.300.000 ₫. Items that wait for the user's confirmation (possible internal transfers, gateway money arriving at the bank, possible refunds) are listed with date, amount and memo, as `revenue-rules.md` says.

## Sample questions (câu hỏi mẫu)

1. Doanh thu tháng 10 bao nhiêu?
2. Tháng này so với tháng trước tăng hay giảm?
3. Doanh thu tuần này của từng điểm bán?
4. Tổng tiền vào tháng 10 bao nhiêu, trong đó bao nhiêu là chuyển nội bộ?
5. Vì sao doanh thu trên SePay khác tổng tiền vào trên sao kê?
