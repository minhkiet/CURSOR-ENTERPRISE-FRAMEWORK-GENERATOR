# Marketing FAQ - Câu Hỏi Thường Gặp

## 1. Email Marketing Questions

### Q1: Tại sao emails của tôi bị đánh dấu là spam?

**Trả lời:**

Có nhiều nguyên nhân khiến email bị đánh dấu spam:

**1. Authentication Issues (Nguyên nhân phổ biến nhất)**

Email không được authenticate đúng cách khiến ISPs nghi ngờ về nguồn gốc.

```typescript
// Kiểm tra authentication records
interface EmailAuthentication {
  spf: {
    passed: boolean;
    records: string[];
  };
  dkim: {
    passed: boolean;
    selector: string;
    domain: string;
  };
  dmarc: {
    policy: 'none' | 'quarantine' | 'reject';
    alignment: 'pass' | 'fail';
  };
}

// Troubleshooting steps
async function diagnoseDeliverability(email: string): Promise<DeliverabilityReport> {
  return {
    // Check if emails are authenticated
    authentication: {
      spf: await checkSPFRecord(email),
      dkim: await checkDKIMRecord(email),
      dmarc: await checkDMARCRecord(email)
    },
    
    // Check sender reputation
    reputation: await checkSenderScore(email),
    
    // Check content for spam triggers
    contentScore: await analyzeContentForSpam(email),
    
    // Check list quality
    listQuality: await assessListQuality(email)
  };
}
```

**2. Content Issues**

- Subject lines chứa spam trigger words ("FREE", "Act Now", "Limited Time")
- Quá nhiều exclamation marks hoặc ALL CAPS
- Email quá ngắn hoặc chỉ có hình ảnh
- Missing unsubscribe link hoặc physical address

```typescript
// Content spam check
const spamTriggers = [
  'FREE', 'Act now', 'Limited time', 'Congratulations',
  'Click here', 'Winner', 'Guarantee', 'No obligation',
  'Risk free', 'Special promotion', 'Discount'
];

function checkContentForSpam(email: EmailContent): SpamAnalysis {
  const issues: string[] = [];
  let score = 0;
  
  // Check subject
  for (const trigger of spamTriggers) {
    if (email.subject.toUpperCase().includes(trigger)) {
      issues.push(`Spam trigger in subject: ${trigger}`);
      score += 10;
    }
  }
  
  // Check for excessive caps
  const capsRatio = (email.subject.match(/[A-Z]/g) || []).length / email.subject.length;
  if (capsRatio > 0.3) {
    issues.push('Excessive capital letters');
    score += 15;
  }
  
  // Check image-to-text ratio
  const hasImage = email.hasImages;
  const hasText = email.textContent.length > 100;
  if (hasImage && !hasText) {
    issues.push('Image-only email (high spam risk)');
    score += 25;
  }
  
  return { score, issues, isSpamRisk: score > 50 };
}
```

**3. List Quality Issues**

- Bounce rate cao (>2%)
- Purchased lists hoặc rented lists
- Chứa spam traps
- Contacts không engaged trong thời gian dài

```typescript
// List quality assessment
async function assessListQuality(listId: string): Promise<ListQualityReport> {
  const stats = await getListStats(listId);
  
  return {
    totalContacts: stats.total,
    validEmails: stats.valid,
    bounced: stats.bounced,
    unsubscribed: stats.unsubscribed,
    spamComplaints: stats.complaints,
    
    bounceRate: stats.bounced / stats.total,
    complaintRate: stats.complaints / stats.total,
    
    engagementRate: stats.activeLast90Days / stats.total,
    spamTrapRisk: await checkForSpamTraps(listId),
    
    recommendation: generateListHealthRecommendation(stats)
  };
}
```

**Giải pháp:**

1. Authenticate emails properly (SPF, DKIM, DMARC)
2. Warm up new sending IPs gradually
3. Clean your list regularly (remove bounces)
4. Improve content quality
5. Increase engagement before sending
6. Use List-Unsubscribe headers
7. Monitor spam complaint rates

### Q2: Làm thế nào để tăng open rate?

**Trả lời:**

Open rate phụ thuộc vào nhiều yếu tố, quan trọng nhất là **subject line** và **send time**.

**1. Subject Line Optimization**

```typescript
// Subject line testing framework
class SubjectLineOptimizer {
  // Test different approaches
  async generateVariants(baseSubject: string): Promise<SubjectVariant[]> {
    return [
      // Personalization
      {
        name: 'with_name',
        subject: `{{firstName}}, ${baseSubject}`
      },
      
      // Urgency
      {
        name: 'urgency',
        subject: `⚠️ ${baseSubject} - Hết hạn sớm!`
      },
      
      // Question
      {
        name: 'question',
        subject: `${baseSubject}? Đây là câu trả lời`
      },
      
      // Numbers
      {
        name: 'numbered',
        subject: `3 lý do ${baseSubject.toLowerCase()}`
      },
      
      // Curiosity
      {
        name: 'curiosity',
        subject: `Điều {{firstName}} cần biết về ${baseSubject}`
      }
    ];
  }
  
  // AI-powered subject generation
  async generateWithAI(
    content: EmailContent,
    contact: Contact
  ): Promise<string> {
    const prompt = `
      Viết 5 subject lines cho email sau:
      - Người nhận: ${contact.firstName}
      - Segment: ${contact.segment}
      - Nội dung: ${content.preview}
      
      Yêu cầu:
      - Dưới 50 ký tự
      - Hấp dẫn, tạo tò mò
      - Không có spam trigger words
      - Có personalization
    `;
    
    return this.ai.generate(prompt);
  }
}
```

**2. Send Time Optimization**

```typescript
// Find optimal send time per contact
class SendTimeOptimizer {
  async findOptimalTime(contactId: string): Promise<SendTime> {
    // Get engagement history
    const engagement = await this.getEngagementByHour(contactId);
    
    if (engagement.length < 20) {
      // Not enough data, use segment defaults
      return this.getSegmentDefault(contactId);
    }
    
    // Analyze which hours have best engagement
    const hourlyPerformance = this.calculateHourlyPerformance(engagement);
    
    // Find best hour
    const bestHour = hourlyPerformance
      .sort((a, b) => b.engagementScore - a.engagementScore)[0];
    
    // Apply timezone adjustment
    const contact = await this.getContact(contactId);
    const adjustedHour = this.adjustForTimezone(
      bestHour.hour,
      contact.timezone
    );
    
    return {
      hour: adjustedHour,
      confidence: bestHour.sampleSize >= 50 ? 'high' : 'medium',
      basedOnData: bestHour.sampleSize
    };
  }
  
  // Batch optimization for campaigns
  async optimizeCampaignSend(
    contacts: Contact[]
  ): Promise<Map<string, SendTime>> {
    // Group by optimal time windows
    const grouped = this.groupByTimeWindow(contacts);
    
    const results = new Map<string, SendTime>();
    
    for (const group of grouped) {
      // Stagger sends to avoid spikes
      const baseTime = group.optimalHour;
      
      for (let i = 0; i < group.contacts.length; i++) {
        const contact = group.contacts[i];
        results.set(contact.id, {
          hour: (baseTime + (i % 3)) % 24, // Stagger within 3-hour window
          minute: Math.floor(Math.random() * 60)
        });
      }
    }
    
    return results;
  }
}
```

**3. Other Factors**

- **Preview text**: Viết preview text hấp dẫn (40-130 ký tự)
- **From name**: Sử dụng recognizable from name
- **List hygiene**: Gửi cho engaged contacts
- **Relevance**: Nội dung phù hợp với segment

### Q3: Phân biệt giữa soft bounce và hard bounce?

**Trả lời:**

| Loại | Ý nghĩa | Xử lý |
|------|---------|--------|
| **Soft Bounce** | Email tạm thời không gửi được (hộp thư đầy, server bận) | Retry, giữ contact trong danh sách |
| **Hard Bounce** | Email vĩnh viễn không gửi được (địa chỉ không tồn tại) | Ngay lập tức xóa khỏi danh sách |

```typescript
// Bounce handling strategy
class BounceHandler {
  async handleBounce(bounce: BounceEvent): Promise<void> {
    const contact = await this.contactRepo.findByEmail(bounce.email);
    
    if (bounce.type === 'hard') {
      // Immediately suppress
      await this.suppressionList.add(bounce.email, {
        reason: 'hard_bounce',
        bouncedAt: bounce.timestamp,
        bounceCode: bounce.code
      });
      
      // Mark contact
      await this.contactRepo.markAsBounced(contact.id, {
        type: 'hard',
        bouncedAt: bounce.timestamp,
        bounceCode: bounce.code
      });
      
      // Log for compliance
      await this.auditLog.record({
        action: 'hard_bounce',
        email: bounce.email,
        bouncedAt: bounce.timestamp
      });
      
    } else if (bounce.type === 'soft') {
      // Increment soft bounce counter
      const currentBounces = await this.getSoftBounceCount(contact.id);
      
      if (currentBounces >= 3) {
        // Too many soft bounces = treat as hard
        await this.convertToHardBounce(contact.id);
      } else {
        // Schedule retry
        await this.scheduleRetry(contact.id, {
          delay: '1 hour',
          attemptNumber: currentBounces + 1
        });
        
        await this.contactRepo.incrementSoftBounces(contact.id);
      }
    }
  }
}

// SMTP bounce codes reference
const BOUNCE_CODES = {
  // Hard bounce codes
  '550': 'Mailbox does not exist',
  '551': 'User not local',
  '553': 'Mailbox name not allowed',
  '554': 'Transaction failed',
  
  // Soft bounce codes
  '421': 'Service not available, try again later',
  '450': 'Mailbox unavailable (busy)',
  '452': 'System storage full',
  '552': 'Mailbox full'
};
```

## 2. Automation & Journey Questions

### Q4: Khi nào nên sử dụng automation thay vì one-time campaign?

**Trả lời:**

| Scenario | Recommendation |
|----------|----------------|
| Welcome new subscribers | **Automation** - consistent, scalable |
| Cart abandonment | **Automation** - immediate, triggers |
| Birthday wishes | **Automation** - timely, personalized |
| Product launch announcement | **One-time Campaign** - special event |
| Flash sale (24 hours) | **One-time Campaign** - time-sensitive |
| Re-engagement | **Automation** - follow-up sequence |
| New blog post notification | **Automation** - recurring |
| Event invitation | Can be either, depends on scale |
| Win-back for churned | **Automation** - multi-touch sequence |
| Survey request | **Automation** - trigger-based |

```typescript
// Decision framework for automation vs campaign
class MarketingStrategySelector {
  async selectApproach(
    objective: MarketingObjective,
    context: MarketingContext
  ): Promise<StrategyRecommendation> {
    const factors = {
      isRecurring: objective.type === 'recurring' || objective.type === 'trigger',
      requiresTimeliness: objective.timeSensitivity === 'high',
      needsPersonalization: objective.personalizationLevel === 'high',
      hasClearTrigger: !!objective.triggerEvent,
      volume: context.audienceSize,
      frequency: context.frequency
    };
    
    // Automation recommended when:
    if (
      factors.isRecurring &&
      factors.requiresTimeliness &&
      factors.needsPersonalization
    ) {
      return {
        recommendation: 'automation',
        reason: 'Recurring, timely, personalized - perfect for automation',
        examples: ['welcome_series', 'cart_abandonment', 'birthday']
      };
    }
    
    // Campaign recommended when:
    if (
      !factors.hasClearTrigger &&
      factors.frequency === 'low' &&
      context.audienceSize > 10000
    ) {
      return {
        recommendation: 'campaign',
        reason: 'One-time event with large audience',
        examples: ['product_launch', 'seasonal_sale']
      };
    }
    
    // Hybrid approach for complex scenarios
    return {
      recommendation: 'hybrid',
      automation: 'trigger_initial_outreach',
      campaign: 'follow_up_broadcast'
    };
  }
}
```

### Q5: Làm thế nào để prevent automation overload?

**Trả lời:**

Automation overload xảy ra khi contacts nhận quá nhiều messages từ multiple journeys cùng lúc.

```typescript
// Communication queue with deduplication
class CommunicationQueueManager {
  private queue: Map<string, Communication[]> = new Map();
  
  async enqueue(communication: Communication): Promise<QueueResult> {
    const contactId = communication.contactId;
    
    // Get existing queued communications
    const existing = this.queue.get(contactId) || [];
    
    // Check for conflicts
    const conflicts = this.findConflicts(communication, existing);
    
    if (conflicts.length > 0) {
      // Resolve conflict
      const resolution = this.resolveConflict(communication, conflicts);
      
      if (resolution.action === 'skip') {
        return {
          action: 'skipped',
          reason: resolution.reason,
          skippedFor: conflicts[0].id
        };
      }
      
      if (resolution.action === 'merge') {
        // Merge similar communications
        communication = this.mergeCommunications(
          communication,
          conflicts[0]
        );
      }
    }
    
    // Add to queue
    existing.push(communication);
    this.queue.set(contactId, existing);
    
    // Schedule based on priority
    const scheduledTime = this.calculateScheduledTime(
      communication,
      existing
    );
    
    return {
      action: 'queued',
      scheduledFor: scheduledTime,
      position: existing.length
    };
  }
  
  private findConflicts(
    newComm: Communication,
    existing: Communication[]
  ): Communication[] {
    return existing.filter(e => 
      // Same campaign recently
      (e.campaignId === newComm.campaignId &&
       this.hoursSince(e.scheduledFor) < 24) ||
      
      // Too many communications today
      (this.hoursSince(e.scheduledFor) < 24 &&
       existing.filter(ex => 
         this.hoursSince(ex.scheduledFor) < 24
       ).length >= 2) ||
      
      // Duplicate content
      (this.contentSimilarity(e.content, newComm.content) > 0.8)
    );
  }
}

// Journey coordination across campaigns
class JourneyCoordinator {
  // Set up cross-journey communication rules
  private readonly RULES = {
    maxDailyEmails: 2,
    maxWeeklyEmails: 5,
    minHoursBetweenEmails: 4,
    priorityChannels: ['transactional', 'critical', 'marketing']
  };
  
  async checkCommunicationAllowed(
    contactId: string,
    communication: Communication
  ): Promise<boolean> {
    const recentComms = await this.getRecentCommunications(contactId, {
      since: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    });
    
    // Check daily limit
    const todayComms = recentComms.filter(
      c => this.isSameDay(c.sentAt, new Date())
    );
    if (todayComms.length >= this.RULES.maxDailyEmails) {
      return false;
    }
    
    // Check priority
    const hasHigherPriority = todayComms.some(
      c => this.getPriority(c) > this.getPriority(communication)
    );
    if (hasHigherPriority) {
      return false;
    }
    
    return true;
  }
}
```

### Q6: Best practices cho welcome series?

**Trả lời:**

Welcome series là cơ hội quan trọng để set expectations và build relationship.

```typescript
// Welcome series best practices
const WELCOME_SERIES_CONFIG = {
  // Total duration: ~7-14 days
  duration: '10 days',
  
  // Optimal number of emails: 3-5
  emailCount: 4,
  
  // Email cadence
  cadence: [
    { email: 1, delay: 'immediate', subject: 'Welcome + Expectation setting' },
    { email: 2, delay: '1 day', subject: 'Value introduction' },
    { email: 3, delay: '3 days', subject: 'Social proof / Case study' },
    { email: 4, delay: '7 days', subject: 'Soft ask + Preference center' }
  ],
  
  // Content strategy
  content: {
    email1: {
      type: 'welcome',
      goals: ['Confirm subscription', 'Set expectations', 'Deliver first value'],
      cta: 'Explore products'
    },
    email2: {
      type: 'value',
      goals: ['Showcase best content', 'Build trust'],
      cta: 'Read more'
    },
    email3: {
      type: 'social_proof',
      goals: ['Build credibility', 'Show success stories'],
      cta: 'See reviews'
    },
    email4: {
      type: 'preference_center',
      goals: ['Gather preferences', 'Reduce unsubscribes'],
      cta: 'Update preferences'
    }
  }
};

// Implementation
class WelcomeSeriesBuilder {
  build(): JourneyDefinition {
    return {
      name: 'Welcome Series',
      entryTrigger: { type: 'contact_created' },
      
      nodes: [
        {
          id: 'email_1',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'welcome-email-1',
            delay: { type: 'immediate' }
          }
        },
        {
          id: 'check_opens',
          type: 'condition',
          config: {
            rules: [{ field: 'lastEmailOpened', hoursAgo: 24 }]
          }
        },
        {
          id: 'email_2',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'welcome-email-2',
            delay: { type: 'wait_duration', duration: 24 }
          }
        },
        {
          id: 'email_3',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'welcome-email-3',
            delay: { type: 'wait_duration', duration: 72 }
          }
        },
        {
          id: 'email_4',
          type: 'action',
          config: {
            actionType: 'send_email',
            templateId: 'welcome-email-4',
            delay: { type: 'wait_duration', duration: 168 }
          }
        },
        {
          id: 'add_to_segments',
          type: 'action',
          config: {
            actionType: 'add_to_segment',
            segments: ['welcome_complete', 'active_subscriber']
          }
        }
      ],
      
      edges: [
        { from: 'email_1', to: 'check_opens' },
        { from: 'check_opens', to: 'email_2', condition: { field: 'opened', equals: true } },
        { from: 'check_opens', to: 'email_2', condition: { field: 'opened', equals: false } },
        { from: 'email_2', to: 'email_3' },
        { from: 'email_3', to: 'email_4' },
        { from: 'email_4', to: 'add_to_segments' }
      ],
      
      settings: {
        exitOnUnsubscribe: true,
        exitOnBounce: true,
        maxDuration: '14 days'
      }
    };
  }
}
```

## 3. Analytics Questions

### Q7: Cách tính ROI cho marketing campaigns?

**Trả lời:**

```typescript
// Marketing ROI calculation
interface MROI {
  revenue: Money;
  costs: CampaignCosts;
  grossProfit: Money;
  netProfit: Money;
  roi: number; // percentage
  cac: Money; // Customer Acquisition Cost
  ltvToCACRatio: number;
  paybackPeriod: number; // days
}

class MarketingROICalculator {
  async calculate(campaignId: string): Promise<MROI> {
    const campaign = await this.campaignRepo.findById(campaignId);
    
    // Revenue attribution
    const attributedRevenue = await this.attributionService.getAttributedRevenue({
      campaignId,
      attributionModel: campaign.attributionModel,
      lookbackWindow: campaign.lookbackDays
    });
    
    // Get new customers acquired
    const newCustomers = await this.customerService.getNewCustomersFromCampaign(
      campaignId
    );
    
    // Calculate costs
    const costs = await this.calculateCampaignCosts(campaign);
    
    // Metrics
    const grossProfit = attributedRevenue.multiply(campaign.avgMargin);
    const netProfit = grossProfit.subtract(costs.total);
    const roi = costs.total > 0 
      ? netProfit.divide(costs.total).multiply(100) 
      : 0;
    
    const cac = newCustomers > 0 
      ? costs.total.divide(newCustomers) 
      : 0;
    
    const avgLTV = await this.calculateAverageLTV(newCustomers);
    const ltvToCACRatio = avgLTV > 0 ? avgLTV.divide(cac) : 0;
    
    // Payback period (months to recover acquisition cost)
    const monthlyRevenuePerCustomer = await this.getMonthlyRevenuePerCustomer(
      newCustomers
    );
    const paybackPeriod = monthlyRevenuePerCustomer > 0
      ? cac.divide(monthlyRevenuePerCustomer)
      : 0;
    
    return {
      revenue: attributedRevenue,
      costs,
      grossProfit,
      netProfit,
      roi,
      cac,
      ltvToCACRatio,
      paybackPeriod
    };
  }
  
  // Attribution models
  async getAttributedRevenue(params: {
    campaignId: string;
    attributionModel: 'first_touch' | 'last_touch' | 'linear' | 'time_decay' | 'position_based';
    lookbackWindow: number;
  }): Promise<Money> {
    const conversions = await this.getConversions(params.campaignId);
    
    switch (params.attributionModel) {
      case 'first_touch':
        return this.calculateFirstTouchAttribution(conversions);
        
      case 'last_touch':
        return this.calculateLastTouchAttribution(conversions);
        
      case 'linear':
        return this.calculateLinearAttribution(conversions);
        
      case 'time_decay':
        return this.calculateTimeDecayAttribution(conversions);
        
      case 'position_based':
        return this.calculatePositionBasedAttribution(conversions);
        
      default:
        return this.calculateLastTouchAttribution(conversions);
    }
  }
}
```

### Q8: Metrics nào quan trọng nhất để track?

**Trả lời:**

```typescript
// Marketing metrics hierarchy
interface MarketingMetrics {
  // Revenue metrics (most important)
  revenue: {
    totalRevenue: Money;
    attributedRevenue: Money;
    averageOrderValue: Money;
    revenuePerSubscriber: Money;
  };
  
  // Customer metrics
  customers: {
    newCustomers: number;
    customerAcquisitionCost: Money;
    customerLifetimeValue: Money;
    ltvToCACRatio: number;
    retentionRate: number;
    churnRate: number;
  };
  
  // Engagement metrics
  engagement: {
    emailOpenRate: number;
    emailClickRate: number;
    clickToOpenRatio: number;
    websiteEngagementRate: number;
    contentEngagementScore: number;
  };
  
  // Efficiency metrics
  efficiency: {
    costPerAcquisition: Money;
    costPerThousandReached: Money;
    conversionRate: number;
    paybackPeriod: number;
    marketingROI: number;
  };
  
  // Health metrics
  health: {
    listGrowthRate: number;
    unsubscribeRate: number;
    bounceRate: number;
    complaintRate: number;
    spamTrapHits: number;
  };
}

// Recommended metrics by campaign type
const CAMPAIGN_METRICS = {
  acquisition: [
    'cost_per_acquisition',
    'conversion_rate',
    'new_customers',
    'ltv_to_cac_ratio'
  ],
  
  engagement: [
    'open_rate',
    'click_rate',
    'engagement_rate',
    'content_consumption'
  ],
  
  retention: [
    'retention_rate',
    'churn_rate',
    'reactivation_rate',
    'nps_score'
  ],
  
  revenue: [
    'revenue',
    'average_order_value',
    'repeat_purchase_rate',
    'roi'
  ]
};
```

## 4. Compliance Questions

### Q9: Làm thế nào để tuân thủ GDPR?

**Trả lời:**

GDPR áp dụng cho tất cả contacts ở EU, bất kể công ty của bạn ở đâu.

```typescript
// GDPR compliance checklist
class GDPRComplianceService {
  // 1. Legal Basis for Processing
  async establishLegalBasis(
    contactId: string,
    purpose: string,
    legalBasis: 'consent' | 'contract' | 'legitimate_interest' | 'legal_obligation'
  ): Promise<void> {
    const record = {
      contactId,
      purpose,
      legalBasis,
      establishedAt: new Date(),
      evidence: await this.gatherConsentEvidence(contactId)
    };
    
    await this.legalBasisRepo.save(record);
  }
  
  // 2. Right to Access
  async handleDataAccessRequest(requestId: string): Promise<DataExport> {
    const request = await this.accessRequestRepo.findById(requestId);
    const contact = await this.contactRepo.findByEmail(request.email);
    
    // Gather all personal data
    const exportData = {
      profile: contact,
      events: await this.getAllContactEvents(contact.id),
      preferences: await this.getContactPreferences(contact.id),
      consentRecords: await this.getConsentRecords(contact.id),
      communications: await this.getContactCommunications(contact.id)
    };
    
    // Return in portable format
    return {
      exportedAt: new Date(),
      data: exportData,
      format: 'json'
    };
  }
  
  // 3. Right to Erasure
  async handleDeletionRequest(requestId: string): Promise<DeletionResult> {
    const request = await this.deletionRequestRepo.findById(requestId);
    const contact = await this.contactRepo.findByEmail(request.email);
    
    // Check for legal obligations to retain
    const retentionObligations = await this.checkRetentionObligations(
      contact.id,
      ['legal', 'financial']
    );
    
    if (retentionObligations.length > 0) {
      // Partial deletion - remove marketing data only
      await this.removeMarketingData(contact.id);
      await this.anonymizePII(contact.id);
    } else {
      // Full deletion
      await this.deleteAllContactData(contact.id);
    }
    
    // Log the deletion
    await this.auditLog.record({
      action: 'data_deletion',
      requestId,
      contactId: contact.id,
      scope: retentionObligations.length > 0 ? 'partial' : 'full'
    });
    
    return { completedAt: new Date(), scope: 'full' };
  }
  
  // 4. Consent Management
  async recordConsent(record: ConsentRecord): Promise<void> {
    // Must be explicit and informed
    if (!record.evidence?.ipAddress || !record.evidence?.userAgent) {
      throw new ConsentValidationError('Missing consent evidence');
    }
    
    await this.consentRepo.save(record);
    
    // Immediately update preferences
    await this.updateContactPreference(
      record.contactId,
      record.consentType,
      true
    );
  }
  
  async withdrawConsent(contactId: string, consentType: ConsentType): Promise<void> {
    await this.consentRepo.recordWithdrawal({
      contactId,
      consentType,
      withdrawnAt: new Date()
    });
    
    // Immediately stop all related communications
    await this.cancelPendingComms(contactId, consentType);
    
    // Add to suppression list
    await this.suppressionList.add(contactId, {
      reason: `consent_withdrawn_${consentType}`
    });
  }
  
  // 5. Data Portability
  async exportContactData(contactId: string): Promise<PortableData> {
    const contact = await this.contactRepo.findById(contactId);
    
    return {
      exportedAt: new Date(),
      data: {
        personalInformation: contact,
        preferences: await this.getPreferences(contactId),
        activityHistory: await this.getActivityHistory(contactId)
      },
      format: 'json',
      schema: 'gdpr_portable_format_v1'
    };
  }
}
```

### Q10: Làm thế nào để handle data subject requests?

**Trả lời:**

GDPR yêu cầu response trong 30 ngày. Implement systematic process.

```typescript
// Data Subject Request Management
class DSRManagementService {
  async createRequest(
    request: DSRRequest
  ): Promise<DSRRequest> {
    // Validate request
    if (!request.email || !request.type) {
      throw new ValidationError('Email and request type required');
    }
    
    // Create request record
    const dsrRequest = DSRRequest.create({
      ...request,
      status: 'pending',
      receivedAt: new Date(),
      deadline: addDays(new Date(), 30)
    });
    
    await this.dsrRepo.save(dsrRequest);
    
    // Verify identity (GDPR requirement)
    await this.verifyIdentity(dsrRequest);
    
    // Route to appropriate handler
    await this.routeRequest(dsrRequest);
    
    return dsrRequest;
  }
  
  // Request types and handlers
  async routeRequest(request: DSRRequest): Promise<void> {
    switch (request.type) {
      case 'access':
        await this.handleAccessRequest(request);
        break;
        
      case 'rectification':
        await this.handleRectificationRequest(request);
        break;
        
      case 'erasure':
        await this.handleErasureRequest(request);
        break;
        
      case 'portability':
        await this.handlePortabilityRequest(request);
        break;
        
      case 'object':
        await this.handleObjectionRequest(request);
        break;
        
      case 'restrict':
        await this.handleRestrictionRequest(request);
        break;
    }
  }
  
  // Track compliance
  async checkComplianceStatus(): Promise<ComplianceReport> {
    const pendingRequests = await this.dsrRepo.findPending();
    const overdueRequests = pendingRequests.filter(
      r => r.deadline < new Date()
    );
    
    return {
      totalRequests: await this.dsrRepo.count(),
      pendingRequests: pendingRequests.length,
      overdueRequests: overdueRequests.length,
      averageProcessingTime: await this.calculateAvgProcessingTime(),
      complianceRate: await this.calculateComplianceRate()
    };
  }
}
```

## 5. Personalization Questions

### Q11: Level nào của personalization là quá nhiều?

**Trả lời:**

Personalization tốt là subtle và value-driven. Quá nhiều trở nên creepy.

```typescript
// Personalization spectrum
const PERSONALIZATION_LEVELS = {
  // Level 1: Basic (safe, expected)
  basic: {
    examples: [
      '{{firstName}}',
      'Dear {{title}}',
      '{{companyName}} team'
    ],
    comfortLevel: 'high',
    effort: 'low'
  },
  
  // Level 2: Contextual (helpful, appropriate)
  contextual: {
    examples: [
      'Based on your interest in {{category}}',
      'Customers like you also viewed...',
      'Your order from {{lastOrderDate}}'
    ],
    comfortLevel: 'high',
    effort: 'medium'
  },
  
  // Level 3: Behavioral (relevant, but watch out)
  behavioral: {
    examples: [
      'We noticed you were browsing {{lastProductCategory}}',
      'You left {{cartProduct}} in your cart',
      'It\'s been {{daysSinceVisit}} since your last visit'
    ],
    comfortLevel: 'medium',
    effort: 'medium'
  },
  
  // Level 4: Predictive (advanced, requires care)
  predictive: {
    examples: [
      'Based on your browsing patterns, you might like...',
      'Predicted to need {{product}} in {{daysUntilReorder}}'
    ],
    comfortLevel: 'low-medium',
    effort: 'high'
  },
  
  // Level 5: Personal Surveillance (avoid!)
  surveillance: {
    examples: [
      'We saw you were on our site for 2 hours yesterday',
      'You looked at {{specificProducts}}',
      'Your exact location is {{currentLocation}}'
    ],
    comfortLevel: 'very low',
    effort: 'high',
    recommendation: 'AVOID - creepy, privacy concerns'
  }
};

// Safe personalization guidelines
class PersonalizationGuidelines {
  // Rules to follow
  private readonly SAFE_RULES = [
    // Always provide value
    'Personalization must add value, not just show data',
    
    // Keep it general
    'Use category/product type, not specific product names',
    'Use time ranges, not exact timestamps',
    
    // Respect privacy
    'Never mention exact locations',
    'Never mention browsing duration',
    'Never mention other customers\' behavior',
    
    // Be transparent
    'If using data, explain why it matters',
    
    // Allow control
    'Provide preference center for personalization level'
  ];
  
  async validatePersonalization(
    content: string,
    context: PersonalizationContext
  ): Promise<ValidationResult> {
    const creepinessScore = await this.calculateCreepinessScore(
      content,
      context
    );
    
    if (creepinessScore > 70) {
      return {
        valid: false,
        warning: 'This personalization may feel intrusive',
        suggestions: this.getAlternativeApproaches(content)
      };
    }
    
    return { valid: true, creepinessScore };
  }
}
```

### Q12: Làm thế nào để implement product recommendations?

**Trả lời:**

```typescript
// Product recommendation engine
class ProductRecommendationService {
  // Collaborative filtering
  async getCollaborativeFilteringRecommendations(
    contactId: string,
    limit: number = 5
  ): Promise<Product[]> {
    // Find similar customers
    const similarCustomers = await this.findSimilarCustomers(contactId);
    
    // Get products they purchased
    const purchasedProducts = await this.getPurchasedProducts(
      similarCustomers.map(c => c.id)
    );
    
    // Rank by popularity among similar customers
    const productScores = this.rankProducts(purchasedProducts);
    
    // Filter out products contact already has
    const contactProducts = await this.getContactProducts(contactId);
    
    return productScores
      .filter(p => !contactProducts.includes(p.id))
      .slice(0, limit);
  }
  
  // Content-based filtering
  async getContentBasedRecommendations(
    contactId: string,
    limit: number = 5
  ): Promise<Product[]> {
    const contact = await this.contactRepo.findById(contactId);
    
    // Get products matching contact preferences
    const preferences = contact.productPreferences;
    
    const products = await this.productRepo.findMatching({
      categories: preferences.categories,
      priceRange: preferences.priceRange,
      attributes: preferences.attributes
    });
    
    // Score by preference match
    return products
      .map(p => ({
        product: p,
        score: this.calculatePreferenceMatch(p, preferences)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, limit)
      .map(r => r.product);
  }
  
  // Hybrid approach
  async getHybridRecommendations(
    contactId: string,
    limit: number = 5
  ): Promise<ProductRecommendation[]> {
    const [collabProducts, contentProducts, popularityProducts] = 
      await Promise.all([
        this.getCollaborativeFilteringRecommendations(contactId, limit * 2),
        this.getContentBasedRecommendations(contactId, limit * 2),
        this.getPopularProducts(contactId, limit)
      ]);
    
    // Combine and weight scores
    const combined = new Map<string, ProductScore>();
    
    for (const product of collabProducts) {
      combined.set(product.id, {
        product,
        cfScore: 0.5
      });
    }
    
    for (const product of contentProducts) {
      const existing = combined.get(product.id);
      if (existing) {
        existing.contentScore = 0.3;
      } else {
        combined.set(product.id, {
          product,
          contentScore: 0.3
        });
      }
    }
    
    for (const product of popularityProducts) {
      const existing = combined.get(product.id);
      if (existing) {
        existing.popularityScore = 0.2;
      } else {
        combined.set(product.id, {
          product,
          popularityScore: 0.2
        });
      }
    }
    
    // Sort by combined score
    return Array.from(combined.values())
      .map(r => ({
        ...r,
        totalScore: (r.cfScore || 0) + (r.contentScore || 0) + (r.popularityScore || 0)
      }))
      .sort((a, b) => b.totalScore - a.totalScore)
      .slice(0, limit);
  }
}
```

## 6. List Management Questions

### Q13: Tần suất nào là phù hợp để gửi email?

**Trả lời:**

Không có con số cố định - phụ thuộc vào audience và content.

```typescript
// Frequency recommendation engine
class FrequencyOptimizer {
  async getRecommendedFrequency(
    contactId: string
  ): Promise<FrequencyRecommendation> {
    const contact = await this.contactRepo.findById(contactId);
    const engagement = await this.getEngagementHistory(contactId);
    
    // Base frequency by segment
    const baseFrequencies = {
      highly_engaged: { min: 2, max: 4, unit: 'week' },
      engaged: { min: 1, max: 2, unit: 'week' },
      moderate: { min: 1, unit: 'week', max: 2 },
      low_engagement: { min: 1, unit: 'month', max: 1 },
      inactive: { min: 1, unit: 'month', max: 1 },
      at_risk: { min: 2, unit: 'month', max: 1 }
    };
    
    const segment = this.determineSegment(contact, engagement);
    const base = baseFrequencies[segment];
    
    // Adjust based on engagement
    let adjustedMax = base.max;
    
    if (engagement.unsubscribeRate > 0.01) {
      adjustedMax = Math.max(1, adjustedMax - 1);
    }
    
    if (engagement.openRate > 0.4) {
      adjustedMax = adjustedMax + 1;
    }
    
    return {
      minimum: base.min,
      maximum: adjustedMax,
      unit: base.unit,
      personalizedMessage: this.generateMessage(segment, base)
    };
  }
  
  // Check if send is allowed
  async canSend(
    contactId: string,
    campaignType: 'promotional' | 'transactional' | 'newsletter'
  ): Promise<SendDecision> {
    const recentSends = await this.getRecentSends(contactId);
    const frequency = await this.getRecommendedFrequency(contactId);
    
    const recentCount = recentSends.filter(
      s => s.type === campaignType &&
           this.isWithinPeriod(sentAt, frequency.unit)
    ).length;
    
    if (recentCount >= frequency.maximum) {
      return {
        allowed: false,
        reason: `Frequency cap reached: ${frequency.maximum} per ${frequency.unit}`,
        nextAvailable: this.getNextAvailableDate(contactId, frequency)
      };
    }
    
    return { allowed: true };
  }
}
```

### Q14: Khi nào nên cleanup danh sách email?

**Trả lời:**

Regular list maintenance là essential cho deliverability.

```typescript
// List cleanup strategy
class ListCleanupScheduler {
  // Different cleanup frequencies
  private readonly CLEANUP_SCHEDULE = {
    // Remove bounces immediately
    bounces: { frequency: 'immediate', severity: 'critical' },
    
    // Review soft bounces after 3 attempts
    soft_bounces: { frequency: 'after_3_attempts', severity: 'medium' },
    
    // Unsubscribes: immediate removal
    unsubscribes: { frequency: 'immediate', severity: 'critical' },
    
    // Complaints: immediate + special handling
    complaints: { frequency: 'immediate', severity: 'critical' },
    
    // Inactive: periodic review
    inactive: { frequency: 'quarterly', severity: 'low' },
    
    // Duplicate: periodic review
    duplicates: { frequency: 'monthly', severity: 'medium' }
  };
  
  // Automatic bounce handling
  @Process('email.bounce')
  async handleBounce(bounce: BounceEvent): Promise<void> {
    if (bounce.type === 'hard') {
      // Immediately suppress
      await this.suppressionList.addHardBounce(bounce.email);
      await this.contactRepo.markAsHardBounced(bounce.email);
    } else {
      // Track soft bounce
      await this.incrementSoftBounceCount(bounce.email);
    }
  }
  
  // Scheduled inactive cleanup
  @Cron('0 3 * * 0') // 3 AM every Sunday
  async cleanupInactiveContacts(): Promise<CleanupReport> {
    const thresholds = {
      highly_active: 0,
      active: 30,       // days since last activity
      at_risk: 90,
      inactive: 180,
      lapsed: 365
    };
    
    const report: CleanupReport = {
      reviewed: 0,
      reactivated: 0,
      suppressed: 0,
      reengagementInitiated: 0
    };
    
    // Identify inactive contacts
    const inactiveContacts = await this.contactRepo.findInactiveContacts({
      daysSinceActivity: thresholds.inactive
    });
    
    for (const contact of inactiveContacts) {
      report.reviewed++;
      
      // Try re-engagement first
      if (contact.engagementScore > 10) {
        await this.enrollInReengagement(contact.id);
        report.reengagementInitiated++;
      } else {
        // Move to suppressed list
        await this.suppressionList.add(contact.email, {
          reason: 'inactive',
          suppressedAt: new Date()
        });
        await this.contactRepo.markAsInactive(contact.id);
        report.suppressed++;
      }
    }
    
    return report;
  }
  
  // Manual cleanup trigger
  async runManualCleanup(options: CleanupOptions): Promise<CleanupReport> {
    // Can target specific segments
    // Can set custom thresholds
    // Can choose cleanup actions
  }
}
```

### Q15: Làm thế nào để handle contact preferences?

**Trả lời:**

Preference management là key để reduce unsubscribes và increase engagement.

```typescript
// Preference center implementation
class PreferenceCenterService {
  async getPreferenceCenter(contactId: string): Promise<PreferenceCenter> {
    const contact = await this.contactRepo.findById(contactId);
    
    return {
      contactId,
      emailFrequency: contact.preferences?.emailFrequency || 'weekly',
      categories: contact.preferences?.categories || [],
      channels: contact.preferences?.channels || ['email'],
      personalizationLevel: contact.preferences?.personalizationLevel || 'standard',
      
      // All available options
      availableFrequencies: [
        { value: 'daily', label: 'Hàng ngày' },
        { value: 'weekly', label: 'Hàng tuần' },
        { value: 'biweekly', label: '2 tuần một lần' },
        { value: 'monthly', label: 'Hàng tháng' },
        { value: 'occasionally', label: 'Khi có ưu đãi đặc biệt' }
      ],
      
      availableCategories: await this.getAllCategories(),
      availableChannels: [
        { value: 'email', label: 'Email', enabled: true },
        { value: 'sms', label: 'SMS', enabled: true },
        { value: 'push', label: 'Push Notification', enabled: true }
      ]
    };
  }
  
  async updatePreferences(
    contactId: string,
    updates: PreferenceUpdates
  ): Promise<void> {
    const contact = await this.contactRepo.findById(contactId);
    
    // Validate
    if (updates.emailFrequency) {
      await this.validateFrequencyUpdate(contactId, updates.emailFrequency);
    }
    
    // Update contact
    contact.preferences = {
      ...contact.preferences,
      ...updates,
      updatedAt: new Date()
    };
    
    await this.contactRepo.save(contact);
    
    // Adjust automation enrollments based on new frequency
    if (updates.emailFrequency) {
      await this.adjustAutomationEnrollments(contactId, updates.emailFrequency);
    }
    
    // Send confirmation
    await this.sendPreferenceConfirmation(contactId, updates);
    
    // Log for audit
    await this.auditLog.recordPreferenceChange(contactId, updates);
  }
  
  // Unsubscribe via preference center
  async processUnsubscribe(contactId: string): Promise<UnsubscribeResult> {
    const contact = await this.contactRepo.findById(contactId);
    
    return {
      // Full unsubscribe
      fullUnsubscribe: async () => {
        await this.withdrawAllConsent(contactId);
        await this.suppressionList.add(contact.email, {
          reason: 'unsubscribed',
          source: 'preference_center'
        });
        await this.contactRepo.markAsUnsubscribed(contactId);
      },
      
      // Channel-specific unsubscribe
      channelUnsubscribe: async (channel: string) => {
        await this.withdrawConsent(contactId, `${channel}_marketing`);
        await this.cancelPendingCommunications(contactId, channel);
      },
      
      // Preference-based unsubscribe (reduce frequency instead)
      reduceFrequency: async (newFrequency: string) => {
        await this.updatePreferences(contactId, {
          emailFrequency: newFrequency
        });
      }
    };
  }
}
```
