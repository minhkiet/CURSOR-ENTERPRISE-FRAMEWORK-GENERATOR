# Marketing Architecture - Kiến Trúc Hệ Thống Marketing Automation

## 1. Tổng Quan Kiến Trúc Marketing

### 1.1 Mục Tiêu và Nguyên Tắc Thiết Kế

Hệ thống Marketing Automation Platform (MAP) được thiết kế để quản lý, tự động hóa và tối ưu hóa mọi tương tác với khách hàng tiềm năng và khách hàng hiện tại. Kiến trúc hướng tới các mục tiêu chính: khả năng mở rộng để xử lý hàng triệu contacts và hàng tỷ events mỗi ngày, độ trễ thấp cho real-time personalization, và tính linh hoạt cao để adapt với các chiến lược marketing thay đổi.

Nguyên tắc thiết kế cốt lõi bao gồm event-driven architecture cho real-time processing, separation of concerns giữa campaigns, journeys và execution engine, extensibility qua plugin architecture cho custom integrations, và data-driven decision making với comprehensive analytics.

### 1.2 High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           MARKETING AUTOMATION PLATFORM                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────┐    ┌────────────────┐    ┌────────────────┐              │
│  │   Campaign     │    │   Journey      │    │   Analytics    │              │
│  │   Manager      │    │   Builder      │    │   Engine       │              │
│  └───────┬────────┘    └───────┬────────┘    └───────┬────────┘              │
│          │                      │                      │                      │
│          └──────────────────────┼──────────────────────┘                      │
│                                 │                                             │
│                          ┌──────▼──────┐                                      │
│                          │   Journey   │                                      │
│                          │   Executor  │                                      │
│                          │   Engine    │                                      │
│                          └──────┬──────┘                                      │
│                                 │                                             │
│  ┌─────────────────────────────┼─────────────────────────────────────────┐  │
│  │                    EXECUTION LAYER                                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                │  │
│  │  │  Email   │  │   SMS    │  │  Push    │  │   Ads    │                │  │
│  │  │  Engine  │  │  Engine  │  │  Engine  │  │  Engine  │                │  │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘                │  │
│  │       │              │              │              │                      │  │
│  │       └──────────────┴──────────────┴──────────────┘                      │  │
│  │                              │                                            │  │
│  │                    ┌─────────▼─────────┐                                  │  │
│  │                    │  Message Queue    │                                  │  │
│  │                    │  (Kafka/Redis)    │                                  │  │
│  │                    └─────────┬─────────┘                                  │  │
│  └─────────────────────────────┼───────────────────────────────────────────┘  │
│                                │                                               │
│  ┌─────────────────────────────┼───────────────────────────────────────────┐ │
│  │                    DATA LAYER                                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                │ │
│  │  │Contact DB │  │Event Store│  │ Campaign │  │ Journey  │                │ │
│  │  │(Postgres)│  │ (Kafka)  │  │   Store  │  │   Store  │                │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘                │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 2. Core Domain Architecture

### 2.1 Contact Management Domain

#### 2.1.1 Contact Entity Model

Contact là aggregate root của toàn bộ hệ thống marketing. Mỗi contact đại diện cho một cá nhân có thể được theo dõi và tương tác qua các marketing channels.

```typescript
interface Contact {
  id: UUID;
  
  // Core identification
  email: string;
  phone?: string;
  
  // Profile data
  profile: ContactProfile;
  demographics: Demographics;
  company?: CompanyInfo;
  
  // Preferences
  communicationPreferences: CommunicationPreferences;
  consentRecords: ConsentRecord[];
  
  // Segmentation
  segments: string[];
  tags: string[];
  
  // Scoring
  engagementScore: number;
  leadScore: number;
  
  // Lifecycle
  lifecycleStage: LifecycleStage;
  acquisitionSource?: string;
  acquisitionDate?: Date;
  
  // Activity tracking
  lastActivityAt?: Date;
  lastEmailAt?: Date;
  lastClickAt?: Date;
  
  // Metadata
  customFields: Record<string, CustomFieldValue>;
  
  createdAt: Date;
  updatedAt: Date;
  version: number;
}

interface ContactProfile {
  firstName?: string;
  lastName?: string;
  fullName?: string;
  title?: string;
  department?: string;
  avatar?: string;
  dateOfBirth?: Date;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  language: string;
  timezone: string;
}

interface CompanyInfo {
  name: string;
  industry?: string;
  size?: '1-10' | '11-50' | '51-200' | '201-500' | '501-1000' | '1000+';
  revenue?: string;
  website?: string;
  linkedInUrl?: string;
  country?: string;
  city?: string;
}
```

#### 2.1.2 Contact Consent Management

Consent management là critical compliance requirement, đặc biệt với GDPR và CCPA.

```typescript
interface ConsentRecord {
  id: UUID;
  contactId: UUID;
  consentType: ConsentType;
  source: ConsentSource;
  grantedAt: Date;
  ipAddress?: string;
  userAgent?: string;
  proof?: string; // URL to consent record
  withdrawnAt?: Date;
  withdrawnSource?: ConsentSource;
}

type ConsentType = 
  | 'email_marketing'
  | 'sms_marketing'
  | 'push_notifications'
  | 'personalization'
  | 'third_party_sharing'
  | 'profiling';

interface ConsentPreferences {
  canEmail: boolean;
  canSms: boolean;
  canPush: boolean;
  canTrack: boolean;
  canShare: boolean;
  preferences: {
    [key: string]: boolean;
  };
}

class ConsentService {
  async grantConsent(
    contactId: UUID,
    consentType: ConsentType,
    source: ConsentSource
  ): Promise<ConsentRecord> {
    // Verify no existing consent withdrawal
    const existingWithdrawal = await this.consentRepo.findWithdrawal(
      contactId, 
      consentType
    );
    
    if (existingWithdrawal) {
      throw new ConsentPreviouslyWithdrawnError(consentType);
    }
    
    const record = ConsentRecord.create({
      contactId,
      consentType,
      source,
      grantedAt: new Date()
    });
    
    await this.consentRepo.save(record);
    await this.eventPublisher.publish(
      new ConsentGrantedEvent(contactId, consentType)
    );
    
    return record;
  }
  
  async withdrawConsent(
    contactId: UUID,
    consentType: ConsentType,
    source: ConsentSource
  ): Promise<void> {
    const record = ConsentRecord.createWithdrawal({
      contactId,
      consentType,
      source,
      withdrawnAt: new Date()
    });
    
    await this.consentRepo.save(record);
    
    // Immediately stop all pending communications
    await this.preferenceService.updatePreference(
      contactId,
      consentType,
      false
    );
    
    await this.eventPublisher.publish(
      new ConsentWithdrawnEvent(contactId, consentType)
    );
  }
  
  async canCommunicate(
    contactId: UUID,
    channel: 'email' | 'sms' | 'push'
  ): Promise<boolean> {
    const contact = await this.contactRepo.findById(contactId);
    const consentType = this.channelToConsentType(channel);
    
    return contact.consentRecords.some(
      c => c.consentType === consentType && !c.withdrawnAt
    );
  }
}
```

### 2.2 Campaign Domain

#### 2.2.1 Campaign Structure

Campaign là container cho các marketing initiatives, chứa settings, targeting criteria và associated journeys.

```typescript
interface Campaign {
  id: UUID;
  name: string;
  description?: string;
  
  // Campaign type and status
  type: CampaignType;
  status: CampaignStatus;
  
  // Timing
  scheduledStartAt?: Date;
  scheduledEndAt?: Date;
  actualStartAt?: Date;
  actualEndAt?: Date;
  
  // Targeting
  targetAudience: TargetAudience;
  suppressionList?: UUID[];
  
  // Budget and goals
  budget?: Money;
  goals: CampaignGoals;
  
  // Channels
  channels: Channel[];
  
  // Settings
  settings: CampaignSettings;
  
  // Tracking
  metrics: CampaignMetrics;
  
  // Metadata
  createdBy: UUID;
  createdAt: Date;
  updatedAt: Date;
}

type CampaignType = 
  | 'email'
  | 'sms'
  | 'push'
  | 'social'
  | 'paid_ads'
  | 'multi_channel'
  | 'event'
  | 'webinar'
  | 'loyalty';

type CampaignStatus = 
  | 'draft'
  | 'scheduled'
  | 'running'
  | 'paused'
  | 'completed'
  | 'archived';

interface CampaignGoals {
  targetContacts: number;
  targetReachRate: number; // percentage
  targetOpenRate: number;
  targetClickRate: number;
  targetConversionRate: number;
  targetRevenue?: Money;
}

interface CampaignSettings {
  trackOpens: boolean;
  trackClicks: boolean;
  trackConversions: boolean;
  suppressInactive: boolean;
  inactiveThresholdDays: number;
  allowDuplicateComms: boolean;
  frequencyCapping?: number; // Max messages per contact per period
  sendTimeOptimization: boolean;
}
```

#### 2.2.2 Campaign Workflow

```typescript
// Campaign state machine
const campaignStateMachine = {
  draft: {
    on: {
      SCHEDULE: 'scheduled',
      LAUNCH: 'running',
      ARCHIVE: 'archived'
    }
  },
  scheduled: {
    on: {
      LAUNCH: 'running',
      CANCEL: 'draft',
      ARCHIVE: 'archived'
    }
  },
  running: {
    on: {
      PAUSE: 'paused',
      COMPLETE: 'completed',
      ARCHIVE: 'archived'
    }
  },
  paused: {
    on: {
      RESUME: 'running',
      COMPLETE: 'completed',
      ARCHIVE: 'archived'
    }
  },
  completed: {
    on: {
      REACTIVATE: 'draft',
      ARCHIVE: 'archived'
    }
  }
};

class CampaignService {
  private stateMachine = campaignStateMachine;
  
  async transitionStatus(
    campaignId: UUID,
    newStatus: CampaignStatus
  ): Promise<Campaign> {
    const campaign = await this.campaignRepo.findById(campaignId);
    
    const allowedTransitions = this.stateMachine[campaign.status]?.on;
    if (!allowedTransitions?.[newStatus]) {
      throw new InvalidCampaignTransitionError(
        campaign.status,
        newStatus
      );
    }
    
    // Execute transition hooks
    await this.executeTransitionHooks(campaign, newStatus);
    
    campaign.status = newStatus;
    if (newStatus === 'running' && !campaign.actualStartAt) {
      campaign.actualStartAt = new Date();
    }
    
    await this.campaignRepo.save(campaign);
    
    return campaign;
  }
  
  private async executeTransitionHooks(
    campaign: Campaign,
    newStatus: CampaignStatus
  ): Promise<void> {
    switch (newStatus) {
      case 'running':
        await this.journeyExecutor.startCampaignJourneys(campaign.id);
        await this.analyticsService.initializeCampaignMetrics(campaign.id);
        break;
      case 'paused':
        await this.journeyExecutor.pauseCampaignJourneys(campaign.id);
        break;
      case 'completed':
        await this.journeyExecutor.stopCampaignJourneys(campaign.id);
        await this.analyticsService.finalizeCampaignMetrics(campaign.id);
        break;
    }
  }
}
```

### 2.3 Journey Builder Domain

#### 2.3.1 Journey Architecture

Journey là sequence of actions được executed cho mỗi contact khi họ enter vào journey. Journey builder cho phép marketers design flows không cần code.

```typescript
interface Journey {
  id: UUID;
  campaignId?: UUID;
  name: string;
  description?: string;
  
  // Journey structure
  entryTrigger: JourneyTrigger;
  nodes: JourneyNode[];
  edges: JourneyEdge[];
  
  // Settings
  settings: JourneySettings;
  
  // Metrics
  stats: JourneyStats;
  
  status: JourneyStatus;
  createdAt: Date;
  updatedAt: Date;
}

// Trigger types
interface JourneyTrigger {
  type: TriggerType;
  config: TriggerConfig;
}

type TriggerType = 
  | 'contact_created'
  | 'segment_entered'
  | 'form_submitted'
  | 'email_opened'
  | 'email_clicked'
  | 'page_visited'
  | 'purchase_made'
  | 'inactivity'
  | 'manual'
  | 'api';

interface TriggerConfig {
  // For segment_entered
  segmentId?: UUID;
  
  // For form_submitted
  formId?: UUID;
  
  // For inactivity
  inactivityDays?: number;
  inactivityScope?: 'any_activity' | 'email_activity' | 'website_activity';
  
  // For page_visited
  pageUrl?: string;
  urlContains?: string;
}

// Node types
type JourneyNode = 
  | ActionNode
  | ConditionNode
  | DelayNode
  | WaitNode
  | SplitterNode
  | GoalNode;

interface ActionNode {
  type: 'action';
  id: string;
  position: { x: number; y: number };
  actionType: ActionType;
  config: ActionConfig;
}

type ActionType = 
  | 'send_email'
  | 'send_sms'
  | 'send_push'
  | 'add_to_segment'
  | 'remove_from_segment'
  | 'update_field'
  | 'assign_owner'
  | 'create_task'
  | 'webhook'
  | 'ai_content_generation';

interface ConditionNode {
  type: 'condition';
  id: string;
  position: { x: number; y: number };
  condition: Condition;
}

interface Condition {
  operator: 'and' | 'or';
  rules: ConditionRule[];
}

interface ConditionRule {
  field: string;
  operator: 'equals' | 'not_equals' | 'contains' | 'greater_than' | 'less_than' | 'is_empty' | 'is_not_empty';
  value: any;
}

interface DelayNode {
  type: 'delay';
  id: string;
  position: { x: number; y: number };
  delay: {
    type: 'immediate' | 'wait_duration' | 'wait_until' | 'send_best_time';
    duration?: number; // minutes
    unit?: 'minutes' | 'hours' | 'days' | 'weeks';
    specificTime?: string; // HH:mm
    timezone?: string;
  };
}

interface GoalNode {
  type: 'goal';
  id: string;
  position: { x: number; y: number };
  goalType: 'conversion' | 'engagement' | 'revenue';
  config: GoalConfig;
}

// Journey execution
interface JourneyInstance {
  id: UUID;
  journeyId: UUID;
  contactId: UUID;
  
  // Current state
  currentNodeId: string;
  nodeHistory: NodeExecutionRecord[];
  
  // Timing
  enteredAt: Date;
  lastActivityAt: Date;
  exitedAt?: Date;
  exitReason?: ExitReason;
  
  // Variables
  variables: Record<string, any>;
}

interface NodeExecutionRecord {
  nodeId: string;
  enteredAt: Date;
  exitedAt?: Date;
  status: 'pending' | 'completed' | 'failed' | 'skipped';
  output?: any;
  error?: string;
}
```

#### 2.3.2 Journey Executor

Journey Executor là engine xử lý journey logic, đọc journey definition và execute nodes cho mỗi contact.

```typescript
class JourneyExecutor {
  constructor(
    private journeyRepo: JourneyRepository,
    private contactRepo: ContactRepository,
    private nodeExecutors: Map<ActionType, NodeExecutor>,
    private eventStore: EventStore,
    private messageQueue: MessageQueue
  ) {}
  
  async executeNode(
    instance: JourneyInstance,
    node: JourneyNode
  ): Promise<NodeExecutionResult> {
    const record: NodeExecutionRecord = {
      nodeId: node.id,
      enteredAt: new Date(),
      status: 'pending'
    };
    
    try {
      const executor = this.getExecutorForNode(node);
      const result = await executor.execute(instance, node);
      
      record.status = 'completed';
      record.output = result;
      record.exitedAt = new Date();
      
      // Determine next node(s)
      const nextNodes = this.getNextNodes(instance.journeyId, node.id, result);
      instance.currentNodeId = nextNodes[0]?.id;
      
      // Schedule delayed nodes if needed
      for (const nextNode of nextNodes) {
        if (nextNode.type === 'delay') {
          await this.scheduleDelayedExecution(instance, nextNode);
        } else {
          // Execute immediately
          await this.messageQueue.publish(
            'journey.node.execute',
            { instanceId: instance.id, nodeId: nextNode.id }
          );
        }
      }
      
    } catch (error) {
      record.status = 'failed';
      record.error = error.message;
      record.exitedAt = new Date();
      
      // Handle error based on journey settings
      const journey = await this.journeyRepo.findById(instance.journeyId);
      if (journey.settings.stopOnError) {
        instance.exitReason = 'error';
        instance.exitedAt = new Date();
      }
    }
    
    // Update instance
    instance.nodeHistory.push(record);
    instance.lastActivityAt = new Date();
    await this.journeyInstanceRepo.save(instance);
    
    return record;
  }
  
  private getExecutorForNode(node: JourneyNode): NodeExecutor {
    switch (node.type) {
      case 'action':
        return this.nodeExecutors.get(node.actionType)!;
      case 'condition':
        return this.conditionNodeExecutor;
      case 'delay':
        return this.delayNodeExecutor;
      case 'goal':
        return this.goalNodeExecutor;
      default:
        throw new UnknownNodeTypeError(node.type);
    }
  }
}

// Example: Email action executor
class SendEmailExecutor implements NodeExecutor {
  constructor(
    private emailService: EmailService,
    private contactRepo: ContactRepository,
    private consentService: ConsentService
  ) {}
  
  async execute(
    instance: JourneyInstance,
    node: ActionNode
  ): Promise<SendEmailResult> {
    const { emailTemplateId, subjectOverride } = node.config;
    
    // Check consent
    const canEmail = await this.consentService.canCommunicate(
      instance.contactId,
      'email'
    );
    
    if (!canEmail) {
      return {
        success: false,
        reason: 'consent_not_granted'
      };
    }
    
    // Check frequency capping
    const recentEmails = await this.emailService.getRecentEmailCount(
      instance.contactId,
      node.config.frequencyCapPeriod
    );
    
    if (recentEmails >= node.config.frequencyCap) {
      return {
        success: false,
        reason: 'frequency_capped'
      };
    }
    
    // Get contact
    const contact = await this.contactRepo.findById(instance.contactId);
    
    // Personalize content
    const email = await this.emailService.createPersonalizedEmail({
      templateId: emailTemplateId,
      contact,
      subjectOverride,
      variables: instance.variables
    });
    
    // Send
    await this.emailService.send({
      to: contact.email,
      ...email
    });
    
    // Publish event
    await this.eventStore.append({
      type: 'email.sent',
      contactId: instance.contactId,
      journeyId: instance.journeyId,
      emailId: email.id,
      timestamp: new Date()
    });
    
    return {
      success: true,
      emailId: email.id
    };
  }
}
```

### 2.4 Personalization Engine

#### 2.4.1 Personalization Architecture

Personalization Engine xử lý dynamic content insertion dựa trên contact data, behavior và context.

```typescript
interface PersonalizationContext {
  contact: Contact;
  journey?: JourneyInstance;
  campaign?: Campaign;
  contentSlot: string;
  timestamp: Date;
  deviceType?: 'desktop' | 'mobile' | 'tablet';
  referringUrl?: string;
}

interface PersonalizationRule {
  id: UUID;
  name: string;
  priority: number;
  condition?: Condition;
  content: PersonalizationContent;
  defaultContent?: string;
}

type PersonalizationContent = 
  | { type: 'text'; value: string }
  | { type: 'image'; url: string; alt?: string }
  | { type: 'html'; value: string }
  | { type: 'offer'; offerId: UUID };

class PersonalizationEngine {
  constructor(
    private ruleRepo: RuleRepository,
    private contentRepo: ContentRepository,
    private aiService?: AIGenerationService
  ) {}
  
  async personalize(
    template: string,
    context: PersonalizationContext
  ): Promise<string> {
    let result = template;
    
    // 1. Handle dynamic fields {{contact.firstName}}
    result = await this.personalizeDynamicFields(result, context);
    
    // 2. Handle conditional content {% if %}
    result = await this.personalizeConditionals(result, context);
    
    // 3. Handle personalization rules
    result = await this.personalizeRules(result, context);
    
    // 4. Handle AI-generated content {{ai:prompt}}
    if (this.aiService) {
      result = await this.personalizeWithAI(result, context);
    }
    
    return result;
  }
  
  private async personalizeDynamicFields(
    template: string,
    context: PersonalizationContext
  ): Promise<string> {
    const fieldPattern = /\{\{([^}]+)\}\}/g;
    
    return template.replace(fieldPattern, (match, path) => {
      const value = this.getNestedValue(context, path.trim());
      return value ?? match;
    });
  }
  
  private async personalizeConditionals(
    template: string,
    context: PersonalizationContext
  ): Promise<string> {
    const conditionalPattern = /\{%\s*if\s+([^}]+)\s*%\}([\s\S]*?)\{%\s*endif\s*%\}/g;
    
    return template.replace(conditionalPattern, (match, condition, content) => {
      const result = this.evaluateCondition(condition, context);
      return result ? content : '';
    });
  }
  
  private async personalizeRules(
    template: string,
    context: PersonalizationContext
  ): Promise<string> {
    const rules = await this.ruleRepo.findByContentSlot(
      context.contentSlot
    );
    
    for (const rule of rules.sort((a, b) => b.priority - a.priority)) {
      if (!rule.condition || this.evaluateCondition(rule.condition, context)) {
        if (rule.content.type === 'text') {
          return template.replace(
            `{{slot:${context.contentSlot}}}`,
            rule.content.value
          );
        }
      }
    }
    
    return template;
  }
  
  private async personalizeWithAI(
    template: string,
    context: PersonalizationContext
  ): Promise<string> {
    const aiPattern = /\{\{ai:([^}]+)\}\}/g;
    
    return template.replace(aiPattern, async (match, prompt) => {
      try {
        const personalizedPrompt = this.personalizeDynamicFields(
          prompt,
          context
        );
        
        const generated = await this.aiService.generate({
          prompt: personalizedPrompt,
          context: {
            contactProfile: context.contact.profile,
            recentActivity: await this.getRecentActivity(context.contact.id)
          }
        });
        
        return generated;
      } catch (error) {
        logger.error('AI personalization failed', { error, prompt });
        return match; // Keep original if AI fails
      }
    });
  }
}
```

## 3. Multi-Channel Execution Architecture

### 3.1 Channel Abstraction Layer

Channel abstraction layer cung cấp unified interface cho các channels khác nhau.

```typescript
interface MarketingChannel {
  readonly type: ChannelType;
  
  // Capabilities
  capabilities: ChannelCapabilities;
  
  // Send methods
  send(message: ChannelMessage): Promise<SendResult>;
  validateRecipient(recipient: Contact): ValidationResult;
  
  // Tracking
  registerWebhook(router: Router): void;
  
  // Metrics
  getChannelMetrics(timeRange: TimeRange): ChannelMetrics;
}

interface ChannelCapabilities {
  supportsHTML: boolean;
  supportsPlainText: boolean;
  supportsTemplates: boolean;
  maxContentSize: number; // bytes
  requiresConsent: boolean;
  characterLimit?: number;
}

interface ChannelMessage {
  contactId: UUID;
  campaignId?: UUID;
  subject?: string;
  content: MessageContent;
  metadata?: Record<string, any>;
}

interface MessageContent {
  html?: string;
  text?: string;
  templateId?: UUID;
  variables?: Record<string, any>;
}

// Email channel implementation
class EmailChannel implements MarketingChannel {
  readonly type: 'email' = 'email';
  
  constructor(
    private emailProvider: EmailProvider,
    private templateRepo: TemplateRepository,
    private trackingService: EmailTrackingService
  ) {}
  
  async send(message: ChannelMessage): Promise<SendResult> {
    const { contactId, content, subject, metadata } = message;
    
    // Resolve template
    let htmlContent = content.html;
    if (content.templateId) {
      const template = await this.templateRepo.findById(content.templateId);
      htmlContent = await this.templateEngine.render(template, content.variables);
    }
    
    // Track links
    const trackedHtml = await this.trackingService.addTracking(
      htmlContent,
      { contactId, campaignId: metadata?.campaignId }
    );
    
    // Generate tracking pixel
    const trackingId = await this.trackingService.createTrackingId({
      contactId,
      campaignId: metadata?.campaignId,
      type: 'open'
    });
    
    // Send via provider
    const result = await this.emailProvider.send({
      to: metadata?.email,
      subject,
      html: trackedHtml + `<img src="${TRACKING_BASE_URL}/${trackingId}" width="1" height="1"/>`,
      text: content.text,
      metadata: {
        contactId,
        campaignId: metadata?.campaignId,
        messageId: metadata?.messageId
      }
    });
    
    return {
      success: result.accepted,
      messageId: result.messageId,
      providerResponse: result
    };
  }
  
  async validateRecipient(recipient: Contact): Promise<ValidationResult> {
    const errors: string[] = [];
    
    if (!recipient.email) {
      errors.push('Contact does not have an email address');
    } else if (!this.isValidEmail(recipient.email)) {
      errors.push('Invalid email format');
    }
    
    if (recipient.communicationPreferences?.canEmail === false) {
      errors.push('Contact has opted out of email communications');
    }
    
    return {
      valid: errors.length === 0,
      errors
    };
  }
  
  registerWebhook(router: Router): void {
    // Handle bounces
    router.post('/webhooks/email/bounce', async (ctx) => {
      const { email, bounceType, timestamp } = ctx.request.body;
      
      await this.trackingService.recordBounce(email, bounceType, timestamp);
      await this.contactService.markEmailBounced(email, bounceType);
    });
    
    // Handle unsubscribes
    router.post('/webhooks/email/unsub', async (ctx) => {
      const { email } = ctx.request.body;
      
      await this.consentService.withdrawConsent(
        email,
        'email_marketing',
        'unsubscribe_link'
      );
    });
    
    // Handle complaints (Spam)
    router.post('/webhooks/email/complaint', async (ctx) => {
      const { email } = ctx.request.body;
      
      await this.contactService.markAsSpamComplaint(email);
    });
  }
}
```

### 3.2 SMS Channel

```typescript
class SmsChannel implements MarketingChannel {
  readonly type: 'sms' = 'sms';
  
  constructor(
    private smsProvider: SmsProvider,
    private phoneValidator: PhoneValidator
  ) {}
  
  get capabilities(): ChannelCapabilities {
    return {
      supportsHTML: false,
      supportsPlainText: true,
      supportsTemplates: true,
      maxContentSize: 1600, // SMS segment limit
      requiresConsent: true,
      characterLimit: 1600
    };
  }
  
  async send(message: ChannelMessage): Promise<SendResult> {
    const { contactId, content, metadata } = message;
    
    // Validate phone number
    const phone = metadata?.phone as string;
    const validation = this.phoneValidator.validate(phone);
    
    if (!validation.valid) {
      return {
        success: false,
        error: 'Invalid phone number',
        providerResponse: { reason: validation.error }
      };
    }
    
    // Format phone (E.164)
    const formattedPhone = this.phoneValidator.toE164(phone);
    
    // Send
    const result = await this.smsProvider.send({
      to: formattedPhone,
      body: content.text || content.html!, // SMS uses text
      metadata: {
        contactId,
        campaignId: metadata?.campaignId
      }
    });
    
    return {
      success: result.success,
      messageId: result.messageId,
      segments: result.segments
    };
  }
}
```

## 4. Analytics Architecture

### 4.1 Event Collection

Marketing platform thu thập và xử lý hàng tỷ events mỗi ngày. Event collection được thiết kế để handle high-throughput, real-time processing.

```typescript
// Event types
interface MarketingEvent {
  id: UUID;
  type: EventType;
  contactId: UUID;
  timestamp: Date;
  properties: Record<string, any>;
  source: EventSource;
  sessionId?: string;
  userAgent?: string;
  ipAddress?: string;
}

type EventType = 
  | 'email_sent'
  | 'email_delivered'
  | 'email_opened'
  | 'email_clicked'
  | 'email_bounced'
  | 'email_unsubscribed'
  | 'sms_sent'
  | 'sms_delivered'
  | 'sms_clicked'
  | 'webpage_visited'
  | 'form_submitted'
  | 'purchase_made'
  | 'product_viewed'
  | 'cart_abandoned'
  | 'custom_event';

// Event collector service
class EventCollector {
  constructor(
    private eventStore: EventStore,
    private kafka: KafkaProducer,
    private metrics: MetricsService
  ) {}
  
  async collect(event: MarketingEvent): Promise<void> {
    // Validate event
    if (!event.contactId || !event.type) {
      throw new InvalidEventError('Missing required fields');
    }
    
    // Enrich event
    const enrichedEvent = {
      ...event,
      enrichedAt: new Date(),
      properties: {
        ...event.properties,
        day: format(event.timestamp, 'yyyy-MM-dd'),
        hour: event.timestamp.getHours()
      }
    };
    
    // Write to event store (for replay)
    await this.eventStore.append(enrichedEvent);
    
    // Publish to Kafka (for real-time processing)
    await this.kafka.send({
      topic: `marketing.events.${event.type}`,
      messages: [{
        key: event.contactId,
        value: enrichedEvent
      }]
    });
    
    // Update real-time metrics
    await this.metrics.increment(`events.${event.type}`);
    
    // Trigger any real-time actions
    await this.triggerRealtimeActions(enrichedEvent);
  }
}

// Kafka topic configuration
const eventTopics = {
  'email.*': 'marketing.events.email',
  'sms.*': 'marketing.events.sms',
  'web.*': 'marketing.events.web',
  'purchase.*': 'marketing.events.commerce'
};
```

### 4.2 Real-Time Analytics

Real-time analytics sử dụng streaming processing để calculate metrics gần như instantaneous.

```typescript
// Real-time metrics aggregation using Kafka Streams
class RealtimeMetricsAggregator {
  private streams: KafkaStreams;
  
  async aggregateEmailMetrics(): Promise<void> {
    const emailEvents = this.streams
      .stream('marketing.events.email')
      .groupBy((event) => event.campaignId)
      .window(TimeWindows.of(Duration.ofMinutes(5)))
      .aggregate(
        { sent: 0, delivered: 0, opened: 0, clicked: 0 },
        (key, event, agg) => {
          switch (event.type) {
            case 'email_sent': return { ...agg, sent: agg.sent + 1 };
            case 'email_delivered': return { ...agg, delivered: agg.delivered + 1 };
            case 'email_opened': return { ...agg, opened: agg.opened + 1 };
            case 'email_clicked': return { ...agg, clicked: agg.clicked + 1 };
          }
          return agg;
        }
      );
    
    await emailEvents.to('marketing.metrics.email.campaign');
  }
}

// In-memory metrics for current-day reporting
class CurrentDayMetrics {
  private metrics: Map<string, DayMetrics> = new Map();
  
  async recordEvent(event: MarketingEvent): Promise<void> {
    const key = this.getMetricKey(event);
    let dayMetrics = this.metrics.get(key);
    
    if (!dayMetrics) {
      dayMetrics = new DayMetrics();
      this.metrics.set(key, dayMetrics);
    }
    
    dayMetrics.increment(event.type);
  }
  
  async getCampaignMetrics(campaignId: UUID): Promise<CampaignMetrics> {
    const key = `campaign:${campaignId}`;
    const metrics = this.metrics.get(key);
    
    if (!metrics) {
      return this.initializeEmptyMetrics();
    }
    
    return {
      sent: metrics.get('email_sent') || 0,
      delivered: metrics.get('email_delivered') || 0,
      opens: metrics.get('email_opened') || 0,
      clicks: metrics.get('email_clicked') || 0,
      bounces: metrics.get('email_bounced') || 0,
      unsubscribes: metrics.get('email_unsubscribed') || 0,
      openRate: this.calculateRate(metrics.get('email_opened'), metrics.get('email_delivered')),
      clickRate: this.calculateRate(metrics.get('email_clicked'), metrics.get('email_delivered')),
      bounceRate: this.calculateRate(metrics.get('email_bounced'), metrics.get('email_sent'))
    };
  }
}
```

### 4.3 Analytics API

```typescript
class AnalyticsApi {
  constructor(
    private metricsStore: MetricsStore,
    private eventStore: EventStore
  ) {}
  
  // Campaign performance
  async getCampaignPerformance(
    campaignId: UUID,
    timeRange: TimeRange
  ): Promise<CampaignPerformance> {
    const [metrics, trends, benchmarks] = await Promise.all([
      this.metricsStore.getCampaignMetrics(campaignId, timeRange),
      this.metricsStore.getCampaignTrends(campaignId, timeRange),
      this.benchmarkService.getIndustryBenchmarks('email_marketing')
    ]);
    
    return {
      summary: this.calculateSummary(metrics),
      trends,
      benchmarks,
      comparison: this.compareToBenchmark(metrics, benchmarks),
      recommendations: await this.generateRecommendations(metrics, benchmarks)
    };
  }
  
  // Journey analytics
  async getJourneyAnalytics(
    journeyId: UUID,
    timeRange: TimeRange
  ): Promise<JourneyAnalytics> {
    const nodes = await this.journeyRepo.getJourneyNodes(journeyId);
    const nodeMetrics = await Promise.all(
      nodes.map(node => this.metricsStore.getNodeMetrics(node.id, timeRange))
    );
    
    const totalEntered = nodeMetrics[0]?.entered || 0;
    
    return {
      totalEntered,
      totalCompleted: nodeMetrics[nodeMetrics.length - 1]?.completed || 0,
      totalExited: await this.metricsStore.getExitedCount(journeyId),
      conversionRate: totalEntered > 0 
        ? (nodeMetrics[nodeMetrics.length - 1]?.completed / totalEntered) * 100 
        : 0,
      nodeMetrics: nodes.map((node, i) => ({
        nodeId: node.id,
        nodeName: node.name,
        entered: nodeMetrics[i]?.entered || 0,
        completed: nodeMetrics[i]?.completed || 0,
        skipped: nodeMetrics[i]?.skipped || 0,
        conversionRate: nodeMetrics[i]?.entered > 0
          ? (nodeMetrics[i].completed / nodeMetrics[i].entered) * 100
          : 0
      }))
    };
  }
  
  // Contact journey timeline
  async getContactTimeline(
    contactId: UUID,
    options: TimelineOptions
  ): Promise<ContactTimeline> {
    const events = await this.eventStore.query({
      contactId,
      types: options.eventTypes,
      from: options.from,
      to: options.to,
      limit: options.limit || 100
    });
    
    const activities = events.map(event => ({
      id: event.id,
      type: event.type,
      timestamp: event.timestamp,
      details: event.properties,
      campaignId: event.properties.campaignId,
      journeyId: event.properties.journeyId
    }));
    
    return {
      contactId,
      activities,
      summary: this.summarizeActivities(activities)
    };
  }
}
```

## 5. Integration Architecture

### 5.1 External System Integration

```typescript
interface IntegrationConnector {
  readonly name: string;
  readonly version: string;
  
  // Authentication
  authenticate(credentials: Credentials): Promise<AuthResult>;
  refreshAuth(): Promise<void>;
  
  // Data operations
  pullContacts(options: PullOptions): Promise<Contact[]>;
  pushContacts(contacts: Contact[]): Promise<PushResult>;
  syncEvents(): Promise<void>;
  
  // Webhooks
  registerWebhooks(): void;
}

// E-commerce integration example
class EcommerceIntegration implements IntegrationConnector {
  readonly name = 'ecommerce';
  readonly version = '1.0';
  
  private apiClient: ApiClient;
  private syncState: SyncState;
  
  async pullContacts(options: PullOptions): Promise<Contact[]> {
    const lastSync = await this.syncState.getLastSync('contacts');
    
    const customers = await this.apiClient.get('/customers', {
      params: {
        updated_after: lastSync?.timestamp,
        limit: 1000
      }
    });
    
    return customers.map(customer => this.mapToContact(customer));
  }
  
  async pushContacts(contacts: Contact[]): Promise<PushResult> {
    const results: { contactId: UUID; success: boolean; error?: string }[] = [];
    
    for (const contact of contacts) {
      try {
        await this.apiClient.post('/customers', this.mapToEcommerceCustomer(contact));
        results.push({ contactId: contact.id, success: true });
      } catch (error) {
        results.push({ 
          contactId: contact.id, 
          success: false, 
          error: error.message 
        });
      }
    }
    
    return {
      total: contacts.length,
      successful: results.filter(r => r.success).length,
      failed: results.filter(r => !r.success).length,
      errors: results.filter(r => !r.success)
    };
  }
  
  private mapToContact(ecCustomer: EcommerceCustomer): Contact {
    return {
      id: uuid(), // Generate new ID
      email: ecCustomer.email,
      profile: {
        firstName: ecCustomer.first_name,
        lastName: ecCustomer.last_name,
        language: ecCustomer.locale
      },
      company: ecCustomer.company ? {
        name: ecCustomer.company.name,
        industry: ecCustomer.company.industry
      } : undefined,
      acquisitionSource: 'ecommerce',
      customFields: {
        customerId: ecCustomer.id, // Reference to external system
        totalOrders: ecCustomer.orders_count,
        totalSpent: ecCustomer.total_spent
      }
    };
  }
}
```

### 5.2 Webhook Management

```typescript
class WebhookManager {
  constructor(
    private webhookRepo: WebhookRepository,
    private eventBus: EventBus,
    private signatureService: SignatureService
  ) {}
  
  // Register external webhooks
  async registerWebhook(config: WebhookConfig): Promise<Webhook> {
    // Verify endpoint
    const verified = await this.verifyEndpoint(config.url);
    if (!verified) {
      throw new EndpointVerificationError();
    }
    
    const webhook = Webhook.create(config);
    await this.webhookRepo.save(webhook);
    
    // Subscribe to events
    for (const eventType of config.events) {
      await this.eventBus.subscribe(
        eventType,
        async (event) => this.sendWebhook(webhook, event)
      );
    }
    
    return webhook;
  }
  
  // Process incoming webhooks
  async handleIncomingWebhook(
    source: string,
    payload: any,
    headers: Record<string, string>
  ): Promise<void> {
    // Verify signature
    const signature = headers['x-webhook-signature'];
    if (!this.signatureService.verify(source, payload, signature)) {
      throw new InvalidSignatureError();
    }
    
    // Parse event
    const event = this.parseWebhookEvent(source, payload);
    
    // Queue for processing
    await this.eventBus.publish(
      `webhook.${source}.${event.type}`,
      event
    );
  }
}
```

## 6. Data Architecture

### 6.1 Data Storage Strategy

Marketing platform sử dụng multi-database strategy cho optimized performance.

```typescript
// Contact database - PostgreSQL for ACID compliance
class ContactDatabase {
  private pool: Pool;
  
  // Optimized for point queries by email/ID
  async findByEmail(email: string): Promise<Contact | null> {
    return this.pool.query(`
      SELECT * FROM contacts 
      WHERE email_hash = $1 AND deleted_at IS NULL
    `, [hash(email)]);
  }
  
  // Optimized for segment queries
  async findBySegment(segmentId: UUID, pagination: Pagination): Promise<Contact[]> {
    return this.pool.query(`
      SELECT c.* FROM contacts c
      JOIN contact_segments cs ON cs.contact_id = c.id
      WHERE cs.segment_id = $1 AND c.deleted_at IS NULL
      ORDER BY c.created_at DESC
      LIMIT $2 OFFSET $3
    `, [segmentId, pagination.limit, pagination.offset]);
  }
}

// Event store - ClickHouse for analytics
class EventDatabase {
  private clickhouse: ClickHouseClient;
  
  // Optimized for aggregations
  async getEmailOpenRate(campaignId: UUID): Promise<number> {
    const result = await this.clickhouse.query(`
      SELECT 
        countIf(type = 'email_delivered') as delivered,
        countIf(type = 'email_opened') as opened
      FROM marketing_events
      WHERE campaign_id = $1 AND timestamp >= now() - interval 7 day
    `, [campaignId]);
    
    return result.data[0].opened / result.data[0].delivered;
  }
}

// Cache - Redis for real-time data
class MarketingCache {
  private redis: Redis;
  
  async getContactScore(contactId: UUID): Promise<number> {
    return this.redis.hget(`contact:${contactId}`, 'score');
  }
  
  async incrementEmailCount(contactId: UUID, period: string): Promise<number> {
    const key = `email_count:${contactId}:${period}`;
    return this.redis.incr(key);
  }
}
```

### 6.2 Data Pipeline

```typescript
// ETL pipeline for data warehouse
class MarketingDataPipeline {
  constructor(
    private sourceDb: ContactDatabase,
    private warehouse: DataWarehouse,
    private scheduler: CronService
  ) {}
  
  // Hourly sync for recent data
  @Cron('0 * * * *') // Every hour
  async syncRecentData(): Promise<void> {
    const since = await this.getLastSyncTimestamp();
    const until = new Date();
    
    const contacts = await this.sourceDb.getContactsModifiedSince(since);
    const events = await this.sourceDb.getEventsSince(since);
    
    await this.warehouse.loadContacts(contacts);
    await this.warehouse.loadEvents(events);
    
    await this.updateSyncTimestamp(until);
  }
  
  // Daily full refresh for analytics
  @Cron('0 3 * * *') // 3 AM daily
  async dailyFullRefresh(): Promise<void> {
    // Refresh aggregates
    await this.refreshContactAggregates();
    await this.refreshCampaignMetrics();
    await this.refreshJourneyMetrics();
    
    // Update calculated fields
    await this.updateLeadScores();
    await this.updateSegmentMembership();
  }
}
```

## 7. Scalability Architecture

### 7.1 Horizontal Scaling

```yaml
# Kubernetes deployment configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: marketing-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: marketing-api
  template:
    spec:
      containers:
      - name: api
        image: marketing-api:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        env:
        - name: DATABASE_POOL_SIZE
          value: "20"
        - name: REDIS_POOL_SIZE
          value: "50"
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: marketing-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    name: marketing-api
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "100"
```

### 7.2 Queue-Based Processing

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MESSAGE QUEUE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Producers                          Consumers                         │
│  ─────────                          ─────────                         │
│                                                                      │
│  ┌─────────┐     ┌─────────┐      ┌─────────┐  ┌─────────┐          │
│  │ API     │────▶│ Kafka   │────▶│ Email   │  │ SMS     │          │
│  │ Server  │     │ Cluster │     │ Workers │  │ Workers │          │
│  └─────────┘     │         │     └────┬────┘  └────┬────┘          │
│                   │ Topics: │           │             │              │
│                   │ - email │           │             │              │
│                   │ - sms   │           │             │              │
│                   │ - push  │           │             │              │
│                   │ - events│           ▼             ▼              │
│                   │         │      ┌─────────┐  ┌─────────┐         │
│                   │ Partitions │   │Provider │  │Provider │         │
│                   └─────┬─────┘     │ (SMTP)  │  │ (Twilio)│        │
│                         │          └─────────┘  └─────────┘         │
│                         │                                               │
│                         ▼                                               │
│                   ┌───────────┐                                         │
│                   │ Event     │                                         │
│                   │ Store     │                                         │
│                   │ (ClickHouse)│                                        │
│                   └───────────┘                                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 8. Security Architecture

### 8.1 Data Security

```typescript
interface SecurityConfig {
  encryption: {
    algorithm: 'AES-256-GCM';
    keyRotationDays: 90;
  };
  
  piiHandling: {
    maskInLogs: boolean;
    maskInResponses: boolean;
    auditAccess: boolean;
  };
  
  accessControl: {
    requireMfa: boolean;
    sessionTimeout: number; // minutes
    maxFailedLogin: number;
  };
}

class PIIProtectionService {
  // Mask PII in logs
  maskForLogging(data: any): string {
    const masked = { ...data };
    const piiFields = ['email', 'phone', 'firstName', 'lastName', 'address'];
    
    for (const field of piiFields) {
      if (masked[field]) {
        masked[field] = this.maskValue(masked[field]);
      }
    }
    
    return JSON.stringify(masked);
  }
  
  // Mask PII in API responses
  maskForResponse(data: any, userPermissions: Permission[]): any {
    if (!userPermissions.includes('view_pii')) {
      return {
        ...data,
        email: data.email ? this.maskEmail(data.email) : undefined,
        phone: data.phone ? this.maskPhone(data.phone) : undefined,
        address: undefined
      };
    }
    return data;
  }
}
```

### 8.2 Consent Management

```typescript
class ConsentEnforcement {
  constructor(
    private consentRepo: ConsentRepository,
    private messageQueue: MessageQueue
  ) {}
  
  // Enforce consent before any communication
  async enforceConsent(
    contactId: UUID,
    channel: 'email' | 'sms' | 'push'
  ): Promise<boolean> {
    const consents = await this.consentRepo.findActiveByContact(contactId);
    const requiredConsent = this.channelToConsentType(channel);
    
    const hasConsent = consents.some(
      c => c.consentType === requiredConsent && !c.withdrawnAt
    );
    
    if (!hasConsent) {
      logger.warn('Communication blocked due to missing consent', {
        contactId,
        channel
      });
      
      // Publish metric
      await this.metrics.increment(`consent.blocked.${channel}`);
    }
    
    return hasConsent;
  }
  
  // Subscribe to consent changes for real-time enforcement
  async onConsentChange(contactId: UUID): Promise<void> {
    // Immediately stop all pending communications
    await this.messageQueue.publish('consent.changed', {
      contactId,
      timestamp: new Date()
    });
  }
}
```

---

# 4. marketingskills Architecture Patterns (sync 2026-07-15)

> System design cho 9 category từ [marketingskills](https://github.com/coreyhaines31/marketingskills). Mỗi section dưới đây map vào 1 cluster of skills, anchor vào knowledge base hiện có.

## 4.1 Conversion Optimization (cro, signup, onboarding, popups, paywalls)

### 4.1.1 Event Taxonomy
```
funnel.page_viewed          { page_id, source, variant }
funnel.cta_clicked          { cta_id, position, copy }
funnel.form_started         { form_id, field_count }
funnel.form_field_completed { form_id, field_name, time_to_complete }
funnel.form_submitted       { form_id, total_time, errors }
funnel.signup_completed     { user_id, method, source }
funnel.activation_achieved  { user_id, activation_event, time_to_aha }
funnel.upgrade_offer_shown  { user_id, plan, trigger }
funwall.upgrade_completed   { user_id, from_plan, to_plan, mrr_delta }
```

### 4.1.2 Funnel State Machine
```
States:  Visitor → Lead → MQL → SQL → Customer → Activated → Expanded
         ↓        ↓       ↓      ↓       ↓            ↓
       DROP    DROP    DROP   DROP   CHURN       EXPAND
```
- Each state has entry trigger + exit criteria
- Drop-off rate per transition: < 30% healthy, > 50% = investigate
- Time-in-state: alarm if > 2x baseline

### 4.1.3 Real-time Personalization Layer
```
Request → Identify user (cookie/JWT) → Lookup segment (Redis)
        → Fetch variant assignment (A/B service)
        → Render with personalization tokens
        → Track exposure event
        → Cache response (30-60s, edge or Redis)
```
Latency budget: < 100ms added to page load.

---

## 4.2 Content & Copy (copywriting, copy-editing, cold-email, emails, sms, social, image, video)

### 4.2.1 Content Pipeline
```
draft → review (peer) → legal (if regulated) → approve → schedule
         ↓                ↓                       ↓
       iterate          iterate               schedule to CMS
                                                       ↓
                                                   publish
                                                       ↓
                                                   measure (24h, 7d, 30d)
                                                       ↓
                                                   iterate or archive
```

### 4.2.2 Email Event Stream
```
emails:
  - email.scheduled    { campaign_id, contact_id, send_at }
  - email.sent         { message_id, smtp_response }
  - email.delivered    { message_id, smtp_response }
  - email.opened       { message_id, ua, ip, timestamp }
  - email.clicked      { message_id, link, ua, ip, timestamp }
  - email.bounced      { message_id, reason, type (hard/soft) }
  - email.complained   { message_id, reason }
  - email.unsubscribed { contact_id, source }
```
Deduplicate opens/clicked with 5-min window per recipient (image-cache proxy).

### 4.2.3 Social Scheduling & Content Adaptation
```
Source asset (blog post)
  → AI rewriter (per platform guidelines)
  → Asset factory (image, video, carousel)
  → Scheduler (Buffer/Hootsuite/queue)
  → Track: impressions, engagement, clicks
  → Repurpose top performers
```

---

## 4.3 SEO & Discovery (seo-audit, ai-seo, programmatic-seo, site-architecture, competitors, schema, aso)

### 4.3.1 Site Crawler Architecture
```
Crawler queue (priority: index, errors, recent)
  → Fetch (respect robots.txt, rate limit)
  → Parse HTML (extract: title, meta, h1-h6, content, links, schema)
  → Store (pages, links, issues)
  → Index (ElasticSearch for full-text, graph for link graph)
  → Report (issues by type, priority, page authority)
```
Crawl budget: < 10 URLs/sec, < 5 min per site < 10k pages.

### 4.3.2 Programmatic SEO Generation Pipeline
```
1. Keyword research (Ahrefs/GSC export) → CSV
2. Template definition (1 per page type)
3. Data hydration (CSVs → render context)
4. Static generation (Next.js, Hugo, custom)
5. Quality gate (uniqueness check, internal links, schema)
6. Deploy to /[category]-for-[use-case]
7. Submit sitemap to GSC, ping IndexNow
```
Scale target: 100-10,000 pages from 1 template.

### 4.3.3 Schema.org Implementation
```
Type registry:
  - Organization (1 per site, global)
  - WebSite + SearchAction (homepage)
  - Article (blog posts, news)
  - Product + Offer (e-commerce)
  - FAQPage (FAQ-rich snippets)
  - SoftwareApplication (B2B SaaS)
  - BreadcrumbList (all non-homepage)
  - LocalBusiness (multi-location)
```
Validation: schema.org validator + Rich Results Test (GSC).

### 4.3.4 AI Search Optimization Layer
```
llms.txt (root, plain markdown)
├── Site summary (one paragraph)
├── Key pages (10-20 most important)
├── Product/service offerings
├── Contact + about
└── last-updated timestamp

robots.txt: allow GPTBot, ClaudeBot, PerplexityBot, anthropic-ai, Applebot-Extended
```

---

## 4.4 Paid & Distribution (ads, ad-creative)

### 4.4.1 Campaign Sync Architecture
```
CRM/Product
  ↓ segments (high-LTV, churned, lookalikes)
Ad platform
  ↓ audience sync (Facebook CAPI, Google Enhanced Conversions)
Audience in platform
  ↓ campaign structure
Reporting
  ↓ spend, CTR, CPA, ROAS back to CRM (daily)
Attribution
  ↓ merge ad platform data + first-party data
Optimization
  ↓ automated bidding rules (target CPA, target ROAS)
```
Latency: 24h reporting loop, 1h audience sync.

### 4.4.2 Creative Iteration Pipeline
```
Angle matrix (3 × 3) → 9 hooks
  → AI generation (3 variants per hook = 27 ads)
  → Upload to ad platform
  → Auto-test (kill bottom 3 after $50 spend)
  → Scale winner
  → Refresh (fatigue every 7-14 days)
```

---

## 4.5 Measurement & Testing (analytics, ab-testing)

### 4.5.1 Event Pipeline
```
SDK (web/mobile/server)
  → Collector endpoint (validate schema)
  → Stream processor (Kafka/Kinesis)
  → Cold storage (S3/Parquet, 7-year retention)
  → Hot warehouse (BigQuery/Snowflake, 90-day hot)
  → Aggregations (sessions, conversions, attribution)
  → Dashboards (Looker/Metabase/Superset)
  → Alerts (PagerDuty/Slack on anomaly)
```

### 4.5.2 A/B Test Service
```
Experiment record: { id, hypothesis, variants[], allocation, success_metric }
  → Assignment: hash(visitor_id + experiment_id) % 100
  → Exposure: log when variant rendered
  → Conversion: matched to success event
  → Statistics: Bayesian or frequentist (sequential testing)
  → Stop: sample size reached OR p < 0.05 + min runtime
```
Guardrails: max 3 concurrent tests per page, < 5% revenue impact cap.

### 4.5.3 Attribution Engine
```
Touchpoints (chronological, deduped):
  session_start → page_view → cta_click → form_start → conversion
Attribution model:
  - Last-touch (default, simple)
  - First-touch (top-of-funnel analysis)
  - Linear (equal weight)
  - Time-decay (exponential, half-life 7d)
  - Data-driven (Shapley value, ML-based)
```
Output: per-channel revenue contribution, ROAS by source.

---

## 4.6 Retention (churn-prevention)

### 4.6.1 Churn Prediction Pipeline
```
Features (per user, daily):
  - login_frequency (7d, 30d)
  - feature_usage_breadth
  - support_tickets (count, sentiment)
  - nps_score (latest)
  - payment_failures
  - team_activity (B2B)

Model: gradient boosting, XGBoost or LightGBM
Output: churn_probability (0-1) per user
Threshold: top 10% = at-risk → trigger save flow
```

### 4.6.2 Save Offer Service
```
Detect cancellation intent
  → Reason: too_expensive | not_using | missing_feature | other
  → Dynamic offer:
      too_expensive: downgrade option OR 30% off for 3 months
      not_using:    pause for 30/60/90 days OR 1:1 onboarding call
      missing:      roadmap preview + workaround doc
      other:        feedback to product team + retention call
  → Confirm
  → If still cancel: feedback survey, reversible for 24h
```

### 4.6.3 Dunning Service (failed payment)
```
Day 0:  retry payment (most issuers allow this)
Day 3:  if failed → email (soft) with card update CTA
Day 7:  retry + email (urgent) + in-app banner
Day 14: retry + final email
Day 21: pause account (read-only)
Day 60: hard delete (with Day 55 warning)
```
Recovery target: 40-60% of failed payments within 14 days.

---

## 4.7 Growth Engineering (co-marketing, free-tools, referrals)

### 4.7.1 Free Tool Architecture
```
Calculator / Grader / Generator
  ├── Input: user-provided data
  ├── Logic: scoring/calc/transform
  ├── Output: result page (shareable URL)
  ├── Email gate: optional, to unlock PDF/save
  └── Embed widget: viral loop on third-party sites
```
Hosting: static SPA, edge-rendered for SEO. Lead capture via email gate.

### 4.7.2 Referral Engine
```
Referral code: per user, base62 8-char unique
  → Reward condition: referee converts to paying customer
  → Double-sided incentive: referrer + referee both get X
  → Anti-fraud: same IP, card, device fingerprint = block
  → Tier system: 1-5 / 6-15 / 16+ refs → increasing reward
  → Payout: account credit OR cashout (Stripe/Bank)
```

### 4.7.3 Co-Marketing Hub
```
Partner record: { name, ICP overlap, audience size, contact }
  → Joint content: webinar, case study, podcast
  → Cross-promo: newsletter mentions, social amplification
  → UTM tracking: ?utm_partner={slug} for attribution
  → Shared landing pages: /partners/[slug]
  → Quarterly review: pipeline generated, CAC shared
```

---

## 4.8 Strategy & Monetization (marketing-ideas, marketing-psychology, marketing-plan, launch, pricing, offers)

### 4.8.1 Pricing Service
```
Plan definition: { tier_id, name, price_monthly, price_annual, features[] }
Pricing rule:    annual = monthly * 12 * 0.83 (17% discount default)
Tier upgrade:    auto-detect usage → show upgrade prompt
Tier downgrade:  require reason + confirmation
Proration:       daily basis, refund credit OR charge difference
```
A/B test framework: variant prices 50/50, measure conversion + LTV.

### 4.8.2 Offer Composition Service
```
Value equation: V = (Dream × Likelihood) / (Time × Effort)
  → Each component has adjustment controls
  → Bonus stack: 3-5 items, each with $ value
  → Guarantee: 30/60/lifetime
  → Urgency: genuine deadline + count
  → Scarcity: cohort-limited
  → Render: pricing page, sales page, email, ad
```

### 4.8.3 Launch Service (Pre/Launch/Post)
```
Pre-launch (T-6w → T-0):
  - Waitlist: lead capture, viral loop
  - Asset backlog: 10-15 content pieces
  - Influencer seeding
  - PR list (50+)

Launch (T+0 → T+1w):
  - Multi-channel blast (email, social, PR)
  - Product Hunt (Tue-Thu 12:01am PT)
  - Onboarding surge handling (capacity)

Post-launch (T+1w → T+6w):
  - Iterate on feedback
  - Retention focus (LTV > acquisition)
  - Retarget launch visitors
  - Content follow-ups
```

### 4.8.4 Marketing Plan Repository
```
Quarterly plan: OKR + channel mix + budget
  → Weekly: standup (blockers, learnings)
  → Monthly: retro + reallocation
  → Quarterly: full retro + next-quarter planning
Format: structured markdown in `marketing/plan/[quarter].md`
```

---

## 4.9 Sales & RevOps (revops, sales-enablement, prospecting, pr, customer-research, competitor-profiling, marketing-council, marketing-loops, directory-submissions)

### 4.9.1 Lead Lifecycle Service
```
Stages: Subscriber → Lead → MQL → SQL → Opportunity → Customer
  → Score (explicit + implicit, see glossary §10)
  → Route (round-robin, territory, named account)
  → SLA: MQL→SQL within 5 days, SQL→Opp within 14 days
  → Stage reporting (funnel + velocity)
  → Win/loss analysis
```

### 4.9.2 Sales Enablement Repository
```
Stage-aware collateral (see best-practice.md §9.10.2):
  ├── awareness/   (blogs, social, podcast)
  ├── consider/    (case studies, comparison, ROI calc)
  ├── decide/      (demo script, proposal template, security FAQ)
  └── onboard/     (implementation guide, success checklist)
Versioning: tied to product release (e.g., v3.2 collaterals)
CMS: Notion, Confluence, or static site with auth
```

### 4.9.3 Prospecting Service
```
List building:
  - Source: LinkedIn Sales Nav, Apollo, ZoomInfo, manual
  - Enrichment: Clearbit, Hunter.io (email/phone)
  - Verification: ZeroBounce, NeverBounce (bounce rate < 3%)

Sequencer:
  - Multi-channel (email + LinkedIn + phone)
  - Personalization tokens (company, role, recent trigger)
  - Send windows: Tue-Thu, 9-11am recipient local time
  - Auto-pause on reply
  - Reply handling: positive → notify AE; objection → tagged template
```

### 4.9.4 PR Distribution Service
```
Tier mapping (see best-practice.md §9.10.4)
  - Daily: HARO response queue (auto-parse, suggest drafts)
  - Weekly: pitch 5-10 new journalists with newsworthy angle
  - Monthly: 1 major announcement cycle (funding, launch, milestone)

Tracking: open rates (read receipts), reply rate, coverage count, sentiment
```

### 4.9.5 Customer Research Repository
```
Interviews: audio + transcript (auto-transcribe)
Synthesis: JTBD statements (see best-practice.md §9.10.5)
  → Tag by persona, stage, pain, gain
  → Cross-reference product roadmap
  → Quarterly synthesis report
Storage: Dovetail, Notion, or git repo with markdown
```

### 4.9.6 Competitor Profiling Service
```
Monitor: pricing page, feature page, blog, changelog, social, jobs
  → Weekly diff (crawled + compared)
  → Alert on major changes (positioning, pricing, new feature)
  → Quarterly: full profile update + battlecard refresh
  → Annual: category landscape analysis
```

### 4.9.7 Marketing Council Engine (multi-persona)
```
Personas registry: 5-7 personas with system prompts
Brief input: 1 marketing question
  → Run all personas in parallel (5-7 LLM calls)
  → Synthesize top 3 actionable angles
  → Output: prioritized idea list + rationale
Frequency: biweekly strategic, weekly tactical
```

### 4.9.8 Marketing Loops (recurring agent workflows)
```
Loop types (see best-practice.md §9.10.8):
  - Content loop: weekly, 1 publish
  - SEO loop: monthly, top 20 audit
  - Outreach loop: daily, prospecting
  - Retention loop: real-time, intervention

Implementation: stateful agent (background queue)
  - Triggers: cron, event, threshold
  - Persistence: external DB for resumability
  - Logging: every step + outcome
  - Halt conditions: explicit guardrails
  - Observability: dashboard with loop health metrics
```

### 4.9.9 Directory Submission Tracker
```
Directory registry: 50-100 directories tagged by tier
  - Submission cadence: 1-2/week to avoid spam signals
  - Status: submitted | live | rejected | needs-update
  - Quality check: title, description, logo, screenshots, link
  - Calendar: track submission dates for re-submission on update
  - Cross-link: each directory link back to canonical profile
```

---

## 4.10 Cross-Cutting: Product-Marketing Context

> Mọi marketing skill/module PHẢI đọc `.agents/product-marketing.md` (fallback `.claude/product-marketing.md`) trước khi thực thi. Nội dung tối thiểu xem `glossary.md §13`.

Service contract:
```typescript
interface ProductMarketingContext {
  product: { name, category, oneLiner, differentiator };
  audience: { primaryICP, secondaryICP, antiICP };
  positioning: { category, mainAlternative };
  pricing: { entryTier, mainTier, topTier, freePolicy };
  channels: { primary, secondary, owned };
  voice: { adjectives, bannedWords, constraints };
}
```
Loading: tại workflow start, fail fast nếu file missing → hỏi user 3 câu tối thiểu.

---

## 4.11 Liên kết section khác

| Section | File | Section number |
|---|---|---|
| Best practice implementation | `best-practice.md` | §9.1-§9.10 |
| Anti-patterns | `anti-pattern.md` | §9.1-§9.10 |
| Pre-deploy checklist | `checklist.md` | §9.1-§9.9 |
| Decision flow (skill routing) | `decision-tree.md` | §9 |
| FAQ by category | `faq.md` | §9.1-§9.9 |
| Skill glossary | `glossary.md` | §9-§13 |
