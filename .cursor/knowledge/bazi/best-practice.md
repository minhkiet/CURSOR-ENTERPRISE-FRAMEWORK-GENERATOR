# Best Practices cho Hệ Thống Bazi

## 1. Thiên Can và Địa Chi

### 1.1 Sử dụng Enum thay vì String

```typescript
// ❌ Anti-pattern: Sử dụng string literal
function getElement(can: string): string {
  if (can === 'Giáp' || can === 'Ất') return 'Mộc';
  if (can === 'Bính' || can === 'Đinh') return 'Hỏa';
  // ...
}

// ✅ Best Practice: Sử dụng Enum
enum Can {
  Giáp = 'Giáp',
  Ất = 'Ất',
  Bính = 'Bính',
  Đinh = 'Đinh',
  Mậu = 'Mậu',
  Kỷ = 'Kỷ',
  Canh = 'Canh',
  Tân = 'Tân',
  Nhâm = 'Nhâm',
  Quý = 'Quý'
}

enum Chi {
  Tý = 'Tý',
  Sửu = 'Sửu',
  Dần = 'Dần',
  Mão = 'Mão',
  Thìn = 'Thìn',
  Tỵ = 'Tỵ',
  Ngọ = 'Ngọ',
  Mùi = 'Mùi',
  Thân = 'Thân',
  Dậu = 'Dậu',
  Tuất = 'Tuất',
  Hợi = 'Hợi'
}

enum Element {
  Mộc = 'Mộc',
  Hỏa = 'Hỏa',
  Thổ = 'Thổ',
  Kim = 'Kim',
  Thủy = 'Thủy'
}

function getElement(can: Can): Element {
  const elementMap: Record<number, Element> = {
    0: Element.Mộc, 1: Element.Mộc,     // Giáp, Ất
    2: Element.Hỏa, 3: Element.Hỏa,    // Bính, Đinh
    4: Element.Thổ, 5: Element.Thổ,    // Mậu, Kỷ
    6: Element.Kim, 7: Element.Kim,    // Canh, Tân
    8: Element.Thủy, 9: Element.Thủy   // Nhâm, Quý
  };
  return elementMap[can];
}
```

### 1.2 Sử dụng Lookup Tables thay vì If-Else Chain

```typescript
// ❌ Anti-pattern: Chain if-else dài
function getNapAm(yearCan: string, yearChi: string): string {
  if (yearCan === 'Giáp' && yearChi === 'Tý') return 'Hải Trung Kim';
  if (yearCan === 'Ất' && yearChi === 'Tý') return 'Hải Trung Kim';
  if (yearCan === 'Bính' && yearChi === 'Tý') return 'Diện Không Hỏa';
  // ... 60 trường hợp
  return 'Không xác định';
}

// ✅ Best Practice: Lookup Table
const NAP_AM_LOOKUP: Record<string, string> = {
  'Giáp Tý': 'Hải Trung Kim',
  'Ất Tý': 'Hải Trung Kim',
  'Bính Tý': 'Diện Không Hỏa',
  'Đinh Tý': 'Diện Không Hỏa',
  'Mậu Tý': 'Sơn Hạ Hỏa',
  'Kỷ Tý': 'Sơn Hạ Hỏa',
  'Canh Tý': 'Lộ Bàng Thổ',
  'Tân Tý': 'Lộ Bàng Thổ',
  'Nhâm Tý': 'Đại Khê Thủy',
  'Quý Tý': 'Đại Khê Thủy',
  // ... đầy đủ 60 combinations
};

function getNapAm(can: Can, chi: Chi): string {
  return NAP_AM_LOOKUP[`${can} ${chi}`] ?? 'Không xác định';
}
```

## 2. Tính Toán Ngày Tháng Năm

### 2.1 Tách Biệt Logic Tính Toán

```typescript
// ❌ Anti-pattern: Logic hỗn hợp
class BaziCalculator {
  calculate(birthDate: string) {
    // Parse date
    const parts = birthDate.split('-');
    const year = parseInt(parts[0]);
    const month = parseInt(parts[1]);
    const day = parseInt(parts[2]);
    
    // Convert to lunar
    const lunar = this.toLunar(year, month, day);
    
    // Calculate year pillar
    const yearCanIndex = (year + 6) % 10;
    const yearChiIndex = (year + 8) % 12;
    
    // ... tất cả trong một method
  }
}

// ✅ Best Practice: Mỗi logic trong method riêng
class BaziCalculator {
  // 1. Date Parsing
  parseBirthDate(dateStr: string): BirthDate {
    const parts = dateStr.split('-').map(Number);
    return {
      year: parts[0],
      month: parts[1],
      day: parts[2]
    };
  }

  // 2. Lunar Conversion
  async toLunarDate(birthDate: BirthDate): Promise<LunarDate> {
    return await this.lunarCalendarClient.convert(birthDate);
  }

  // 3. Year Pillar Calculation
  calculateYearPillar(lunarYear: number): Pillar {
    const canIndex = (lunarYear + 6) % 10;
    const chiIndex = (lunarYear + 8) % 12;
    return {
      can: Can[canIndex],
      chi: Chi[chiIndex]
    };
  }

  // 4. Month Pillar Calculation  
  calculateMonthPillar(yearCan: Can, lunarMonth: number): Pillar {
    const canTable = this.getMonthCanTable(yearCan);
    const chiIndex = (lunarMonth + 1) % 12;
    return {
      can: canTable[lunarMonth],
      chi: Chi[chiIndex]
    };
  }

  // 5. Day Pillar Calculation
  calculateDayPillar(lunarDate: LunarDate): Pillar {
    const jd = this.toJulianDay(lunarDate);
    const canIndex = (jd + 1) % 10;
    const chiIndex = (jd + 1) % 12;
    return {
      can: Can[canIndex],
      chi: Chi[chiIndex]
    };
  }

  // 6. Hour Pillar Calculation
  calculateHourPillar(dayCan: Can, hour: number): Pillar {
    const chiIndex = Math.floor((hour + 1) / 2) % 12;
    const canTable = this.getHourCanTable(dayCan);
    const canIndex = canTable[chiIndex];
    return {
      can: Can[canIndex],
      chi: Chi[chiIndex]
    };
  }
}
```

### 2.2 Sử dụng Pipeline cho Tính Toán

```typescript
// ✅ Best Practice: Function Pipeline
interface BaziCalculationPipeline {
  input: {
    birthDate: Date;
    birthTime: string;
    timeZone: string;
  };
  
  steps: [
    { name: 'parseDate'; fn: (d: Date) => ParsedDate },
    { name: 'toLunar'; fn: (p: ParsedDate) => LunarDate },
    { name: 'calcYearPillar'; fn: (l: LunarDate) => Pillar },
    { name: 'calcMonthPillar'; fn: (l: LunarDate, y: Pillar) => Pillar },
    { name: 'calcDayPillar'; fn: (l: LunarDate) => Pillar },
    { name: 'calcHourPillar'; fn: (d: Pillar, t: string) => Pillar },
    { name: 'calcElements'; fn: (p: Pillar[]) => ElementBalance },
    { name: 'calcNapAm'; fn: (p: Pillar[]) => NapAmInfo }
  ];
}

class BaziCalculationPipeline {
  async execute(input: Input): Promise<BaziResult> {
    return pipe(
      input,
      this.parseDate,
      this.toLunar,
      this.calculateYearPillar,
      this.calculateMonthPillar,
      this.calculateDayPillar,
      this.calculateHourPillar,
      this.calculateElements,
      this.calculateNapAm
    );
  }
}
```

## 3. Validation và Error Handling

### 3.1 Comprehensive Input Validation

```typescript
// ✅ Best Practice: Comprehensive Validation
class BaziInputValidator {
  validate(input: CreateBaziInput): ValidationResult {
    const errors: ValidationError[] = [];

    // 1. Validate date format
    if (!this.isValidDateFormat(input.birthDate)) {
      errors.push({
        field: 'birthDate',
        message: 'Định dạng ngày sinh không hợp lệ (YYYY-MM-DD)'
      });
    }

    // 2. Validate date range
    const date = new Date(input.birthDate);
    const minDate = new Date('1900-01-01');
    const maxDate = new Date();
    
    if (date < minDate || date > maxDate) {
      errors.push({
        field: 'birthDate',
        message: 'Ngày sinh phải từ 1900-01-01 đến hiện tại'
      });
    }

    // 3. Validate time format
    if (!this.isValidTimeFormat(input.birthTime)) {
      errors.push({
        field: 'birthTime',
        message: 'Định dạng giờ sinh không hợp lệ (HH:MM)'
      });
    }

    // 4. Validate time range (0:00 - 23:59)
    const [hours] = input.birthTime.split(':').map(Number);
    if (hours < 0 || hours > 23) {
      errors.push({
        field: 'birthTime',
        message: 'Giờ sinh phải từ 00:00 đến 23:59'
      });
    }

    // 5. Validate timezone
    if (!this.isValidTimezone(input.timeZone)) {
      errors.push({
        field: 'timeZone',
        message: 'Múi giờ không hợp lệ'
      });
    }

    // 6. Validate gender
    if (!['male', 'female'].includes(input.gender)) {
      errors.push({
        field: 'gender',
        message: 'Giới tính phải là "male" hoặc "female"'
      });
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  private isValidDateFormat(date: string): boolean {
    return /^\d{4}-\d{2}-\d{2}$/.test(date);
  }

  private isValidTimeFormat(time: string): boolean {
    return /^\d{2}:\d{2}$/.test(time);
  }

  private isValidTimezone(tz: string): boolean {
    try {
      Intl.DateTimeFormat(undefined, { timeZone: tz });
      return true;
    } catch {
      return false;
    }
  }
}
```

### 3.2 Graceful Error Handling

```typescript
// ✅ Best Practice: Structured Error Handling
class BaziService {
  async calculateBazi(input: CreateBaziInput): Promise<Result<BaziChart>> {
    try {
      // 1. Validate input
      const validation = this.validator.validate(input);
      if (!validation.isValid) {
        return Result.failure({
          code: 'VALIDATION_ERROR',
          message: 'Dữ liệu đầu vào không hợp lệ',
          details: validation.errors
        });
      }

      // 2. Check cache
      const cached = await this.cache.get(input);
      if (cached) {
        return Result.success(cached);
      }

      // 3. Convert to lunar date
      let lunarDate: LunarDate;
      try {
        lunarDate = await this.lunarCalendar.convert(input.birthDate, input.timeZone);
      } catch (error) {
        return Result.failure({
          code: 'LUNAR_CONVERSION_ERROR',
          message: 'Không thể chuyển đổi sang âm lịch',
          details: { originalError: error.message }
        });
      }

      // 4. Calculate Bazi
      const chart = this.calculator.calculate(lunarDate, input.birthTime);

      // 5. Save to cache
      await this.cache.set(input, chart);

      return Result.success(chart);

    } catch (error) {
      logger.error('Bazi calculation failed', { error, input });
      return Result.failure({
        code: 'INTERNAL_ERROR',
        message: 'Đã xảy ra lỗi nội bộ'
      });
    }
  }
}

// Result Type
type Result<T> = 
  | { success: true; data: T }
  | { success: false; error: ErrorInfo };

interface ErrorInfo {
  code: string;
  message: string;
  details?: unknown;
}
```

## 4. Performance Optimization

### 4.1 Caching Strategy

```typescript
// ✅ Best Practice: Multi-level Caching
class BaziCacheService {
  private memoryCache: LRUCache<string, BaziChart>;
  private redisCache: Redis;
  
  constructor() {
    this.memoryCache = new LRUCache({
      max: 1000,
      ttl: 5 * 60 * 1000 // 5 minutes
    });
  }

  async get(key: string): Promise<BaziChart | null> {
    // 1. Check memory cache first
    const memoryResult = this.memoryCache.get(key);
    if (memoryResult) {
      metrics.increment('bazi.cache.hit.memory');
      return memoryResult;
    }

    // 2. Check Redis
    const redisResult = await this.redisCache.get(key);
    if (redisResult) {
      const chart = JSON.parse(redisResult);
      this.memoryCache.set(key, chart);
      metrics.increment('bazi.cache.hit.redis');
      return chart;
    }

    // 3. Cache miss
    metrics.increment('bazi.cache.miss');
    return null;
  }

  async set(key: string, chart: BaziChart): Promise<void> {
    // 1. Set in memory
    this.memoryCache.set(key, chart);
    
    // 2. Set in Redis with longer TTL
    await this.redisCache.setex(
      key,
      86400, // 24 hours
      JSON.stringify(chart)
    );
  }
}
```

### 4.2 Batch Processing

```typescript
// ✅ Best Practice: Batch Processing cho Multiple Charts
class BaziBatchService {
  async calculateBatch(inputs: CreateBaziInput[]): Promise<BaziChart[]> {
    // 1. Validate all inputs first
    const validInputs: CreateBaziInput[] = [];
    const errors: BatchError[] = [];
    
    for (let i = 0; i < inputs.length; i++) {
      const validation = this.validator.validate(inputs[i]);
      if (validation.isValid) {
        validInputs.push(inputs[i]);
      } else {
        errors.push({ index: i, errors: validation.errors });
      }
    }

    // 2. Check cache for all valid inputs
    const uncachedInputs: CreateBaziInput[] = [];
    const cachedResults: BaziChart[] = [];
    
    for (const input of validInputs) {
      const cached = await this.cache.get(this.getCacheKey(input));
      if (cached) {
        cachedResults.push(cached);
      } else {
        uncachedInputs.push(input);
      }
    }

    // 3. Calculate uncached in parallel (max 10 at a time)
    const calculatedResults = await this.processInBatches(
      uncachedInputs,
      10,
      (input) => this.calculateSingle(input)
    );

    // 4. Save all to cache
    await Promise.all([
      ...calculatedResults.map(r => this.cache.set(this.getCacheKey(r.input), r.chart)),
      ...cachedResults.map(r => this.cache.set(this.getCacheKey(r), r))
    ]);

    // 5. Return combined results
    return [...cachedResults, ...calculatedResults.map(r => r.chart)];
  }

  private async processInBatches<T, R>(
    items: T[],
    batchSize: number,
    processor: (item: T) => Promise<R>
  ): Promise<R[]> {
    const results: R[] = [];
    for (let i = 0; i < items.length; i += batchSize) {
      const batch = items.slice(i, i + batchSize);
      const batchResults = await Promise.all(batch.map(processor));
      results.push(...batchResults);
    }
    return results;
  }
}
```

## 5. Data Integrity

### 5.1 Immutable Records

```typescript
// ✅ Best Practice: Immutable Bazi Chart
class BaziChart implements Immutable<BaziChart> {
  readonly id: string;
  readonly birthDate: Date;
  readonly lunarDate: LunarDate;
  readonly yearPillar: Pillar;
  readonly monthPillar: Pillar;
  readonly dayPillar: Pillar;
  readonly hourPillar: Pillar;
  readonly elementBalance: ElementBalance;
  readonly menhInfo: MenhInfo;
  readonly napAmInfo: NapAmInfo;
  readonly version: number;
  readonly createdAt: Date;
  readonly updatedAt: Date;

  constructor(data: BaziChartData) {
    // Deep freeze on creation
    Object.freeze(data);
    Object.assign(this, data);
  }

  // Không có setters - tạo new instance thay vì mutate
  withAnalysis(analysis: BaziAnalysis): BaziChartWithAnalysis {
    return new BaziChartWithAnalysis({
      ...this.toObject(),
      analysis
    });
  }
}
```

### 5.2 Version Control

```typescript
// ✅ Best Practice: Optimistic Locking
interface BaziChartVersioned {
  id: string;
  version: number;
}

class BaziChartRepository {
  async update(chart: BaziChart): Promise<BaziChart> {
    const result = await this.db.query(`
      UPDATE bazi_charts 
      SET data = $1, version = version + 1, updated_at = NOW()
      WHERE id = $2 AND version = $3
      RETURNING *
    `, [JSON.stringify(chart), chart.id, chart.version]);

    if (result.rowCount === 0) {
      throw new ConcurrentModificationError(
        `Chart ${chart.id} đã được cập nhật bởi process khác`
      );
    }

    return result.rows[0];
  }
}
```

## 6. API Design Best Practices

### 6.1 Consistent Response Format

```typescript
// ✅ Best Practice: Standardized API Response
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    timestamp: string;
    requestId: string;
    pagination?: PaginationInfo;
    calculationTime?: number;
  };
}

class BaziController {
  async getChart(req: Request, res: Response) {
    try {
      const chart = await this.baziService.getChart(req.params.id);
      
      res.json({
        success: true,
        data: chart,
        meta: {
          timestamp: new Date().toISOString(),
          requestId: req.headers['x-request-id']
        }
      });
    } catch (error) {
      res.status(error.statusCode || 500).json({
        success: false,
        error: {
          code: error.code,
          message: error.message
        },
        meta: {
          timestamp: new Date().toISOString(),
          requestId: req.headers['x-request-id']
        }
      });
    }
  }
}
```

### 6.2 Pagination

```typescript
// ✅ Best Practice: Cursor-based Pagination
interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  pagination: {
    cursor: string | null;
    hasMore: boolean;
    total: number;
    limit: number;
  };
}

class BaziController {
  async getUserCharts(req: Request, res: Response) {
    const { limit = 20, cursor } = req.query;
    
    const result = await this.baziService.getUserCharts({
      userId: req.params.userId,
      limit: parseInt(limit as string),
      cursor: cursor as string
    });

    res.json({
      success: true,
      data: result.data,
      pagination: {
        cursor: result.nextCursor,
        hasMore: result.hasMore,
        total: result.total,
        limit: parseInt(limit as string)
      }
    });
  }
}
```

## 7. Testing Best Practices

### 7.1 Unit Testing Calculations

```typescript
// ✅ Best Practice: Comprehensive Unit Tests
describe('BaziCalculator', () => {
  describe('Year Pillar Calculation', () => {
    it('should calculate Giáp Tý for year 1984', () => {
      const result = calculator.calculateYearPillar(1984);
      expect(result.can).toBe(Can.Giáp);
      expect(result.chi).toBe(Chi.Tý);
    });

    it('should calculate Nhâm Tuất for year 2022', () => {
      const result = calculator.calculateYearPillar(2022);
      expect(result.can).toBe(Can.Nhâm);
      expect(result.chi).toBe(Chi.Tuất);
    });

    // Edge cases
    it('should handle year 1900 correctly', () => {
      const result = calculator.calculateYearPillar(1900);
      expect(result.can).toBe(Can.Canh);
      expect(result.chi).toBe(Chi.Tý);
    });

    it('should handle year 2100 correctly', () => {
      const result = calculator.calculateYearPillar(2100);
      expect(result.can).toBe(Can.Canh);
      expect(result.chi).toBe(Chi.Tý);
    });
  });

  describe('Element Balance', () => {
    it('should calculate correct element balance', () => {
      const pillars: Pillar[] = [
        { can: 'Giáp', chi: 'Tý' },
        { can: 'Bính', chi: 'Dần' },
        { can: 'Nhâm', chi: 'Tý' },
        { can: 'Giáp', chi: 'Tí' }
      ];
      
      const balance = calculator.calculateElementBalance(pillars);
      
      expect(balance.wood).toBe(2); // Giáp = Mộc
      expect(balance.fire).toBe(1); // Bính = Hỏa
      expect(balance.water).toBe(1); // Nhâm = Thủy
    });
  });
});
```

### 7.2 Integration Testing

```typescript
// ✅ Best Practice: Integration Tests
describe('Bazi API Integration', () => {
  let app: Express;
  let db: Database;
  
  beforeAll(async () => {
    app = await createTestApp();
    db = await createTestDatabase();
  });

  afterAll(async () => {
    await db.cleanup();
  });

  describe('POST /api/v1/bazi/charts', () => {
    it('should create a new Bazi chart', async () => {
      const response = await request(app)
        .post('/api/v1/bazi/charts')
        .send({
          birthDate: '1990-05-15',
          birthTime: '14:30',
          timeZone: 'Asia/Ho_Chi_Minh',
          gender: 'male'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('id');
      expect(response.body.data).toHaveProperty('yearPillar');
      expect(response.body.data).toHaveProperty('menhInfo');
    });

    it('should return cached result on duplicate request', async () => {
      const input = {
        birthDate: '1990-05-15',
        birthTime: '14:30',
        timeZone: 'Asia/Ho_Chi_Minh',
        gender: 'male'
      };

      // First request
      await request(app).post('/api/v1/bazi/charts').send(input);
      
      // Second request should hit cache
      const response = await request(app)
        .post('/api/v1/bazi/charts')
        .send(input)
        .expect(201);

      expect(response.body.meta.cacheHit).toBe(true);
    });
  });
});
```

## 8. Logging và Monitoring

### 8.1 Structured Logging

```typescript
// ✅ Best Practice: Structured Logging
class BaziService {
  private logger: Logger;

  async calculateBazi(input: CreateBaziInput): Promise<Result<BaziChart>> {
    const startTime = Date.now();
    const requestId = generateRequestId();

    this.logger.info('Starting Bazi calculation', {
      requestId,
      birthDate: input.birthDate,
      birthTime: input.birthTime,
      timeZone: input.timeZone
    });

    try {
      const result = await this.performCalculation(input);
      
      this.logger.info('Bazi calculation completed', {
        requestId,
        chartId: result.id,
        duration: Date.now() - startTime,
        cacheHit: result.fromCache
      });

      return Result.success(result);

    } catch (error) {
      this.logger.error('Bazi calculation failed', {
        requestId,
        error: error.message,
        stack: error.stack,
        duration: Date.now() - startTime
      });
      
      throw error;
    }
  }
}
```

### 8.2 Metrics Collection

```typescript
// ✅ Best Practice: Application Metrics
const baziMetrics = {
  // Counter: Đếm số lượng requests
  requestsTotal: new Counter({
    name: 'bazi_requests_total',
    help: 'Tổng số requests Bazi',
    labelNames: ['endpoint', 'method', 'status']
  }),

  // Histogram: Phân bố thời gian xử lý
  calculationDuration: new Histogram({
    name: 'bazi_calculation_duration_seconds',
    help: 'Thời gian tính toán Bazi',
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5]
  }),

  // Gauge: Số lượng charts đang active
  activeCharts: new Gauge({
    name: 'bazi_active_charts',
    help: 'Số lượng Bazi charts đang được sử dụng'
  }),

  // Summary: Tổng hợp cache hit rate
  cacheHitRate: new Summary({
    name: 'bazi_cache_hit_rate',
    help: 'Tỷ lệ cache hit'
  })
};
```
