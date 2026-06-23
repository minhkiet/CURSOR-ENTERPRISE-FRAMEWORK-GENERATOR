# Anti-Patterns trong Hệ Thống Numerology

## 1. Calculation Anti-Patterns

### 1.1 Hardcoded Letter Values

```typescript
// ❌ Anti-pattern: Hardcoded values in calculation
function calculatePythagorean(name: string): number {
  let sum = 0;
  for (const char of name.toUpperCase()) {
    if (char === 'A') sum += 1;
    else if (char === 'B') sum += 2;
    else if (char === 'C') sum += 3;
    // ... hundreds of if-else statements
  }
  return sum;
}

// ✅ Solution: Lookup table
const PYTHAGOREAN_VALUES: Record<string, number> = {
  'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
  'I': 9, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7,
  'Q': 8, 'R': 9, 'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6,
  'Y': 7, 'Z': 8
};

function calculatePythagorean(name: string): number {
  const letters = name.toUpperCase().split('').filter(l => /[A-Z]/.test(l));
  return letters.reduce((sum, letter) => sum + (PYTHAGOREAN_VALUES[letter] || 0), 0);
}
```

### 1.2 Ignoring Master Numbers

```typescript
// ❌ Anti-pattern: Always reduce to single digit
function reduceNumber(num: number): number {
  while (num > 9) {
    num = num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  }
  return num; // 11 becomes 2, which is wrong!
}

// ✅ Solution: Preserve master numbers
const MASTER_NUMBERS = [11, 22, 33];

function reduceNumber(num: number, preserveMaster: boolean = true): { value: number; isMaster: boolean } {
  if (preserveMaster && MASTER_NUMBERS.includes(num)) {
    return { value: num, isMaster: true };
  }
  
  if (num <= 9) {
    return { value: num, isMaster: false };
  }
  
  const sum = num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  return reduceNumber(sum, preserveMaster);
}
```

### 1.3 Inconsistent Number Reduction

```typescript
// ❌ Anti-pattern: Different reduction logic in different places
class SomeService {
  reduceToSingleDigit(num: number): number {
    while (num > 9) {
      num = num.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return num;
  }
}

class OtherService {
  reduceToSingleDigit(num: number): number {
    // Different implementation!
    const digits = num.toString().split('').map(Number);
    let result = digits.reduce((a, b) => a + b, 0);
    while (result > 9) {
      result = result.toString().split('').reduce((a, b) => a + parseInt(b), 0);
    }
    return result;
  }
}

// ✅ Solution: Shared reducer utility
class NumberReducer {
  private readonly masters = [11, 22, 33];
  
  reduce(num: number, options: { preserveMaster?: boolean } = {}): ReductionResult {
    return this._reduce(num, options.preserveMaster ?? true, 0);
  }

  private _reduce(num: number, preserve: boolean, depth: number): ReductionResult {
    if (preserve && this.masters.includes(num)) {
      return { value: num, isMaster: true };
    }
    if (num <= 9) {
      return { value: num, isMaster: false };
    }
    const sum = this.sumDigits(num);
    return this._reduce(sum, preserve, depth + 1);
  }

  private sumDigits(num: number): number {
    return num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  }
}

// Use shared instance
const reducer = new NumberReducer();
```

## 2. Name Analysis Anti-Patterns

### 2.1 Not Handling Diacritics

```typescript
// ❌ Anti-pattern: Ignoring Vietnamese diacritics
function calculateName(name: string): number {
  const letters = name.toUpperCase().split('');
  // 'Ễ' is not in table, so it's ignored!
  // Results are inconsistent for Vietnamese names
  return letters.reduce((sum, letter) => sum + VALUES[letter], 0);
}

// 'NGUYỄN' would be calculated incorrectly
// N=5, G=7, U=3, Y=7, = wrong because Ễ, Ộ are missing

// ✅ Solution: Normalize diacritics first
const DIACRITIC_MAP: Record<string, string> = {
  'Ạ': 'A', 'ạ': 'a', 'Ả': 'A', 'ả': 'a', 'Ấ': 'A', 'ấ': 'a',
  'Ầ': 'A', 'ầ': 'a', 'Ẩ': 'A', 'ẩ': 'a', 'Ẫ': 'A', 'ẫ': 'a',
  'Ậ': 'A', 'ậ': 'a', 'Ắ': 'A', 'ắ': 'a', 'Ằ': 'A', 'ằ': 'a',
  'Ẳ': 'A', 'ẳ': 'a', 'Ẵ': 'A', 'ẵ': 'a', 'Ặ': 'A', 'ặ': 'a',
  // ... all Vietnamese diacritics
};

function normalizeName(name: string): string {
  return name.split('').map(c => DIACRITIC_MAP[c] || c).join('').toUpperCase();
}

function calculateName(name: string): number {
  const normalized = normalizeName(name);
  const letters = normalized.split('').filter(l => /[A-Z]/.test(l));
  return letters.reduce((sum, letter) => sum + VALUES[letter], 0);
}
```

### 2.2 Not Separating Vowels/Consonants

```typescript
// ❌ Anti-pattern: Treating all letters the same for Soul Urge
function calculateSoulUrge(fullName: string): number {
  // This is wrong! Soul Urge should only use vowels
  return calculateExpression(fullName);
}

// ✅ Solution: Separate vowel and consonant calculation
const VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y'];

function calculateSoulUrge(name: string): number {
  const vowels = name.toUpperCase().split('').filter(l => VOWELS.includes(l));
  return vowels.reduce((sum, v) => sum + VALUES[v], 0);
}

function calculatePersonality(name: string): number {
  const consonants = name.toUpperCase().split('')
    .filter(l => /[A-Z]/.test(l) && !VOWELS.includes(l));
  return consonants.reduce((sum, c) => sum + VALUES[c], 0);
}
```

### 2.3 Including Spaces in Calculation

```typescript
// ❌ Anti-pattern: Including spaces in calculation
function calculateName(name: string): number {
  const letters = name.toUpperCase();
  let sum = 0;
  for (const char of letters) {
    sum += VALUES[char] || 0; // Space returns undefined = 0, but this is sloppy
  }
  return sum;
}

// ✅ Solution: Filter out non-letters
function calculateName(name: string): number {
  const letters = name.toUpperCase().split('').filter(l => /[A-Z]/.test(l));
  return letters.reduce((sum, letter) => sum + VALUES[letter], 0);
}
```

## 3. Life Path Anti-Patterns

### 3.1 Wrong Date Format Handling

```typescript
// ❌ Anti-pattern: Assuming single date format
function calculateLifePath(birthDate: string): number {
  const parts = birthDate.split('-'); // Assumes YYYY-MM-DD
  // Will fail for '05/15/1990' or '15-05-1990'
  const sum = parts.reduce((sum, p) => sum + parseInt(p), 0);
  return reduceNumber(sum);
}

// ✅ Solution: Handle multiple formats
function parseBirthDate(dateStr: string): { day: number; month: number; year: number } {
  // Try multiple formats
  const isoMatch = dateStr.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  if (isoMatch) {
    return { year: parseInt(isoMatch[1]), month: parseInt(isoMatch[2]), day: parseInt(isoMatch[3]) };
  }
  
  const usMatch = dateStr.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (usMatch) {
    return { month: parseInt(usMatch[1]), day: parseInt(usMatch[2]), year: parseInt(usMatch[3]) };
  }
  
  const euMatch = dateStr.match(/^(\d{2})-(\d{2})-(\d{4})$/);
  if (euMatch) {
    return { day: parseInt(euMatch[1]), month: parseInt(euMatch[2]), year: parseInt(euMatch[3]) };
  }
  
  throw new Error(`Cannot parse date: ${dateStr}`);
}
```

### 3.2 Not Using Full Birth Date

```typescript
// ❌ Anti-pattern: Only using year for Life Path
function calculateLifePath(birthDate: Date): number {
  const year = birthDate.getFullYear();
  const sum = year.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
  return reduceNumber(sum);
  // This only uses year! Should use full date.
}

// ✅ Solution: Use complete date
function calculateLifePath(birthDate: Date): number {
  const dateStr = `${birthDate.getFullYear()}${
    String(birthDate.getMonth() + 1).padStart(2, '0')
  }${
    String(birthDate.getDate()).padStart(2, '0')
  }`;
  
  // Or: year + month + day
  const sum = birthDate.getFullYear() + 
              (birthDate.getMonth() + 1) + 
              birthDate.getDate();
  
  return reduceNumber(sum);
}
```

## 4. API Anti-Patterns

### 4.1 Missing Validation

```typescript
// ❌ Anti-pattern: No input validation
class NumerologyController {
  async createChart(req: Request, res: Response) {
    const chart = await this.service.calculate(
      req.body.fullName,
      req.body.birthDate
    );
    // fullName could be empty, birthDate could be invalid
  }
}

// ✅ Solution: Comprehensive validation
class NumerologyInputValidator {
  validate(input: CreateNumerologyInput): ValidationResult {
    const errors: ValidationError[] = [];

    // Name validation
    if (!input.fullName || input.fullName.trim().length < 2) {
      errors.push({ field: 'fullName', message: 'Tên phải có ít nhất 2 ký tự' });
    }
    
    if (input.fullName && input.fullName.length > 200) {
      errors.push({ field: 'fullName', message: 'Tên quá dài (tối đa 200 ký tự)' });
    }

    // Birth date validation
    if (!input.birthDate) {
      errors.push({ field: 'birthDate', message: 'Ngày sinh là bắt buộc' });
    } else {
      const date = new Date(input.birthDate);
      if (isNaN(date.getTime())) {
        errors.push({ field: 'birthDate', message: 'Ngày sinh không hợp lệ' });
      }
      if (date > new Date()) {
        errors.push({ field: 'birthDate', message: 'Ngày sinh không thể là tương lai' });
      }
    }

    return { isValid: errors.length === 0, errors };
  }
}
```

### 4.2 Inconsistent Error Responses

```typescript
// ❌ Anti-pattern: Different error formats
catch (error) {
  res.status(500).json({ message: error.message }); // String message
}

catch (error) {
  res.status(404).json({ error: 'Not found' }); // Different format
}

catch (error) {
  res.status(400).json({ code: 'INVALID', details: {} }); // Different again
}

// ✅ Solution: Consistent error format
catch (error) {
  res.status(error.statusCode || 500).json({
    success: false,
    error: {
      code: error.code || 'INTERNAL_ERROR',
      message: error.message,
      details: error.details
    },
    meta: {
      timestamp: new Date().toISOString(),
      requestId: req.headers['x-request-id']
    }
  });
}
```

### 4.3 No Rate Limiting

```typescript
// ❌ Anti-pattern: No rate limiting
class NumerologyController {
  async calculate(req: Request, res: Response) {
    // Unlimited requests!
    const result = await this.service.calculate(req.body);
    res.json(result);
  }
}

// ✅ Solution: Rate limiting
const rateLimiter = {
  createChart: { limit: 20, window: '1m' },
  getMeaning: { limit: 100, window: '1m' },
  compatibility: { limit: 10, window: '1m' }
};

class NumerologyController {
  @RateLimit(rateLimiter.createChart)
  async createChart(req: Request, res: Response) {
    // Implementation
  }
}
```

## 5. Data Model Anti-Patterns

### 5.1 Storing Only Final Numbers

```typescript
// ❌ Anti-pattern: Only store final result
CREATE TABLE numerology_charts (
  id UUID PRIMARY KEY,
  life_path INT,
  expression INT,
  soul_urge INT
  -- Lost all intermediate calculations!
);

class ChartRepository {
  async save(chart: NumerologyChart) {
    await db.query(`
      INSERT INTO numerology_charts (id, life_path, expression, soul_urge)
      VALUES ($1, $2, $3, $4)
    `, [chart.id, chart.lifePathNumber, chart.expressionNumber, chart.soulUrgeNumber]);
    // Cannot recalculate or verify!
  }
}

// ✅ Solution: Store full calculation details
CREATE TABLE numerology_charts (
  id UUID PRIMARY KEY,
  full_name VARCHAR(200),
  birth_date DATE,
  
  -- Main numbers
  life_path_number INT,
  life_path_master BOOLEAN,
  
  -- Full name analysis
  name_analysis JSONB, -- Stores all letter values
  
  -- Calculation details
  calculation_log JSONB, -- For debugging/verification
  
  -- Timestamps
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

interface NameAnalysis {
  originalName: string;
  normalizedName: string;
  letterValues: Record<string, number>[];
  vowelSum: number;
  consonantSum: number;
  totalSum: number;
  reducedNumber: number;
  isMasterNumber: boolean;
}
```

### 5.2 No Indexes

```typescript
// ❌ Anti-pattern: No indexes
CREATE TABLE numerology_charts (
  id UUID PRIMARY KEY,
  full_name VARCHAR(200),
  birth_date DATE
  -- No indexes!
);

// Slow queries
SELECT * FROM numerology_charts WHERE birth_date > '1990-01-01';
SELECT * FROM numerology_charts WHERE life_path_number = 11;

// ✅ Solution: Proper indexes
CREATE TABLE numerology_charts (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  full_name VARCHAR(200) NOT NULL,
  birth_date DATE NOT NULL,
  life_path_number INT NOT NULL,
  expression_number INT NOT NULL,
  soul_urge_number INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_numerology_user ON numerology_charts(user_id);
CREATE INDEX idx_numerology_birth ON numerology_charts(birth_date);
CREATE INDEX idx_numerology_lifepath ON numerology_charts(life_path_number);
CREATE INDEX idx_numerology_expression ON numerology_charts(expression_number);
```

## 6. Caching Anti-Patterns

### 6.1 No Cache Invalidation

```typescript
// ❌ Anti-pattern: Cache never invalidated
class CacheService {
  async set(key: string, value: any) {
    await redis.set(key, JSON.stringify(value));
    // Never expires, never invalidated
  }
}

// User updates name -> cached old name still used!

// ✅ Solution: Proper cache invalidation
class NumerologyCacheService {
  async invalidateChart(chartId: string): Promise<void> {
    const keys = await redis.keys(`numerology:${chartId}:*`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }

  async updateChart(chart: NumerologyChart): Promise<void> {
    // Invalidate old cache
    await this.invalidateChart(chart.id);
    
    // Save new data
    await this.chartRepo.save(chart);
    
    // Cache new data
    await this.cacheChart(chart);
  }
}
```

### 6.2 Cache Stampede

```typescript
// ❌ Anti-pattern: Multiple requests trigger multiple calculations
async function getLifePath(birthDate: string) {
  const cached = await redis.get(`lifepath:${birthDate}`);
  if (cached) return JSON.parse(cached);
  
  // All 100 concurrent requests miss cache
  // -> 100 calculations triggered!
  const result = calculateLifePath(birthDate);
  await redis.set(`lifepath:${birthDate}`, JSON.stringify(result));
  return result;
}

// ✅ Solution: Distributed lock
async function getLifePath(birthDate: string) {
  const cached = await redis.get(`lifepath:${birthDate}`);
  if (cached) return JSON.parse(cached);

  const lockKey = `lock:lifepath:${birthDate}`;
  const acquired = await redis.set(lockKey, '1', 'NX', 'EX', 30);

  if (!acquired) {
    // Wait for other process
    return await waitForCache(`lifepath:${birthDate}`, 5000);
  }

  try {
    const result = calculateLifePath(birthDate);
    await redis.setex(`lifepath:${birthDate}`, 86400, JSON.stringify(result));
    return result;
  } finally {
    await redis.del(lockKey);
  }
}
```

## 7. Testing Anti-Patterns

### 7.1 Hardcoded Test Expectations

```typescript
// ❌ Anti-pattern: Hardcoded expected values
it('should calculate expression number', () => {
  const result = calculate('ABC');
  expect(result).toBe(6); // Why 6? Not documented
});

// ✅ Solution: Well-documented test cases
it('should calculate expression number for ABC', () => {
  // A=1, B=2, C=3
  // Sum = 1 + 2 + 3 = 6
  const result = calculate('ABC');
  expect(result).toBe(6);
  
  // Pythagorean: A=1, B=2, C=3
  // Total = 6, which is already single digit
});

it('should reduce double digits', () => {
  // I=9, O=6
  // Sum = 9 + 6 = 15
  // 1 + 5 = 6
  const result = calculate('IO');
  expect(result).toBe(6);
});
```

### 7.2 No Edge Case Testing

```typescript
// ❌ Anti-pattern: Only happy path
describe('Calculator', () => {
  it('works for normal names', () => {
    expect(calculate('John')).toBeDefined();
  });
});

// ✅ Solution: Edge cases
describe('Calculator', () => {
  // Empty/minimal input
  it('should handle single letter name', () => {
    expect(calculate('A')).toBe(1);
  });

  it('should handle empty string', () => {
    expect(() => calculate('')).toThrow(ValidationError);
  });

  // Unicode
  it('should handle Vietnamese names', () => {
    const result = calculate('NGUYỄN');
    expect(result).toBeGreaterThan(0);
  });

  it('should handle names with spaces', () => {
    // Spaces should be ignored
    const withSpaces = calculate('John Doe');
    const withoutSpaces = calculate('JohnDoe');
    expect(withSpaces).toBe(withoutSpaces);
  });

  // Master numbers
  it('should preserve master numbers', () => {
    const result = reducer.reduce(11);
    expect(result.isMasterNumber).toBe(true);
    expect(result.value).toBe(11);
  });

  it('should handle triple digits', () => {
    const result = reducer.reduce(999);
    expect(result.value).toBe(9); // 9+9+9=27, 2+7=9
  });

  // Boundary
  it('should handle boundary values', () => {
    expect(reducer.reduce(0).value).toBe(0);
    expect(reducer.reduce(9).value).toBe(9);
  });
});
```

## 8. Performance Anti-Patterns

### 8.1 Recalculating Everything

```typescript
// ❌ Anti-pattern: Recalculate on every request
async function getChartAnalysis(chartId: string) {
  const chart = await chartRepo.findById(chartId);
  
  // Recalculate everything
  const lifePath = calculateLifePath(chart.birthDate);
  const expression = calculateExpression(chart.fullName);
  // ... recalculate everything
  
  return analysis;
}

// ✅ Solution: Cache results
async function getChartAnalysis(chartId: string) {
  // Check cache first
  const cached = await cache.get(`analysis:${chartId}`);
  if (cached) return cached;
  
  // Only compute if needed
  const chart = await chartRepo.findById(chartId);
  const analysis = computeAnalysis(chart);
  
  // Cache result
  await cache.set(`analysis:${chartId}`, analysis, { ttl: 43200 });
  
  return analysis;
}
```

### 8.2 String Concatenation in Loops

```typescript
// ❌ Anti-pattern: String concatenation in loop
function sumDigitsSlowly(num: number): number {
  let sum = 0;
  let str = num.toString();
  for (let i = 0; i < str.length; i++) {
    sum += parseInt(str[i]); // String access is slow
  }
  return sum;
}

// ✅ Solution: Modern approaches
function sumDigitsFast(num: number): number {
  return num.toString().split('').reduce((sum, d) => sum + parseInt(d), 0);
}

// Or even faster for integers:
function sumDigitsFastest(num: number): number {
  let sum = 0;
  while (num > 0) {
    sum += num % 10;
    num = Math.floor(num / 10);
  }
  return sum;
}
```
