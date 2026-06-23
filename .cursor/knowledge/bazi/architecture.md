# Bazi Architecture - Kiến Trúc Hệ Thống Bazi

## Tổng quan kiến trúc

Hệ thống Bazi là một nền tảng phân tích phong thủy và tử vi được xây dựng trên kiến trúc microservices, cho phép mở rộng linh hoạt và tích hợp đa nền tảng. Kiến trúc được thiết kế theo nguyên tắc Domain-Driven Design (DDD), tách biệt rõ ràng các domain nghiệp vụ và infrastructure. Hệ thống bao gồm các module chính: Core Engine (xử lý tính toán Bazi), API Gateway, Database Layer, Cache Layer, AI/ML Services, và Frontend Applications.

Kiến trúc tuân thủ mô hình Layered Architecture với sự phân tách rõ ràng giữa Presentation Layer, Business Logic Layer, Data Access Layer, và Infrastructure Layer. Mỗi layer có trách nhiệm riêng biệt và giao tiếp thông qua các interfaces được định nghĩa rõ ràng. Điều này đảm bảo tính maintainable, testable, và scalable của hệ thống trong quá trình phát triển và vận hành lâu dài.

## Kiến trúc chi tiết các thành phần

### 1. Core Engine Layer - Tầng Xử Lý Tính Toán Cốt Lõi

Core Engine là thành phần quan trọng nhất của hệ thống, chịu trách nhiệm thực hiện tất cả các tính toán liên quan đến Bazi. Module này được viết bằng các ngôn ngữ có hiệu suất cao như TypeScript, Python, hoặc Rust để đảm bảo tốc độ xử lý. Core Engine bao gồm các submodule chính: LunarCalendarService (chuyển đổi Dương Lịch sang Âm Lịch), BaZiCalculator (tính toán Bát Tự), ElementAnalyzer (phân tích Ngũ Hành), RelationshipResolver (xác định quan hệ giữa các yếu tố).

LunarCalendarService sử dụng thuật toán chuyển đổi chính xác giữa Dương Lịch và Âm Lịch, bao gồm cả các năm nhuận âm lịch. Đây là module foundation vì hầu hết các tính toán Bazi đều dựa trên ngày tháng âm lịch. Thuật toán cần xử lý múi giờ chính xác vì giờ sinh ảnh hưởng trực tiếp đến kết quả lá số. Service này được implement như một microservice riêng biệt, có thể được gọi từ bất kỳ ứng dụng nào cần thông tin âm lịch.

BaZiCalculator là module trung tâm thực hiện các tính toán chính: xác định thiên can và địa chi cho năm, tháng, ngày, giờ sinh; tính toán ngũ hành của từng cột; xác định thập thần; phân tích cục diện. Các thuật toán trong module này dựa trên các công thức toán học và logic nghiệp vụ chuyên sâu về Bazi. Module cần được test kỹ lưỡng với các test cases từ các nguồn uy tín để đảm bảo độ chính xác cao nhất.

ElementAnalyzer xử lý các phân tích liên quan đến ngũ hành: tính tổng số ngũ hành trong lá số, xác định ngũ hành vượng và ngũ hành thiếu, tính toán các chỉ số cân bằng ngũ hành. Module này cung cấp các API để các service khác có thể truy vấn thông tin ngũ hành. Kết quả từ ElementAnalyzer là input quan trọng cho các module phân tích cao cấp hơn như FortuneTeller và HoroscopeGenerator.

RelationshipResolver xác định các mối quan hệ giữa các yếu tố trong Bazi: Lục Hợp, Lục Xung, Tam Hợp, Tứ Hành Xung, và các quan hệ giữa các thiên can. Module này trả về ma trận quan hệ có thể được sử dụng để phân tích sự tương thích, xác định thời điểm tốt/xấu, và đưa ra các đề xuất phong thủy. RelationshipResolver là module có độ phức tạp cao vì cần xử lý nhiều loại quan hệ và các trường hợp đặc biệt.

### 2. API Gateway Layer - Tầng Cổng API

API Gateway đóng vai trò điểm đầu vào duy nhất cho tất cả các request từ client applications. Layer này xử lý authentication, authorization, rate limiting, request routing, và response caching. API Gateway được implement bằng Kong, AWS API Gateway, hoặc tự xây dựng bằng Node.js/Express với các middleware cần thiết. Tất cả các API endpoints được định nghĩa rõ ràng trong OpenAPI Specification để đảm bảo tính nhất quán và dễ dàng tích hợp.

Authentication trong API Gateway sử dụng JWT tokens với refresh token mechanism. Users được xác thực qua email/password, OAuth providers (Google, Facebook), hoặc phone number OTP. Mỗi user có một profile chứa thông tin Bazi cơ bản đã được tính toán sẵn để giảm thời gian xử lý cho các request thường xuyên. JWT tokens có thời hạn ngắn (15 phút) và refresh tokens có thời hạn dài hơn (30 ngày) để đảm bảo bảo mật.

Rate limiting được implement ở cả user level và IP level để ngăn chặn abuse và đảm bảo chất lượng dịch vụ cho tất cả users. Các endpoint có giới hạn request khác nhau tùy thuộc vào độ phức tạp của tính toán: simple endpoints có thể cho phép 100 requests/phút, trong khi các endpoints phân tích sâu có thể giới hạn ở mức 10 requests/phút. Rate limit information được trả về trong response headers để clients có thể xử lý phù hợp.

Request routing trong API Gateway phân phối requests đến các microservices tương ứng dựa trên URL path và các rules được cấu hình. Gateway sử dụng circuit breaker pattern để handle failures từ downstream services một cách graceful, trả về cached responses hoặc fallback responses khi services không khả dụng. Health checks được implement để monitor trạng thái của các microservices và tự động remove unhealthy services khỏi pool.

### 3. Data Access Layer - Tầng Truy Cập Dữ Liệu

Data Access Layer cung cấp interface thống nhất để truy cập các nguồn dữ liệu khác nhau: Relational Database (PostgreSQL/MySQL), Document Database (MongoDB), Cache (Redis), và Search Engine (Elasticsearch). Layer này sử dụng Repository Pattern để tách biệt logic truy cập dữ liệu khỏi business logic. Mỗi aggregate root trong domain có một repository tương ứng với các CRUD operations và các query methods chuyên biệt.

UserRepository quản lý thông tin người dùng: profile, authentication data, subscription status, và preferences. User entity là một trong những entity quan trọng nhất trong hệ thống vì nó chứa thông tin Bazi đã được tính toán sẵn (birth data, calculated BaZi). Các queries phổ biến như "tìm user theo email" hoặc "lấy thông tin subscription của user" được optimize với appropriate indexes. User data được replicated sang Redis để giảm latency cho các read-heavy operations.

BaZiRepository lưu trữ các lá số đã tính toán và các kết quả phân tích liên quan. Mỗi lá số được lưu với các computed fields: thiên can, địa chi, ngũ hành, thập thần, cục diện. Repository cũng lưu trữ các phiên bản khác nhau của cùng một lá số (khi người dùng thay đổi ngày sinh hoặc khi có cập nhật về thuật toán). History tracking được implement để support việc xem lại các phân tích trước đó.

ReportRepository quản lý các báo cáo phân tích chi tiết được tạo ra cho người dùng. Reports có thể được regenerate dựa trên lá số và thời điểm hiện tại, nên repository lưu trữ template và parameters thay vì static content. Cache mechanism được implement để lưu các reports thường xuyên được truy cập. Reports có thể được export ra various formats: PDF, HTML, JSON với appropriate rendering logic.

### 4. Caching Layer - Tầng Cache

Redis được sử dụng làm caching layer chính với các chiến lược cache khác nhau cho các loại dữ liệu khác nhau. Cache-aside pattern được áp dụng cho các read-heavy operations như lấy thông tin user, lá số, và các báo cáo thường xuyên được truy cập. Cache được invalidate theo TTL hoặc khi có data changes để đảm bảo consistency. Memory footprint của Redis được monitor để đảm bảo không vượt quá giới hạn và cache hit ratio được track để optimize caching strategy.

Session management cũng được xử lý qua Redis với TTL phù hợp cho từng loại session. User sessions, API sessions, và temporary calculation sessions có các TTL khác nhau. Session data bao gồm authentication tokens, user preferences, và recent calculation results. Redis cluster được setup với replication để đảm bảo high availability và failover capability.

Distributed locking được implement bằng Redis để handle concurrent access đến các shared resources. Ví dụ khi nhiều services cùng truy cập và update một lá số, distributed lock đảm bảo consistency. Lock timeout được set phù hợp để tránh deadlock và resource contention. Các operations như billing, subscription changes, và data migrations sử dụng locking mechanism này.

### 5. AI/ML Services Layer - Tầng Dịch Vụ AI/ML

AI/ML Services cung cấp các tính năng thông minh: phân tích lá số tự động, đề xuất cá nhân hóa, chatbot tư vấn, và dự đoán xu hướng. Layer này được xây dựng trên các ML frameworks như TensorFlow, PyTorch, hoặc sử dụng managed services như OpenAI API, Google Gemini. Các models được trained trên large datasets về Bazi readings và historical outcomes.

Interpretation Engine sử dụng NLP models để tạo ra các bản phân tích lá số tự động bằng ngôn ngữ tự nhiên. Engine nhận input là structured BaZi data và output là paragraphs về tính cách, vận mệnh, và đề xuất. Quality của interpretations được continuously improved thông qua feedback loop từ users và expert reviewers. Engine cũng hỗ trợ multiple languages để phục vụ users từ different regions.

Recommendation Engine sử dụng collaborative filtering và content-based approaches để đề xuất các sản phẩm và dịch vụ phù hợp với từng user. Recommendations được cá nhân hóa dựa trên BaZi profile, usage patterns, và explicit feedback. Engine tích hợp với e-commerce module để track conversion rates và optimize recommendation algorithms. A/B testing framework được implement để test các recommendation strategies mới.

Chatbot Service cung cấp conversational interface cho users để hỏi về lá số của họ, yêu cầu phân tích chi tiết, hoặc tìm hiểu về các khái niệm Bazi. Chatbot được implement bằng combination của rule-based logic và AI models. Context management cho phép users có multi-turn conversations về cùng một lá số. Integration với WhatsApp, Facebook Messenger, và website chat widgets mở rộng reach của service.

### 6. Frontend Applications - Các Ứng Dụng Frontend

Web Application được xây dựng bằng Next.js hoặc React với server-side rendering cho SEO và performance optimization. Application bao gồm các trang chính: landing page, user dashboard, BaZi calculator, report viewer, và settings. UI được design responsive để support cả desktop và mobile users. State management sử dụng Redux Toolkit hoặc Zustand với proper caching và optimistic updates.

Mobile Application được phát triển bằng React Native hoặc Flutter để support cả iOS và Android. App bao gồm các tính năng tương tự web application nhưng được optimize cho touch interfaces và offline usage. Local storage được sử dụng để cache user data và recent calculations. Push notifications được implement để remind users về favorable dates hoặc new features. App có integration với device calendar để schedule reminders.

Admin Dashboard cho phép administrators quản lý users, subscriptions, content, và system configurations. Dashboard cung cấp analytics về usage patterns, revenue metrics, và system health. CMS integration cho phép content team update interpretations và explanations mà không cần developer involvement. Role-based access control đảm bảo only authorized personnel có access đến sensitive functions.

## Database Schema Design

### Core Tables

Users table chứa thông tin authentication và profile. Các columns quan trọng: id (UUID), email, password_hash, phone, birth_date, birth_time, birth_timezone, gender, created_at, updated_at, subscription_tier, subscription_expires_at. Indexes được tạo trên email, phone, và subscription fields. Soft delete được implement để preserve user data và support data recovery.

BaZi readings table lưu trữ các lá số đã tính toán. Mỗi reading có relationship 1:1 với user nhưng có thể có multiple readings cho cùng user (khi user update birth info). Reading entity chứa tất cả các computed fields: year_can, year_chi, month_can, month_chi, day_can, day_chi, hour_can, hour_chi, element_counts, destiny_number, luck_number. Denormalized design được sử dụng để optimize read performance vì reads远远多于 writes.

Relationships table lưu trữ các mối quan hệ giữa users (cho tính năng so sánh lá số, tìm bạn đời). Relationships có type: FRIEND, PARTNER, BUSINESS, FAMILY. Compatibility scores được calculated và cached trong table. Graph database (Neo4j) có thể được sử dụng thay vì relational table để optimize traversal queries.

Subscriptions table tracking billing và subscription information. Integration với payment gateways (Stripe, PayPal) được implement để handle recurring payments. Webhook handlers process payment events và update subscription status. Invoice history được maintained cho compliance và user reference. Refund và cancellation logic được implement với proper state management.

## Security Architecture

Authentication sử dụng multi-factor authentication (MFA) cho enhanced security. Passwords được hashed bằng bcrypt với appropriate salt rounds. OAuth 2.0 flows được implement cho social logins. API keys được provided cho programmatic access với rate limiting cao hơn. Session tokens có short expiration và rotation mechanism để minimize security risks.

Authorization sử dụng role-based access control (RBAC) với predefined roles: GUEST, USER, PREMIUM_USER, ADMIN, SUPER_ADMIN. Permissions được defined theo resource và action. API Gateway enforce authorization checks trước khi routing requests đến services. Audit logging được implement để track sensitive operations và support security investigations.

Data encryption được applied ở cả data-at-rest và data-in-transit. TLS 1.3 được enforced cho all communications. Database encryption sử dụng AES-256 cho sensitive fields như PII và payment information. Key management được handled bằng cloud KMS services (AWS KMS, Azure Key Vault). Regular security audits và penetration testing được conducted để identify và fix vulnerabilities.

## Deployment Architecture

Container orchestration sử dụng Kubernetes cho container management, scaling, và high availability. Services được containerized với Docker và deployed lên Kubernetes cluster. Horizontal pod autoscaling được configured dựa trên CPU và memory usage. PodDisruptionBudgets đảm bảo minimum availability during maintenance và failures. Multi-region deployment được setup để minimize latency cho global users.

CI/CD pipeline sử dụng GitHub Actions hoặc GitLab CI để automate testing, building, và deployment. Pipeline bao gồm stages: lint, unit tests, integration tests, security scans, build, deploy to staging, smoke tests, deploy to production. Blue-green deployment strategy được sử dụng để minimize downtime và enable quick rollbacks. Canary deployments cho phép gradual rollout của new features với small percentage users.

Monitoring và observability được setup với Prometheus cho metrics, Grafana cho visualization, ELK stack cho logging, và Jaeger cho distributed tracing. Alerts được configured cho critical metrics và automated remediation được implement cho common issues. Regular SLO reviews và error budget tracking đảm bảo system reliability. Runbooks được maintained để guide operators through incident response procedures.

## Integration Architecture

Payment integrations với Stripe và PayPal handle subscriptions và one-time payments. Webhook handlers process payment events asynchronously. Idempotency được implement để handle duplicate events gracefully. Refund và dispute handling được automated với proper notifications to users.

Notification integrations với email providers (SendGrid, AWS SES), SMS providers (Twilio), và push notification services (Firebase) cung cấp multi-channel communications. Templates được managed centrally và supports multiple languages. Rate limiting được implemented per channel để avoid spam và maintain sender reputation.

Third-party API integrations với calendar services, social media platforms, và other Bazi resources mở rộng functionality của platform. API clients được implement với retry logic, circuit breakers, và proper error handling. Data synchronization với external services được handled asynchronously để avoid blocking main flows.

## Scalability và Performance Considerations

Database sharding được implemented khi data size vượt quá single node capacity. Sharding key được chọn carefully để ensure even distribution và minimize cross-shard queries. Consistent hashing được sử dụng để minimize data movement khi adding/removing shards.

Read replicas được configured để handle read-heavy workloads. Caching strategy được optimized để reduce database load. Query optimization với proper indexes và query plans. Connection pooling được used để maximize database connection efficiency.

Asynchronous processing với message queues (RabbitMQ, Kafka) cho các operations không cần immediate response: report generation, email sending, analytics processing. Workers consume messages và process asynchronously. Dead letter queues handle failed messages cho investigation và retry.

## Disaster Recovery và Business Continuity

Backup strategy bao gồm automated daily backups với point-in-time recovery capability. Backups được stored ở multiple geographic locations để ensure data durability. Regular backup restoration tests được conducted để verify backup integrity.

Multi-region deployment với active-active hoặc active-passive setup đảm bảo business continuity. Automated failover mechanisms detect failures và route traffic to healthy region. Data replication between regions được configured với appropriate consistency guarantees.

Incident response procedures được documented và regularly tested. Communication plans đảm bảo stakeholders được notified promptly during incidents. Post-mortem reviews được conducted after major incidents để prevent recurrence.
