# Best Practices cho Hệ Thống Tử Vi

## 1. Sao và Cung Management

### 1.1 Sử dụng Enum cho Sao Types

```typescript
// ❌ Anti-pattern: String literals
function getSaoBrightness(sao: string): string {
  if (sao === 'Tử Vi') return 'duong';
  if (sao === 'Thiên Cơ') return 'am';
  // ... many cases
}

// ✅ Best Practice: Enum-based approach
enum SaoType {
  Chinh = 'chinh',
  Phu = 'phu',
  TuTan = 'tutan',
  BatQuai = 'batquai'
}

enum SaoBrightness {
  Duong = 'duong',
  Am = 'am',
  Trung = 'trung'
}

enum Element {
  Kim = 'Kim',
  Mộc = 'Mộc',
  Thủy = 'Thủy',
  Hỏa = 'Hỏa',
  Thổ = 'Thổ'
}

interface Sao {
  name: string;
  type: SaoType;
  brightness: SaoBrightness;
  element: Element;
  meanings: string[];
}

// Lookup table
const SAO_INFO: Record<string, Omit<Sao, 'name'>> = {
  'Tử Vi': { type: SaoType.Chinh, brightness: SaoBrightness.Duong, element: Element.Thổ, meanings: ['Quyền uy', 'Địa vị'] },
  'Thiên Cơ': { type: SaoType.Chinh, brightness: SaoBrightness.Am, element: Element.Mộc, meanings: ['Trí tuệ', 'Thay đổi'] },
  'Thái Dương': { type: SaoType.Chinh, brightness: SaoBrightness.Duong, element: Element.Hỏa, meanings: ['Năng lượng', 'Sáng tạo'] },
  'Thái Âm': { type: SaoType.Chinh, brightness: SaoBrightness.Am, element: Element.Thủy, meanings: ['Nhạy cảm', 'Nội tâm'] },
  // ... more stars
};
```

### 1.2 Immutable Sao Collections

```typescript
// ✅ Best Practice: Immutable Sao collections
class SaoCollection {
  private readonly saos: ReadonlyArray<Sao>;

  constructor(saos: Sao[]) {
    this.saos = Object.freeze([...saos]);
  }

  getByCung(cungName: CungName): ReadonlyArray<Sao> {
    return this.saos.filter(s => s.position === cungName);
  }

  getByType(type: SaoType): ReadonlyArray<Sao> {
    return this.saos.filter(s => s.type === type);
  }

  getChinhSao(): ReadonlyArray<Sao> {
    return this.saos.filter(s => s.type === SaoType.Chinh);
  }

  hasSao(name: string): boolean {
    return this.saos.some(s => s.name === name);
  }
}

// Usage
const collection = new SaoCollection(calculatedSaos);
const menhSao = collection.getByCung('Mệnh');
const allChinhSao = collection.getChinhSao();
```

### 1.3 Cung Factory Pattern

```typescript
// ✅ Best Practice: Cung Factory
class CungFactory {
  private readonly cungInfo: ReadonlyMap<CungName, CungInfo>;
  private readonly elementByCung: ReadonlyMap<CungName, Element>;

  constructor() {
    this.cungInfo = new Map([
      ['Mệnh', { description: '...', meaning: '...' }],
      ['Phụ Mẫu', { description: '...', meaning: '...' }],
      // ... all 12 cungs
    ]);
    
    this.elementByCung = new Map([
      ['Mệnh', Element.Kim],
      ['Phụ Mẫu', Element.Thổ],
      ['Phúc Đức', Element.Thổ],
      ['Điền Trạch', Element.Thổ],
      ['Quan Lộc', Element.Kim],
      ['Nô Bộc', Element.Kim],
      ['Thiên Di', Element.Thủy],
      ['Tật Ách', Element.Thủy],
      ['Tài Bạch', Element.Kim],
      ['Tử Tức', Element.Mộc],
      ['Phu Thê', Element.Hỏa],
      ['Huỵệt', Element.Hỏa]
    ]);
  }

  createCung(name: CungName, stars: Sao[], cungMenhIndex: number): Cung {
    const info = this.cungInfo.get(name);
    if (!info) throw new Error(`Unknown cung: ${name}`);

    const cungIndex = CUNG_NAMES.indexOf(name);
    const position = (cungIndex - cungMenhIndex + 12) % 12;

    return Object.freeze({
      name,
      index: cungIndex,
      stars: Object.freeze([...stars]),
      info: Object.freeze({ ...info }),
      element: this.elementByCung.get(name) || Element.Thổ,
      position,
      isEmpty: this.isEmpty(stars),
      occupant: this.getOccupant(stars),
      owner: this.getOwner(name)
    });
  }

  private isEmpty(stars: Sao[]): boolean {
    return !stars.some(s => s.type === SaoType.Chinh);
  }

  private getOccupant(stars: Sao[]): string | undefined {
    const chinhSao = stars.find(s => s.type === SaoType.Chinh);
    return chinhSao?.name;
  }

  private getOwner(cungName: CungName): string {
    // Logic xác định sao chủ cung
    return this.determineOwner(cungName);
  }
}
```

## 2. Vận Hạn Calculation

### 2.1 Vận Hạn Pipeline

```typescript
// ✅ Best Practice: Vận Hạn Pipeline
interface VanHanCalculationInput {
  birthYear: number;
  birthMonth: number;
  birthDay: number;
  gender: Gender;
  cungMenhIndex: number;
}

interface VanHanCalculationOutput {
  vanHans: VanHan[];
  currentVan: VanHan;
  nextVan: VanHan;
}

class VanHanCalculator {
  calculate(input: VanHanCalculationInput): VanHanCalculationOutput {
    const { birthYear, gender, cungMenhIndex } = input;
    
    // 1. Xác định bắt đầu Vận
    const vanStartYear = this.calculateVanStartYear(birthYear, gender);
    
    // 2. Tính từng Vận
    const vanHans = this.calculateAllVan(
      vanStartYear,
      birthYear,
      cungMenhIndex,
      gender
    );
    
    // 3. Xác định Vận hiện tại
    const currentYear = new Date().getFullYear();
    const currentVan = this.getCurrentVan(vanHans, currentYear);
    const nextVan = this.getNextVan(vanHans, currentVan);
    
    return { vanHans, currentVan, nextVan };
  }

  private calculateVanStartYear(birthYear: number, gender: Gender): number {
    // Nam: Bắt đầu từ năm sinh
    // Nữ: Bắt đầu từ năm sinh + 1
    return gender === 'male' ? birthYear : birthYear + 1;
  }

  private calculateAllVan(
    startYear: number,
    birthYear: number,
    cungMenhIndex: number,
    gender: Gender
  ): VanHan[] {
    const vanHans: VanHan[] = [];
    const vanTypes: VanType[] = ['thien', 'nhan', 'dia'];
    
    for (let i = 0; i < 12; i++) {
      const vanYear = startYear + i * 10;
      const age = vanYear - birthYear;
      const vanType = vanTypes[i % 3];
      
      vanHans.push({
        year: vanYear,
        age,
        van: vanType,
        han: this.calculateHan(vanYear, cungMenhIndex, gender),
        lichSu: this.getLichSuVan(age, gender),
        forecast: this.generateForecast(vanYear, gender)
      });
    }
    
    return vanHans;
  }
}
```

### 2.2 Han Calculation Service

```typescript
// ✅ Best Practice: Separated Han Calculation
class HanCalculationService {
  private readonly HAN_TABLE = {
    thien: [
      { name: 'Tràng Sinh', element: 'Mộc', meaning: 'Sống lâu' },
      { name: 'Mộc Dục', element: 'Mộc', meaning: 'Tắm rửa' },
      { name: 'Quan Đới', element: 'Mộc', meaning: 'Quan tài' },
      // ... 12 thiện hạn
    ],
    nhan: [
      { name: 'Tuệ Giải', element: 'Thủy', meaning: 'Trí tuệ' },
      { name: 'Tài Trì', element: 'Thủy', meaning: 'Tài lộc' },
      // ... 12 nhân hạn
    ],
    dia: [
      { name: 'Lâm Quan', element: 'Thổ', meaning: 'Đến quan' },
      { name: 'Lâm Chung', element: 'Thổ', meaning: 'Trọng quan' },
      // ... 12 địa hạn
    ]
  };

  calculate(vanType: VanType, age: number, gender: Gender): Han[] {
    const index = Math.floor(age / 10) % 12;
    const hanList = this.HAN_TABLE[vanType];
    
    return hanList.map((han, i) => ({
      ...han,
      position: (index + i) % 12,
      isFavorable: this.isFavorable(han.name, gender)
    }));
  }

  private isFavorable(hanName: string, gender: Gender): boolean {
    // Logic xác định hạn tốt/xấu theo giới tính
    const unfavorableHans = gender === 'male' 
      ? ['Tử Thọ', 'Tái Sát']
      : ['Tử Phù', 'Ngũ Bất'];
    
    return !unfavorableHans.includes(hanName);
  }
}
```

## 3. Chart Building

### 3.1 Builder Pattern cho TuviChart

```typescript
// ✅ Best Practice: TuviChart Builder
class TuviChartBuilder {
  private data: Partial<TuviChartData> = {};

  setBirthInfo(info: BirthInfo): this {
    this.data.birthDate = info.date;
    this.data.birthTime = info.time;
    this.data.timeZone = info.timezone;
    this.data.gender = info.gender;
    return this;
  }

  setLunarDate(lunar: LunarDate): this {
    this.data.lunarDate = Object.freeze({ ...lunar });
    return this;
  }

  setMenhCach(menh: MenhCach): this {
    this.data.menhCach = Object.freeze({ ...menh });
    return this;
  }

  setCungs(cungs: Cung[]): this {
    this.data.cungs = cungs.map(c => Object.freeze({ ...c }));
    return this;
  }

  setSaos(saos: SaoPositionResult): this {
    this.data.cungStars = Object.freeze(saos.cungStars);
    this.data.allSaos = Object.freeze([...saos.allStars]);
    return this;
  }

  setVanHan(vanHans: VanHan[]): this {
    this.data.vanHan = vanHans.map(v => Object.freeze({ ...v }));
    return this;
  }

  build(): TuviChart {
    this.validate();
    
    return Object.freeze({
      id: generateUUID(),
      ...this.data,
      version: 1,
      createdAt: new Date(),
      updatedAt: new Date()
    }) as TuviChart;
  }

  private validate(): void {
    if (!this.data.birthDate) throw new Error('Missing birthDate');
    if (!this.data.menhCach) throw new Error('Missing menhCach');
    if (!this.data.cungs || this.data.cungs.length !== 12) {
      throw new Error('Must have exactly 12 cungs');
    }
  }
}

// Usage
const chart = new TuviChartBuilder()
  .setBirthInfo({ date, time, timezone, gender })
  .setLunarDate(lunarDate)
  .setMenhCach(menhCach)
  .setCungs(cungs)
  .setSaos(saos)
  .setVanHan(vanHans)
  .build();
```

### 3.2 Functional Update cho Cungs

```typescript
// ✅ Best Practice: Immutable Cung updates
class CungUpdater {
  updateCung(
    cungs: Cung[],
    cungName: CungName,
    updater: (cung: Cung) => Cung
  ): Cung[] {
    return cungs.map(c => 
      c.name === cungName ? updater(c) : c
    );
  }

  addSaoToCung(
    cungs: Cung[],
    cungName: CungName,
    sao: Sao
  ): Cung[] {
    return this.updateCung(cungs, cungName, cung => ({
      ...cung,
      stars: [...cung.stars, sao],
      isEmpty: false,
      occupant: sao.type === 'chinh' ? sao.name : cung.occupant
    }));
  }

  removeSaoFromCung(
    cungs: Cung[],
    cungName: CungName,
    saoName: string
  ): Cung[] {
    return this.updateCung(cungs, cungName, cung => {
      const newStars = cung.stars.filter(s => s.name !== saoName);
      const hasChinhSao = newStars.some(s => s.type === 'chinh');
      
      return {
        ...cung,
        stars: newStars,
        isEmpty: !hasChinhSao,
        occupant: hasChinhSao 
          ? newStars.find(s => s.type === 'chinh')?.name 
          : undefined
      };
    });
  }
}
```

## 4. Analysis Generation

### 4.1 Strategy Pattern cho Analysis

```typescript
// ✅ Best Practice: Analysis Strategy
interface AnalysisStrategy {
  analyze(chart: TuviChart): AnalysisResult;
}

class MenhCachAnalyzer implements AnalysisStrategy {
  analyze(chart: TuviChart): AnalysisResult {
    const { menhCach } = chart;
    
    return {
      type: 'menh_cach',
      summary: this.getMenhSummary(menhCach),
      details: {
        element: this.analyzeElement(menhCach.element),
        strengths: this.getStrengths(menhCach),
        weaknesses: this.getWeaknesses(menhCach),
        compatible: this.getCompatibleElements(menhCach.element)
      }
    };
  }

  private getMenhSummary(menh: MenhCach): string {
    const templates = {
      'Kim': 'Người mệnh Kim thường có ý chí mạnh mẽ, quyết đoán và kiên trì...',
      'Mộc': 'Người mệnh Mộc thường có tinh thần hướng nội, sáng tạo và nhạy cảm...',
      'Thủy': 'Người mệnh Thủy thường có trí tuệ linh hoạt, giao tiếp tốt...',
      'Hỏa': 'Người mệnh Hỏa thường có năng lượng dồi dào, nhiệt tình...',
      'Thổ': 'Người mệnh Thổ thường có tính ổn định, đáng tin cậy...'
    };
    
    return templates[menh.element] || '';
  }
}

class CungAnalyzer implements AnalysisStrategy {
  analyze(chart: TuviChart): AnalysisResult {
    const { cungs } = chart;
    
    return {
      type: 'cung',
      summary: this.getCungSummary(cungs),
      details: cungs.reduce((acc, cung) => {
        acc[cung.name] = this.analyzeSingleCung(cung);
        return acc;
      }, {} as Record<string, CungAnalysis>)
    };
  }

  private analyzeSingleCung(cung: Cung): CungAnalysis {
    return {
      name: cung.name,
      isEmpty: cung.isEmpty,
      occupant: cung.occupant,
      stars: cung.stars.map(s => s.name),
      analysis: this.generateCungAnalysis(cung),
      recommendation: this.getRecommendation(cung)
    };
  }
}

class AnalysisEngine {
  private strategies: AnalysisStrategy[];

  constructor() {
    this.strategies = [
      new MenhCachAnalyzer(),
      new CungAnalyzer(),
      new SaoAnalyzer(),
      new VanHanAnalyzer(),
      new PhuongMenAnalyzer()
    ];
  }

  analyzeChart(chart: TuviChart): FullAnalysis {
    const results = this.strategies.map(s => s.analyze(chart));
    
    return {
      chartId: chart.id,
      results,
      generatedAt: new Date()
    };
  }
}
```

### 4.2 Parallel Analysis

```typescript
// ✅ Best Practice: Parallel Analysis Generation
class ParallelAnalysisEngine {
  async analyzeChart(chart: TuviChart): Promise<FullAnalysis> {
    const [
      menhAnalysis,
      cungAnalysis,
      saoAnalysis,
      vanHanAnalysis,
      phuongMenAnalysis
    ] = await Promise.all([
      this.analyzeMenhCach(chart),
      this.analyzeCungs(chart),
      this.analyzeSaos(chart),
      this.analyzeVanHan(chart),
      this.analyzePhuongMen(chart)
    ]);

    return {
      chartId: chart.id,
      menh: menhAnalysis,
      cungs: cungAnalysis,
      saos: saoAnalysis,
      vanHan: vanHanAnalysis,
      phuongMen: phuongMenAnalysis,
      generatedAt: new Date()
    };
  }

  private async analyzeMenhCach(chart: TuviChart): Promise<MenhAnalysis> {
    // Analysis logic
  }

  private async analyzeCungs(chart: TuviChart): Promise<CungAnalysis[]> {
    // Analysis logic
  }

  private async analyzeSaos(chart: TuviChart): Promise<SaoAnalysis> {
    // Analysis logic
  }

  private async analyzeVanHan(chart: TuviChart): Promise<VanHanAnalysis> {
    // Analysis logic
  }

  private async analyzePhuongMen(chart: TuviChart): Promise<PhuongMenAnalysis> {
    // Analysis logic
  }
}
```

## 5. API Design

### 5.1 Consistent Response Format

```typescript
// ✅ Best Practice: Standardized Response
interface TuviApiResponse<T> {
  success: boolean;
  data?: T;
  error?: TuviApiError;
  meta: {
    requestId: string;
    timestamp: string;
    version: string;
  };
}

interface TuviApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

class TuviController {
  private readonly logger: Logger;

  async getChart(req: Request, res: Response) {
    const requestId = generateRequestId();

    try {
      const chart = await this.tuviService.getChart(req.params.id);

      res.json({
        success: true,
        data: this.transformChart(chart),
        meta: {
          requestId,
          timestamp: new Date().toISOString(),
          version: '1.0.0'
        }
      });

    } catch (error) {
      this.logger.error('Error getting chart', { requestId, error });
      
      res.status(error.statusCode || 500).json({
        success: false,
        error: {
          code: error.code || 'INTERNAL_ERROR',
          message: error.message
        },
        meta: {
          requestId,
          timestamp: new Date().toISOString(),
          version: '1.0.0'
        }
      });
    }
  }

  private transformChart(chart: TuviChart): TuviChartDTO {
    return {
      id: chart.id,
      birthInfo: {
        date: formatDate(chart.birthDate),
        time: chart.birthTime,
        timezone: chart.timeZone,
        gender: chart.gender
      },
      menhCach: {
        name: chart.menhCach.name,
        element: chart.menhCach.element,
        can: chart.menhCach.can,
        chi: chart.menhCach.chi
      },
      cungs: chart.cungs.map(c => ({
        name: c.name,
        position: c.position,
        stars: c.stars.map(s => s.name),
        isEmpty: c.isEmpty
      })),
      vanHan: chart.vanHan.map(v => ({
        year: v.year,
        age: v.age,
        van: v.van,
        han: v.han
      }))
    };
  }
}
```

### 5.2 Pagination

```typescript
// ✅ Best Practice: Cursor-based Pagination
class ChartListResponse {
  data: TuviChartSummary[];
  pagination: {
    nextCursor: string | null;
    prevCursor: string | null;
    hasMore: boolean;
    total: number;
  };
}

class TuviController {
  async listUserCharts(req: Request, res: Response) {
    const { userId } = req.params;
    const { limit = 20, cursor, sort = 'createdAt' } = req.query;

    const result = await this.tuviService.listCharts({
      userId,
      limit: parseInt(limit as string),
      cursor: cursor as string,
      sort: sort as 'createdAt' | 'birthDate'
    });

    res.json({
      success: true,
      data: result.data.map(c => this.toSummary(c)),
      pagination: {
        nextCursor: result.nextCursor,
        prevCursor: result.prevCursor,
        hasMore: result.hasMore,
        total: result.total
      }
    });
  }
}
```

## 6. Performance

### 6.1 Caching Strategy

```typescript
// ✅ Best Practice: Multi-layer Caching
class TuviCacheService {
  private memoryCache: LRUCache<string, TuviChart>;
  private redis: Redis;

  constructor() {
    this.memoryCache = new LRUCache({
      max: 500,
      ttl: 5 * 60 * 1000 // 5 minutes
    });
    this.redis = new Redis(config.redis);
  }

  async getChart(id: string): Promise<TuviChart | null> {
    // L1: Memory cache
    const memResult = this.memoryCache.get(id);
    if (memResult) return memResult;

    // L2: Redis cache
    const redisResult = await this.redis.get(`tuvi:chart:${id}`);
    if (redisResult) {
      const chart = JSON.parse(redisResult);
      this.memoryCache.set(id, chart);
      return chart;
    }

    return null;
  }

  async setChart(chart: TuviChart): Promise<void> {
    // Set in both layers
    this.memoryCache.set(chart.id, chart);
    await this.redis.setex(
      `tuvi:chart:${chart.id}`,
      86400,
      JSON.stringify(chart)
    );
  }

  async invalidateChart(id: string): Promise<void> {
    this.memoryCache.delete(id);
    await this.redis.del(`tuvi:chart:${id}`);
    await this.redis.del(`tuvi:analysis:${id}`);
  }
}
```

### 6.2 Batch Processing

```typescript
// ✅ Best Practice: Batch Chart Creation
class TuviBatchService {
  async createBatch(inputs: CreateTuviRequest[]): Promise<BatchResult<TuviChart>> {
    const results: BatchResultItem<TuviChart>[] = [];
    const errors: BatchError[] = [];

    // Validate all first
    for (let i = 0; i < inputs.length; i++) {
      const validation = this.validator.validate(inputs[i]);
      if (!validation.isValid) {
        errors.push({ index: i, errors: validation.errors });
      }
    }

    // Process valid inputs in batches
    const validInputs = inputs.filter((_, i) => 
      !errors.some(e => e.index === i)
    );

    const chunks = this.chunkArray(validInputs, 10);
    for (const chunk of chunks) {
      const chunkResults = await Promise.all(
        chunk.map(input => this.createSingleChart(input))
      );
      results.push(...chunkResults);
    }

    return { results, errors };
  }

  private chunkArray<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }
}
```

## 7. Testing

### 7.1 Unit Tests

```typescript
// ✅ Best Practice: Comprehensive Unit Tests
describe('TuviCalculator', () => {
  describe('MenhCach Calculation', () => {
    it('should calculate Kim menh for male with Giáp day', () => {
      const result = calculator.calculateMenhCach('Giáp', 'male');
      expect(result.name).toBe('Kim');
      expect(result.element).toBe('Kim');
    });

    it('should calculate Mộc menh for female with Giáp day', () => {
      const result = calculator.calculateMenhCach('Giáp', 'female');
      expect(result.name).toBe('Mộc');
    });

    it('should calculate correct menh for all day cans', () => {
      const maleResults = ['Kim', 'Mộc', 'Thủy', 'Hỏa', 'Thổ'];
      const cans = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu'];
      
      cans.forEach((can, i) => {
        const result = calculator.calculateMenhCach(can, 'male');
        expect(result.name).toBe(maleResults[i]);
      });
    });
  });

  describe('CungMenh Calculation', () => {
    it('should place Mệnh cung correctly for male', () => {
      const cungIndex = calculator.calculateCungMenh('Giáp', 'male');
      expect(cungIndex).toBe(0); // Mệnh is index 0
    });

    it('should place Mệnh cung correctly for female', () => {
      const cungIndex = calculator.calculateCungMenh('Giáp', 'female');
      expect(cungIndex).toBe(0); // Mệnh is index 0
    });
  });

  describe('VanHan Calculation', () => {
    it('should start van from birth year for male', () => {
      const vanStart = calculator.getVanStartYear(1990, 'male');
      expect(vanStart).toBe(1990);
    });

    it('should start van from birth year + 1 for female', () => {
      const vanStart = calculator.getVanStartYear(1990, 'female');
      expect(vanStart).toBe(1991);
    });

    it('should calculate correct van types', () => {
      const vanTypes = calculator.calculateVanTypes(1990, 'male');
      expect(vanTypes[0].van).toBe('thien');
      expect(vanTypes[1].van).toBe('nhan');
      expect(vanTypes[2].van).toBe('dia');
    });
  });
});
```

### 7.2 Integration Tests

```typescript
// ✅ Best Practice: Integration Tests
describe('Tuvi API Integration', () => {
  let app: Express;
  let db: TestDatabase;

  beforeAll(async () => {
    app = await createTestApp();
    db = await createTestDatabase();
    await db.seed();
  });

  describe('POST /api/v1/tuvi/charts', () => {
    it('should create tuvi chart successfully', async () => {
      const response = await request(app)
        .post('/api/v1/tuvi/charts')
        .send({
          birthDate: '1990-05-15',
          birthTime: '14:30',
          timeZone: 'Asia/Ho_Chi_Minh',
          gender: 'male'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data.menhCach).toBeDefined();
      expect(response.body.data.cungs).toHaveLength(12);
      expect(response.body.data.vanHan).toBeDefined();
    });

    it('should return cached result', async () => {
      const input = {
        birthDate: '1990-05-15',
        birthTime: '14:30',
        timeZone: 'Asia/Ho_Chi_Minh',
        gender: 'male'
      };

      await request(app).post('/api/v1/tuvi/charts').send(input);
      
      const response = await request(app)
        .post('/api/v1/tuvi/charts')
        .send(input)
        .expect(201);

      expect(response.body.meta.cacheHit).toBe(true);
    });
  });
});
```
