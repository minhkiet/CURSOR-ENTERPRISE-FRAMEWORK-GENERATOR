# Marketing Best Practices - Thực Hành Tốt Nhất

## 1. Contact Management Best Practices

### 1.1 Sử Dụng Unified Contact Profile

Centralize tất cả contact data để có single source of truth, tránh duplicate records và ensure consistent personalization across all channels.

```typescript
// ❌ Anti-pattern: Multiple data sources without unification
interface CustomerData {
  ecommerceCustomer: {
    id: string;
    name: string;
    email: string;
  };
  supportCustomer: {
    id: string;
    customerName: string;
    emailAddress: string;
  };
  marketingContact: {
    contactId: string;
    fullName: string;
    emailAddr: string;
  };
}

// ✅ Best practice: Unified contact model
interface UnifiedContact {
  id: UUID;
  email: string; // Single source of truth
  profile: ContactProfile;
  
  // All integrations store data here
  integrations: {
    ecommerce?: EcommerceData;
    support?: SupportData;
    crm?: CRMData;
  };
}

class ContactUnificationService {
  async unifyContact(
    email: string,
    sources: ContactSource[]
  ): Promise<UnifiedContact> {
    // Find or create primary contact
    let contact = await this.contactRepo.findByEmail(email);
    
    if (!contact) {
      contact = UnifiedContact.create({ email });
    }
    
    // Merge data from all sources
    for (const source of sources) {
      contact.mergeFrom(source);
    }
    
    await this.contactRepo.save(contact);
    
    return contact;
  }
}
```

### 1.2 Implement Progressive Profiling

Thu thập contact data incrementally over time thay vì yêu cầu quá nhiều thông tin trong form ban đầu.

```typescript
// Progressive profiling configuration
interface ProgressiveProfileConfig {
  formId: UUID;
  fields: ProfileField[];
  priorityRules: PriorityRule[];
}

interface ProfileField {
  key: string;
  type: 'text' | 'select' | 'date' | 'number';
  required: boolean;
  weight: number; // Higher = more important
  showAfterViews?: number; // Show after N page views
  showAfterDays?: number; // Show after N days since first visit
}

// Progressive form selection algorithm
class ProgressiveProfilingService {
  selectFieldsForForm(
    contact: Contact,
    availableFields: ProfileField[],
    maxFields: number = 5
  ): ProfileField[] {
    const missingFields = availableFields.filter(
      field => !contact.hasField(field.key)
    );
    
    // Sort by priority: missing data > high value > low effort
    const sorted = missingFields.sort((a, b) => {
      const aScore = this.calculateFieldScore(a, contact);
      const bScore = this.calculateFieldScore(b, contact);
      return bScore - aScore;
    });
    
    return sorted.slice(0, maxFields);
  }
  
  private calculateFieldScore(
    field: ProfileField,
    contact: Contact
  ): number {
    let score = field.weight * 10;
    
    // Boost if this data would enable segmentation
    if (this.enablesSegmentation(field.key)) {
      score += 20;
    }
    
    // Boost if low completion rate (most users don't have it)
    const completionRate = this.getFieldCompletionRate(field.key);
    if (completionRate < 0.3) {
      score += 15;
    }
    
    // Penalize if form with this field has low conversion
    if (this.hasLowConversion(field.key)) {
      score -= 10;
    }
    
    return score;
  }
}
```

### 1.3 Data Quality Maintenance

Implement automated data quality checks và cleaning processes.

```typescript
class ContactDataQualityService {
  constructor(
    private emailValidator: EmailValidator,
    private phoneValidator: PhoneValidator
  ) {}
  
  async validateContact(contact: Contact): Promise<ValidationResult> {
    const issues: DataQualityIssue[] = [];
    
    // Email validation
    if (contact.email) {
      const emailValidation = await this.emailValidator.validate(contact.email);
      if (!emailValidation.valid) {
        issues.push({
          field: 'email',
          severity: 'error',
          message: emailValidation.reason
        });
      } else if (emailValidation.isRoleAccount) {
        issues.push({
          field: 'email',
          severity: 'warning',
          message: 'Email appears to be a role account (info@, support@)'
        });
      }
    }
    
    // Phone validation
    if (contact.phone) {
      const phoneValidation = this.phoneValidator.validate(contact.phone);
      if (!phoneValidation.valid) {
        issues.push({
          field: 'phone',
          severity: 'error',
          message: phoneValidation.reason
        });
      }
    }
    
    // Completeness check
    const profileCompleteness = this.calculateCompleteness(contact.profile);
    if (profileCompleteness < 0.3) {
      issues.push({
        field: 'profile',
        severity: 'warning',
        message: `Profile only ${Math.round(profileCompleteness * 100)}% complete`
      });
    }
    
    return {
      valid: !issues.some(i => i.severity === 'error'),
      issues
    };
  }
  
  // Scheduled data cleaning
  @Cron('0 2 * * *') // 2 AM daily
  async runDataCleaningTasks(): Promise<void> {
    await this.removeDuplicateContacts();
    await this.cleanInvalidEmails();
    await this.standardizePhoneNumbers();
    await this.updateDecayedEngagementScores();
  }
}
```

## 2. Email Marketing Best Practices

### 2.1 Email Template Best Practices

Thiết kế email templates responsive, accessible và maintainable.

```typescript
// Responsive email template structure
const emailTemplate = `
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{subject}}</title>
  <style>
    /* Mobile-first responsive design */
    .container {
      max-width: 600px;
      margin: 0 auto;
    }
    
    @media only screen and (max-width: 480px) {
      .container {
        width: 100% !important;
        padding: 10px !important;
      }
      .mobile-hidden {
        display: none !important;
      }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
      .email-body {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
      }
    }
  </style>
</head>
<body style="margin: 0; padding: 0;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
    <!-- Header -->
    <tr>
      <td class="header" style="padding: 20px; text-align: center;">
        <img src="{{headerLogo}}" alt="{{companyName}}" width="150">
      </td>
    </tr>
    
    <!-- Content -->
    <tr>
      <td class="content" style="padding: 30px 20px;">
        <h1 style="margin: 0 0 20px; font-size: 24px;">
          Xin chào {{contact.firstName || 'bạn'}},
        </h1>
        <p style="margin: 0 0 20px; line-height: 1.6;">
          {{mainContent}}
        </p>
      </td>
    </tr>
    
    <!-- CTA Button -->
    <tr>
      <td style="padding: 0 20px 30px; text-align: center;">
        <a href="{{ctaUrl}}" 
           style="display: inline-block; 
                  padding: 15px 40px; 
                  background-color: #0066cc;
                  color: #ffffff;
                  text-decoration: none;
                  border-radius: 4px;
                  font-weight: bold;">
          {{ctaText}}
        </a>
      </td>
    </tr>
    
    <!-- Footer -->
    <tr>
      <td class="footer" style="padding: 20px; font-size: 12px; color: #666;">
        <p style="margin: 0 0 10px;">
          {{companyName}} | {{companyAddress}}
        </p>
        <p style="margin: 0 0 10px;">
          Bạn nhận được email này vì đã đăng ký nhận bản tin từ chúng tôi.
        </p>
        <p style="margin: 0;">
          <a href="{{unsubscribeUrl}}" style="color: #666;">
            Hủy đăng ký
          </a> | 
          <a href="{{preferencesUrl}}" style="color: #666;">
            Cập nhật tùy chọn
          </a>
        </p>
      </td>
    </tr>
  </table>
  
  <!-- Tracking pixel -->
  <img src="{{trackingPixel}}" width="1" height="1" alt="" style="display:none;">
</body>
</html>
`;

// Template rendering with personalization
class EmailTemplateService {
  async renderEmail(
    templateId: UUID,
    contact: Contact,
    data: Record<string, any>
  ): Promise<RenderedEmail> {
    const template = await this.templateRepo.findById(templateId);
    
    const context = {
      contact,
      company: await this.getCompanySettings(),
      ...data
    };
    
    // Apply personalization
    let html = this.personalize(template.html, context);
    
    // Inline CSS for email client compatibility
    html = await this.inlineCss(html);
    
    // Replace merge tags
    html = this.replaceMergeTags(html, context);
    
    return {
      subject: this.personalize(template.subject, context),
      html,
      text: this.htmlToText(html)
    };
  }
}
```

### 2.2 Subject Line Best Practices

Optimize subject lines cho open rates với personalization và clear value proposition.

```typescript
class SubjectLineOptimizer {
  // Subject line templates
  private subjectTemplates = [
    {
      template: '{{contact.firstName}}, ưu đãi đặc biệt dành riêng cho bạn',
      emoji: '🎁',
      conditions: { hasFirstName: true, isCustomer: true }
    },
    {
      template: 'Khám phá bộ sưu tập mới {{productCategory}}',
      emoji: '✨',
      conditions: { hasCategory: true }
    },
    {
      template: 'Chỉ còn {{hoursLeft}} giờ - Giảm giá {{discountPercent}}%',
      emoji: '⏰',
      conditions: { hasUrgency: true }
    },
    {
      template: '{{companyName}} gửi tặng bạn quà sinh nhật',
      emoji: '🎂',
      conditions: { isBirthday: true }
    }
  ];
  
  async generateSubject(
    contact: Contact,
    campaign: Campaign
  ): Promise<string> {
    // Find best matching template
    const template = this.findBestTemplate(contact, campaign);
    
    // Personalize
    let subject = this.personalize(template.template, contact);
    
    // Add emoji (A/B test emoji vs no emoji)
    if (this.shouldUseEmoji(campaign)) {
      subject = `${template.emoji} ${subject}`;
    }
    
    // Truncate if too long
    if (subject.length > 50) {
      subject = subject.substring(0, 47) + '...';
    }
    
    return subject;
  }
  
  private shouldUseEmoji(campaign: Campaign): boolean {
    // A/B test: 50% get emoji
    const hash = this.hashString(campaign.id + campaign.name);
    return hash % 2 === 0;
  }
}
```

### 2.3 Send Time Optimization

Gửi emails vào thời điểm tối ưu cho từng contact dựa trên engagement history.

```typescript
class SendTimeOptimizationService {
  async calculateOptimalSendTime(contactId: UUID): Promise<SendTime> {
    // Get historical engagement data
    const engagementHistory = await this.analyticsService.getEngagementByHour(
      contactId
    );
    
    if (engagementHistory.length < 10) {
      // Not enough data, use segment average
      return this.getSegmentDefaultSendTime(contactId);
    }
    
    // Find best performing hours
    const hourPerformance = this.aggregateByHour(engagementHistory);
    
    // Weight by recency
    const weightedScores = this.weightByRecency(hourPerformance);
    
    // Find optimal time
    const optimalHour = this.findOptimalHour(weightedScores);
    
    // Apply business rules
    const adjustedTime = this.applyBusinessRules(optimalHour);
    
    return {
      sendAt: adjustedTime,
      confidence: this.calculateConfidence(engagementHistory.length)
    };
  }
  
  private aggregateByHour(history: EngagementEvent[]): Map<number, Metrics> {
    const byHour = new Map<number, Metrics>();
    
    for (const event of history) {
      const hour = event.timestamp.getHours();
      const metrics = byHour.get(hour) || { opens: 0, clicks: 0, emails: 0 };
      
      metrics.emails++;
      if (event.type === 'email_opened') metrics.opens++;
      if (event.type === 'email_clicked') metrics.clicks++;
      
      byHour.set(hour, metrics);
    }
    
    return byHour;
  }
  
  // Batch optimization for campaign send
  async optimizeCampaignSendTime(
    campaignId: UUID,
    contacts: Contact[]
  ): Promise<Map<UUID, SendTime>> {
    const results = new Map<UUID, SendTime>();
    
    // Group contacts by segment for batch processing
    const segments = this.groupBySegment(contacts);
    
    for (const [segmentId, segmentContacts] of segments) {
      // Get segment-level optimal times
      const segmentTimes = await this.getSegmentOptimalTimes(segmentId);
      
      for (const contact of segmentContacts) {
        // Personal optimization if enough data
        if (this.hasEnoughEngagementData(contact)) {
          results.set(contact.id, await this.calculateOptimalSendTime(contact.id));
        } else {
          // Use segment default
          results.set(contact.id, segmentTimes[0]);
        }
      }
    }
    
    return results;
  }
}
```

## 3. Segmentation Best Practices

### 3.1 Behavioral Segmentation

Tạo segments dựa trên behavior patterns thay vì chỉ demographic data.

```typescript
// Behavioral segment definitions
interface BehavioralSegment {
  id: UUID;
  name: string;
  type: 'engagement' | 'purchase' | 'browse' | 'lifecycle';
  criteria: SegmentCriteria;
}

class BehavioralSegmentationService {
  // High-engagement newsletter subscribers
  async identifyEngagedSubscribers(): Promise<UUID[]> {
    const sevenDaysAgo = subtractDays(new Date(), 7);
    
    return this.contactRepo.findByQuery(`
      SELECT DISTINCT c.id FROM contacts c
      JOIN email_events e ON e.contact_id = c.id
      WHERE e.type = 'email_opened'
        AND e.timestamp > $1
      GROUP BY c.id
      HAVING COUNT(*) >= 3
    `, [sevenDaysAgo]);
  }
  
  // Cart abandoners
  async identifyCartAbandoners(): Promise<UUID[]> {
    const oneDayAgo = subtractDays(new Date(), 1);
    const sevenDaysAgo = subtractDays(new Date(), 7);
    
    return this.contactRepo.findByQuery(`
      SELECT DISTINCT c.id FROM contacts c
      WHERE EXISTS (
        SELECT 1 FROM cart_events ce
        WHERE ce.contact_id = c.id
          AND ce.type = 'cart_created'
          AND ce.timestamp BETWEEN $1 AND $2
      )
      AND NOT EXISTS (
        SELECT 1 FROM cart_events ce
        WHERE ce.contact_id = c.id
          AND ce.type = 'cart_converted'
          AND ce.timestamp BETWEEN $1 AND $2
      )
    `, [sevenDaysAgo, oneDayAgo]);
  }
  
  // VIP customers
  async identifyVIPCustomers(): Promise<UUID[]> {
    return this.contactRepo.findByQuery(`
      SELECT c.id FROM contacts c
      WHERE c.lifetime_value >= 10000000  -- 10M VND
        AND c.order_count >= 5
        AND c.avg_order_value >= 2000000  -- 2M VND
    `);
  }
  
  // Re-engagement candidates
  async identifyReEngagementCandidates(): Promise<UUID[]> {
    const sixMonthsAgo = subtractMonths(new Date(), 6);
    const threeMonthsAgo = subtractMonths(new Date(), 3);
    
    return this.contactRepo.findByQuery(`
      SELECT c.id FROM contacts c
      WHERE c.last_activity_at BETWEEN $1 AND $2
        AND c.email_bounced = false
        AND c.consent_email = true
        AND NOT EXISTS (
          SELECT 1 FROM email_events e
          WHERE e.contact_id = c.id
            AND e.timestamp > $2
        )
    `, [sixMonthsAgo, threeMonthsAgo]);
  }
}
```

### 3.2 Dynamic Segmentation

Real-time segment updates khi contact behavior changes.

```typescript
class DynamicSegmentService {
  constructor(
    private segmentRepo: SegmentRepository,
    private contactRepo: ContactRepository,
    private eventBus: EventBus
  ) {}
  
  // Register event listeners for dynamic segments
  registerDynamicSegments(): void {
    this.eventBus.subscribe('order.completed', async (event) => {
      await this.updateOrderBasedSegments(event.contactId);
    });
    
    this.eventBus.subscribe('email.opened', async (event) => {
      await this.updateEngagementSegments(event.contactId);
    });
    
    this.eventBus.subscribe('lifecycle.changed', async (event) => {
      await this.updateLifecycleSegments(event.contactId);
    });
  }
  
  private async updateEngagementSegments(contactId: UUID): Promise<void> {
    const contact = await this.contactRepo.findById(contactId);
    
    // Remove from "inactive" segments
    await this.segmentService.removeFromSegments(
      contactId,
      ['inactive_90_days', 'dormant']
    );
    
    // Add to "active" segments
    if (contact.engagementScore >= 50) {
      await this.segmentService.addToSegments(contactId, ['highly_engaged']);
    }
    
    // Update recency segments
    await this.updateRecencySegments(contact);
  }
  
  // Segment membership query
  async getSegmentContacts(
    segmentId: UUID,
    pagination: Pagination
  ): Promise<PaginatedResult<Contact>> {
    const segment = await this.segmentRepo.findById(segmentId);
    
    if (!segment.isDynamic) {
      // Static segment - just query membership table
      return this.contactRepo.findBySegment(segmentId, pagination);
    }
    
    // Dynamic segment - evaluate criteria
    return this.evaluateDynamicSegment(segment, pagination);
  }
  
  private async evaluateDynamicSegment(
    segment: Segment,
    pagination: Pagination
  ): Promise<PaginatedResult<Contact>> {
    // Build SQL from segment criteria
    const { whereClause, params } = this.buildQueryFromCriteria(
      segment.criteria
    );
    
    const query = `
      SELECT c.* FROM contacts c
      WHERE ${whereClause}
      ORDER BY c.created_at DESC
      LIMIT $${params.length + 1} OFFSET $${params.length + 2}
    `;
    
    const countQuery = `
      SELECT COUNT(*) FROM contacts c
      WHERE ${whereClause}
    `;
    
    const [contacts, countResult] = await Promise.all([
      this.contactRepo.query(query, [...params, pagination.limit, pagination.offset]),
      this.contactRepo.query(countQuery, params)
    ]);
    
    return {
      items: contacts,
      total: parseInt(countResult.rows[0].count),
      page: pagination.page,
      limit: pagination.limit
    };
  }
}
```

## 4. Personalization Best Practices

### 4.1 AI-Powered Content Personalization

Use machine learning để generate và recommend personalized content.

```typescript
class AIPersonalizationService {
  constructor(
    private openai: OpenAIService,
    private contentRepo: ContentRepository,
    private analyticsService: AnalyticsService
  ) {}
  
  // Generate personalized email content
  async generatePersonalizedEmail(
    contact: Contact,
    campaign: Campaign,
    variantId: UUID
  ): Promise<GeneratedContent> {
    // Gather context
    const context = {
      contactProfile: this.formatContactProfile(contact),
      recentPurchases: await this.getRecentPurchases(contact.id),
      browsingHistory: await this.getBrowsingHistory(contact.id, 7),
      preferences: contact.preferences,
      company: await this.getCompanyContext()
    };
    
    // Generate content with AI
    const generation = await this.openai.generate({
      model: 'gpt-4',
      messages: [
        {
          role: 'system',
          content: `Bạn là chuyên gia marketing với 10 năm kinh nghiệm. 
Viết email marketing thuyết phục, personalized cho từng khách hàng.
Email phải:
- Có subject line hấp dẫn (dưới 50 ký tự)
- Nội dung phù hợp với profile của khách hàng
- Có clear CTA
- Tôn trọng văn hóa Việt Nam`
        },
        {
          role: 'user',
          content: `Tạo email cho chiến dịch "${campaign.name}".
Khách hàng: ${JSON.stringify(context)}
Variant: ${variantId}`
        }
      ],
      temperature: 0.7,
      max_tokens: 1000
    });
    
    const content = this.parseGeneratedContent(generation);
    
    // Validate content
    const validation = await this.validateGeneratedContent(content);
    if (!validation.valid) {
      throw new ContentValidationError(validation.errors);
    }
    
    return content;
  }
  
  // Product recommendation
  async recommendProducts(
    contactId: UUID,
    limit: number = 5
  ): Promise<ProductRecommendation[]> {
    const contact = await this.contactRepo.findById(contactId);
    const browsingHistory = await this.getBrowsingHistory(contactId, 30);
    const purchaseHistory = await this.getPurchaseHistory(contactId);
    
    // Get candidate products
    const candidates = await this.productService.getRecommendedProducts({
      excludeIds: purchaseHistory.map(p => p.productId),
      category: contact.interestCategories,
      priceRange: contact.typicalOrderValue
    });
    
    // Score and rank
    const scored = await Promise.all(
      candidates.map(async (product) => ({
        product,
        score: await this.calculateRecommendationScore(
          product,
          contact,
          browsingHistory,
          purchaseHistory
        )
      }))
    );
    
    return scored
      .sort((a, b) => b.score - a.score)
      .slice(0, limit);
  }
  
  private async calculateRecommendationScore(
    product: Product,
    contact: Contact,
    browsing: BrowseEvent[],
    purchasing: Purchase[]
  ): Promise<number> {
    let score = 0;
    
    // Collaborative filtering component
    const cfScore = await this.collaborativeFilter.score(contact.id, product.id);
    score += cfScore * 0.4;
    
    // Content-based component
    const cbScore = this.contentBased.score(product, contact);
    score += cbScore * 0.3;
    
    // Popularity component
    const popScore = this.popularity.getScore(product.id);
    score += popScore * 0.1;
    
    // Recency boost
    if (browsing.some(b => b.productId === product.id)) {
      score *= 1.2; // 20% boost for viewed products
    }
    
    // Category affinity
    if (contact.interestCategories.includes(product.category)) {
      score *= 1.1;
    }
    
    return score;
  }
}
```

### 4.2 Dynamic Content Blocks

Use content blocks có thể dynamically swap dựa trên contact data.

```typescript
// Content block configuration
interface ContentBlock {
  id: string;
  type: 'hero' | 'feature' | 'testimonial' | 'product_grid' | 'cta';
  variants: ContentVariant[];
  selectionStrategy: 'random' | 'ab_test' | 'personalized';
  displayConditions?: Condition[];
}

class DynamicContentService {
  async selectContentBlock(
    block: ContentBlock,
    contact: Contact,
    context: PersonalizationContext
  ): Promise<ContentVariant> {
    // Check display conditions
    if (block.displayConditions) {
      const meetsConditions = this.evaluateConditions(
        block.displayConditions,
        contact
      );
      if (!meetsConditions) {
        return { hidden: true };
      }
    }
    
    // Filter applicable variants
    const applicableVariants = block.variants.filter(v => 
      !v.conditions || this.evaluateConditions(v.conditions, contact)
    );
    
    if (applicableVariants.length === 0) {
      return block.variants[0]; // Fallback to first
    }
    
    // Select variant based on strategy
    switch (block.selectionStrategy) {
      case 'random':
        return this.selectRandom(applicableVariants);
      
      case 'ab_test':
        return this.selectByABTest(block.id, applicableVariants);
      
      case 'personalized':
        return this.selectPersonalized(applicableVariants, contact, context);
      
      default:
        return applicableVariants[0];
    }
  }
  
  // Hero banner with personalization
  async renderHeroBlock(
    contact: Contact,
    campaign: Campaign
  ): Promise<HeroBlock> {
    const variants = await this.getHeroVariants(campaign.id);
    
    // Select based on contact segment
    if (contact.lifecycleStage === 'new') {
      return variants.find(v => v.name === 'welcome') || variants[0];
    }
    
    if (contact.lifecycleStage === 'loyal') {
      return variants.find(v => v.name === 'loyalty_rewards') || variants[0];
    }
    
    // A/B test for others
    return this.selectByABTest('hero', variants);
  }
  
  // Product grid with personalized recommendations
  async renderProductGrid(
    contact: Contact,
    options: { rows: number; columns: number }
  ): Promise<ProductGridBlock> {
    const recommendations = await this.recommendProducts(
      contact.id,
      options.rows * options.columns
    );
    
    return {
      id: 'product_grid',
      products: recommendations.map(rec => ({
        product: rec.product,
        reason: this.getRecommendationReason(rec.product, contact)
      })),
      layout: {
        rows: options.rows,
        columns: options.columns
      }
    };
  }
}
```

## 5. Automation Best Practices

### 5.1 Journey Design Best Practices

Thiết kế customer journeys hiệu quả với clear goals và minimal friction.

```typescript
// Journey building best practices
class JourneyDesignGuide {
  // Welcome journey template
  static welcomeJourney(): JourneyDefinition {
    return {
      name: 'Welcome Journey',
      goal: 'Onboard new subscribers',
      
      nodes: [
        {
          id: 'start',
          type: 'trigger',
          config: { type: 'contact_created' }
        },
        {
          id: 'welcome_email',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'welcome-email',
            delay: { type: 'immediate' }
          }
        },
        {
          id: 'check_segment',
          type: 'condition',
          config: {
            rules: [{ field: 'source', operator: 'equals', value: 'ecommerce' }]
          }
        },
        {
          id: 'ecommerce_welcome',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'ecommerce-welcome',
            delay: { type: 'wait_duration', duration: 1, unit: 'days' }
          }
        },
        {
          id: 'ask_preferences',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'preference-center',
            delay: { type: 'wait_duration', duration: 3, unit: 'days' }
          }
        },
        {
          id: 'goal_complete',
          type: 'goal',
          config: { goalType: 'engagement' }
        }
      ],
      
      edges: [
        { from: 'start', to: 'welcome_email' },
        { from: 'welcome_email', to: 'check_segment' },
        { from: 'check_segment', to: 'ecommerce_welcome', condition: { path: 'source', equals: 'ecommerce' } },
        { from: 'check_segment', to: 'ask_preferences', condition: { path: 'source', notEquals: 'ecommerce' } },
        { from: 'ask_preferences', to: 'goal_complete' }
      ]
    };
  }
  
  // Abandoned cart journey
  static abandonedCartJourney(): JourneyDefinition {
    return {
      name: 'Abandoned Cart Recovery',
      goal: 'Recover abandoned carts',
      
      trigger: {
        type: 'event',
        config: {
          eventType: 'cart_abandoned',
          conditions: [
            { field: 'cart_value', operator: 'greater_than', value: 100000 }
          ]
        }
      },
      
      nodes: [
        {
          id: 'first_reminder',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'cart-reminder-1h',
            delay: { type: 'wait_duration', duration: 1, unit: 'hours' }
          }
        },
        {
          id: 'check_activity',
          type: 'condition',
          config: {
            rules: [
              { field: 'last_activity', operator: 'equals', value: 'email_opened' }
            ]
          }
        },
        {
          id: 'second_reminder',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'cart-reminder-24h',
            delay: { type: 'wait_duration', duration: 24, unit: 'hours' }
          }
        },
        {
          id: 'offer_incentive',
          type: 'condition',
          config: {
            rules: [
              { field: 'cart_value', operator: 'greater_than', value: 500000 }
            ]
          }
        },
        {
          id: 'discount_offer',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'cart-discount-offer',
            delay: { type: 'wait_duration', duration: 48, unit: 'hours' }
          }
        },
        {
          id: 'exit_goal',
          type: 'goal',
          config: { goalType: 'conversion' }
        }
      ],
      
      settings: {
        maxDuration: '7 days',
        exitOnPurchase: true,
        frequencyCap: { emails: 3, period: '7 days' }
      }
    };
  }
}
```

### 5.2 Automation Testing

Test automation workflows thoroughly trước khi activate.

```typescript
class AutomationTestingService {
  // Journey simulation testing
  async simulateJourney(
    journeyId: UUID,
    testContact: Contact
  ): Promise<JourneySimulationResult> {
    const journey = await this.journeyRepo.findById(journeyId);
    const simulation: SimulationStep[] = [];
    
    let currentNodeId = journey.entryTrigger;
    const executedNodes = new Set<string>();
    
    while (currentNodeId && simulation.length < 100) {
      if (executedNodes.has(currentNodeId)) {
        simulation.push({
          nodeId: currentNodeId,
          status: 'loop_detected',
          warning: 'Journey would loop infinitely'
        });
        break;
      }
      
      const node = journey.nodes.find(n => n.id === currentNodeId);
      if (!node) break;
      
      executedNodes.add(currentNodeId);
      
      try {
        const result = await this.simulateNode(node, testContact);
        
        simulation.push({
          nodeId: node.id,
          nodeType: node.type,
          status: 'success',
          output: result,
          duration: result.duration
        });
        
        currentNodeId = result.nextNodeId;
        
      } catch (error) {
        simulation.push({
          nodeId: node.id,
          nodeType: node.type,
          status: 'error',
          error: error.message
        });
        break;
      }
    }
    
    return {
      completed: simulation.every(s => s.status === 'success'),
      steps: simulation,
      totalDuration: this.calculateTotalDuration(simulation),
      potentialIssues: this.identifyIssues(simulation)
    };
  }
  
  // A/B test setup for journeys
  async setupJourneyABTest(
    journeyId: UUID,
    variants: ABTestVariant[]
  ): Promise<ABTest> {
    // Validate variants
    for (const variant of variants) {
      const simulation = await this.simulateJourney(
        variant.journeyId,
        this.createTestContact()
      );
      
      if (!simulation.completed) {
        throw new JourneyValidationError(
          `Variant ${variant.name} has errors: ${simulation.potentialIssues}`
        );
      }
    }
    
    const test = ABTest.create({
      journeyId,
      variants,
      allocation: variants.map(v => ({
        variantId: v.id,
        percentage: 100 / variants.length
      })),
      startDate: new Date(),
      minSampleSize: 1000,
      confidenceLevel: 0.95
    });
    
    await this.abTestRepo.save(test);
    return test;
  }
}
```

## 6. Analytics Best Practices

### 6.1 Campaign Measurement Framework

Implement comprehensive measurement framework để track campaign performance.

```typescript
interface CampaignMeasurementFramework {
  // Attribution model configuration
  attribution: {
    model: 'first_touch' | 'last_touch' | 'linear' | 'time_decay' | 'position_based';
    lookbackWindow: number; // days
    touchpointTypes: string[];
  };
  
  // Metrics to track
  metrics: MetricDefinition[];
  
  // Conversion events
  conversions: ConversionEvent[];
}

class CampaignAnalyticsService {
  // Calculate campaign ROI
  async calculateCampaignROI(campaignId: UUID): Promise<CROIMetrics> {
    const campaign = await this.campaignRepo.findById(campaignId);
    
    const [revenue, costs] = await Promise.all([
      this.attributionService.getAttributedRevenue(campaignId),
      this.getCampaignCosts(campaignId)
    ]);
    
    const grossProfit = revenue * campaign.avgMargin;
    const netProfit = grossProfit - costs.total;
    const roi = costs.total > 0 ? (netProfit / costs.total) * 100 : 0;
    
    return {
      revenue,
      costs: {
        media: costs.media,
        production: costs.production,
        platform: costs.platform,
        total: costs.total
      },
      grossProfit,
      netProfit,
      roi,
      paybackPeriod: this.calculatePaybackPeriod(revenue, costs.total)
    };
  }
  
  // Multi-touch attribution
  async calculateAttribution(
    contactId: UUID,
    conversionType: string
  ): Promise<AttributionResult> {
    const touchpoints = await this.getTouchpoints(contactId);
    const conversion = await this.getConversion(contactId, conversionType);
    
    if (!conversion) {
      return { attributed: false };
    }
    
    const model = await this.getAttributionModel(contactId);
    
    switch (model) {
      case 'first_touch':
        return {
          attributed: true,
          touchpoint: touchpoints[0],
          credit: 1
        };
      
      case 'last_touch':
        return {
          attributed: true,
          touchpoint: touchpoints[touchpoints.length - 1],
          credit: 1
        };
      
      case 'linear':
        return this.calculateLinearAttribution(touchpoints);
      
      case 'time_decay':
        return this.calculateTimeDecayAttribution(touchpoints, conversion.timestamp);
      
      case 'position_based':
        return this.calculatePositionBasedAttribution(touchpoints);
      
      default:
        return { attributed: false };
    }
  }
}
```

### 6.2 Real-Time Dashboard Metrics

Provide real-time visibility vào campaign performance.

```typescript
class RealTimeDashboardService {
  // Live campaign metrics
  async getLiveCampaignMetrics(
    campaignId: UUID
  ): Promise<LiveCampaignMetrics> {
    const cacheKey = `campaign:${campaignId}:live`;
    
    // Check cache first
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }
    
    // Calculate from event stream
    const [sent, delivered, opens, clicks, bounces, unsubscribes] = 
      await Promise.all([
        this.getEventCount(campaignId, 'email_sent'),
        this.getEventCount(campaignId, 'email_delivered'),
        this.getEventCount(campaignId, 'email_opened'),
        this.getEventCount(campaignId, 'email_clicked'),
        this.getEventCount(campaignId, 'email_bounced'),
        this.getEventCount(campaignId, 'email_unsubscribed')
      ]);
    
    const metrics: LiveCampaignMetrics = {
      sent,
      delivered,
      opens,
      clicks,
      bounces,
      unsubscribes,
      openRate: delivered > 0 ? (opens / delivered) * 100 : 0,
      clickRate: delivered > 0 ? (clicks / delivered) * 100 : 0,
      clickToOpenRate: opens > 0 ? (clicks / opens) * 100 : 0,
      bounceRate: sent > 0 ? (bounces / sent) * 100 : 0,
      unsubscribeRate: sent > 0 ? (unsubscribes / sent) * 100 : 0,
      updatedAt: new Date()
    };
    
    // Cache for 1 minute
    await this.redis.setex(cacheKey, 60, JSON.stringify(metrics));
    
    return metrics;
  }
  
  // Engagement velocity tracking
  async getEngagementVelocity(
    campaignId: UUID
  ): Promise<VelocityMetrics> {
    const events = await this.getEventsWithTimestamps(campaignId);
    
    // Group by minute
    const byMinute = this.groupByMinute(events);
    
    // Calculate velocity
    const now = new Date();
    const lastHour = byMinute.filter(m => 
      differenceInMinutes(now, m.timestamp) <= 60
    );
    
    const avgPerMinute = lastHour.reduce((sum, m) => sum + m.events, 0) / 60;
    const peakMinute = lastHour.reduce(
      (max, m) => m.events > max.events ? m : max,
      { timestamp: now, events: 0 }
    );
    
    // Predict completion time
    const remaining = await this.getRemainingDeliveries(campaignId);
    const predictedCompleteAt = new Date(
      now.getTime() + (remaining / avgPerMinute) * 60000
    );
    
    return {
      currentVelocity: avgPerMinute,
      peakVelocity: peakMinute.events,
      peakTime: peakMinute.timestamp,
      predictedCompleteAt,
      eventsByMinute: lastHour
    };
  }
}
```

## 7. Compliance Best Practices

### 7.1 GDPR & CCPA Compliance

Ensure all marketing activities comply với privacy regulations.

```typescript
class PrivacyComplianceService {
  // GDPR Right to be Forgotten
  async processDataDeletionRequest(
    requestId: UUID
  ): Promise<DeletionResult> {
    const request = await this.deletionRepo.findById(requestId);
    const contact = await this.contactRepo.findByEmail(request.email);
    
    if (!contact) {
      return { success: true, message: 'Contact not found' };
    }
    
    // 1. Anonymize PII
    await this.anonymizeContact(contact.id);
    
    // 2. Delete from all integrations
    await this.deleteFromExternalSystems(contact);
    
    // 3. Remove from all segments
    await this.segmentService.removeFromAllSegments(contact.id);
    
    // 4. Cancel all pending communications
    await this.cancelPendingCommunications(contact.id);
    
    // 5. Delete event history (optional based on legal basis)
    if (request.includeEvents) {
      await this.deleteContactEvents(contact.id);
    }
    
    // 6. Log deletion for audit
    await this.auditLog.record({
      action: 'data_deletion_completed',
      contactId: contact.id,
      requestId,
      timestamp: new Date()
    });
    
    // 7. Send confirmation
    await this.emailService.send({
      to: request.email,
      template: 'deletion-confirmation'
    });
    
    return { success: true };
  }
  
  // Consent management
  async recordConsent(record: ConsentRecord): Promise<void> {
    // Validate consent
    if (!this.isValidConsentRecord(record)) {
      throw new InvalidConsentError();
    }
    
    // Store consent
    await this.consentRepo.save(record);
    
    // Update contact preferences immediately
    await this.updateContactPreference(
      record.contactId,
      record.consentType,
      true
    );
    
    // Trigger any consent-triggered actions
    await this.onConsentGranted(record);
  }
  
  // Data portability (GDPR Right to Data Portability)
  async exportContactData(contactId: UUID): Promise<ExportPackage> {
    const contact = await this.contactRepo.findById(contactId);
    const events = await this.eventStore.getContactEvents(contactId);
    const segments = await this.segmentService.getContactSegments(contactId);
    
    return {
      exportedAt: new Date(),
      contact: this.sanitizeForExport(contact),
      events: events.map(e => this.sanitizeEventForExport(e)),
      segments: segments.map(s => s.name),
      preferences: await this.getContactPreferences(contactId)
    };
  }
}
```

### 7.2 Email Compliance

Follow email marketing regulations (CAN-SPAM, CASL, GDPR).

```typescript
class EmailComplianceService {
  async validateCampaignCompliance(
    campaign: Campaign
  ): Promise<ComplianceResult> {
    const violations: ComplianceViolation[] = [];
    
    // Check sender identification
    if (!campaign.sender.name || !campaign.sender.email) {
      violations.push({
        type: 'missing_sender_info',
        severity: 'error',
        message: 'Campaign must have sender name and email'
      });
    }
    
    // Check physical address (CAN-SPAM requirement)
    const companyInfo = await this.getCompanyInfo();
    if (!companyInfo.physicalAddress) {
      violations.push({
        type: 'missing_physical_address',
        severity: 'error',
        message: 'Email must include physical mailing address'
      });
    }
    
    // Check unsubscribe mechanism
    if (!campaign.includeUnsubscribeLink) {
      violations.push({
        type: 'missing_unsubscribe',
        severity: 'error',
        message: 'Email must include working unsubscribe link'
      });
    }
    
    // Check consent for purchased lists
    if (campaign.usePurchasedList) {
      violations.push({
        type: 'purchased_list',
        severity: 'warning',
        message: 'Using purchased lists may violate GDPR consent requirements'
      });
    }
    
    // Validate subject line
    const subjectIssues = this.validateSubjectLine(campaign.subject);
    violations.push(...subjectIssues);
    
    return {
      compliant: violations.filter(v => v.severity === 'error').length === 0,
      violations,
      warnings: violations.filter(v => v.severity === 'warning')
    };
  }
  
  // Honor unsubscribe requests immediately
  @Process('email.unsubscribe')
  async processUnsubscribe(email: string): Promise<void> {
    const contact = await this.contactRepo.findByEmail(email);
    
    if (contact) {
      await this.consentService.withdrawConsent(
        contact.id,
        'email_marketing',
        'unsubscribe_link'
      );
      
      // Cancel all pending emails
      await this.cancelPendingEmails(contact.id);
      
      // Add to suppression list
      await this.suppressionList.add(email);
      
      logger.info('Unsubscribe processed', { email, contactId: contact.id });
    }
  }
}
```

## 8. Testing Best Practices

### 8.1 A/B Testing Framework

Implement systematic A/B testing cho continuous optimization.

```typescript
class ABTestService {
  // Create experiment
  async createExperiment(config: ExperimentConfig): Promise<Experiment> {
    // Validate
    if (config.variants.length < 2) {
      throw new ValidationError('Experiment must have at least 2 variants');
    }
    
    // Ensure variant percentages sum to 100
    const totalPercentage = config.variants.reduce(
      (sum, v) => sum + v.allocation, 0
    );
    if (totalPercentage !== 100) {
      throw new ValidationError('Variant allocations must sum to 100%');
    }
    
    // Check minimum sample size is achievable
    const estimatedReach = await this.estimateReach(config);
    if (estimatedReach < config.minSampleSize) {
      throw new ValidationError(
        `Estimated reach (${estimatedReach}) is below minimum sample size`
      );
    }
    
    const experiment = Experiment.create({
      ...config,
      status: 'draft',
      createdAt: new Date()
    });
    
    await this.experimentRepo.save(experiment);
    return experiment;
  }
  
  // Assign variant to contact
  async getVariant(
    experimentId: UUID,
    contactId: UUID
  ): Promise<Variant> {
    // Check for existing assignment (consistency)
    const existing = await this.getAssignment(contactId, experimentId);
    if (existing) {
      return existing;
    }
    
    // Get experiment
    const experiment = await this.experimentRepo.findById(experimentId);
    
    // Deterministic assignment based on contact ID hash
    const hash = this.hashString(contactId + experimentId);
    const percentile = hash % 100;
    
    let cumulative = 0;
    for (const variant of experiment.variants) {
      cumulative += variant.allocation;
      if (percentile < cumulative) {
        await this.saveAssignment(contactId, experimentId, variant.id);
        return variant;
      }
    }
    
    return experiment.variants[0];
  }
  
  // Calculate statistical significance
  async calculateSignificance(
    experimentId: UUID
  ): Promise<SignificanceResult> {
    const experiment = await this.experimentRepo.findById(experimentId);
    
    const variantResults = await Promise.all(
      experiment.variants.map(async (variant) => {
        const [control, variant_] = await Promise.all([
          this.getVariantMetrics(experiment.controlVariantId),
          this.getVariantMetrics(variant.id)
        ]);
        
        const { significant, pValue, confidenceInterval } = 
          this.calculateZTest(control, variant_);
        
        return {
          variantId: variant.id,
          variantName: variant.name,
          metrics: variant_,
          controlMetrics: control,
          lift: this.calculateLift(control, variant_),
          pValue,
          confidenceInterval,
          significant
        };
      })
    );
    
    return {
      experimentId,
      results: variantResults,
      recommendedVariant: this.selectWinner(variantResults),
      recommendationConfidence: this.calculateConfidence(variantResults)
    };
  }
}
```

### 8.2 Pre-deployment Testing

Comprehensive testing trước khi activate marketing campaigns.

```typescript
class CampaignPreDeploymentService {
  // Run all pre-deployment checks
  async runPreDeploymentChecks(
    campaignId: UUID
  ): Promise<DeploymentChecklist> {
    const checks: ChecklistItem[] = [];
    
    // 1. Technical checks
    checks.push(await this.checkEmailRendering(campaignId));
    checks.push(await this.checkLinkValidity(campaignId));
    checks.push(await this.checkSpamScore(campaignId));
    checks.push(await this.checkListQuality(campaignId));
    
    // 2. Compliance checks
    checks.push(await this.checkConsentCompliance(campaignId));
    checks.push(await this.checkSenderAuth(campaignId));
    checks.push(await this.checkUnsubscribeLink(campaignId));
    
    // 3. Content checks
    checks.push(await this.checkPersonalizationTokens(campaignId));
    checks.push(await this.checkImageAltText(campaignId));
    checks.push(await this.checkSubjectLineLength(campaignId));
    
    // 4. Targeting checks
    checks.push(await this.checkAudienceSize(campaignId));
    checks.push(await this.checkSuppressionList(campaignId));
    checks.push(await this.checkFrequencyCapping(campaignId));
    
    return {
      passed: checks.filter(c => c.status === 'pass').length,
      failed: checks.filter(c => c.status === 'fail').length,
      warnings: checks.filter(c => c.status === 'warn').length,
      items: checks,
      readyToDeploy: checks.every(c => c.status !== 'fail')
    };
  }
  
  // Visual email preview across clients
  async generateEmailPreviews(
    campaignId: UUID
  ): Promise<EmailPreview[]> {
    const emailHtml = await this.getRenderedEmail(campaignId);
    
    const clients = [
      { name: 'Gmail Desktop', viewport: '1440x900' },
      { name: 'Gmail Mobile', viewport: '375x667' },
      { name: 'Outlook 2016', viewport: '1280x720' },
      { name: 'Apple Mail', viewport: '1280x800' }
    ];
    
    const previews = await Promise.all(
      clients.map(async (client) => {
        const screenshot = await this.renderer.render(emailHtml, {
          viewport: client.viewport,
          client: client.name
        });
        
        const issues = await this.checkRenderingIssues(screenshot);
        
        return {
          client: client.name,
          viewport: client.viewport,
          screenshot,
          issues
        };
      })
    );
    
    return previews;
  }
  
  // Test send to seed list
  async sendToSeedList(
    campaignId: UUID
  ): Promise<SeedListResult> {
    const seedContacts = await this.getSeedList();
    
    const results = await Promise.all(
      seedContacts.map(async (seed) => {
        try {
          await this.sendTestEmail(campaignId, seed);
          return { email: seed.email, status: 'sent' };
        } catch (error) {
          return { email: seed.email, status: 'failed', error: error.message };
        }
      })
    );
    
    return {
      total: results.length,
      sent: results.filter(r => r.status === 'sent').length,
      failed: results.filter(r => r.status === 'failed').length,
      details: results
    };
  }
}
```
