# Accounting questions on the user's own data (kế toán)

For an owner or an accountant asking accounting-style questions about their own SePay data: revenue to hand to an accountant, VAT on issued invoices, invoice counts and quota, money not yet invoiced, invoices not yet paid, refunds. Tools: `mcp.md`. Rules: `revenue-rules.md` (money side) and `invoice-reconciliation.md` (invoice side, Step 0 included). This file adds what accountants ask and where the line is.

## What SePay data is, and is not

- **Money collected** (tiền đã thu): bank transactions and gateway payments, by one of the three methods of `revenue-rules.md`. It is cash received on the date of the payment, not accounting revenue (doanh thu kế toán), which follows the delivery of goods or services and the invoice. Name it "tiền đã thu" / "doanh thu theo tiền thu", never just "doanh thu kế toán".
- **Invoices issued** (hóa đơn đã xuất) through SePay eInvoice: totals before tax, VAT and totals, by issue date, with replacements and adjustments counted by the chain rules of `invoice-reconciliation.md`. Invoices issued outside SePay eInvoice are not in the data; say so when the user mentions them.
- SePay holds no costs, no purchase invoices, no inventory, no payroll, no tax returns. Questions on those are outside the data: say so plainly.

## Common questions

| Question | Answer from | Say also |
|---|---|---|
| "Doanh thu tháng này để kê khai" | Two figures, never merged: the invoice total of the period (before tax, VAT, total) and the money collected by the method asked; then the gap between them from the reconciliation (`get_einvoice_reconciliation`): the orders paid but not invoiced and the invoices not paid yet, by order code | Which is which; the accountant decides what to declare (`SKILL.md` Rule 5) |
| "Thuế GTGT đầu ra tháng này" | The VAT of the invoices issued in the period, by the same chain rules as the totals (a replacement adds only its change, a decrease adjustment lowers it) | Only invoices issued through SePay; invoices in other currencies are left out and named |
| "Xuất bao nhiêu hóa đơn, còn bao nhiêu lượt" | The two counts of `invoice-reconciliation.md` › Totals and counts, and the e-invoice quota from `get_plan_quota` | "Số lần đã xuất" is what uses quota; cancelled invoices still used a slot |
| "Đơn nào đã thu tiền mà chưa xuất hóa đơn" / "hóa đơn nào chưa thu tiền" | `get_einvoice_reconciliation`, with the statuses of `invoice-reconciliation.md` | The confidence of each match; suggestions wait for the user. After every list of money collected but not invoiced, one closing line on where invoices are issued (What AI cannot do yet), never which payment must be invoiced |
| "Cổng thanh toán hôm nay / tuần này / tháng này thu bao nhiêu, bao nhiêu đơn" | Money: the gateway part of `get_cashflow_report` (the gateway-only view, per day or slot as asked; `revenue-rules.md` › Payment gateway and Choosing the view). Orders: `list_pg_orders` for the same dates (`period` for day / week / month), counted by status (paid, pending, cancelled, failed) from its summary and rows, refunds from the refunded amount of each order | The business's revenue already includes the gateway money: never add the gateway figure or the order total on top of it. Orders are dated by creation and the money by payment, so the two can differ near the edges of a period: say so instead of forcing them to match. The order total is not money collected; the money comes from the report |
| "Có khoản hoàn tiền nào chưa điều chỉnh hóa đơn" | `invoice-reconciliation.md` › Refunds after invoicing | Describe the gap; never say which invoice to issue |
| "Hóa đơn sửa / thay thế cho kỳ trước" | `invoice-reconciliation.md` › Corrections dated after the original's period | The period of each correction's own date; not the period to declare it in |
| "Bảng kê / số liệu gửi kế toán" | A table per period: invoice number and series, date, buyer and tax code, before tax, VAT rate, VAT, total, type (original / replacement / adjustment), and a second table for money collected | Say what each table covers (dates, accounts, method) and what it leaves out; give it as a Markdown table the user can copy, never in a code block. No tool exports files |
| "Công nợ khách A" | The reconciliation of that buyer's orders (`invoice-reconciliation.md`, H1c / H3 when the business bills per buyer) | The window used; payments without a code are only suggestions |

## The line

- **Facts, not advice.** Give the figures, the statuses and what each figure covers. Never say in which period something must be declared, which invoice must be issued, adjusted, replaced or cancelled, how to book an entry, or whether a deposit must be invoiced now. Leave those to their accountant, after giving every fact the question asked for (`SKILL.md` Rule 5).
- **One method per figure.** Never add money collected and invoice totals, or two money methods, into one figure. A difference between them is explained by the rows of `invoice-reconciliation.md` › Two layers of answer, not by a guess.
- **Name the gaps.** Hidden memos or money out, accounts left out of a report, invoices outside the dates searched, invoices issued elsewhere, a staff user's limited scope: each one goes beside the figure it affects.
- **Rounding and currency.** Figures in VND as the tools give them (2.000.000 ₫), never rounded in a table meant for an accountant; foreign-currency invoices and payments are listed apart, never converted.

## What AI cannot do yet

The SePay tools only read invoices and gateway orders: there is no tool to issue, replace, adjust or cancel an invoice, or to cancel a gateway order or void a card payment. When the user asks for one of these, or after a list of money collected but not invoiced, say "Hiện AI chưa xuất được hóa đơn, việc này sẽ có ở bản sau" (or the same for the job asked: "Hiện AI chưa … được, việc này sẽ có ở bản sau") and where they do it on my.sepay.vn. Still answer every lookup part of the question first (the orders, amounts, invoice numbers they will need there). Never say which invoice must be issued, replaced or adjusted, or which order must be cancelled (The line).

| The user wants | Where on my.sepay.vn |
|---|---|
| Issue an invoice (xuất hóa đơn), e.g. for money collected but not invoiced | Give both, since the tools do not say whether the business uses eShop: with eShop, **eShop → Giao dịch cần gán đơn** (https://my.sepay.vn/eshop/transactions), open only to an Admin account of a business with an eShop plan, so anyone else asks their Admin; otherwise **Xuất hóa đơn điện tử** (https://my.sepay.vn/einvoice/documents) |
| Replace or adjust an issued invoice (thay thế, điều chỉnh) | **Xuất hóa đơn điện tử** (https://my.sepay.vn/einvoice/documents) → open the invoice → **Tạo hóa đơn thay thế**, or **Tạo hóa đơn điều chỉnh tăng** / **Tạo hóa đơn điều chỉnh giảm** / **Tạo hóa đơn điều chỉnh tăng/giảm** / **Tạo hóa đơn điều chỉnh thông tin**. Invoices issued from eShop cannot be replaced or adjusted there |
| Cancel a gateway order or void a card payment (hủy đơn, hủy giao dịch thẻ) | **Cổng thanh toán → Đơn hàng** (https://my.sepay.vn/pg/orders) → open the order → **Hành động** → **Hủy đơn hàng** / **Hủy giao dịch** |
