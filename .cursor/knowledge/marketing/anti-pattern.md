# Marketing Anti-Patterns - Các Mẫu Thiết Kế Cần Tránh

## 1. Contact Management Anti-Patterns

### 1.1 Anti-Pattern: Buying Email Lists

**Vấn đề**: Mua email lists từ third parties là một trong những marketing anti-pattern nguy hiểm nhất.

```typescript
// ❌ Anti-pattern: Purchased list usage
class PurchasedListCampaign {
  async execute() {
    // Buying list from third party
    const purchasedContacts = await this.listBroker.getList('leads-50k');
    
    // Mass sending without proper targeting
    for (const email of purchasedContacts) {
      await this.emailService.send({
        to: email,
        subject: 'Hot deal just for you!',
        content: genericPromoContent
      });
    }
  }
}

// Consequences:
// - High bounce rates (damages sender reputation)
// - Spam complaints
// - GDPR/CAN-SPAM violations
// - Low engagement
// - Potential legal action
```

**Giải pháp**: Build organic list through proper lead generation.

```typescript
// ✅ Giải pháp: Organic list building
class OrganicListBuildingService {
  // Multi-channel lead capture
  async captureLead(source: LeadSource, data: LeadData): Promise<Contact> {
    // Validate consent explicitly
    if (!data.explicitConsent) {
      throw new ConsentRequiredError();
    }
    
    // Create contact with proper consent record
    const contact = await this.contactService.create({
      email: data.email,
      source: source.type,
      acquisitionDate: new Date(),
      consentRecords: [{
        consentType: 'email_marketing',
        grantedAt: new Date(),
        source: source.type,
        ipAddress: data.ipAddress,
        userAgent: data.userAgent
      }]
    });
    
    // Trigger welcome journey
    await this.journeyService.enrollContact(
      contact.id,
      'welcome-journey'
    );
    
    return contact;
  }
  
  // Landing page with clear value proposition
  async createHighConvertingLandingPage(config: LandingPageConfig): Promise<void> {
    // Transparent opt-in
    // Clear privacy policy link
    // Easy unsubscribe option
    // Value exchange clearly communicated
  }
}
```

### 1.2 Anti-Pattern: Ignoring Consent

**Vấn đề**: Gửi marketing communications mà không có proper consent verification.

```typescript
// ❌ Anti-pattern: Consent not checked
class EmailMarketingService {
  async sendCampaign(campaignId: UUID): Promise<void> {
    const contacts = await this.contactRepo.getAllActive();
    
    for (const contact of contacts) {
      // NO consent check!
      await this.emailService.send({
        to: contact.email,
        template: campaignId
      });
    }
  }
}
```

**Giải pháp**: Strict consent enforcement.

```typescript
// ✅ Giải pháp: Consent-first approach
class ConsentAwareEmailService {
  constructor(
    private consentService: ConsentService,
    private suppressionList: SuppressionListService
  ) {}
  
  async canSendTo(contactId: UUID, channel: Channel): Promise<boolean> {
    // Check suppression list first
    const contact = await this.contactRepo.findById(contactId);
    if (await this.suppressionList.isSuppressed(contact.email)) {
      return false;
    }
    
    // Check consent
    return this.consentService.hasActiveConsent(contactId, channel);
  }
  
  async sendCampaign(campaignId: UUID): Promise<SendResult> {
    const contacts = await this.contactRepo.getActiveForCampaign(campaignId);
    let sent = 0, blocked = 0;
    
    for (const contact of contacts) {
      if (await this.canSendTo(contact.id, 'email')) {
        await this.emailService.send({
          to: contact.email,
          template: campaignId
        });
        sent++;
      } else {
        blocked++;
        await this.logBlocked(contact.id, campaignId, 'consent_missing');
      }
    }
    
    return { sent, blocked, total: contacts.length };
  }
}
```

### 1.3 Anti-Pattern: Duplicate Contacts

**Vấn đề**: Không handle duplicates, leading to multiple sends to same person.

```typescript
// ❌ Anti-pattern: No deduplication
class ImportService {
  async importContacts(data: ImportData[]): Promise<void> {
    for (const row of data) {
      await this.contactRepo.create({
        email: row.email,
        firstName: row.first_name,
        lastName: row.last_name
      });
      // No check if email already exists!
    }
  }
}

// Result: Same person imported multiple times
// → Multiple welcome emails
// → Multiple copies of same campaign
// → Confused analytics
```

**Giải pháp**: Robust deduplication và merging.

```typescript
// ✅ Giải pháp: Smart deduplication
class SmartImportService {
  async importWithDeduplication(data: ImportData[]): Promise<ImportResult> {
    const results = {
      created: 0,
      merged: 0,
      duplicates: 0,
      errors: 0
    };
    
    for (const row of data) {
      try {
        // Find existing contact
        const existing = await this.findByEmail(row.email);
        
        if (existing) {
          // Merge new data with existing
          const merged = this.mergeContactData(existing, row);
          await this.contactRepo.save(merged);
          results.merged++;
        } else {
          // Check for fuzzy duplicates
          const fuzzyMatch = await this.findFuzzyDuplicate(row);
          if (fuzzyMatch) {
            // Offer merge or skip
            const merged = this.mergeContactData(fuzzyMatch, row);
            await this.contactRepo.save(merged);
            results.merged++;
          } else {
            // Create new
            await this.contactRepo.create(this.toContact(row));
            results.created++;
          }
        }
      } catch (error) {
        results.errors++;
        await this.logImportError(row, error);
      }
    }
    
    return results;
  }
  
  private async findFuzzyDuplicate(data: ImportData): Promise<Contact | null> {
    // Find by similar email
    const emailVariants = this.generateEmailVariants(data.email);
    for (const variant of emailVariants) {
      const existing = await this.contactRepo.findByEmail(variant);
      if (existing) return existing;
    }
    
    // Find by name + company
    if (data.firstName && data.lastName && data.company) {
      return this.contactRepo.findByNameAndCompany(
        data.firstName,
        data.lastName,
        data.company
      );
    }
    
    return null;
  }
}
```

## 2. Email Marketing Anti-Patterns

### 2.1 Anti-Pattern: Generic One-Size-Fits-All Emails

**Vấn đề**: Gửi cùng một email cho tất cả contacts, không personalization.

```typescript
// ❌ Anti-pattern: Generic mass email
const genericEmail = {
  subject: 'Special Offer Just For You!',
  content: `
    <h1>Dear Customer,</h1>
    <p>We have exciting news for you!</p>
    <p>Check out our products...</p>
  `
};

// Problems:
// - Low engagement (impersonal)
// - High unsubscribe rates
// - Poor conversion
// - Damages sender reputation
```

**Giải pháp**: Personalization và segmentation.

```typescript
// ✅ Giải pháp: Personalized, segmented emails
class PersonalizationService {
  async personalizeEmail(
    contact: Contact,
    campaign: Campaign
  ): Promise<PersonalizedEmail> {
    const context = {
      contact,
      company: await this.getCompanyContext(),
      segment: await this.getContactSegment(contact.id)
    };
    
    return {
      subject: this.personalizeSubject(campaign.subjectTemplate, context),
      content: this.personalizeContent(campaign.contentTemplate, context),
      images: await this.selectPersonalizedImages(contact),
      products: await this.getPersonalizedRecommendations(contact)
    };
  }
  
  private personalizeSubject(template: string, ctx: PersonalizationContext): string {
    // Replace {{contact.firstName}} etc.
    let subject = template;
    
    if (ctx.contact.firstName) {
      subject = subject.replace('{{firstName}}', ctx.contact.firstName);
    }
    
    // Segment-based content
    if (ctx.segment === 'vip') {
      subject = subject.replace('{{segment_suffix}}', '✨ VIP Exclusive');
    } else if (ctx.segment === 'new') {
      subject = subject.replace('{{segment_suffix}}', 'Welcome!');
    }
    
    return subject;
  }
}
```

### 2.2 Anti-Pattern: Excessive Email Frequency

**Vấn đề**: Gửi quá nhiều emails, leading to list fatigue và unsubscribes.

```typescript
// ❌ Anti-pattern: No frequency control
class AggressiveEmailService {
  async sendPromotionalCampaign(campaignId: UUID): Promise<void> {
    // Get ALL active contacts
    const contacts = await this.contactRepo.getAllActive();
    
    for (const contact of contacts) {
      // Check if already received emails this week? NO!
      
      // Just send!
      await this.emailService.send({
        to: contact.email,
        template: campaignId
      });
    }
  }
}

// Result: Same contact receives 10 emails in one week
// → Spam complaints
// → Mass unsubscribes
// → Low engagement
```

**Giải pháp**: Frequency capping và preference centers.

```typescript
// ✅ Giải pháp: Smart frequency management
class FrequencyManagementService {
  private readonly FREQUENCY_LIMITS = {
    promotional: { max: 2, period: 'week' },
    newsletter: { max: 1, period: 'week' },
    transactional: { max: 5, period: 'day' }
  };
  
  async canSendEmail(
    contactId: UUID,
    emailType: EmailType
  ): Promise<{ allowed: boolean; reason?: string }> {
    const limit = this.FREQUENCY_LIMITS[emailType];
    
    // Count recent sends
    const recentSends = await this.emailEventRepo.countSends({
      contactId,
      emailType,
      since: this.getPeriodStart(limit.period)
    });
    
    if (recentSends >= limit.max) {
      return {
        allowed: false,
        reason: `Frequency cap reached: ${limit.max} per ${limit.period}`
      };
    }
    
    // Check for send today
    const todaySends = await this.emailEventRepo.countSends({
      contactId,
      since: startOfDay(new Date())
    });
    
    if (todaySends > 0 && emailType === 'promotional') {
      // Don't send multiple promotional emails on same day
      return {
        allowed: false,
        reason: 'Already sent promotional email today'
      };
    }
    
    return { allowed: true };
  }
  
  async getContactPreferences(contactId: UUID): Promise<FrequencyPreferences> {
    const contact = await this.contactRepo.findById(contactId);
    
    return {
      maxWeeklyEmails: contact.preferences?.maxWeeklyEmails || 3,
      preferredCategories: contact.preferences?.preferredCategories || [],
      doNotDisturb: contact.preferences?.doNotDisturb || null
    };
  }
}
```

### 2.3 Anti-Pattern: Broken Links và Images

**Vấn đề**: URLs không hoạt động, broken images, gây poor user experience.

```typescript
// ❌ Anti-pattern: Hardcoded URLs, no validation
const emailTemplate = `
  <a href="https://mysite.com/product/123">Buy Now</a>
  <img src="https://cdn.mysite.com/images/banner.jpg">
`;

// Problems:
// - Product may be discontinued
// - CDN URL may change
// - No tracking
// - No fallback
```

**Giải pháp**: Dynamic link management và validation.

```typescript
// ✅ Giải pháp: Robust link và image management
class LinkManagementService {
  constructor(
    private linkRepository: LinkRepository,
    private imageRepository: ImageRepository
  ) {}
  
  async processEmailContent(
    content: string,
    context: { contactId: UUID; campaignId: UUID }
  ): Promise<ProcessedContent> {
    // Find all URLs
    const urls = this.extractUrls(content);
    
    // Validate each URL
    const validLinks = await Promise.all(
      urls.map(async (url) => {
        const exists = await this.linkRepository.exists(url);
        if (!exists) {
          // Try to find redirect
          const redirect = await this.linkRepository.findRedirect(url);
          return redirect || { original: url, valid: false };
        }
        
        // Add tracking
        const trackingId = await this.createTrackingId({
          url,
          contactId: context.contactId,
          campaignId: context.campaignId
        });
        
        return {
          original: url,
          valid: true,
          trackingUrl: this.buildTrackingUrl(trackingId)
        };
      })
    );
    
    // Replace broken links with fallback
    let processedContent = content;
    for (const link of validLinks) {
      if (!link.valid) {
        processedContent = processedContent.replace(
          link.original,
          this.getFallbackUrl()
        );
      } else {
        processedContent = processedContent.replace(
          link.original,
          link.trackingUrl
        );
      }
    }
    
    return {
      content: processedContent,
      links: validLinks,
      warnings: validLinks.filter(l => !l.valid).map(l => l.original)
    };
  }
  
  async validateImages(content: string): Promise<ImageValidation[]> {
    const imageUrls = this.extractImageUrls(content);
    
    return Promise.all(
      imageUrls.map(async (url) => {
        const exists = await this.imageRepository.exists(url);
        
        if (!exists) {
          return {
            url,
            valid: false,
            suggestion: await this.findAlternativeImage(url)
          };
        }
        
        // Check file size
        const fileSize = await this.imageRepository.getFileSize(url);
        if (fileSize > 100 * 1024) { // 100KB
          return {
            url,
            valid: true,
            warning: 'Large image may affect load time'
          };
        }
        
        return { url, valid: true };
      })
    );
  }
}
```

## 3. Automation Anti-Patterns

### 3.1 Anti-Pattern: Infinite Journey Loops

**Vấn đề**: Journey designs có thể loop infinitely nếu không có proper exit conditions.

```typescript
// ❌ Anti-pattern: Looping journey
const badJourney = {
  nodes: [
    {
      id: 'welcome_email',
      type: 'action',
      config: { actionType: 'send_email' }
    },
    {
      id: 'check_opened',
      type: 'condition',
      config: { field: 'lastEmailOpened' }
    }
  ],
  edges: [
    { from: 'welcome_email', to: 'check_opened' },
    // NO EXIT from this loop!
    { from: 'check_opened', to: 'send_another_email' },
    { from: 'send_another_email', to: 'check_opened' } // Back to check
  ]
};

// Result: Contact stuck in infinite loop
```

**Giải pháp**: Proper exit conditions và loop detection.

```typescript
// ✅ Giải pháp: Safe journey design
class JourneyValidationService {
  async validateJourney(journey: Journey): Promise<ValidationResult> {
    const issues: JourneyIssue[] = [];
    
    // Check for infinite loops
    const loops = this.detectLoops(journey);
    if (loops.length > 0) {
      issues.push({
        type: 'infinite_loop',
        severity: 'error',
        nodes: loops,
        message: 'Journey contains infinite loops without exit conditions'
      });
    }
    
    // Check all paths lead to terminal nodes
    const unreachableTerminals = this.findUnreachableTerminals(journey);
    if (unreachableTerminals.length > 0) {
      issues.push({
        type: 'unreachable_node',
        severity: 'warning',
        nodes: unreachableTerminals
      });
    }
    
    // Check loop count limits
    const loopNodes = this.findLoopNodes(journey);
    for (const node of loopNodes) {
      const maxIterations = node.config.maxIterations || 5;
      if (maxIterations > 10) {
        issues.push({
          type: 'excessive_loop_iterations',
          severity: 'warning',
          node: node.id,
          maxIterations
        });
      }
    }
    
    return {
      valid: !issues.some(i => i.severity === 'error'),
      issues
    };
  }
  
  private detectLoops(journey: Journey): string[][] {
    const graph = this.buildAdjacencyList(journey);
    const loops: string[][] = [];
    
    // Use DFS to find cycles
    const visited = new Set<string>();
    const recStack = new Set<string>();
    const path: string[] = [];
    
    const dfs = (nodeId: string): void => {
      visited.add(nodeId);
      recStack.add(nodeId);
      path.push(nodeId);
      
      for (const neighbor of graph.get(nodeId) || []) {
        if (!visited.has(neighbor)) {
          dfs(neighbor);
        } else if (recStack.has(neighbor)) {
          // Found cycle
          const cycleStart = path.indexOf(neighbor);
          loops.push(path.slice(cycleStart));
        }
      }
      
      path.pop();
      recStack.delete(nodeId);
    };
    
    for (const node of journey.nodes) {
      if (!visited.has(node.id)) {
        dfs(node.id);
      }
    }
    
    return loops;
  }
}

// Journey executor with loop protection
class SafeJourneyExecutor {
  private readonly MAX_NODE_ITERATIONS = 10;
  
  async executeNode(instance: JourneyInstance, node: JourneyNode): Promise<void> {
    // Check iteration count
    const nodeExecutions = instance.nodeHistory.filter(
      n => n.nodeId === node.id
    );
    
    if (nodeExecutions.length >= this.MAX_NODE_ITERATIONS) {
      logger.warn('Journey iteration limit reached', {
        instanceId: instance.id,
        nodeId: node.id
      });
      
      instance.exitReason = 'iteration_limit_reached';
      instance.exitedAt = new Date();
      return;
    }
    
    // Execute node...
  }
}
```

### 3.2 Anti-Pattern: Automation Without Testing

**Vấn đề**: Activate automation workflows mà không test, leading to embarrassing hoặc harmful mistakes.

```typescript
// ❌ Anti-pattern: Activate without testing
class CampaignActivationService {
  async activateCampaign(campaignId: UUID): Promise<void> {
    // Just flip the switch!
    await this.campaignRepo.updateStatus(campaignId, 'active');
    
    // No testing done
    // No preview sent
    // No validation
  }
}

// Real stories:
// - Test email "Hi [first name]" sent to millions as "Hi undefined"
// - Discount email with wrong percentage
// - Wrong audience segment
// - Broken unsubscribe links
```

**Giải pháp**: Comprehensive testing framework.

```typescript
// ✅ Giải pháp: Multi-stage testing process
class CampaignTestingService {
  // Stage 1: Unit tests
  async runUnitTests(campaignId: UUID): Promise<TestResult> {
    const tests = [
      this.testPersonalizationTokens(campaignId),
      this.testLinkValidity(campaignId),
      this.testImageAccessibility(campaignId),
      this.testSpamScore(campaignId)
    ];
    
    return this.aggregateResults(await Promise.all(tests));
  }
  
  // Stage 2: Visual preview
  async generatePreviews(campaignId: UUID): Promise<Preview[]> {
    const testProfiles = [
      { name: 'New Contact', contact: this.createTestContact({ lifecycle: 'new' }) },
      { name: 'VIP Customer', contact: this.createTestContact({ lifecycle: 'vip', lifetimeValue: 50000000 }) },
      { name: 'Inactive User', contact: this.createTestContact({ lastActivity: subtractDays(new Date(), 90) }) }
    ];
    
    return Promise.all(
      testProfiles.map(async (profile) => ({
        profile: profile.name,
        html: await this.renderForContact(profile.contact, campaignId),
        issues: await this.validateRender(profile.html)
      }))
    );
  }
  
  // Stage 3: Seed list test
  async sendToSeedList(campaignId: UUID): Promise<SeedResult> {
    const seedContacts = await this.getInternalSeedList();
    
    const results = await Promise.all(
      seedContacts.map(seed => this.sendTestEmail(campaignId, seed))
    );
    
    return {
      sent: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      inboxPlacement: await this.checkInboxPlacement(results)
    };
  }
  
  // Stage 4: Small segment test
  async runSmallSegmentTest(
    campaignId: UUID,
    segmentSize: number = 1000
  ): Promise<TestResult> {
    const testContacts = await this.contactRepo.getRandomContacts(segmentSize);
    
    // Send to test segment
    await this.sendCampaignToContacts(campaignId, testContacts);
    
    // Wait for initial metrics
    await this.delay(4 * 60 * 60 * 1000); // 4 hours
    
    // Analyze metrics
    return this.analyzeTestResults(campaignId, testContacts.map(c => c.id));
  }
  
  // Final activation requires passing all stages
  async activateCampaign(campaignId: UUID): Promise<void> {
    const preActivationChecks = await Promise.all([
      this.runUnitTests(campaignId),
      this.generatePreviews(campaignId),
      this.sendToSeedList(campaignId)
    ]);
    
    // All must pass
    if (!this.allTestsPassed(preActivationChecks)) {
      throw new CampaignValidationError(
        'Campaign failed validation',
        preActivationChecks
      );
    }
    
    // Optional: run small segment test
    const smallTest = await this.runSmallSegmentTest(campaignId);
    if (smallTest.unsubscribeRate > 0.5) {
      throw new CampaignValidationError(
        'Unsubscribe rate too high in test'
      );
    }
    
    await this.campaignRepo.updateStatus(campaignId, 'active');
  }
}
```

### 3.3 Anti-Pattern: Trigger Overload

**Vấn đề**: Quá nhiều triggers gửi too many messages to same contact.

```typescript
// ❌ Anti-pattern: Multiple triggers, no coordination
// Welcome journey: sends 5 emails
// Product browse: sends 3 emails  
// Cart abandonment: sends 4 emails
// Re-engagement: sends 3 emails
// Newsletter: sends 1 email/week

// Result: One contact receives 16 emails in first week!
// → Complete burnout
```

**Giải pháp**: Unified communication queue.

```typescript
// ✅ Giải pháp: Communication queue with prioritization
class UnifiedCommunicationQueue {
  private queue: CommunicationItem[] = [];
  
  async enqueue(item: CommunicationItem): Promise<void> {
    // Check for conflicts
    const conflicts = await this.findConflicts(item);
    
    if (conflicts.length > 0) {
      // Apply conflict resolution
      const resolution = this.resolveConflicts(item, conflicts);
      
      switch (resolution.strategy) {
        case 'skip':
          logger.info('Skipping duplicate communication', {
            contactId: item.contactId,
            reason: resolution.reason
          });
          return;
          
        case 'merge':
          // Merge with existing communication
          item = this.mergeCommunications(item, conflicts[0]);
          break;
          
        case 'prioritize':
          // Keep higher priority, skip others
          item = this.keepHigherPriority(item, conflicts);
          break;
      }
    }
    
    this.queue.push(item);
    await this.persistQueue();
  }
  
  private resolveConflicts(
    newItem: CommunicationItem,
    conflicts: CommunicationItem[]
  ): ConflictResolution {
    // Same campaign in last 24 hours?
    const recentSameCampaign = conflicts.find(
      c => c.campaignId === newItem.campaignId &&
           c.enqueuedAt > subtractHours(new Date(), 24)
    );
    
    if (recentSameCampaign) {
      return { strategy: 'skip', reason: 'same_campaign_recently' };
    }
    
    // High frequency?
    const recentCount = conflicts.filter(
      c => c.enqueuedAt > subtractDays(new Date(), 1)
    ).length;
    
    if (recentCount >= 2) {
      return { 
        strategy: 'prioritize', 
        reason: 'high_frequency',
        keepHighestPriority: true
      };
    }
    
    // Merge similar messages
    if (this.areSimilar(newItem, conflicts[0])) {
      return { strategy: 'merge', reason: 'similar_content' };
    }
    
    return { strategy: 'skip', reason: 'too_many_conflicts' };
  }
}
```

## 4. Analytics Anti-Patterns

### 4.1 Anti-Pattern: Vanity Metrics Focus

**Vấn đề**: Theo dõi metrics không liên quan đến business outcomes.

```typescript
// ❌ Anti-pattern: Vanity metrics obsession
class VanityMetricsDashboard {
  getMetrics(): DashboardMetrics {
    return {
      totalEmailsSent: 1000000,      // "We sent a million emails!"
      totalSubscribers: 500000,       // "Half a million subscribers!"
      socialFollowers: 100000,        // "100K followers!"
      websiteVisits: 500000,           // "Half a million visits!"
      emailOpenRate: 25,              // "Great open rate!"
      
      // But what about...
      // revenue_generated?
      // customer_acquisition_cost?
      // lifetime_value?
      // conversion_rate?
      // roi?
    };
  }
}
```

**Giải pháp**: Business-aligned metrics framework.

```typescript
// ✅ Giải pháp: Business metrics focus
class BusinessMetricsService {
  async calculateMarketingROI(campaignId: UUID): Promise<MarketingROI> {
    const campaign = await this.campaignRepo.findById(campaignId);
    
    // Attribution
    const attributedRevenue = await this.attributionService
      .getAttributedRevenue(campaignId);
    
    const attributedCustomers = await this.attributionService
      .getNewCustomers(campaignId);
    
    // Costs
    const costs = await this.calculateCampaignCosts(campaignId);
    
    // Calculate metrics
    const grossProfit = attributedRevenue * campaign.avgMargin;
    const netProfit = grossProfit - costs.total;
    const roi = costs.total > 0 ? (netProfit / costs.total) * 100 : 0;
    
    // Customer metrics
    const cac = costs.total / (attributedCustomers || 1);
    const ltv = await this.calculateAverageLTV(attributedCustomers);
    const ltvToCACRatio = ltv / cac;
    
    return {
      revenue: attributedRevenue,
      customers: attributedCustomers,
      costs: costs.total,
      grossProfit,
      netProfit,
      roi,
      cac,
      ltv,
      ltvToCACRatio,
      paybackPeriod: this.calculatePaybackPeriod(campaign, attributedRevenue)
    };
  }
  
  // Engagement metrics that matter
  async calculateEngagementScore(contactId: UUID): Promise<EngagementMetrics> {
    const events = await this.getContactEvents(contactId, { 
      days: 90 
    });
    
    const recency = this.calculateRecencyScore(events);
    const frequency = this.calculateFrequencyScore(events);
    const monetary = await this.calculateMonetaryScore(contactId);
    const engagement = this.calculateEngagementScore(events);
    
    return {
      rfmScore: (recency + frequency + monetary) / 3,
      recency,
      frequency,
      monetary,
      engagement,
      trends: this.calculateEngagementTrends(events),
      recommendedActions: this.getRecommendedActions(recency, frequency, engagement)
    };
  }
}
```

### 4.2 Anti-Pattern: Ignoring Data Quality

**Vấn đề**: Báo cáo trên dirty data, leading to wrong decisions.

```typescript
// ❌ Anti-pattern: Report on all data
class DirtyReportService {
  async generateReport(): Promise<Report> {
    const contacts = await this.contactRepo.getAll();
    
    // No data cleaning!
    // Bounced emails included
    // Unsubscribed contacts included
    // Duplicate records counted
    // Test contacts included
    
    return {
      totalSubscribers: contacts.length, // WRONG
      activeContacts: contacts.length,   // WRONG
      emailOpens: this.calculateOpenRate(contacts)
    };
  }
}
```

**Giải pháp**: Data quality framework.

```typescript
// ✅ Giải pháp: Clean data reporting
class CleanReportService {
  async generateReport(): Promise<Report> {
    // Get clean contact list
    const contacts = await this.contactService.getCleanContactList();
    
    // Exclude:
    // - Bounced emails
    // - Unsubscribed
    // - Duplicates
    // - Test contacts
    // - Spam complainers
    
    const activeContacts = contacts.filter(c => 
      c.status === 'active' &&
      !c.isBounced &&
      !c.isUnsubscribed &&
      !c.isTest &&
      c.hasValidEmail
    );
    
    // Only count real engagement
    const engagedContacts = activeContacts.filter(c =>
      c.lastActivityAt > subtractDays(new Date(), 90)
    );
    
    return {
      totalSubscribers: activeContacts.length,
      engagedSubscribers: engagedContacts.length,
      engagementRate: engagedContacts.length / activeContacts.length,
      
      // With data quality breakdown
      qualityMetrics: {
        validEmails: activeContacts.filter(c => c.hasValidEmail).length,
        bounced: contacts.filter(c => c.isBounced).length,
        unsubscribed: contacts.filter(c => c.isUnsubscribed).length,
        duplicates: await this.countDuplicates(),
        testContacts: contacts.filter(c => c.isTest).length
      }
    };
  }
  
  async getDataQualityScore(): Promise<DataQualityScore> {
    const [totalContacts, validContacts, cleanContacts] = await Promise.all([
      this.contactRepo.countAll(),
      this.contactRepo.countValid(),
      this.contactService.getCleanContactList()
    ]);
    
    return {
      totalContacts,
      validContacts,
      cleanContacts,
      score: (cleanContacts.length / totalContacts) * 100,
      issues: await this.identifyDataQualityIssues()
    };
  }
}
```

## 5. Personalization Anti-Patterns

### 5.1 Anti-Pattern: Stalker Personalization

**Vấn đề**: Personalization quá creepy, making customers uncomfortable.

```typescript
// ❌ Anti-pattern: Creepy personalization
const creepyEmail = {
  subject: 'We noticed you were looking at {{lastProductViewed}}...',
  content: `
    Hi {{firstName}},
    
    We saw you were browsing our site for 2 hours yesterday.
    You looked at ${productCount} items.
    You seemed interested in ${productNames}.
    
    Your birthday is coming up on {{dateOfBirth}}!
    Last purchase: {{lastPurchaseDate}}
    Average order: {{avgOrderValue}}
    
    Don't worry, we're not watching you... much.
  `
};

// Result:
// - Privacy concerns
// - Uncomfortable customers
// - Brand trust damage
// - Legal issues (GDPR)
```

**Giải pháp**: Subtle, value-driven personalization.

```typescript
// ✅ Giải pháp: Tasteful personalization
class TastefulPersonalizationService {
  async personalizeContent(
    contact: Contact,
    content: ContentTemplate
  ): Promise<PersonalizedContent> {
    // Only use data that adds value
    const personalizationData = {
      // ✅ Good: Obvious value-adds
      firstName: contact.profile.firstName,
      companyName: contact.company?.name,
      preferredCategory: contact.preferences?.preferredCategory,
      
      // ✅ OK: Clear why we know this
      accountType: contact.accountType,
      membershipTier: contact.membershipTier,
      
      // ❌ Don't use: Privacy invasive
      // dateOfBirth (unless birthday campaign)
      // browsing history details
      // exact purchase history (unless relevant)
    };
    
    // Keep content natural
    let subject = content.subject;
    let body = content.body;
    
    // Personalize only if it makes sense
    if (personalizationData.firstName) {
      subject = subject.replace('{{firstName}}', personalizationData.firstName);
    }
    
    // Offer relevant products (not stalker-ish)
    if (personalizationData.preferredCategory) {
      body = body.replace(
        '{{relevantProducts}}',
        await this.getProductsInCategory(personalizationData.preferredCategory)
      );
    }
    
    return { subject, body };
  }
  
  // Privacy-respecting recommendations
  async getRecommendations(contactId: UUID): Promise<Product[]> {
    const contact = await this.contactRepo.findById(contactId);
    
    // Use aggregate patterns, not individual behavior
    // "Customers like you also bought..."
    const similarCustomers = await this.findSimilarCustomers(
      contact.company,
      contact.preferences
    );
    
    return this.aggregateRecommendations(similarCustomers);
  }
}
```

### 5.2 Anti-Pattern: Personalization Failures

**Vấn đề**: Failed personalization tokens hiển thị ugly "undefined" hoặc raw tokens.

```typescript
// ❌ Anti-pattern: No fallback handling
const template = `
  Hi {{firstName}},
  
  Thanks for being a {{membershipTier}} member since {{joinDate}}.
  
  Your last order was on {{lastOrderDate}}.
`;

const rendered = template
  .replace('{{firstName}}', contact.firstName) // If undefined → "Hi undefined,"
  .replace('{{membershipTier}}', contact.membershipTier)
  .replace('{{joinDate}}', contact.joinDate)
  .replace('{{lastOrderDate}}', contact.lastOrderDate);

// Result:
// "Hi undefined,"
// "Thanks for being a null member since null."
// "Your last order was on undefined."
```

**Giải pháp**: Robust personalization engine.

```typescript
// ✅ Giải pháp: Safe personalization
class SafePersonalizationService {
  private readonly FALLBACKS: Record<string, string | ((ctx: any) => string)> = {
    firstName: 'bạn',
    lastName: '',
    companyName: '',
    membershipTier: 'valued',
    joinDate: () => 'gần đây',
    lastOrderDate: 'lần cuối bạn mua sắm'
  };
  
  personalize(template: string, context: PersonalizationContext): string {
    return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      const value = this.getNestedValue(context, key);
      
      if (value === null || value === undefined) {
        const fallback = this.FALLBACKS[key];
        if (typeof fallback === 'function') {
          return fallback(context);
        }
        return fallback ?? match; // Keep original if no fallback
      }
      
      // Format value appropriately
      return this.formatValue(value, key);
    });
  }
  
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce(
      (current, key) => current?.[key],
      obj
    );
  }
  
  private formatValue(value: any, key: string): string {
    switch (key) {
      case 'joinDate':
      case 'lastOrderDate':
        return this.formatDate(value);
      case 'membershipTier':
        return this.formatTier(value);
      case 'firstName':
        return this.sanitizeName(value);
      default:
        return String(value);
    }
  }
  
  private sanitizeName(name: string): string {
    // Remove any HTML/injection attempts
    return name.replace(/<[^>]*>/g, '').trim();
  }
  
  private formatTier(tier: string): string {
    const tierNames: Record<string, string> = {
      'gold': 'Khách hàng Vàng',
      'silver': 'Khách hàng Bạc',
      'bronze': 'Khách hàng Đồng',
      'standard': 'khách hàng'
    };
    return tierNames[tier.toLowerCase()] || tier;
  }
}
```

## 6. Segmentation Anti-Patterns

### 6.1 Anti-Pattern: Over-Segmentation

**Vấn đề**: Quá nhiều tiny segments, mỗi cái chỉ vài contacts.

```typescript
// ❌ Anti-pattern: Obsessive segmentation
const hyperSpecificSegments = [
  'male_25_30_engineer_sf_rent_2000_2500',
  'female_28_35_doctor_ny_interest_sports',
  'single_30_35_engineer_la_income_100k_150k',
  // ... thousands more
];

// Result:
// - Each segment has 10-50 contacts
// - Can't run effective campaigns
// - Analytics meaningless
// - Maintenance nightmare
```

**Giải pháp**: Actionable segmentation framework.

```typescript
// ✅ Giải pháp: Strategic segmentation
class StrategicSegmentationService {
  private readonly ACTIONABLE_SEGMENTS = [
    // Lifecycle segments (7 max)
    { id: 'prospect', description: 'New leads', minSize: 100 },
    { id: 'qualified', description: 'MQLs ready for sales', minSize: 50 },
    { id: 'customer_new', description: 'First 90 days', minSize: 100 },
    { id: 'customer_active', description: 'Regular buyers', minSize: 500 },
    { id: 'customer_loyal', description: 'High LTV, repeat buyers', minSize: 200 },
    { id: 'at_risk', description: 'Declining engagement', minSize: 100 },
    { id: 'lapsed', description: 'No activity 90+ days', minSize: 100 },
    
    // Engagement segments (5 max)
    { id: 'engaged_email', description: 'Opens emails regularly', minSize: 500 },
    { id: 'engaged_site', description: 'Visits website', minSize: 300 },
    { id: 'engaged_social', description: 'Active on social', minSize: 200 },
    { id: 'disengaged', description: 'Not engaging', minSize: 500 },
    { id: 'never_engaged', description: 'No activity ever', minSize: 100 }
  ];
  
  async getSegmentContacts(
    segmentId: string,
    options: { minSize?: number } = {}
  ): Promise<Contact[]> {
    const segment = this.ACTIONABLE_SEGMENTS.find(s => s.id === segmentId);
    
    if (!segment) {
      throw new InvalidSegmentError(segmentId);
    }
    
    const contacts = await this.querySegment(segment);
    
    // Warn if segment too small
    if (contacts.length < segment.minSize) {
      logger.warn('Segment below minimum size', {
        segment: segmentId,
        current: contacts.length,
        minimum: segment.minSize
      });
    }
    
    return contacts;
  }
}
```

### 6.2 Anti-Pattern: Static Segments

**Vấn đề**: Segments không update khi contact behavior changes.

```typescript
// ❌ Anti-pattern: Static segment membership
const staticSegment = {
  name: 'VIP Customers',
  members: ['contact-1', 'contact-2', 'contact-3'], // Snapshot!
  createdAt: new Date('2025-01-01')
};

// Problems:
// - Contact loses VIP status → still in VIP segment
// - New VIP → not added automatically
// - Segment becomes stale
// - Wrong targeting
```

**Giải pháp**: Dynamic, real-time segmentation.

```typescript
// ✅ Giải pháp: Dynamic segment evaluation
class DynamicSegmentationService {
  async getSegmentContacts(
    segmentId: UUID,
    pagination: Pagination
  ): Promise<PaginatedResult<Contact>> {
    const segment = await this.segmentRepo.findById(segmentId);
    
    if (segment.isStatic) {
      // Use cached membership
      return this.getStaticSegmentMembers(segmentId, pagination);
    }
    
    // Dynamic segment - evaluate criteria in real-time
    return this.evaluateDynamicSegment(segment, pagination);
  }
  
  private async evaluateDynamicSegment(
    segment: Segment,
    pagination: Pagination
  ): Promise<PaginatedResult<Contact>> {
    // Build query from segment criteria
    const { whereClause, params } = this.buildCriteriaQuery(
      segment.criteria
    );
    
    // Execute query
    const [contacts, total] = await Promise.all([
      this.contactRepo.query(`
        SELECT c.* FROM contacts c
        WHERE ${whereClause}
        ORDER BY c.last_activity_at DESC
        LIMIT $${params.length + 1} OFFSET $${params.length + 2}
      `, [...params, pagination.limit, pagination.offset]),
      
      this.contactRepo.query(`
        SELECT COUNT(*) FROM contacts c
        WHERE ${whereClause}
      `, params)
    ]);
    
    return {
      items: contacts,
      total: parseInt(total.rows[0].count),
      page: pagination.page,
      limit: pagination.limit
    };
  }
}

// Real-time segment updates
class SegmentUpdateService {
  // Listen to relevant events
  registerEventListeners(): void {
    this.eventBus.subscribe('order.completed', async (event) => {
      // Maybe now VIP?
      await this.updateVIPStatus(event.contactId);
    });
    
    this.eventBus.subscribe('email.opened', async (event) => {
      // Update engagement score
      await this.recalculateEngagementScore(event.contactId);
    });
    
    this.eventBus.subscribe('lifecycle.changed', async (event) => {
      // Update lifecycle segments
      await this.updateLifecycleSegments(event.contactId);
    });
  }
}
```

## 7. Testing Anti-Patterns

### 7.1 Anti-Pattern: No A/B Testing

**Vấn đề**: Never testing assumptions, always guessing.

```typescript
// ❌ Anti-pattern: "I think this will work"
class CampaignManager {
  async createCampaign(): Promise<void> {
    // Assumptions everywhere
    const subject = 'Amazing Deal Just For You!'; // "Feels good"
    const sendTime = '9 AM'; // "That's when people check email"
    const ctaText = 'Buy Now'; // "Short and direct"
    const colorScheme = 'Red'; // "Red converts!"
    
    // No testing
    // No data
    // Pure guesswork
  }
}
```

**Giải pháp**: Test-driven optimization.

```typescript
// ✅ Giải pháp: Systematic testing
class TestDrivenCampaignService {
  async createCampaign(config: CampaignConfig): Promise<void> {
    // Create experiment
    const experiment = await this.experimentService.create({
      name: `${config.name} - Subject Line Test`,
      variants: [
        { name: 'personalized', subject: this.generatePersonalizedSubject(config) },
        { name: 'urgency', subject: this.generateUrgencySubject(config) },
        { name: 'benefit', subject: this.generateBenefitSubject(config) }
      ],
      metric: 'click_rate',
      minSampleSize: 1000
    });
    
    // Test send times
    const timeExperiment = await this.experimentService.create({
      name: `${config.name} - Send Time Test`,
      variants: [
        { name: 'morning', sendTime: '8 AM' },
        { name: 'afternoon', sendTime: '2 PM' },
        { name: 'evening', sendTime: '6 PM' }
      ],
      metric: 'open_rate'
    });
    
    // Test CTA
    const ctaExperiment = await this.experimentService.create({
      name: `${config.name} - CTA Test`,
      variants: [
        { name: 'buy_now', ctaText: 'Mua ngay', ctaColor: 'red' },
        { name: 'learn_more', ctaText: 'Tìm hiểu thêm', ctaColor: 'blue' },
        { name: 'get_offer', ctaText: 'Nhận ưu đãi', ctaColor: 'green' }
      ],
      metric: 'click_rate'
    });
    
    // Run all experiments
    // Analyze results
    // Apply winning variants
  }
  
  async calculateSignificance(
    experimentId: UUID
  ): Promise<SignificanceResult> {
    // Statistical significance calculation
    // Ensure results are meaningful, not random
  }
}
```

### 7.2 Anti-Pattern: Testing Too Small Samples

**Vấn đề**: Drawing conclusions từ samples quá nhỏ.

```typescript
// ❌ Anti-pattern: "We tested 10 people"
class TinyTestService {
  async analyzeResults(): Promise<TestResult> {
    const results = {
      variantA: { sent: 5, opens: 2, clicks: 1 },
      variantB: { sent: 5, opens: 1, clicks: 0 }
    };
    
    // "Variant A wins with 40% open rate!"
    // "Let's send to everyone!"
    
    // Problem:
    // - 5 vs 5 is statistically meaningless
    // - Random chance explains the difference
    // - Wrong decision based on noise
  }
}
```

**Giải pháp**: Statistical rigor.

```typescript
// ✅ Giải pháp: Sample size calculation and significance testing
class StatisticalTestService {
  // Calculate minimum sample size needed
  calculateRequiredSampleSize(params: {
    baselineRate: number;      // Current open rate: 20%
    minimumDetectableEffect: number; // Want to detect: 10% lift
    confidenceLevel: number;   // 95%
    statisticalPower: number;  // 80%
  }): number {
    const { baselineRate, minimumDetectableEffect } = params;
    
    const p1 = baselineRate;
    const p2 = baselineRate * (1 + minimumDetectableEffect);
    
    const zAlpha = 1.96; // 95% confidence
    const zBeta = 0.84; // 80% power
    
    const pAvg = (p1 + p2) / 2;
    const effect = Math.abs(p2 - p1);
    
    const n = (
      (2 * pAvg * (1 - pAvg) * Math.pow(zAlpha + zBeta, 2)) /
      Math.pow(effect, 2)
    );
    
    return Math.ceil(n * 2); // Per variant
  }
  
  // Calculate statistical significance
  async calculateSignificance(
    experimentId: UUID
  ): Promise<SignificanceResult> {
    const data = await this.getExperimentData(experimentId);
    
    // Use chi-squared test for conversion rates
    const chiSquare = this.chiSquaredTest(
      data.variantA.conversions,
      data.variantA.samples,
      data.variantB.conversions,
      data.variantB.samples
    );
    
    // Calculate confidence interval
    const p1 = data.variantA.conversions / data.variantA.samples;
    const p2 = data.variantB.conversions / data.variantB.samples;
    const lift = p2 - p1;
    const se = Math.sqrt(
      (p1 * (1 - p1) / data.variantA.samples) +
      (p2 * (1 - p2) / data.variantB.samples)
    );
    
    const ci95 = {
      lower: lift - 1.96 * se,
      upper: lift + 1.96 * se
    };
    
    return {
      pValue: chiSquare.pValue,
      significant: chiSquare.pValue < 0.05,
      confidenceInterval: ci95,
      lift,
      recommendation: this.getRecommendation(chiSquare.pValue, ci95)
    };
  }
}
```

## 8. Compliance Anti-Patterns

### 8.1 Anti-Pattern: Ignoring Unsubscribe Requests

**Vấn đề**: Không process unsubscribes promptly, leading to spam complaints.

```typescript
// ❌ Anti-pattern: Slow unsubscribe processing
class BadUnsubscribeService {
  async processUnsubscribe(email: string): Promise<void> {
    // Just log it somewhere
    await this.logUnsubscribe(email);
    
    // Send confirmation email (wrong!)
    await this.emailService.send({
      to: email,
      subject: 'You have been unsubscribed'
    });
    
    // Maybe remove from list next week...
    // Maybe...
  }
}

// Result:
// - Continued sends to unsubscribe
// - Spam complaints
// - ISP blocks
// - Legal action
```

**Giải pháp**: Immediate, reliable unsubscribe processing.

```typescript
// ✅ Giải pháp: Real-time unsubscribe processing
class ImmediateUnsubscribeService {
  @Process('email.unsubscribe')
  async processUnsubscribe(data: UnsubscribeData): Promise<void> {
    const { email, source, timestamp } = data;
    
    // 1. Immediately add to suppression list
    await this.suppressionList.add(email, {
      reason: 'unsubscribed',
      source,
      timestamp
    });
    
    // 2. Immediately revoke email consent
    await this.consentService.withdrawConsent(email, 'email_marketing', source);
    
    // 3. Immediately cancel ALL pending emails
    await this.emailQueue.cancelPendingForEmail(email);
    
    // 4. Update contact record
    await this.contactRepo.markAsUnsubscribed(email);
    
    // 5. Log for compliance
    await this.auditLog.record({
      action: 'unsubscribe_processed',
      email,
      timestamp,
      latencyMs: Date.now() - new Date(timestamp).getTime()
    });
    
    // 6. Send one-time confirmation (clear, not marketing)
    // Note: Some regulations require this
    await this.sendUnsubscribeConfirmation(email);
  }
  
  // Honor List-Unsubscribe-Post (RFC 8058)
  @Post('/list-unsubscribe/post')
  async handleListUnsubscribePost(
    @Body() body: { email: string; }
  ): Promise<void> {
    // List-Unsubscribe-Post requires simple POST
    // No login required
    await this.processUnsubscribe({
      email: body.email,
      source: 'list_unsubscribe_post',
      timestamp: new Date()
    });
    
    return { success: true };
  }
}
```

### 8.2 Anti-Pattern: Poor Data Security

**Vấn đề**: Không protect contact data properly.

```typescript
// ❌ Anti-pattern: No data protection
class InsecureDataService {
  async getContact(id: string): Promise<Contact> {
    // Returns all data including PII
    // No encryption
    // No access control
    // No audit logging
    
    return this.db.query('SELECT * FROM contacts WHERE id = $1', [id]);
  }
  
  async exportAllContacts(): Promise<string> {
    // CSV with all fields including PII
    // No encryption
    // No access logging
    
    return this.generateCSV(await this.db.query('SELECT * FROM contacts'));
  }
}
```

**Giải pháp**: Security-first data handling.

```typescript
// ✅ Giải pháp: Security-first approach
class SecureDataService {
  constructor(
    private encryptionService: EncryptionService,
    private accessControl: AccessControlService,
    private auditLog: AuditLogService
  ) {}
  
  async getContact(
    id: string,
    requestingUser: User
  ): Promise<Contact> {
    // Check access permissions
    const hasAccess = await this.accessControl.canAccess(
      requestingUser,
      'contact',
      id
    );
    
    if (!hasAccess) {
      throw new AccessDeniedError();
    }
    
    // Log access
    await this.auditLog.record({
      action: 'contact_accessed',
      userId: requestingUser.id,
      resourceId: id,
      timestamp: new Date()
    });
    
    const contact = await this.db.query(
      'SELECT * FROM contacts WHERE id = $1',
      [id]
    );
    
    // Mask sensitive fields based on permissions
    if (!requestingUser.permissions.includes('view_pii')) {
      return this.maskSensitiveFields(contact);
    }
    
    return contact;
  }
  
  async exportContacts(
    request: ExportRequest,
    requestingUser: User
  ): Promise<SecureExport> {
    // Check export permissions
    if (!requestingUser.permissions.includes('export_contacts')) {
      throw new PermissionDeniedError();
    }
    
    // Get contacts based on request criteria
    const contacts = await this.queryContacts(request.criteria);
    
    // Apply field restrictions
    const exportableFields = this.getExportableFields(
      requestingUser.permissions
    );
    
    // Encrypt export
    const encryptedData = await this.encryptionService.encrypt(
      JSON.stringify({
        contacts: contacts.map(c => this.pickFields(c, exportableFields)),
        exportedAt: new Date(),
        exportedBy: requestingUser.id
      })
    );
    
    // Log export
    await this.auditLog.record({
      action: 'contact_export',
      userId: requestingUser.id,
      recordCount: contacts.length,
      fields: exportableFields,
      timestamp: new Date()
    });
    
    // Schedule auto-delete
    const expiryUrl = await this.createExpiryLink(encryptedData);
    
    return {
      downloadUrl: expiryUrl,
      expiresAt: addHours(new Date(), 24),
      recordCount: contacts.length
    };
  }
}
```

---

## 9. marketingskills Anti-Patterns (sync 2026-07-15)

> Top failure modes cho 9 category từ [marketingskills](https://github.com/coreyhaines31/marketingskills). Mỗi section nêu symptom, root cause, fix.

### 9.1 Conversion Optimization Anti-Patterns

**9.1.1 Optimizing form fields instead of motivation**
- **Symptom**: A/B testing input length, button color, microcopy → +0.5% conversion
- **Root cause**: Visitor motivation is the limiting factor, not UX friction
- **Fix**: Rework the offer/value prop FIRST; then optimize friction

**9.1.2 Pre-filling form fields to "help" users**
- **Symptom**: Smart-defaults reduces field count; conversion drops
- **Root cause**: Pre-fills often wrong; users don't notice; submission produces bad data
- **Fix**: Use only canonical defaults (country = user's locale); never pre-fill personal data

**9.1.3 Welcome email drip fired before user is "ready"**
- **Symptom**: Welcome Day-1 open rate < 10%, unsubscribes spike
- **Root cause**: User just signed up; overwhelmed by immediate asks
- **Fix**: Send welcome → wait for activation event → then drip value

**9.1.4 Exit-intent popup on every page**
- **Symptom**: Popup CTR high, capture rate low, brand feels spammy
- **Root cause**: Popups interrupt intent; on every page is over-rotation
- **Fix**: Show on high-intent pages only (pricing, blog end); cap at 1/visit; dismissible

**9.1.5 Skipping onboarding → "figure it out yourself" product**
- **Symptom**: Trial-to-paid conversion < 5%; day-1 activation < 30%
- **Root cause**: No guided path; users never reach aha moment
- **Fix**: 3-step activation checklist with progress bar; empty states that teach

### 9.2 Content & Copy Anti-Patterns

**9.2.1 Subject line: RE:Viagra at scale**
- **Symptom**: High open rate from curiosity, no clicks, spam complaints
- **Root cause**: Misleading subject drives opens, not engagement
- **Fix**: A/B subject lines by genuine angle, not tricks; aim for > 10% click rate

**9.2.2 Send-everyone-the-same-email blast**
- **Symptom**: Mass unsubscribes after every newsletter
- **Root cause**: One-size-fits-all content doesn't respect segment interests
- **Fix**: Segment by behavior, role, stage; personalize hero + CTA

**9.2.3 Long-form copy without structure**
- **Symptom**: Skim depth 30%, bounce rate high
- **Root cause**: Wall of text with no scannable hierarchy
- **Fix**: Bullet-3-then-elaborate, subheadings every 200 words, bold key phrases

**9.2.4 Cold-email copy-paste with first name only**
- **Symptom**: Reply rate < 1%, hard bounces increasing
- **Root cause**: One variable token doesn't make email relevant
- **Fix**: Reference trigger event (new funding, hiring, blog post) in 1 sentence

**9.2.5 Sending SMS without opt-in**
- **Symptom**: TCPA/text-law complaints, fines ($500-$1500/message in US)
- **Root cause**: Marketing uses business phone numbers without consent
- **Fix**: Double opt-in for SMS; clear opt-out language; honor STOP within 1 minute

**9.2.6 Image generation: random surreal visuals**
- **Symptom**: Brand incoherence, low engagement on social
- **Root cause**: AI image gen without brand style guide
- **Fix**: Style reference (3-5 brand adjectives), negative prompts, human review

### 9.3 SEO & Discovery Anti-Patterns

**9.3.1 "Just write more content" with no keyword strategy**
- **Symptom**: 200+ blog posts, organic traffic flat
- **Root cause**: Volume without search-intent targeting = zero ranking gains
- **Fix**: Keyword research first, cluster by topic, internal-link to pillar page

**9.3.2 Programmatic SEO = spam**
- **Symptom**: 10k pages indexed, manual action from Google, traffic drops to 0
- **Root cause**: Thin content, no unique value per page, doorway intent
- **Fix**: Add unique data per page (real examples, original research); human-quality bar

**9.3.3 llms.txt copied from competitor**
- **Symptom**: AI search engines cite competitor content
- **Root cause**: Generic / non-specific to your product
- **Fix**: Write to YOUR product/audience; include unique data points

**9.3.4 Schema dump: marking up everything wrong**
- **Symptom**: Manual action for spammy structured data
- **Root cause**: FAQPage with non-questions; Product without offers; irrelevant markup
- **Fix**: Match schema.org spec exactly; validate with Rich Results Test

**9.3.5 Site architecture: 4-level deep URLs**
- **Symptom**: Crawl budget wasted; low ranking on long-tail
- **Root cause**: Categorical depth > 3; every click costs crawl budget
- **Fix**: Flatten to /[category]/[page]; max 3 URL levels; breadcrumbs as nav

**9.3.6 ASO: keyword stuffing title**
- **Symptom**: App store rejects; rank drops after update
- **Root cause**: Title + keyword field same words = spam
- **Fix**: Title (brand + 1-2 key terms); subtitle for 2-3 more; keyword field for remaining

### 9.4 Paid & Distribution Anti-Patterns

**9.4.1 Launching ads with no conversion event tracked**
- **Symptom**: Spend $5k, "conversions" show but no qualified leads
- **Root cause**: Optimizing for micro-conversions (page view) instead of macro
- **Fix**: Track qualified lead, signup, sale — whichever maps to LTV

**9.4.2 Ad creative fatigue: same ad for 30+ days**
- **Symptom**: CTR drops 50% over month; CPM increases
- **Root cause**: Audience sees same creative, ignores
- **Fix**: Rotate creative every 7-14 days; build 3-5 ad variants upfront

**9.4.3 "Set and forget" retargeting**
- **Symptom**: Retargeting list of 50k people, conversion 0.1%
- **Root cause**: Audience stale; products/prices changed; no creative refresh
- **Fix**: Refresh audience every 30 days; cap audience size; exclude converters

**9.4.4 Scaling winners before profitability validated**
- **Symptom**: CPA doubles as spend scales; LTV/CAC < 1
- **Root cause**: Optimizing platform-side (ROAS 3) but blended ROAS < 1
- **Fix**: Verify LTV/CAC > 3 before scale; reserve 20% budget for new tests

### 9.5 Measurement & Testing Anti-Patterns

**9.5.1 "Test everything"**
- **Symptom**: 50+ running tests, none reach significance, results noise
- **Root cause**: Underpowered tests, multiple comparisons
- **Fix**: Max 3 concurrent tests per page; require MDE + sample size calc

**9.5.2 Stopping tests at first significance**
- **Symptom**: Ship a "winning" variant that reverts over time
- **Root cause**: Peeking; p < 0.05 is not the same as confirmed effect
- **Fix**: Pre-register duration; use sequential testing or full sample size

**9.5.3 Tracking vanity metrics**
- **Symptom**: Page views up 30%, revenue flat
- **Root cause**: Optimizing for traffic, not pipeline or revenue
- **Fix**: North-star metric: weekly active + revenue per active

**9.5.4 Mixing attribution across events**
- **Symptom**: Channel A "credited" 3x for one conversion
- **Root cause**: Multiple events trigger conversion; double-count
- **Fix**: One canonical conversion event; deduplicate by user+session

### 9.6 Retention Anti-Patterns

**9.6.1 Dunning from day 0 of failed payment**
- **Symptom**: Cancellation rate spikes; complaints about aggressive
- **Root cause**: Most failures are temporary (insufficient funds, expired card)
- **Fix**: Wait 3 days after first failure; retry with smart backoff

**9.6.2 Save offer = free 1 year**
- **Symptom**: Users learn to ask for 100% off; gross margin collapses
- **Root cause**: Single-skill save flow with no segmentation
- **Fix**: Tiered save (10% / 25% / 50% / downgrade) by churn reason

**9.6.3 Pause subscription without usage tracking**
- **Symptom**: User pauses, never returns; resurrected count 0
- **Root cause**: Pause = hidden cancel; no re-engagement
- **Fix**: Pause = 30/60/90 day cap; re-engage at 50% of pause window

### 9.7 Growth Engineering Anti-Patterns

**9.7.1 Free tool = thinly-veiled landing page**
- **Symptom**: Tool ranks #1, but converts 0% to product
- **Root cause**: Tool doesn't deliver value, just collects email
- **Fix**: Solve real problem; reveal product as natural next step (not forced)

**9.7.2 Referral program without fraud guardrails**
- **Symptom**: 30% of referrals are fraud (same IP, device, family)
- **Root cause**: No matching engine; reward per email
- **Fix**: Match by device fingerprint + payment method + IP; review top referrers

**9.7.3 Co-marketing with non-overlapping ICP**
- **Symptom**: Joint webinar, 100 attendees, 0 leads
- **Root cause**: Audience mismatch; one side dominates
- **Fix**: ICP overlap test; co-marketing with 3-5x audience overlap wins

### 9.8 Strategy & Monetization Anti-Patterns

**9.8.1 Pricing page with 5 plans**
- **Symptom**: Decision paralysis; most pick middle or no-plan
- **Root cause**: Choice overload; no clear "default"
- **Fix**: 3 plans (good/better/best); highlight middle as recommended

**9.8.2 Launch with no waitlist**
- **Symptom**: Day 1 traffic spike, then fade; momentum lost
- **Root cause**: No pre-built audience; product hunt alone insufficient
- **Fix**: 4-6 week pre-launch; waitlist; email warm-up; ambassador seeding

**9.8.3 Offer with no clear guarantee**
- **Symptom**: Conversion 1%, refund rate 5%
- **Root cause**: Risk on buyer; high-intent users drop off
- **Fix**: Risk-reversal (30-day money back, no-questions); visible CTA

**9.8.4 Yearly plan: "save 17%" off monthly x 12**
- **Symptom**: Annual take rate < 10%
- **Root cause**: Math doesn't trigger; user values cash flow
- **Fix**: Position annual as "2 months free" or "X% off, paid upfront"

### 9.9 Sales & RevOps Anti-Patterns

**9.9.1 Lead scoring: only form-fill weight**
- **Symptom**: MQL volume huge, SQL conversion 1%
- **Root cause**: Form fills ≠ intent; self-reported intent ≠ behavior
- **Fix**: Combine behavior (visit pricing, request demo) with form data

**9.9.2 Routing by territory, not expertise**
- **Symptom**: Mid-market leads routed to SMB reps; close rate low
- **Root cause**: Territory > fit; reps unfamiliar with segment
- **Fix**: Route by segment + product fit; territory only as tie-breaker

**9.9.3 Sales enablement: deck for every stage, none used**
- **Symptom**: Reps create own decks; brand incoherence; off-message
- **Root cause**: Decks not stage-aware; don't map to discovery
- **Fix**: Stage-aware collateral; track usage; retire unused

**9.9.4 Pitching features, not outcomes**
- **Symptom**: Demo shows all 47 features, no qualified pipeline
- **Root cause**: Feature tour ≠ value articulation
- **Fix**: Frame features as outcomes (e.g., "Reduce churn 20% via __")

**9.9.5 Cold outreach: blast to whole role**
- **Symptom**: 1k emails/week, 3 replies, 0 deals
- **Root cause**: Targeting by job title only; no trigger events
- **Fix**: Layer intent signals (hiring, funding, blog) on top of role

**9.9.6 PR pitching: untargeted blast**
- **Symptom**: 0 coverage, journalist unsubscribes
- **Root cause**: Pitching wrong beat; press release vs. story
- **Fix**: Research journalist's recent articles; pitch angle that fits

**9.9.7 Customer research: only "power users"**
- **Symptom**: Insights biased toward existing fans
- **Root cause**: Sampling bias; missing pain points of churned users
- **Fix**: Mix of activated, churned, never-activated; tier sample by segment

**9.9.8 Marketing council without context**
- **Symptom**: Brainstorm outputs generic ("be more authentic")
- **Root cause**: Personas lack product/audience context
- **Fix**: Pass product-marketing context (see glossary §13) to each persona

**9.9.9 Marketing loops: hard-coded assumptions**
- **Symptom**: Outreach loop sends stale templates forever
- **Root cause**: Loop has no feedback mechanism or refresh
- **Fix**: Loop reads current data; refreshes weekly; abort on quality drop

**9.9.10 Directory spam: 100 submissions in 1 day**
- **Symptom**: Some directories flag; profile rejected
- **Root cause**: Mass submission triggers spam detection
- **Fix**: 1-2 submissions/week; quality bar (full profile, screenshot, link)
