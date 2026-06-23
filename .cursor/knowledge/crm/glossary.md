# CRM Glossary - Từ Điển Thuật Ngữ Quản Lý Khách Hàng

## Giới thiệu

Tài liệu này cung cấp danh sách đầy đủ các thuật ngữ chuyên ngành CRM (Customer Relationship Management), bao gồm các khái niệm về quản lý quan hệ khách hàng, automation marketing, và các công cụ liên quan. Mỗi thuật ngữ được định nghĩa chi tiết với ngữ cảnh ứng dụng trong thực tế và cách implement trong hệ thống.

## Các thuật ngữ cơ bản

### 1. CRM (Customer Relationship Management)

CRM là hệ thống quản lý quan hệ khách hàng, giúp doanh nghiệp theo dõi và tương tác với khách hàng một cách hiệu quả. CRM lưu trữ thông tin khách hàng, lịch sử giao dịch, và các điểm tiếp xúc để tạo ra cái nhìn 360 độ về mỗi khách hàng. Hệ thống CRM hiện đại tích hợp với email, điện thoại, mạng xã hội, và các kênh khác để quản lý tất cả interactions ở một nơi duy nhất.

Trong hệ thống, CRM được implement như một application với các modules chính: Contact Management, Deal Management, Task Management, Reporting, và Automation. Dữ liệu được tổ chức theo relational model với các entities như Contacts, Companies, Deals, Activities, và Tickets.

### 2. Lead (Khách Hàng Tiềm Năng)

Lead là một cá nhân hoặc tổ chức đã thể hiện quan tâm đến sản phẩm hoặc dịch vụ nhưng chưa trở thành khách hàng. Lead được phân loại theo mức độ quan tâm và khả năng chuyển đổi: Cold Lead (ít quan tâm), Warm Lead (quan tâm), Hot Lead (sẵn sàng mua). Quản lý leads hiệu quả giúp tăng tỷ lệ chuyển đổi và giảm chi phí acquisition.

Lead scoring là phương pháp gán điểm cho leads dựa trên các hành vi và thông tin: mức độ tương tác, thông tin công ty, ngân sách, timeline mua hàng. Hệ thống tự động score leads để ưu tiên xử lý những leads có khả năng chuyển đổi cao nhất.

### 3. Contact (Danh Bạ Liên Lạc)

Contact là thông tin về một cá nhân cụ thể trong hệ thống CRM, bao gồm tên, email, số điện thoại, chức vụ, và các thông tin liên quan khác. Mỗi contact có thể thuộc về một hoặc nhiều companies và có thể tham gia nhiều deals. Contacts là đối tượng cơ bản nhất trong CRM, làm nền tảng cho tất cả các hoạt động khác.

Trong hệ thống, Contact entity bao gồm các trường: basic info (tên, email, phone), company info (công ty, chức vụ, địa chỉ), social info (LinkedIn, Twitter, Facebook), custom fields, và các relationships với deals, activities, và tickets. Contacts có thể được import từ các nguồn khác nhau hoặc được tạo thủ công.

### 4. Company (Công Ty)

Company là thông tin về một tổ chức/doanh nghiệp trong hệ thống CRM. Company có thể có nhiều contacts và có thể tham gia nhiều deals. Company information bao gồm tên công ty, ngành nghề, quy mô, doanh thu, địa chỉ, và các thông tin firmographic khác. Company giúp nhóm các contacts liên quan và track deals theo tổ chức.

Company có thể có hierarchical structure (công ty mẹ - công ty con) để reflect cấu trúc tổ chức thực tế. Company enrichment là tính năng tự động điền thông tin công ty từ các nguồn bên ngoài như LinkedIn, Clearbit, hoặc Dun & Bradstreet.

### 5. Deal (Giao Dịch)

Deal là một cơ hội kinh doanh trong hệ thống CRM, đại diện cho một giao dịch tiềm năng với giá trị cụ thể. Deal có các thuộc tính: tên deal, giá trị, stage (giai đoạn), probability (xác suất thành công), expected close date, owner. Deal được track qua các stages trong pipeline từ initial contact đến closed won hoặc closed lost.

Pipeline là visualization của các deals theo stages, cho phép sales team theo dõi flow của deals và identify bottlenecks. Các stages phổ biến bao gồm: Qualification, Proposal, Negotiation, Closed Won, Closed Lost. Automation có thể tự động move deals qua các stages dựa trên triggers.

### 6. Pipeline (Đường Ống Bán Hàng)

Pipeline là visualization của quy trình bán hàng, thể hiện các deals đang di chuyển từ initial contact đến closed. Pipeline có nhiều stages, mỗi stage đại diện cho một giai đoạn trong quy trình bán hàng. Pipeline metrics quan trọng bao gồm: total value, weighted value (giá trị nhân xác suất), average time in stage, conversion rates giữa các stages.

Trong hệ thống, Pipeline được implement như một view với drag-and-drop functionality cho phép users di chuyển deals giữa các stages. Kanban board là visualization phổ biến nhất cho pipeline, hiển thị các columns là các stages với deals như cards.

### 7. Activity (Hoạt Động)

Activity là bất kỳ tương tác nào với khách hàng hoặc lead, bao gồm email, cuộc gọi, meeting, task, và note. Activities được log trong hệ thống CRM để maintain complete history của customer interactions. Activity timeline hiển thị chronological sequence của tất cả activities liên quan đến một contact hoặc deal.

Các loại activity phổ biến: Email (sent/received), Call (inbound/outbound), Meeting (scheduled/completed), Task (todo items), Note (general notes), Deal Update, System Activities (auto-logged). Activities có thể được log tự động thông qua integrations (email sync, calendar sync) hoặc manually bởi users.

### 8. Task (Nhiệm Vụ)

Task là một công việc cần được hoàn thành liên quan đến contacts, companies, hoặc deals. Task có các thuộc tính: tiêu đề, mô tả, người phụ trách, deadline, trạng thái (pending/completed), priority. Tasks có thể được tạo thủ công hoặc tự động tạo bởi automation workflows.

Task reminders và notifications đảm bảo tasks được completed đúng hạn. Overdue tasks được highlight để users có thể prioritize. Task templates cho phép tạo nhiều tasks theo pattern, ví dụ: khi tạo deal mới, tự động tạo các tasks: "Gọi khách hàng", "Gửi proposal", "Follow up sau 3 ngày".

### 9. Stage (Giai Đoạn)

Stage là một bước trong quy trình bán hàng hoặc customer lifecycle. Trong sales pipeline, stages đại diện cho các giai đoạn từ khi deal được tạo đến khi closed. Mỗi stage có probability và expected time để deal di chuyển qua. Stages được customize theo business process của từng organization.

Các stages phổ biến trong sales pipeline: Initial Contact, Qualification, Proposal/Price Quote, Negotiation, Closed Won (thành công), Closed Lost (thất bại). Stages có thể có automation rules: khi deal move vào stage, trigger actions như gửi email tự động, assign task, update fields.

### 10. Churn Rate (Tỷ Lệ Rời Bỏ)

Churn Rate là tỷ lệ khách hàng rời bỏ dịch vụ trong một khoảng thời gian, thường được tính hàng tháng hoặc hàng năm. Churn Rate = (Số khách hàng mất / Số khách hàng đầu kỳ) × 100%. Churn là metric quan trọng để đánh giá health của business và effectiveness của retention strategies.

Customer Lifetime Value (CLV) và Churn Rate có mối quan hệ nghịch: churn rate cao làm giảm CLV. Reducing churn là cách hiệu quả nhất để grow business vì retention cheaper than acquisition. Hệ thống CRM có thể identify customers có nguy cơ churn cao dựa trên usage patterns và engagement metrics.

### 11. Customer Lifetime Value (CLV)

CLV là tổng giá trị doanh thu mà một khách hàng mang lại trong suốt vòng đời của họ với doanh nghiệp. CLV calculation bao gồm: average purchase value, purchase frequency, customer lifespan, và margins. CLV helps businesses understand profitability của từng customer segment và informs acquisition và retention investments.

CLV calculation model: CLV = (Average Order Value × Purchase Frequency × Customer Lifespan) - Customer Acquisition Cost. Businesses thường target CLV:CAC ratio > 3:1 để ensure sustainable growth. Hệ thống CRM có thể calculate và track CLV cho từng customer để inform personalized engagement strategies.

### 12. Customer Acquisition Cost (CAC)

CAC là chi phí trung bình để có được một khách hàng mới, bao gồm tất cả chi phí marketing và sales. CAC = Tổng chi phí Marketing & Sales / Số khách hàng mới có được. CAC được so sánh với CLV để đánh giá sustainability của business model.

CAC by channel cho phép businesses hiểu ROI của từng acquisition channel. CAC by segment giúp identify customer segments có cost-effective để acquire. Reducing CAC while maintaining quality của customers là key growth strategy. Hệ thống CRM có thể track CAC by attributing marketing spend to customer acquisitions.

### 13. Email Template (Mẫu Email)

Email Template là mẫu có sẵn được sử dụng để gửi email nhanh chóng và nhất quán. Templates bao gồm placeholders cho personalization (tên khách hàng, company, deal value). Email templates ensure consistency trong messaging và reduce time để compose emails. Templates có thể được personalizable và trackable.

Trong hệ thống, Email Templates được managed trong content library với versioning và approval workflows. Merge tags cho phép dynamic content insertion. A/B testing email templates giúp optimize open rates và conversions. Email templates có thể được used trong automation sequences.

### 14. Workflow Automation (Tự Động Hóa Quy Trình)

Workflow Automation là việc tự động hóa các quy trình business dựa trên triggers và actions. Workflows được tạo bằng visual builder cho phép users define rules mà không cần code. Automation có thể handle repetitive tasks, ensure consistency, và scale operations.

Ví dụ workflow: Khi deal move vào stage "Proposal Sent", tự động gửi email template "Follow up proposal", tạo task "Follow up call" sau 3 ngày, notify sales manager qua Slack. Workflow triggers có thể là events (deal created, email opened), schedules (daily, weekly), hoặc field changes.

### 15. Segmentation (Phân Khúc)

Segmentation là việc chia customers thành các nhóm dựa trên shared characteristics để enable targeted marketing và personalization. Segmentation criteria có thể bao gồm: demographics, behavior, preferences, lifecycle stage, value. Effective segmentation enables businesses deliver relevant messages đến right audience.

Behavioral segmentation dựa trên actions: purchase history, engagement patterns, usage frequency. Value-based segmentation dựa trên CLV, margin, hoặc frequency. Lifecycle segmentation dựa trên customer journey stage: new customer, regular, at-risk, churned. Hệ thống CRM có thể auto-update segments based on real-time behavior.

### 16. Integration (Tích Hợp)

Integration là kết nối giữa CRM và các công cụ/ứng dụng khác để share data và automate workflows. Popular CRM integrations bao gồm: email (Gmail, Outlook), calendar (Google Calendar, Office 365), communication (Slack, Zoom), marketing (Mailchimp, HubSpot), accounting (QuickBooks, Xero), e-commerce (Shopify, WooCommerce).

Integration methods: API (for custom integrations), Zapier/Make (for no-code integrations), Native integrations (built-in by CRM vendor). Two-way sync ensures data consistency across systems. Webhooks enable real-time event-based integrations. Integration management trong CRM cho phép admins monitor và troubleshoot connectivity.

### 17. Reporting và Analytics

Reporting và Analytics cung cấp insights về sales performance, customer behavior, và business health. CRM reports bao gồm: pipeline reports, activity reports, sales forecast, team performance, conversion rates, revenue analysis. Reports có thể be scheduled và shared với stakeholders automatically.

Advanced analytics sử dụng ML để identify patterns và predict outcomes: churn prediction, lead scoring, next best action recommendations. Dashboard cung cấp real-time visibility vào key metrics. Custom report builder cho phép users create reports theo specific needs. Data export cho phép deep-dive analysis trong external tools.

### 18. Data Hygiene (Vệ Sinh Dữ Liệu)

Data Hygiene là practices để maintain accurate, complete, và consistent data trong CRM. Poor data quality impacts: reporting accuracy, campaign effectiveness, customer experience. Data hygiene practices bao gồm: validation rules, duplicate detection, data enrichment, regular audits.

Duplicate management identify và merge duplicate records. Data validation enforce format và required fields. Regular data audits identify outdated hoặc incorrect information. Data enrichment services update records với fresh information từ external sources. Data governance policies define ownership và responsibilities.

## Kết luận

Từ điển thuật ngữ này cung cấp nền tảng kiến thức vững chắc về các khái niệm CRM. Việc hiểu rõ từng thuật ngữ giúp xây dựng hệ thống CRM hiệu quả và phù hợp với nhu cầu kinh doanh thực tế.
