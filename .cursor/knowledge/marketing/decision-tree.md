# Marketing Decision Tree - Cây Quyết Định Marketing

## 1. Email Marketing Decision Tree

```
BẮT ĐẦU: Quyết định Email Marketing
│
├─► Mục tiêu chính của email?
│   │
│   ├─► Tăng doanh số trực tiếp
│   │   │
│   │   └─► LOOP: Đi đến "Campaign Type Decision"
│   │
│   ├─► Xây dựng mối quan hệ khách hàng
│   │   │
│   │   └─► Newsletter / Drip Campaign
│   │       │
│   │       ├─► Frequency: 1-2 lần/tuần
│   │       ├─► Content: Giá trị, không bán hàng trực tiếp
│   │       └─► Focus: Education, storytelling
│   │
│   ├─► Khôi phục khách hàng cũ
│   │   │
│   │   └─► Re-engagement Campaign
│   │       │
│   │       ├─► Segment: Contacts inactive 60-90 ngày
│   │       ├─► Content: Win-back offers, "We miss you"
│   │       └─► Exit criteria: Nếu không engage sau 2 emails → suppress
│   │
│   └─► Giới thiệu sản phẩm mới
│       │
│       └─► Product Launch Campaign
│           │
│           ├─► Pre-launch: Teaser, waitlist
│           ├─► Launch: Multiple touchpoints
│           └─► Post-launch: Follow-up, social proof
│
│
├─► Audience size?
│   │
│   ├─► < 1,000 contacts
│   │   │
│   │   └─► Gửi tất cả, personalize manually
│   │
│   ├─► 1,000 - 50,000 contacts
│   │   │
│   │   └─► Segmentation cần thiết
│   │       │
│   │       ├─► Có clear segments? → Segment và personalize
│   │       └─► No clear segments? → RFM analysis trước
│   │
│   └─► > 50,000 contacts
│       │
│       └─► Việc gửi vào lúc nào?
│           │
│           ├─► Immediate (flash sale) → Batch gửi theo giờ
│           └─► Không urgent → Stagger sends theo engagement
│
│
├─► Content strategy?
│   │
│   ├─► Single message fits all?
│   │   │
│   │   └─► YES → Dùng dynamic content blocks
│   │       │
│   │       ├─► Cần personalization?
│   │       │   │
│   │       │   ├─► YES → Merge tags + dynamic blocks
│   │       │   └─► NO → Basic merge tags
│   │       │
│   │       └─► Cần different offers cho segments?
│   │           │
│   │           ├─► YES → Create segment-specific variants
│   │           └─► NO → One variant với dynamic offers
│   │
│   └─► Different messages cho different groups?
│       │
│       └─► YES → Create multiple variants
│           │
│           ├─► A/B test để optimize
│           └─► Send best performer to remaining
│
│
└─► Follow-up strategy?
    │
    ├─► Gửi một lần duy nhất?
    │   │
    │   └─► YES → Track metrics, learn for next time
    │
    └─► Multi-touch sequence?
        │
        ├─► Welcome series → 3-5 emails trong 10-14 ngày
        │
        ├─► Nurture sequence → 5-10 emails trong 30-60 ngày
        │
        └─► Re-engagement → 3-5 emails trong 2-3 tuần
```

## 2. Personalization Decision Tree

```
BẮT ĐẦU: Quyết định Personalization Level
│
├─► Bạn có data để personalize không?
│   │
│   ├─► Có - Basic data (name, email)
│   │   │
│   │   └─► Sử dụng basic personalization
│   │       ├─► {{firstName}}
│   │       ├─► {{companyName}}
│   │       └─► {{segment}}
│   │
│   ├─► Có - Behavioral data
│   │   │
│   │   ├─► Purchase history?
│   │   │   │
│   │   │   ├─► YES → Product recommendations, "You bought X"
│   │   │   └─► NO → Skip
│   │   │
│   │   ├─► Browsing history?
│   │   │   │
│   │   │   ├─► YES → "Based on your interest in..."
│   │   │   └─► NO → Skip
│   │   │
│   │   └─► Engagement history?
│   │       │
│   │       ├─► YES → RFM-based content
│   │       └─► NO → Skip
│   │
│   └─► Không có data
│       │
│       └─► Sử dụng generic content + collect data dần
│           │
│           ├─► Progressive profiling
│           ├─► Preference center
│           └─► Survey/quizzes
│
│
├─► Level of personalization?
│   │
│   ├─► Level 1: Basic (Safe)
│   │   │
│   │   └─► {{firstName}}, {{companyName}}
│   │
│   ├─► Level 2: Contextual (Good)
│   │   │
│   │   ├─► "Customers who bought X also bought Y"
│   │   ├─► "Based on your interest in category Z"
│   │   └─► "Your last order was on [date]"
│   │
│   ├─► Level 3: Behavioral (Effective)
│   │   │
│   │   ├─► "You left [product] in your cart"
│   │   ├─► "It's been X days since you visited"
│   │   └─► Product recommendations
│   │
│   └─► Level 4: Predictive (Advanced)
│       │
│       ├─► AI-generated content
│       ├─► "You might need X in Y days"
│       └─► Chỉ dùng khi có đủ data + testing
│
│
└─► Có thể personalization trở nên "creepy"?
    │
    ├─► Những thứ KHÔNG BAO GIỜ làm:
    │   ├─► "We saw you were on our site for 2 hours"
    │   ├─► "You looked at X, Y, Z products"
    │   ├─► Mention exact location
    │   └─► Reference other customers' behavior
    │
    └─► Luôn đảm bảo:
        ├─► Personalization add value
        ├─► Keep data aggregated/general
        ├─► Be transparent
        └─► Allow opt-out
```

## 3. Campaign Type Decision Tree

```
BẮT ĐẦU: Chọn Campaign Type
│
├─► Đây là campaign một lần hay recurring?
│   │
│   ├─► One-time event
│   │   │
│   │   ├─► Product launch
│   │   │   │
│   │   │   ├─► Timeline: 4-6 weeks
│   │   │   ├─► Sequence: Pre → Launch → Follow-up
│   │   │   └─► Channels: Email + Social + Ads
│   │   │
│   │   ├─► Seasonal promotion (Black Friday, etc.)
│   │   │   │
│   │   │   ├─► Timeline: 2-4 weeks trước event
│   │   │   ├─► Frequency: Escalate gradually
│   │   │   └─► Content: Urgency, exclusivity
│   │   │
│   │   ├─► Flash sale
│   │   │   │
│   │   │   ├─► Timeline: 24-48 hours
│   │   │   ├─► Frequency: Multiple sends
│   │   │   └─► Content: Countdown, limited stock
│   │   │
│   │   └─► Event invitation
│   │       │
│   │       ├─► Timeline: 3-4 weeks before
│   │       ├─► Sequence: Invite → Reminder → Last call
│   │       └─► Content: Value proposition, speakers
│   │
│   └─► Recurring/Ongoing
│       │
│       ├─► Newsletter
│       │   │
│       │   ├─► Frequency: Weekly or bi-weekly
│       │   ├─► Content: Mix of value + promotion
│       │   └─► Segments: By interest
│       │
│       ├─► Promotional series
│       │   │
│       │   ├─► Frequency: Monthly
│       │   ├─► Content: Product highlights
│       │   └─► Segments: By purchase history
│       │
│       └─► Content marketing
│           │
│           ├─► Frequency: Weekly
│           ├─► Content: Educational, entertaining
│           └─► Goal: Brand building, engagement
│
│
├─► Bạn đang targeting ai?
│   │
│   ├─► New leads (chưa mua)
│   │   │
│   │   └─► Lead nurturing sequence
│   │       ├─► Focus: Education, build trust
│   │       ├─► CTA: Gated content, consultation
│   │       └─► Length: 5-10 emails
│   │
│   ├─► Existing customers (đã mua)
│   │   │
│   │   ├─► Repeat purchase
│   │   │   │
│   │   │   ├─► Focus: New products, replenishment
│   │   │   └─► CTA: "Time to reorder?"
│   │   │
│   │   ├─► Upsell/Cross-sell
│   │   │   │
│   │   │   ├─► Focus: Complementary products
│   │   │   └─► CTA: "Complete your look"
│   │   │
│   │   └─► Loyalty/Retention
│   │       │
│   │       ├─► Focus: Appreciation, exclusive offers
│   │       └─► CTA: "Thank you" + reward
│   │
│   └─► Churned customers
│       │
│       └─► Win-back campaign
│           ├─► Focus: Re-engage, offer incentive
│           ├─► If no response → suppress
│           └─► Length: 2-3 emails max
│
│
└─► Call-to-action chính là gì?
    │
    ├─► Mua hàng
    │   │
    │   └─► Direct response campaign
    │
    ├─► Đăng ký event
    │   │
    │   └─► Registration campaign
    │
    ├─► Download content
    │   │
    │   └─► Lead generation campaign
    │
    ├─► Book meeting
    │   │
    │   └─► Outbound/appointment setting
    │
    └─► Increase engagement
        │
        └─► Engagement campaign
```

## 4. Segmentation Decision Tree

```
BẮT ĐẦU: Xây dựng Segmentation Strategy
│
├─► Bạn có những data nào?
│   │
│   ├─► Demographics (age, gender, location)
│   │   │
│   │   └─► Basic segmentation
│   │       ├─► Age groups
│   │       ├─► Geographic regions
│   │       └─► Gender
│   │
│   ├─► Firmographics (company, industry, size)
│   │   │
│   │   └─► B2B segmentation
│   │       ├─► Company size (SMB, Mid-market, Enterprise)
│   │       ├─► Industry vertical
│   │       └─► Job title/role
│   │
│   ├─► Behavioral data (purchase, engagement)
│   │   │
│   │   └─► Behavioral segmentation
│   │       ├─► RFM (Recency, Frequency, Monetary)
│   │       ├─► Purchase history
│   │       ├─► Engagement level
│   │       └─► Product preferences
│   │
│   └─► Psychographic data (preferences, interests)
│       │
│       └─► Interest-based segmentation
│           ├─► Content preferences
│           ├─► Communication preferences
│           └─► Value propositions
│
│
├─► Mục đích segmentation là gì?
│   │
│   ├─► Better targeting → Use behavioral + demographic
│   │
│   ├─► Personalization → Use preferences + interests
│   │
│   ├─► Increased relevance → Use behavioral
│   │
│   └─► Reduced churn → Use lifecycle stage
│
│
├─► Cấu trúc segment hierarchy:
│   │
│   ├─► Primary segments (tổng quan)
│   │   ├─► New leads
│   │   ├─► Active customers
│   │   ├─► At-risk customers
│   │   └─► Churned customers
│   │
│   └─► Secondary segments (chi tiết)
│       │
│       ├─► Trong "Active customers":
│       │   ├─► VIP (high value, loyal)
│       │   ├─► Regular (consistent purchases)
│       │   ├─► Occasional (sporadic purchases)
│       │   └─► Bargain hunters (price-sensitive)
│       │
│       └─► Trong "At-risk":
│           ├─► Declining engagement
│           ├─→ Long time no purchase
│           └─► Decreased activity
│
│
└─► Segment size và viability:
    │
    ├─► Minimum viable segment size?
    │   │
    │   ├─► High personalization: 100+
    │   ├─► Standard campaign: 500+
    │   └─► Statistical significance: 1000+
    │
    └─► Nếu segment quá nhỏ?
        │
        ├─► Merge với similar segment
        ├─► Widen criteria
        └─► Sử dụng dynamic content thay vì separate segment
```

## 5. Automation Journey Decision Tree

```
BẮT ĐẦU: Thiết kế Automation Journey
│
├─► Journey trigger là gì?
│   │
│   ├─► Event-based trigger
│   │   ├─► Contact submits form
│   │   ├─► Contact makes purchase
│   │   ├─► Contact abandons cart
│   │   ├─► Contact visits specific page
│   │   └─► Contact opens/clicks email
│   │
│   ├─► Date-based trigger
│   │   ├─► Birthday/anniversary
│   │   ├─► Membership anniversary
│   │   ├─► Subscription renewal date
│   │   └─► Scheduled date
│   │
│   ├─► Segment-based trigger
│   │   ├─► Contact enters segment
│   │   ├─► Contact changes lifecycle stage
│   │   └─► Contact score threshold reached
│   │
│   └─► Manual trigger
│       └─► User action/API call
│
│
├─► Journey có bao nhiêu steps?
│   │
│   ├─► Simple (2-3 steps)
│   │   │
│   │   └─► Best cho: Welcome, simple follow-up
│   │       Example: Welcome → 1 day later → Value email
│   │
│   ├─► Medium (4-7 steps)
│   │   │
│   │   └─► Best cho: Nurture, onboarding
│   │       Example: Welcome → Education series → Offer → Conversion
│   │
│   └─► Complex (8+ steps)
│       │
│       └─► Cần cẩn thận:
│           ├─► Monitor for infinite loops
│           ├─► Set maximum journey duration
│           ├─► Implement exit conditions
│           └─► Test all branches
│
│
├─► Cần branch/condition nào?
│   │
│   ├─► YES → Có bao nhiêu branches?
│   │   │
│   │   ├─► 2 branches (Yes/No)
│   │   │   │
│   │   │   └─► Opened email? Clicked? Purchased?
│   │   │
│   │   ├─► 3-4 branches
│   │   │   │
│   │   │   ├─► Engagement level (high/medium/low)
│   │   │   └─► Purchase behavior (bought/didn't buy)
│   │   │
│   │   └─► Multiple conditions (AND/OR)
│   │       │
│   │       └─► Consider simplifying
│   │
│   └─► NO → Linear journey
│       └─► Use delay nodes between actions
│
│
├─► Timing giữa các steps?
│   │
│   ├─► Immediate (real-time)
│   │   └─► Best cho: High-intent actions, urgent
│   │
│   ├─► Short delay (1-24 hours)
│   │   └─► Best cho: Follow-up to action
│   │
│   ├─► Medium delay (1-7 days)
│   │   └─► Best cho: Nurture sequences
│   │
│   └─► Long delay (1-4 weeks)
│       └─► Best cho: Lifecycle transitions
│
│
└─► Exit conditions nào cần thiết?
    │
    ├─► Unsubscribe → Exit immediately
    ├─► Bounce → Exit immediately
    ├─► Purchase completed → Exit (nếu là purchase journey)
    ├─► Maximum duration reached → Exit gracefully
    ├─► Too many emails → Exit (frequency cap)
    └─► Negative engagement → Exit re-engagement journey
```

## 6. Send Time Decision Tree

```
BẮT ĐẦU: Quyết định Send Time
│
├─► Bạn có đủ data để optimize không?
│   │
│   ├─► YES (> 1000 sends, 30+ days data)
│   │   │
│   │   ├─► Analyze by segment
│   │   │   │
│   │   │   ├─► B2B → Tuesday-Thursday, 9-11 AM
│   │   │   ├─► B2C → Evening/weekend options
│   │   │   └─► Each segment có thể khác nhau
│   │   │
│   │   └─► Use AI/ML để predict optimal time
│   │
│   └─► NO (limited data)
│       │
│       ├─► Sử dụng best practices:
│       │   ├─► B2B: Weekday mornings
│       │   ├─► B2C: Tuesday-Thursday or weekend
│       │   └─► General: 9 AM hoặc 6 PM local time
│       │
│       └─► Start collecting engagement data
│
│
├─► Segment của bạn thuộc loại nào?
│   │
│   ├─► B2B (business professionals)
│   │   │
│   │   ├─► Best days: Tuesday, Wednesday, Thursday
│   │   ├─► Best times: 8-10 AM, 2-4 PM
│   │   ├─► Avoid: Monday morning, Friday afternoon
│   │   └─► Consider: Time zones
│   │
│   ├─► B2C Consumers
│   │   │
│   │   ├─► Best days: Tuesday, Wednesday, Saturday
│   │   ├─► Best times: 6-8 PM hoặc 10-11 AM
│   │   ├─► Avoid: Monday, Sunday
│   │   └─► Consider: Age groups differently
│   │
│   ├─► Millennials/Gen Z
│   │   │
│   │   ├─► More flexible timing
│   │   ├─► Evening và weekend acceptable
│   │   └─► Mobile usage patterns matter
│   │
│   └─► Seniors
│       │
│       ├─► Earlier in the day
│       └─► Weekday preference
│
│
├─► Type của email campaign?
│   │
│   ├─► Time-sensitive (flash sale, deadline)
│   │   │
│   │   └─► Send khi audience awake
│   │       └─► A/B test to find best window
│   │
│   ├─► Transactional
│   │   │
│   │   └─► Send immediately (real-time)
│   │
│   ├─► Newsletter
│   │   │
│   │   └─► Consistent schedule (builds expectation)
│   │       └─► Test different days for your audience
│   │
│   └─► Nurture/Educational
│       │
│       └─► Flexible timing
│           └─► Optimize for engagement
│
│
└─► Scaling strategy cho large lists?
    │
    ├─► Stagger sends (batching)
    │   │
    │   ├─► Split list into 3-4 batches
    │   ├─► Send over 2-4 hours
    │   └─► Prevents email volume spikes
    │
    ├─► Priority-based sending
    │   │
    │   ├─► Most engaged → Send first
    │   ├─► Less engaged → Later batches
    │   └─► Maximizes early engagement
    │
    └─► Time-zone based sending
        │
        ├─► Group by timezone
        ├─► Send at optimal time per zone
        └─► Best for global audiences
```

## 7. Content Strategy Decision Tree

```
BẮT ĐẦU: Xây dựng Content Strategy
│
├─► Content purpose chính là gì?
│   │
│   ├─► Educate → Informational content
│   │   │
│   │   ├─► How-to guides
│   │   ├─► Tips and tricks
│   │   ├─► Best practices
│   │   └─► Industry insights
│   │
│   ├─► Entertain → Engaging content
│   │   │
│   │   ├─► Stories
│   │   ├─► User-generated content
│   │   ├─► Behind-the-scenes
│   │   └─► Memes/Trending topics
│   │
│   ├─► Inspire → Aspirational content
│   │   │
│   │   ├─► Customer success stories
│   │   ├─► Case studies
│   │   ├─► Transformation stories
│   │   └─► Expert interviews
│   │
│   └─► Convert → Promotional content
│       │
│       ├─► Product showcases
│       ├─► Special offers
│       ├─► Limited-time deals
│       └─► Call-to-action focused
│
│
├─► Balance giữa value và promotion?
│   │
│   ├─► 80/20 Rule (Industry standard)
│   │   │
│   │   ├─► 80% Value content
│   │   └─► 20% Promotion
│   │
│   ├─► 70/30 Rule (B2B often)
│   │   │
│   │   ├─► 70% Educational
│   │   └─► 30% Promotional
│   │
│   └─► Full promotional
│       │
│       └─► Chỉ cho: Flash sales, urgent offers
│           └─► Risk: Higher unsubscribes
│
│
├─► Content format nào?
│   │
│   ├─► Text-heavy (Newsletter style)
│   │   │
│   │   ├─► Good cho: Thought leadership
│   │   └─► Tips: Scannable headers, bullet points
│   │
│   ├─► Visual-heavy (Image-focused)
│   │   │
│   │   ├─► Good cho: Product showcases
│   │   └─► Tips: Alt text, fallback text
│   │
│   ├─► Mixed (Hybrid)
│   │   │
│   │   ├─► Good cho: General purpose
│   │   └─► Tips: Balance images và text
│   │
│   └─► Interactive (AMP, polls)
│       │
│       └─► Good cho: High engagement
│           └─► Tips: Progressive enhancement
│
│
└─► Content calendar structure?
    │
    ├─► Weekly newsletter
    │   ├─► Monday: Industry news
    │   ├─► Tuesday: Tips/Tutorial
    │   ├─► Wednesday: Customer story
    │   ├─► Thursday: Product update
    │   └─► Friday: Fun/Engagement
    │
    ├─► Monthly campaign
    │   ├─► Week 1: Educational
    │   ├─► Week 2: Product spotlight
    │   ├─► Week 3: Case study/Social proof
    │   └─► Week 4: Special offer/Promo
    │
    └─► Campaign-based
        └─► Align với product launches, events
```

## 8. Testing Decision Tree

```
BẮT ĐẦU: Quyết định A/B Test Strategy
│
├─► Bạn có đủ traffic để test không?
│   │
│   ├─► High traffic (> 10,000 emails/send)
│   │   │
│   │   ├─► Test multiple elements simultaneously
│   │   ├─► Longer test duration (2-4 weeks)
│   │   └─► Multiple variants (3-4)
│   │
│   ├─► Medium traffic (1,000-10,000)
│   │   │
│   │   ├─► Test one element at a time
│   │   ├─► Shorter test (1-2 weeks)
│   │   └─► 2 variants max
│   │
│   └─► Low traffic (< 1,000)
│       │
│       ├─► Combine with historical data
│       ├─► Test less frequently
│       └─► A/B test subject lines, everything else conservative
│
│
├─► Test element nào trước?
│   │
│   ├─► Priority by impact:
│   │   │
│   │   ├─► 1. Subject Line (highest impact)
│   │   │   │
│   │   │   ├─► Test: Length, personalization, urgency
│   │   │   └─► Metric: Open rate
│   │   │
│   │   ├─► 2. CTA (conversion driver)
│   │   │   │
│   │   │   ├─► Test: Text, color, placement, size
│   │   │   └─► Metric: Click rate
│   │   │
│   │   ├─► 3. Send time
│   │   │   │
│   │   │   ├─► Test: Day, time
│   │   │   └─► Metric: Engagement
│   │   │
│   │   ├─► 4. Content/Offers
│   │   │   │
│   │   │   ├─► Test: Different offers, angles
│   │   │   └─► Metric: Conversion rate
│   │   │
│   │   └─► 5. Design/Layout
│   │       │
│   │       ├─► Test: Visual hierarchy
│   │       └─► Metric: Engagement
│   │
│   └─► Don't test everything at once
│       │
│       └─► One change at a time → clear results
│
│
├─► Sample size calculation:
│   │
│   ├─► Baseline open rate: 20%
│   │   │
│   │   ├─► Detect 10% lift (to 22%):
│   │   │   └─► Need ~16,000 per variant
│   │   │
│   │   ├─► Detect 20% lift (to 24%):
│   │   │   └─► Need ~4,000 per variant
│   │   │
│   │   └─► Detect 50% lift (to 30%):
│   │       └─► Need ~700 per variant
│   │
│   └─► Baseline click rate: 2%
│       │
│       ├─► Detect 20% lift:
│       │   └─► Need ~24,000 per variant
│       │
│       └─► Click tests need MORE traffic than open tests
│
│
└─► Khi nào kết luận test?
    │
    ├─► Statistical significance reached?
    │   │
    │   ├─► YES (>95% confidence) → Implement winner
    │   │
    │   ├─► Close but not there (~90%) → Continue testing
    │   │
    │   └─► NO → Continue or increase sample size
    │
    ├─► Test duration reached?
    │   │
    │   ├─► YES → Analyze và decide
    │   │   ├─► Clear winner → Implement
    │   │   └─► No difference → Keep current
    │   │
    │   └─► NO → Continue unless poor performance
    │
    └─► Winner clear?
        │
        ├─► YES → Implement và document learnings
        │
        └─► NO (marginal difference) → Keep current, test again later
```

## 9. Compliance Decision Tree

```
BẮT ĐẦU: Quyết định Compliance Requirements
│
├─► Ai là audience của bạn?
│   │
│   ├─► EU citizens/companies
│   │   │
│   │   └─► GDPR applies
│   │       │
│   │       ├─► Need explicit consent
│   │       ├─► Right to access
│   │       ├─► Right to erasure
│   │       ├─► Data portability
│   │       └─► 30-day response window
│   │
│   ├─► California residents
│   │   │
│   │   └─► CCPA applies
│   │       │
│   │       ├─► Right to know
│   │       ├─► Right to delete
│   │       ├─► Right to opt-out
│   │       └─► Non-discrimination
│   │
│   ├─► Brazil residents
│   │   │
│   │   └─► LGPD applies
│   │       │
│   │       ├─► Similar to GDPR
│   │       └─► Legal basis required
│   │
│   └─► General (no specific regulation)
│       │
│       └─► Follow CAN-SPAM (US) hoặc best practices
│
│
├─► Bạn có purchased/ rented list không?
│   │
│   ├─► YES
│   │   │
│   │   ├─► ⚠️ High risk - most regulations require consent
│   │   │
│   │   ├─► Purchased lists = likely non-compliant
│   │   │   └─► Recommendation: Don't use
│   │   │
│   │   └─► Rented lists = consent unclear
│   │       └─► Recommendation: Verify consent, re-permission
│   │
│   └─► NO (organic list)
│       │
│       ├─► Verify consent was explicit
│       ├─► Document consent records
│       └─► Regular list hygiene
│
│
├─► Consent collection method:
│   │
│   ├─► Single opt-in
│   │   │
│   │   └─► Risk: Higher invalid emails
│   │       └─► Add verification step
│   │
│   └─► Double opt-in (recommended)
│       │
│       └─► Benefits:
│           ├─► Confirms email validity
│           ├─► Shows explicit intent
│           ├─► Strong legal evidence
│           └─► Reduces spam complaints
│
│
├─► Required elements cho compliance:
│   │
│   ├─► Email identification
│   │   ├─► Physical address
│   │   └─► Sender name/company
│   │
│   ├─► Unsubscribe mechanism
│   │   ├─► Easy to find
│   │   ├─► One-click unsubscribe
│   │   ├─► Process within 10 days (CAN-SPAM)
│   │   └─► Honor immediately (best practice)
│   │
│   └─► Disclosure
│       └─► Clear why you're emailing
│           └─► What's in it for them
│
│
└─► Data retention policy:
    │
    ├─► How long to keep inactive contacts?
    │   │
    │   ├─► 6 months - 1 year no engagement → Consider suppression
    │   ├─► 1-2 years no engagement → Suppress or re-engagement
    │   └─► After re-engagement failure → Remove
    │
    └─► Document retention rules
        │
        ├─► Consent records: Keep as long as relationship active
        ├─► Transaction data: Keep for legal requirements
        └─► Activity logs: Keep for analytics/metrics
```

## 10. List Quality Decision Tree

```
BẮT ĐẦU: Đánh giá List Quality
│
├─► Health metrics hiện tại?
│   │
│   ├─► Bounce rate
│   │   │
│   │   ├─► < 2% → Healthy
│   │   ├─► 2-5% → Needs attention
│   │   └─► > 5% → Critical - clean immediately
│   │
│   ├─► Complaint rate
│   │   │
│   │   ├─► < 0.1% → Healthy
│   │   └─► > 0.1% → Critical - review practices
│   │
│   ├─► Unsubscribe rate
│   │   │
│   │   ├─► < 0.5% → Healthy
│   │   ├─► 0.5-1% → Monitor
│   │   └─► > 1% → Review frequency/content
│   │
│   └─► Engagement rate
│       │
│       ├─► > 25% open rate → Very healthy
│       ├─► 15-25% → Good
│       ├─► 5-15% → Needs improvement
│       └─► < 5% → Re-engagement or suppress
│
│
├─► Cần clean up không?
│   │
│   ├─► Bounce rate > 2%?
│   │   │
│   │   └─► YES → Remove hard bounces, re-try soft bounces
│   │
│   ├─► Engagement dropping?
│   │   │
│   │   └─► YES → Re-engagement campaign
│   │
│   ├─► List growing but engagement declining?
│   │   │
│   │   └─► YES → Quality issue, not just quantity
│   │
│   └─► Complaint rate increasing?
│       │
│       └─► YES → Review targeting and content
│
│
├─► Cleanup strategy:
│   │
│   ├─► Immediate actions
│   │   ├─► Remove all hard bounces
│   │   ├─► Suppress all spam complaints
│   │   └─► Honor all unsubscribes
│   │
│   ├─► Weekly maintenance
│   │   ├─► Remove new bounces
│   │   ├─► Update engagement scores
│   │   └─► Review complaint patterns
│   │
│   ├─► Monthly review
│   │   ├─► Segment by engagement
│   │   ├─► Identify at-risk contacts
│   │   └─► Review feedback loops
│   │
│   └─► Quarterly deep clean
│       ├─► Re-engagement campaigns
│       ├─► List re-verification
│       └─► Strategy review
│
│
└─► Re-engagement campaign cho inactive?
    │
    ├─► Define "inactive"
    │   ├─► No opens in 90+ days
    │   ├─► No clicks in 120+ days
    │   └─► No purchases in 180+ days
    │
    ├─► Re-engagement sequence
    │   ├─► Step 1: "We miss you" + incentive offer
    │   ├─► Step 2: "Is this still relevant?" (if no response)
    │   └─► Step 3: Final chance + confirmation
    │
    └─► After re-engagement fails
        │
        ├─► If no engagement after 2-3 emails → Suppress
        ├─► Document reason: "re-engagement failed"
        └─► Never re-add to list
```

---

## 11. marketingskills Routing Tree (sync 2026-07-15)

> Mục đích: routing request → category → knowledge section → implementation. Mỗi decision dưới đây map 1 trigger phrase đến 1 knowledge file đã có sẵn (không tạo file mới — Superpowers concept-ref pattern, xem `skill-registry.mdc §8.1`).

### 11.1 Routing cho Conversion Optimization

```
"Cải thiện conversion trang"
   │
   ├─► Page type?
   │   ├─► Landing page → best-practice.md §2.1 + checklist.md §9.1.1
   │   ├─► Pricing page  → best-practice.md §5.2 + architecture.md §4.1.2
   │   ├─► Signup form   → best-practice.md §2.2 + anti-pattern.md §9.1.2
   │   └─► Onboarding    → best-practice.md §5.1 + architecture.md §4.1.2
   │
   ├─► Optimization target?
   │   ├─► Form fields    → best-practice.md §2.2 §2.3
   │   ├─► CTA copy       → best-practice.md §2.4
   │   ├─► Social proof   → best-practice.md §2.5
   │   └─► Page speed     → performance rules (vercel-react-best-practices)
   │
   └─► A/B test setup → best-practice.md §8.1 + checklist.md §9.5.2

"Optimize onboarding activation"
   │
   ├─► Activation event defined? 
   │   ├─► Yes  → best-practice.md §5.1 + architecture.md §4.1.2
   │   └─► No   → faq.md §4.2 "Định nghĩa activation event"
   │
   └─► Issues?
       ├─► Drop-off at step 3+ → checklist.md §9.1.1
       ├─► Low day-1 retention → anti-pattern.md §9.1.5
       └─► No clear aha moment → faq.md §4.2 "Tìm aha moment"

"Setup exit popup"
   │
   ├─► Type?
   │   ├─► Exit-intent  → best-practice.md §2.4 + checklist.md §9.1.2
   │   └─► Time-delayed → best-practice.md §2.4
   │
   └─► Targeting?
       ├─► All visitors  → ❌ anti-pattern.md §9.1.4
       └─► High-intent only → best-practice.md §2.4 ✓

"Paywall upgrade flow"
   │
   ├─► Trigger?
   │   ├─► Feature limit hit → architecture.md §4.7 + best-practice.md §5.2
   │   └─► Trial expiration → best-practice.md §5.2
   │
   └─► Offer?
       ├─► Discount  → best-practice.md §10.5 (offer stack)
       └─► Plan switch → best-practice.md §10.4 (pricing)
```

### 11.2 Routing cho Content & Copy

```
"Viết email subject line"
   │
   ├─► Email type?
   │   ├─► Newsletter  → best-practice.md §2.1 (subject A/B)
   │   ├─► Cold email  → best-practice.md §2.5
   │   └─► Transactional → best-practice.md §2.10
   │
   └─► Anti-pattern check → anti-pattern.md §9.2.1 (RE:Viagra)

"Soạn cold email sequence"
   │
   ├─► Number of touches?
   │   ├─► 3-5 emails over 2 weeks → best-practice.md §2.5
   │   └─► 7+ emails / multi-channel → best-practice.md §2.5 + architecture.md §4.2.2
   │
   └─► Personalization depth?
       ├─► Basic (name, company) → best-practice.md §2.5
       └─► Trigger event → anti-pattern.md §9.2.4

"Generate social post from blog"
   │
   ├─► Platforms?
   │   ├─► LinkedIn / Twitter → best-practice.md §2.6 + checklist.md §9.2.4
   │   ├─► Instagram / TikTok → best-practice.md §2.6 (image + video)
   │   └─► Multi-platform    → architecture.md §4.2.3
   │
   └─► Assets?
       ├─► Image (AI) → best-practice.md §2.7 + anti-pattern.md §9.2.6
       ├─► Video (programmatic) → best-practice.md §2.8
       └─► Carousel → best-practice.md §2.6

"SMS marketing"
   │
   ├─► Compliance? → anti-pattern.md §9.2.5 + checklist.md §9.2.3
   ├─► Frequency? → best-practice.md §2.9
   └─► Opt-in flow? → best-practice.md §2.9 + architecture.md §4.2.2
```

### 11.3 Routing cho SEO & Discovery

```
"SEO audit"
   │
   ├─► Site size?
   │   ├─► <1k pages   → best-practice.md §3.1 + architecture.md §4.3.1
   │   └─► >1k pages   → architecture.md §4.3.1 (crawler scale)
   │
   └─► Issues found?
       ├─► Indexing   → faq.md §3.1 "Tại sao page không index"
       ├─► Schema     → architecture.md §4.3.3 + checklist.md §9.3.4
       ├─► Cannibalization → faq.md §3.3
       └─► Speed      → performance rules

"Optimize cho AI search"
   │
   ├─► Engine target?
   │   ├─► ChatGPT / Claude / Gemini → architecture.md §4.3.4 + best-practice.md §3.1
   ├─► Perplexity → best-practice.md §3.1
   └─► Google AI Overviews → architecture.md §4.3.3 (schema) + best-practice.md §3.1
   │
   └─► Has llms.txt? → best-practice.md §3.1 ✓ ; else → checklist.md §9.3.2 ✗

"Build 1000 programmatic pages"
   │
   ├─► Data source? → best-practice.md §3.2 + architecture.md §4.3.2
   ├─► Template strategy? → architecture.md §4.3.2
   ├─► Quality gate? → anti-pattern.md §9.3.2 + checklist.md §9.3.3
   └─► Volume? 
       ├─► <1k → manageable
       └─► >10k → architecture.md §4.3.2 + warning: anti-pattern.md §9.3.2

"Compare page: [competitor] vs [us]"
   │
   ├─► Data gathering → best-practice.md §3.3 + architecture.md §4.9.6
   └─► Template → best-practice.md §3.3

"Schema markup issue"
   │
   ├─► Type?
   │   ├─► Product / Offer → architecture.md §4.3.3 + best-practice.md §3.4
   │   ├─► Article / FAQ   → best-practice.md §3.4
   │   └─► LocalBusiness   → best-practice.md §3.4
   │
   └─► Validation → checklist.md §9.3.4 + Rich Results Test

"App Store Optimization"
   │
   ├─► iOS / Android → best-practice.md §3.5 + checklist.md §9.3.5
   └─► Localization → best-practice.md §3.5
```

### 11.4 Routing cho Paid & Distribution

```
"Launch Google/Meta ads"
   │
   ├─► Conversion tracking? → checklist.md §9.4.1 ✗ blocker
   ├─► Audience size? → checklist.md §9.4.1 (need > 1000)
   ├─► Creative variants? → best-practice.md §4.2 + checklist.md §9.4.1
   └─► Campaign structure? → best-practice.md §4.1 + anti-pattern.md §9.4.1

"Creative fatigue (CTR drop)"
   │
   ├─► Last refresh? → anti-pattern.md §9.4.2 (> 14 days = refresh)
   └─► Build new variants → best-practice.md §4.2 + architecture.md §4.4.2
```

### 11.5 Routing cho Measurement & Testing

```
"Setup tracking"
   │
   ├─► Tool?
   │   ├─► GA4 → best-practice.md §6.1 + architecture.md §4.5.1
   │   ├─► Mixpanel / Amplitude → best-practice.md §6.1
   │   └─► Custom (Kafka + warehouse) → architecture.md §4.5.1
   │
   └─► Event taxonomy → architecture.md §4.5.1 + checklist.md §9.5.1

"Run A/B test"
   │
   ├─► Hypothesis stage → anti-pattern.md §9.5.1 (max 3/page)
   ├─► Sample size → checklist.md §9.5.2 + decision tree
   │   ├─► Baseline 5%, MDE +10% → ~3,800/total (typical)
   │   └─► Use calculator: optimizely.com/sample-size
   ├─► Duration → checklist.md §9.5.2 + decision tree
   │   ├─► Min 1 week (capture weekday cycle)
   │   └─► Min 2 weeks (capture seasonality)
   └─► Stop criteria → checklist.md §9.5.2 (sample + p)

"Attribution"
   │
   ├─► Model?
   │   ├─► Last-touch (simple) → architecture.md §4.5.3 (default)
   │   ├─► Data-driven (ML) → architecture.md §4.5.3 (Shapley)
   │   └─► Need more detail → best-practice.md §6.2
   └─► Cross-device? → architecture.md §4.5.1 (identity stitching)
```

### 11.6 Routing cho Retention

```
"High churn detected"
   │
   ├─► Diagnosis
   │   ├─► Voluntary (cancel intent) → architecture.md §4.6.2 + best-practice.md §7.1
   │   ├─► Involuntary (failed payment) → architecture.md §4.6.3 + best-practice.md §7.1
   │   └─► Passive (low usage) → best-practice.md §7.1 + segment re-engagement
   │
   └─► Save offer
       ├─► Discount → best-practice.md §10.5
       ├─► Pause   → architecture.md §4.6.2 + checklist.md §9.6.1
       └─► Plan downgrade → best-practice.md §10.4

"Dunning system"
   │
   ├─► Cadence → architecture.md §4.6.3 + checklist.md §9.6.1
   ├─► Recovery target → architecture.md §4.6.3 (40-60% in 14d)
   └─► Anti-pattern → anti-pattern.md §9.6.1
```

### 11.7 Routing cho Growth Engineering

```
"Build free tool"
   │
   ├─► Tool type?
   │   ├─► Calculator / Grader → architecture.md §4.7.1 + best-practice.md §9.2
   │   ├─► Template / Generator → best-practice.md §9.2
   │   └─► Embed widget → architecture.md §4.7.1
   │
   └─► Lead gate?
       ├─► Yes → architecture.md §4.7.1 (ethical gate)
       └─► No  → best-practice.md §9.2 (faster viral loop)

"Setup referral program"
   │
   ├─► Reward type → best-practice.md §9.3 + checklist.md §9.7.2
   ├─► Fraud guardrails → architecture.md §4.7.2 + anti-pattern.md §9.7.2
   └─► Tier / payout → architecture.md §4.7.2 + checklist.md §9.7.2

"Co-marketing"
   │
   ├─► ICP overlap > 30%? → anti-pattern.md §9.7.3 ✗ 
   ├─► Joint asset plan → checklist.md §9.7.3 + architecture.md §4.7.3
   └─► Tracking → architecture.md §4.7.3 (UTM partner slug)
```

### 11.8 Routing cho Strategy & Monetization

```
"Đặt giá sản phẩm"
   │
   ├─► Tiered or flat?
   │   ├─► Tiered  → best-practice.md §10.4 + checklist.md §9.8.1
   │   └─► Flat + usage → best-practice.md §10.4
   │
   └─► Optimize
       ├─► A/B test prices → best-practice.md §10.4 + decision tree §11.5
       └─► Annual discount → best-practice.md §10.4

"Launch strategy"
   │
   ├─► New product? → architecture.md §4.8.3 + checklist.md §9.8.3
   ├─► New feature? → architecture.md §4.8.3 (smaller scope)
   └─► Waitlist? → anti-pattern.md §9.8.2 (launch without waitlist = fail)

"Quarterly marketing plan"
   │
   ├─► Template → architecture.md §4.8.4 + best-practice.md §10.1
   ├─► Tactic ideas → best-practice.md §10.1 (140 ideas catalog)
   └─► Channel mix → architecture.md §4.8.4 + best-practice.md §10.1
```

### 11.9 Routing cho Sales & RevOps

```
"Setup lead scoring"
   │
   ├─► Inputs?
   │   ├─► Form data only → ❌ anti-pattern.md §9.9.1
   │   └─► Behavior + form → architecture.md §4.9.1 + best-practice.md §11.7
   │
   └─► Routing
       ├─► By expertise → checklist.md §9.9.1
       └─► By territory → architecture.md §4.9.1

"Outreach campaign"
   │
   ├─► Sequence
   │   ├─► 5-7 touches → architecture.md §4.9.3 + checklist.md §9.9.3
   │   └─► Multi-channel → best-practice.md §11.2
   │
   └─► Quality
       ├─► Bounce handling → checklist.md §9.9.3
       └─► Reply handling → architecture.md §4.9.3

"Customer research"
   │
   ├─► Recruitment → checklist.md §9.9.5 + best-practice.md §11.5
   ├─► Interview guide → best-practice.md §11.5
   ├─► Synthesis → architecture.md §4.9.5 + JTBD framework
   └─► Anti-pattern → anti-pattern.md §9.9.7 (sampling bias)

"PR pitch"
   │
   ├─► Media list → checklist.md §9.9.4 + best-practice.md §11.3
   ├─► Pitch angle → best-practice.md §11.3 + anti-pattern.md §9.9.6
   └─► Coverage tracking → architecture.md §4.9.4

"Marketing council brainstorm"
   │
   ├─► Persona count → best-practice.md §11.7 (5-7)
   ├─► Context passed → glossary.md §13 (product-marketing context) mandatory
   └─► Output format → best-practice.md §11.7 (prioritized ideas)

"Setup marketing loop (recurring agent)"
   │
   ├─► Type
   │   ├─► Content   → architecture.md §4.9.8 + checklist.md §9.9.7
   │   ├─► SEO       → architecture.md §4.9.8
   │   ├─► Outreach  → architecture.md §4.9.8 + anti-pattern.md §9.9.9
   │   └─► Retention → architecture.md §4.9.8
   │
   └─► Must have
       ├─► Persistence → architecture.md §4.9.8
       ├─► Halt conditions → checklist.md §9.9.7 + architecture.md §4.9.8
       └─► Observability → architecture.md §4.9.8

"Directory submission"
   │
   ├─► Tier selection → best-practice.md §11.4 + checklist.md §9.9.7
   ├─► Submission plan → checklist.md §9.9.7 (1-2/week)
   └─► Quality check → checklist.md §9.9.7 + anti-pattern.md §9.9.10
```

### 11.10 Master Decision Tree (Catch-all)

```
User request về marketing
   │
   ├─► Has specific category keyword? (cro/seo/ads/launch/pricing/...)
   │   ├─► Yes → jump to relevant §11.1-§11.9
   │   └─► No  → continue
   │
   ├─► Has specific skill slug? (signup-flow-cro, ab-test-setup, ...)
   │   ├─► Yes → glossary.md §12 (v1.x rename map)
   │   │
   │   └─► v2.0 slug → glossary.md §11 routing table
   │
   ├─► Has product context loaded? (see glossary.md §13)
   │   ├─► Yes → execute skill per §11.X
   │   └─► No  → read .agents/product-marketing.md first
   │           (if missing: ask 3 minimal questions, scaffold)
   │
   └─► Apply pre-flight blocker check (checklist.md §9.10)
       ├─► Pass → execute
       └─► Fail → surface blockers to user
```

---

## 12. Routing Performance Notes

- Mỗi routing step < 100ms (lookup section, no file creation)
- Decision tree compiled once into Python module `cursor_framework/context_router.py` §marketing
- Edge cases logged in `decisions/marketing/<date>.md` for monthly tuning
