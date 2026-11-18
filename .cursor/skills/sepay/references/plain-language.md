# Plain words for non-technical users

Some SePay users are shop owners or people who cannot read the code an AI agent writes for them. They want the payment to work, not to learn the jargon. Developers find this register patronising, so it is never the default.

## Who gets plain words

Default: developer register (concise, technical, no glossary). Switch only on a clear sign, judged from the user's words and the project:

| Plain words when the user... | Stay technical when the user... |
|---|---|
| says so: "không biết code", "không rành kỹ thuật", "mới học", "mình bán hàng, không phải dev" | uses the terms themselves: webhook, endpoint, HMAC, route, middleware, env var, a framework or library name |
| describes only the business outcome ("khách chuyển khoản xong đơn tự xác nhận") and cannot answer "ngôn ngữ / framework nào?" | pastes code, a stack trace, logs, a curl command or an API field name |
| asks what a basic term means (webhook, API key, terminal) | works in an existing codebase (source files, tests, CI, lockfile) or names versions |
| uses a no-code / hosted platform (WordPress / WooCommerce, Haravan, Sapo, a site builder) and asks you to "làm hết giúp" | asks about design trade-offs: concurrency, retries, idempotency, schema |
| writes from a chat app with no terminal (`SKILL.md` › No terminal) or from an empty project, shares no code, and asks only for the outcome ("làm cho web tôi tự xác nhận chuyển khoản") | does the same but names their stack or hosting ("Laravel trên VPS", "Next.js trên Vercel") |
| answers "Chọn giúp tôi" to the stack question (`SKILL.md` Rule 11) | |

- Not signs either way: casual or unaccented writing, typos, short messages, building with an AI agent, Vietnamese vs English.
- Mixed or unclear: stay concise and technical, and explain a term only when asked. Do not ask the user how technical they are; the first stack question carries the "Chọn giúp tôi" option instead (Rule 11).
- One explanation request from a developer is a lookup, not a switch: answer it and stay technical.
- Once you switch, keep it for the session unless the user starts using technical terms; then switch back at once and stop explaining.

## How to talk

- Lead with the result in one sentence: "Xong rồi: khi khách chuyển khoản đúng nội dung, đơn tự chuyển sang Đã thanh toán."
- Use everyday words. The first time a term is unavoidable, explain it in a few words in brackets, then reuse it the same way (table below).
- One action per step, numbered. Say where to click (my.sepay.vn labels verbatim) or give the exact command to copy, then what they will see when it worked.
- You do the technical work: write the code into files, run the tests, then say in plain words what you did and why it matters. Do not paste long code into the chat unless asked.
- Every setup ends with a test before real money: Test mode → **Mô phỏng giao dịch** first, then one small real transfer.
- A finished integration ends with numbered go-live steps (`testing-go-live.md` › Go-live: real bank account, payment code structure, web online and the live webhook, one small real transfer), each a my.sepay.vn label or one command, then a short **Theo dõi sau khi chạy thật** part: turn on **Tự động gửi lại khi server trả lỗi** and **Bật cảnh báo khi webhook gặp lỗi liên tiếp**, glance at **Lịch sử gửi** in the first days. With the `sepay` CLI, offer to do the steps it covers yourself (production changes: you dry-run them and the user runs each command, Rule 3) and list only what is left for the user. Then how to run the shop on this machine, in one line.
- Leave the inside out: no signature algorithm, HTTP status, build tool, container, test flag or file path in the reply. Say what now works, what you checked, and what the user does next; technical detail goes in the README for whoever maintains the code.
- Ask with choices, not open questions: every question you end with is a short list of answers, the recommended one first (Rule 11).
- When you refuse or hold back (secrets, production changes), give the reason in one plain sentence: "Mình không gửi file `.env` đi đâu vì trong đó có mật khẩu; ai có nó là lấy được tiền/đơn hàng của bạn."
- Warnings name the concrete consequence ("khách có thể bị ghi nhận đã trả 2 lần"), not the technical cause.

## Term → plain Vietnamese

| Term | Say it as |
|---|---|
| Webhook | SePay tự báo cho web của bạn mỗi khi tài khoản có tiền vào |
| Webhook URL / endpoint | địa chỉ trên web của bạn để SePay gửi tin báo tới |
| IPN | tin báo kết quả thanh toán từ cổng thanh toán gửi về web của bạn |
| API | cách để code của bạn hỏi hoặc ra lệnh cho SePay |
| API key / token | chìa khoá để code của bạn được dùng tài khoản SePay; giữ kín như mật khẩu |
| Secret / chữ ký HMAC | mật mã chung giữa SePay và web của bạn, để biết tin báo đúng là từ SePay chứ không phải ai giả mạo |
| Sandbox / Test mode | chế độ chạy thử: tiền giả, không ảnh hưởng tài khoản thật |
| Production / live | chạy thật, tiền thật |
| Mô phỏng giao dịch / `sandbox simulate` | giả lập một khoản chuyển khoản để xem web có tự xác nhận đơn không |
| `webhook listen` | cho máy của bạn nhận tin báo của SePay khi đang làm thử, chưa cần đưa web lên mạng |
| VA (tài khoản ảo) | một số tài khoản riêng cho từng đơn, khách chuyển vào là biết ngay đơn nào |
| Payment code / mã thanh toán | mã đơn khách ghi vào nội dung chuyển khoản, để SePay nhận ra đơn nào |
| Đối soát (reconciliation) | định kỳ kiểm lại danh sách giao dịch để không sót đơn nào khi tin báo bị lỡ |
| Chống trùng (dedupe / idempotent) | một khoản tiền chỉ được tính một lần, dù SePay gửi tin báo nhiều lần |
| CLI / terminal | công cụ gõ lệnh; mình chạy giúp, bạn chỉ cần đồng ý |
| `.env` | file cất mật khẩu và chìa khoá của web, không đưa lên mạng hay gửi cho ai |
| HTTPS | địa chỉ web có ổ khoá, dữ liệu đi trên mạng được mã hoá |
| localhost | web đang chạy trên chính máy của bạn, người ngoài không vào được |
| Deploy | đưa web lên mạng cho khách dùng |
| Log | nhật ký web tự ghi lại; không ghi số tài khoản đầy đủ hay tên khách vào đó |
