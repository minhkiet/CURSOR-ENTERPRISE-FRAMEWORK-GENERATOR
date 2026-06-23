# Best Practices cho Hệ Thống Numerology

## 1. Number Calculation Best Practices

### 1.1 Centralized Letter Value Tables

```typescript
// ❌ Anti-pattern: Hardcoded values everywhere
function calculatePythagorean(name: string): number {
  // Hardcoded values
  const values: Record<string, number> = {
    'A': 1, 'B': 2, 'C': 3
    // ... hardcoded everywhere
  };
  // Logic
}

// ❌ Anti-pattern: Different implementations
function calculateChaldean(name: string): number {
  // Different hardcoded values
}

// ✅ Best Practice: Centralized tables
const LetterValues = {
  pythagorean: Object.freeze({
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
    'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
    'Y': 7, 'Z': 8
  }),
  
  chaldean: Object.freeze({
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'U': 6, 'O': 7, 'F': 8,
    'I': 9, 'Y': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'X': 6,
    'G': 7, 'H': 8, 'Z': 8, 'P': 8, 'Q': 1, 'R': 2, 'S': 3, 'T': 4,
    'V': 6, 'W': 6, 'D': 4
  })
};

class NumerologyCalculator {
  calculate(name: string, system: 'pythagorean' | 'chaldean'): number {
    const values = LetterValues[system];
    const letters = this.removeNonLetters(name);
    return this.sumAndReduce(letters, values);
  }

  private sumAndReduce(letters: string[], values: Record<string, number>): number {
    const sum = letters.reduce((acc, letter) => {
      return acc + (values[letter.toUpperCase()] || 0);
    }, 0);
    
    return this.reduceNumber(sum);
  }
}
```

### 1.2 Master Number Handling

```typescript
// ❌ Anti-pattern: Ignoring master numbers
function reduceNumber(num: number): number {
  while (num > 9) {
    num = num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  }
  return num;
}

// This will reduce 11, 22, 33 which is wrong!

// ✅ Best Practice: Master number preservation
const MASTER_NUMBERS = [11, 22, 33] as const;
type MasterNumber = typeof MASTER_NUMBERS[number];

interface ReductionResult {
  value: number;
  isMasterNumber: boolean;
  secondaryValue?: number; // For 11 -> 2
}

function reduceNumber(num: number, preserveMaster: boolean = true): ReductionResult {
  // Don't reduce master numbers
  if (preserveMaster && MASTER_NUMBERS.includes(num as MasterNumber)) {
    const secondary = num === 11 ? 2 : num === 22 ? 4 : 6;
    return {
      value: num,
      isMasterNumber: true,
      secondaryValue: secondary
    };
  }

  if (num <= 9) {
    return { value: num, isMasterNumber: false };
  }

  const sum = num.toString().split('').reduce((acc, d) => acc + parseInt(d), 0);
  return reduceNumber(sum, preserveMaster);
}

// Usage
const result = reduceNumber(22);
console.log(result);
// { value: 22, isMasterNumber: true, secondaryValue: 4 }
```

### 1.3 Consistent Number Reduction

```typescript
// ✅ Best Practice: Unified reduction logic
class NumberReducer {
  private readonly masterNumbers = [11, 22, 33];

  reduce(num: number, options: {
    preserveMaster?: boolean;
    maxIterations?: number;
  } = {}): ReductionResult {
    const { preserveMaster = true, maxIterations = 10 } = options;
    
    return this.reduceRecursive(num, preserveMaster, 0, maxIterations);
  }

  private reduceRecursive(
    num: number,
    preserveMaster: boolean,
    iterations: number,
    maxIterations: number
  ): ReductionResult {
    // Check master number
    if (preserveMaster && this.masterNumbers.includes(num)) {
      return {
        value: num,
        isMasterNumber: true,
        secondaryValue: this.getSecondaryValue(num),
        iterations
      };
    }

    // Base case
    if (num <= 9) {
      return {
        value: num,
        isMasterNumber: false,
        iterations
      };
    }

    // Max iterations check
    if (iterations >= maxIterations) {
      return {
        value: num,
        isMasterNumber: false,
        iterations,
        warning: 'Max iterations reached'
      };
    }

    // Sum digits and recurse
    const sum = this.sumDigits(num);
    return this.reduceRecursive(sum, preserveMaster, iterations + 1, maxIterations);
  }

  private sumDigits(num: number): number {
    return num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  }

  private getSecondaryValue(master: number): number {
    const map: Record<number, number> = {
      11: 2, // 1+1=2
      22: 4, // 2+2=4
      33: 6  // 3+3=6
    };
    return map[master];
  }
}
```

## 2. Name Analysis Best Practices

### 2.1 Name Parsing

```typescript
// ✅ Best Practice: Comprehensive name parsing
class NameParser {
  parseName(fullName: string): ParsedName {
    const cleanName = this.cleanName(fullName);
    const parts = cleanName.trim().split(/\s+/);
    
    return {
      firstName: parts[parts.length - 1] || '',
      middleNames: parts.slice(1, -1),
      lastName: parts[0] || '',
      fullName: cleanName,
      letterCount: this.countLetters(cleanName),
      hasAccents: this.hasAccents(fullName)
    };
  }

  private cleanName(name: string): string {
    // Remove extra spaces
    let cleaned = name.trim().replace(/\s+/g, ' ');
    
    // Handle Vietnamese diacritics
    cleaned = this.normalizeDiacritics(cleaned);
    
    return cleaned.toUpperCase();
  }

  private normalizeDiacritics(name: string): string {
    // Map Vietnamese to basic Latin
    const diacriticMap: Record<string, string> = {
      'Ạ': 'A', 'ạ': 'a', 'Ả': 'A', 'ả': 'a', 'Ấ': 'A', 'ấ': 'a',
      'Ầ': 'A', 'ầ': 'a', 'Ẩ': 'A', 'ẩ': 'a', 'Ẫ': 'A', 'ẫ': 'a',
      'Ậ': 'A', 'ậ': 'a', 'Ắ': 'A', 'ắ': 'a', 'Ằ': 'A', 'ằ': 'a',
      'Ẳ': 'A', 'ẳ': 'a', 'Ẵ': 'A', 'ẵ': 'a', 'Ặ': 'A', 'ặ': 'a',
      'Ẹ': 'E', 'ẹ': 'e', 'Ẻ': 'E', 'ẻ': 'e', 'Ẽ': 'E', 'ẽ': 'e',
      'Ế': 'E', 'ế': 'e', 'Ề': 'E', 'ề': 'e', 'Ể': 'E', 'ể': 'e',
      'Ễ': 'E', 'ễ': 'e', 'Ệ': 'E', 'ệ': 'e', 'Ị': 'I', 'ị': 'i',
      'Ỉ': 'I', 'ỉ': 'i', 'Ĩ': 'I', 'ĩ': 'i', 'Ọ': 'O', 'ọ': 'o',
      'Ỏ': 'O', 'ỏ': 'o', 'Ố': 'O', 'ố': 'o', 'Ồ': 'O', 'ồ': 'o',
      'Ổ': 'O', 'ổ': 'o', 'Ỗ': 'O', 'ỗ': 'o', 'Ộ': 'O', 'ộ': 'o',
      'Ớ': 'O', 'ớ': 'o', 'Ờ': 'O', 'ờ': 'o', 'Ở': 'O', 'ở': 'o',
      'Ỡ': 'O', 'ỡ': 'o', 'Ợ': 'O', 'ợ': 'o', 'Ụ': 'U', 'ụ': 'u',
      'Ủ': 'U', 'ủ': 'u', 'Ữ': 'U', 'ữ': 'u', 'Ứ': 'U', 'ứ': 'u',
      'Ừ': 'U', 'ừ': 'u', 'Ử': 'U', 'ử': 'u', 'Ữ': 'U', 'ữ': 'u',
      'Ự': 'U', 'ự': 'u', 'Ỳ': 'Y', 'ỳ': 'y', 'Ỵ': 'Y', 'ỵ': 'y',
      'Ỷ': 'Y', 'ỷ': 'y', 'Ỹ': 'Y', 'ỹ': 'y'
    };

    return name.split('').map(char => diacriticMap[char] || char).join('');
  }
}
```

### 2.2 Vowel/Consonant Separation

```typescript
// ✅ Best Practice: Clear vowel/consonant separation
const VOWELS = new Set(['A', 'E', 'I', 'O', 'U', 'Y']);

class LetterAnalyzer {
  analyzeLetters(name: string): LetterAnalysis {
    const letters = name.toUpperCase().split('');
    
    const vowelLetters = letters.filter(l => VOWELS.has(l));
    const consonantLetters = letters.filter(l => /[A-Z]/.test(l) && !VOWELS.has(l));
    
    return {
      allLetters: letters.filter(l => /[A-Z]/.test(l)),
      vowels: vowelLetters,
      consonants: consonantLetters,
      vowelCount: vowelLetters.length,
      consonantCount: consonantLetters.length
    };
  }

  calculateSoulUrge(vowelLetters: string[], values: Record<string, number>): number {
    const sum = vowelLetters.reduce((acc, letter) => {
      return acc + (values[letter] || 0);
    }, 0);
    return this.reduceNumber(sum);
  }

  calculatePersonality(consonantLetters: string[], values: Record<string, number>): number {
    const sum = consonantLetters.reduce((acc, letter) => {
      return acc + (values[letter] || 0);
    }, 0);
    return this.reduceNumber(sum);
  }
}
```

## 3. Birth Date Calculation

### 3.1 Date Parsing

```typescript
// ✅ Best Practice: Robust date parsing
class BirthDateParser {
  parse(input: string | Date): ParsedBirthDate {
    let date: Date;
    
    if (input instanceof Date) {
      date = input;
    } else if (typeof input === 'string') {
      date = this.parseDateString(input);
    } else {
      throw new InvalidBirthDateException(input);
    }

    this.validateDate(date);

    return {
      date,
      day: date.getDate(),
      month: date.getMonth() + 1,
      year: date.getFullYear(),
      dayOfWeek: date.getDay(),
      formattedDate: this.formatDate(date)
    };
  }

  private parseDateString(dateStr: string): Date {
    // Try multiple formats
    const formats = [
      /^(\d{4})-(\d{2})-(\d{2})$/,           // YYYY-MM-DD
      /^(\d{2})\/(\d{2})\/(\d{4})$/,          // MM/DD/YYYY
      /^(\d{2})-(\d{2})-(\d{4})$/,            // DD-MM-YYYY
    ];

    for (const format of formats) {
      const match = dateStr.match(format);
      if (match) {
        const date = new Date(dateStr);
        if (!isNaN(date.getTime())) {
          return date;
        }
      }
    }

    // Fallback to Date constructor
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) {
      throw new InvalidBirthDateException(dateStr);
    }
    return date;
  }

  private validateDate(date: Date): void {
    const now = new Date();
    
    if (date > now) {
      throw new InvalidBirthDateException('Birth date cannot be in the future');
    }
    
    if (date < new Date('1900-01-01')) {
      throw new InvalidBirthDateException('Birth date is too old');
    }
  }
}
```

### 3.2 Life Path Calculation

```typescript
// ✅ Best Practice: Life Path calculation
class LifePathCalculator {
  constructor(private reducer: NumberReducer) {}

  calculate(birthDate: ParsedBirthDate): LifePathResult {
    // Format: YYYYMMDD
    const dateStr = `${birthDate.year}${String(birthDate.month).padStart(2, '0')}${String(birthDate.day).padStart(2, '0')}`;
    
    // Sum all digits
    const sum = dateStr.split('').reduce((acc, char) => {
      if (/\d/.test(char)) {
        return acc + parseInt(char);
      }
      return acc;
    }, 0);

    // Reduce
    const result = this.reducer.reduce(sum, true);

    return {
      number: result.value,
      isMasterNumber: result.isMasterNumber,
      secondaryNumber: result.secondaryValue,
      calculation: {
        rawDigits: dateStr.split('').filter(c => /\d/.test(c)),
        sum,
        reducedTo: result.value
      },
      meaning: this.getMeaning(result.value),
      compatibility: this.getCompatibility(result.value)
    };
  }
}
```

## 4. Life Cycles Calculation

### 4.1 Pinnacle Numbers

```typescript
// ✅ Best Practice: Pinnacle calculation
class PinnacleCalculator {
  calculate(birthDate: ParsedBirthDate, lifePathNumber: number): PinnacleResult {
    // First Pinnacle: Sum of Day + Month
    const firstPinnacle = this.reducer.reduce(
      birthDate.day + birthDate.month
    );

    // Second Pinnacle: Sum of Day + Year
    const yearDigits = this.sumDigits(birthDate.year);
    const secondPinnacle = this.reducer.reduce(
      birthDate.day + yearDigits
    );

    // Third Pinnacle: Sum of First + Second
    const thirdPinnacle = this.reducer.reduce(
      firstPinnacle.value + secondPinnacle.value
    );

    // Fourth Pinnacle: Sum of Month + Year
    const fourthPinnacle = this.reducer.reduce(
      birthDate.month + yearDigits
    );

    // Calculate ages
    const firstCycleEnd = this.calculateFirstCycleEnd(lifePathNumber);
    const secondCycleEnd = firstCycleEnd + 9;

    return {
      first: { number: firstPinnacle.value, ageEnd: firstCycleEnd },
      second: { number: secondPinnacle.value, ageEnd: secondCycleEnd },
      third: { number: thirdPinnacle.value, ageEnd: 81 },
      fourth: { number: fourthPinnacle.value, ageEnd: 100 },
      descriptions: this.getDescriptions(firstPinnacle.value, secondPinnacle.value, thirdPinnacle.value, fourthPinnacle.value)
    };
  }

  private sumDigits(num: number): number {
    return num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  }

  private calculateFirstCycleEnd(lifePathNumber: number): number {
    // First cycle usually ends between ages 0-36
    // Based on day of birth + month
    return Math.min(36, 27 + (lifePathNumber % 10));
  }
}
```

## 5. API Design

### 5.1 Consistent Response Format

```typescript
// ✅ Best Practice: Standardized API responses
interface NumerologyApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  meta: ResponseMeta;
}

interface ResponseMeta {
  requestId: string;
  timestamp: string;
  calculationTime: number;
  system: string;
}

interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

class NumerologyController {
  async calculateLifePath(req: Request, res: Response) {
    const startTime = Date.now();

    try {
      const { birthDate, system = 'pythagorean' } = req.body;
      
      const result = await this.numerologyService.calculateLifePath(birthDate, system);

      res.json({
        success: true,
        data: result,
        meta: {
          requestId: req.headers['x-request-id'] as string,
          timestamp: new Date().toISOString(),
          calculationTime: Date.now() - startTime,
          system
        }
      });

    } catch (error) {
      this.handleError(res, error, startTime);
    }
  }

  private handleError(res: Response, error: Error, startTime: number): void {
    const statusCode = error.statusCode || 500;
    
    res.status(statusCode).json({
      success: false,
      error: {
        code: error.code || 'INTERNAL_ERROR',
        message: error.message
      },
      meta: {
        requestId: '',
        timestamp: new Date().toISOString(),
        calculationTime: Date.now() - startTime,
        system: 'pythagorean'
      }
    });
  }
}
```

### 5.2 Batch Processing

```typescript
// ✅ Best Practice: Batch calculations
class NumerologyBatchService {
  async calculateBatch(
    inputs: CalculateRequest[]
  ): Promise<BatchResult<NumerologyChart>> {
    const results: BatchResultItem<NumerologyChart>[] = [];
    const errors: BatchError[] = [];

    // Validate all first
    for (let i = 0; i < inputs.length; i++) {
      const validation = this.validator.validate(inputs[i]);
      if (!validation.isValid) {
        errors.push({ index: i, errors: validation.errors });
      }
    }

    // Process valid inputs
    const validInputs = inputs.filter((_, i) => 
      !errors.some(e => e.index === i)
    );

    // Calculate in parallel with limit
    const chunks = this.chunk(validInputs, 10);
    for (const chunk of chunks) {
      const chunkResults = await Promise.all(
        chunk.map(input => this.calculateSingle(input))
      );
      results.push(...chunkResults);
    }

    return { results, errors };
  }

  private chunk<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }
}
```

## 6. Performance

### 6.1 Caching Strategy

```typescript
// ✅ Best Practice: Multi-level caching
class NumerologyCacheService {
  private memoryCache: LRUCache<string, any>;
  private redis: Redis;

  constructor() {
    this.memoryCache = new LRUCache({
      max: 500,
      ttl: 5 * 60 * 1000 // 5 minutes
    });
  }

  async getNameNumber(name: string, system: string): Promise<NumberResult | null> {
    const key = `name:${name}:${system}`;

    // L1: Memory cache
    const memResult = this.memoryCache.get(key);
    if (memResult) return memResult;

    // L2: Redis cache
    const redisResult = await this.redis.get(key);
    if (redisResult) {
      const result = JSON.parse(redisResult);
      this.memoryCache.set(key, result);
      return result;
    }

    return null;
  }

  async setNameNumber(name: string, system: string, result: NumberResult): Promise<void> {
    const key = `name:${name}:${system}`;

    this.memoryCache.set(key, result);
    await this.redis.setex(key, 7 * 24 * 60 * 60, JSON.stringify(result)); // 7 days
  }

  async getLifePath(birthDate: string): Promise<LifePathResult | null> {
    const key = `lifepath:${birthDate}`;

    const cached = await this.redis.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    return null;
  }

  async setLifePath(birthDate: string, result: LifePathResult): Promise<void> {
    const key = `lifepath:${birthDate}`;
    await this.redis.setex(key, 30 * 24 * 60 * 60, JSON.stringify(result)); // 30 days
  }
}
```

## 7. Testing

### 7.1 Unit Tests

```typescript
// ✅ Best Practice: Comprehensive tests
describe('NumerologyCalculator', () => {
  describe('Pythagorean calculation', () => {
    it('should calculate correctly for simple name', () => {
      const result = calculator.calculate('ABC', 'pythagorean');
      expect(result).toBe(6); // A=1, B=2, C=3 = 6
    });

    it('should reduce double digits', () => {
      const result = calculator.calculate('IO', 'pythagorean');
      // I=9, O=6, sum=15 -> 1+5=6
      expect(result).toBe(6);
    });

    it('should preserve master numbers', () => {
      // Calculate to get 11
      // E=5, L=3, I=9, E=5 = 22 (not master in this case)
      // Need specific calculation
      const result = calculator.reduceNumber(11);
      expect(result.isMasterNumber).toBe(true);
      expect(result.value).toBe(11);
    });

    it('should handle Vietnamese names with diacritics', () => {
      const result = calculator.calculate('NGUYỄN', 'pythagorean');
      // Should normalize to NGUYEN
      expect(result).toBeGreaterThan(0);
    });
  });

  describe('Life Path calculation', () => {
    it('should calculate for known date', () => {
      const result = calculator.calculateLifePath('1990-05-15');
      // Should return a number 1-9 or master
      expect(result.number).toBeGreaterThanOrEqual(1);
      expect(result.number).toBeLessThanOrEqual(33);
      expect([11, 22, 33].includes(result.number)).toBe(result.isMasterNumber);
    });

    it('should handle master number birth dates', () => {
      // Birth date that sums to 11, 22, or 33
      const result = calculator.calculateLifePath('2000-11-11');
      expect(result.isMasterNumber).toBe(true);
    });
  });

  describe('Number reduction', () => {
    const testCases = [
      { input: 1, expected: 1 },
      { input: 10, expected: 1 },
      { input: 11, expected: 11, isMaster: true },
      { input: 19, expected: 1 },
      { input: 22, expected: 22, isMaster: true },
      { input: 1999, expected: 1 },
    ];

    testCases.forEach(({ input, expected, isMaster }) => {
      it(`should reduce ${input} to ${expected}`, () => {
        const result = reducer.reduce(input);
        expect(result.value).toBe(expected);
        if (isMaster) {
          expect(result.isMasterNumber).toBe(true);
        }
      });
    });
  });
});
```

### 7.2 Integration Tests

```typescript
// ✅ Best Practice: Integration tests
describe('Numerology API Integration', () => {
  let app: Express;
  let db: TestDatabase;

  beforeAll(async () => {
    app = await createTestApp();
    db = await createTestDatabase();
  });

  describe('POST /api/v1/numerology/charts', () => {
    it('should create numerology chart', async () => {
      const response = await request(app)
        .post('/api/v1/numerology/charts')
        .send({
          fullName: 'Nguyen Van A',
          birthDate: '1990-05-15'
        })
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveProperty('lifePathNumber');
      expect(response.body.data).toHaveProperty('expressionNumber');
      expect(response.body.data).toHaveProperty('soulUrgeNumber');
    });

    it('should calculate correctly for Pythagorean system', async () => {
      const response = await request(app)
        .post('/api/v1/numerology/charts')
        .send({
          fullName: 'ABC',
          birthDate: '1990-05-15',
          system: 'pythagorean'
        })
        .expect(201);

      // A=1, B=2, C=3 = 6 (expression)
      expect(response.body.data.expressionNumber.value).toBe(6);
    });

    it('should return cached result', async () => {
      const input = {
        fullName: 'Test User',
        birthDate: '1990-05-15'
      };

      await request(app).post('/api/v1/numerology/charts').send(input);
      
      const response = await request(app)
        .post('/api/v1/numerology/charts')
        .send(input)
        .expect(201);

      expect(response.body.meta.cacheHit).toBe(true);
    });
  });
});
```
