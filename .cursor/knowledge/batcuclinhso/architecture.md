# Bát Cửu Linh Số - Architecture & Analysis Framework

## System Overview

Bát Cửu Linh Số (八久灵数) là hệ thống phân tích năng lượng số học dựa trên 8 ngôi sao năng lượng, được thiết kế để phân tích và đánh giá các con số trong đời sống hàng ngày.

## Core Components

### 1. Energy Star System (Hệ Thống 8 Sao)

```
Bát Tinh = 4 Cát Tinh + 4 Hung Tinh
```

#### Cát Tinh (Good Stars)

| Star | Meaning | Highest Energy Pairs |
|------|---------|---------------------|
| Thiên Y (天医) | Wealth & Health | 13/31 |
| Diên Niên (延年) | Career & Longevity | 19/91 |
| Sinh Khí (生气) | Noble & Joy | 14/41 |
| Phục Vị (伏位) | Stability & Patience | 11/22 |

#### Hung Tinh (Challenging Stars)

| Star | Meaning | Highest Energy Pairs |
|------|---------|---------------------|
| Ngũ Quỷ (五鬼) | Intelligence & Uniqueness | 18/81 |
| Tuyệt Mệnh (绝命) | Courage & Decision | 12/21 |
| Họa Hại (祸害) | Speech & Argument | 17/71 |
| Lục Sát (六煞) | Emotion & Romance | 16/61 |

### 2. Special Numbers System

```
Number System = Star Numbers + Special Numbers (0, 5)
```

- **Number 0**: Concealment, Yin, weakens energy
- **Number 5**: Display, Yang, amplifies energy

### 3. Analysis Layers

```
Analysis = Điểm → Tuyến → Diện → Thể
```

| Layer | Description | Example |
|-------|-------------|---------|
| Điểm (Point) | Single star | 13 |
| Tuyến (Line) | 2-3 stars combination | 1319 |
| Diện (Plane) | 4 stars combination | 18141319 |
| Thể (Body) | Multiple stars | Full phone number |

## Algorithm Flow

```
Input Number → Parse Stars → Analyze Layers → Apply Rules → Output Interpretation
```

### Step 1: Parse Stars

```javascript
function parseStars(number) {
  // Split number into star pairs
  // Match each pair to star type and energy level
  // Handle special numbers (0, 5)
  return {
    stars: [],
    energyLevels: [],
    specialNumbers: []
  };
}
```

### Step 2: Analyze Layers

```javascript
function analyzeLayers(stars) {
  return {
    point: analyzeSingleStar(stars[0]),
    line: analyzeTwoStars(stars[0], stars[1]),
    plane: analyzeFourStars(stars.slice(0, 4)),
    body: analyzeAllStars(stars)
  };
}
```

### Step 3: Apply Rules

1. **Order Rule**: Front star = origin, Back star = direction
2. **Energy Rule**: Higher level = stronger energy
3. **Position Rule**: 4-6 last digits = 60% total energy
4. **Harmony Rule**: Good + Good = Better, Bad + Bad = Worse

### Step 4: Generate Interpretation

```javascript
function interpret(starCombinations) {
  return {
    wealth: calculateWealthEnergy(stars),
    career: calculateCareerEnergy(stars),
    health: calculateHealthIndicators(stars),
    relationships: calculateRelationshipEnergy(stars),
    warnings: identifyPotentialIssues(stars),
    suggestions: generateSuggestions(stars)
  };
}
```

## Data Models

### Star Object

```typescript
interface Star {
  name: string;           // e.g., "Thiên Y"
  code: string;          // e.g., "TY"
  pairs: string[];        // e.g., ["13", "31"]
  level: number;         // 1-4 (1 = highest)
  type: "cat" | "hung";  // Good or Challenging
  meanings: {
    wealth?: string;
    career?: string;
    health?: string;
    relationships?: string;
  };
  strengths: string[];
  weaknesses: string[];
  healthWarnings: string[];
}
```

### Number Analysis Result

```typescript
interface AnalysisResult {
  input: string;
  parsedStars: Star[];
  layers: {
    point: StarAnalysis;
    line: LineAnalysis;
    plane: PlaneAnalysis;
    body: BodyAnalysis;
  };
  overallScore: number;  // -100 to 100
  interpretation: Interpretation;
  suggestions: Suggestion[];
  warnings: Warning[];
}
```

## Key Rules Engine

### Harmony Resolution Rules

```javascript
const harmonyRules = {
  "Tuyệt Mệnh": {
    resolvesBy: ["Thiên Y"],
    description: "Thiên Y hóa giải Tuyệt Mệnh"
  },
  "Họa Hại": {
    resolvesBy: ["Sinh Khí"],
    description: "Sinh Khí hóa giải Họa Hại"
  },
  "Lục Sát": {
    resolvesBy: ["Diên Niên"],
    description: "Diên Niên hóa giải Lục Sát"
  },
  "Ngũ Quỷ": {
    resolvesBy: ["Sinh Khí", "Thiên Y", "Diên Niên"],
    description: "Cần 3 Cát tinh hóa giải"
  }
};
```

### Position Rules

```javascript
const positionRules = {
  criticalPositions: [0, 1, 2, 3],  // Last 4 digits (0-indexed)
  energyDistribution: {
    last4: 0.4,    // 40%
    last6: 0.6,    // 60%
    middle: 0.3,   // 30%
    first: 0.1     // 10%
  }
};
```

## Analysis Examples

### Example 1: 1319 (Thiên Y + Diên Niên)

```
Stars: Thiên Y (Cấp 1) + Diên Niên (Cấp 1)
Meaning: Có tiền (Thiên Y) + Biết giữ tiền (Diên Niên)
Interpretation: Rất tốt cho tài lộc và quản lý gia đình
```

### Example 2: 318 (Thiên Y + Ngũ Quỷ)

```
Stars: Thiên Y (Cấp 1) + Ngũ Quỷ (Cấp 1)
Meaning: Có tiền nhưng dễ mất do sự thay đổi của Ngũ Quỷ
Interpretation: Dễ phá tài, tình cảm trắc trở
```

### Example 3: 18141319 (Ngũ Quỷ + Sinh Khí + Thiên Y + Diên Niên)

```
Stars: Ngũ Quỷ (18) → Sinh Khí (14) + Thiên Y (13) + Diên Niên (19)
Meaning: Ngũ Quỷ đầu được hóa giải bởi chuỗi Cát tinh
Interpretation: Biến trí tuệ thành quý nhân và tài lộc
```

## Validation Rules

### Input Validation

```javascript
function validateInput(number) {
  const errors = [];
  
  if (!/^\d+$/.test(number)) {
    errors.push("Chỉ chấp nhận số");
  }
  
  if (number.length < 4) {
    errors.push("Số phải có ít nhất 4 chữ số");
  }
  
  if (number.includes('0') && countZeros(number) > 2) {
    errors.push("Có quá nhiều số 0");
  }
  
  return { valid: errors.length === 0, errors };
}
```

### Star Pair Validation

```javascript
function validateStarPair(pair) {
  const validPairs = [
    // Thiên Y
    "13", "31", "68", "86", "49", "94", "27", "72",
    // Diên Niên
    "19", "91", "78", "87", "34", "43", "26", "62",
    // Sinh Khí
    "14", "41", "67", "76", "39", "93", "28", "82",
    // Phục Vị
    "11", "22", "88", "99", "66", "77", "33", "44",
    // Ngũ Quỷ
    "18", "81", "79", "97", "36", "63", "24", "42",
    // Tuyệt Mệnh
    "12", "21", "69", "96", "48", "84", "37", "73",
    // Họa Hại
    "17", "71", "89", "98", "46", "64", "23", "32",
    // Lục Sát
    "16", "61", "47", "74", "38", "83", "29", "92"
  ];
  
  return validPairs.includes(pair);
}
```

## Scoring System

### Overall Score Calculation

```javascript
function calculateOverallScore(stars) {
  let score = 0;
  
  for (const star of stars) {
    if (star.type === "cat") {
      score += (5 - star.level) * 10;  // Cấp 1 = +40, Cấp 4 = +10
    } else {
      score -= (5 - star.level) * 10;  // Cấp 1 = -40, Cấp 4 = -10
    }
  }
  
  // Apply position weight
  score *= getPositionWeight(stars);
  
  // Apply harmony bonus
  score += calculateHarmonyBonus(stars);
  
  return Math.max(-100, Math.min(100, score));
}
```

## Integration Points

### WeChat Integration

- Tên tài khoản → Phân tích ID
- Ảnh đại diện → Phân tích năng lượng

### Banking Integration

- Số thẻ → Phân tích "kho chứa"
- Tài khoản → Phân tích dòng tiền

### Real Estate Integration

- Số nhà → Phân tích năng lượng ngôi nhà
- Số tầng → Phân tích vị trí

### Vehicle Integration

- Biển số xe → Phân tích 4 số cuối
- Ngày đăng ký → Phân tích vận hạn

## Technical Implementation

### Database Schema

```sql
CREATE TABLE stars (
  id INTEGER PRIMARY KEY,
  name_vi TEXT NOT NULL,
  name_zh TEXT,
  code TEXT UNIQUE,
  type TEXT CHECK(type IN ('cat', 'hung')),
  pair TEXT NOT NULL,
  level INTEGER CHECK(level BETWEEN 1 AND 4)
);

CREATE TABLE number_analyses (
  id INTEGER PRIMARY KEY,
  input_number TEXT NOT NULL,
  analysis_result JSON NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE harmony_rules (
  id INTEGER PRIMARY KEY,
  star_code TEXT NOT NULL,
  resolves_star_code TEXT NOT NULL,
  description TEXT
);
```

## Performance Considerations

1. **Caching**: Cache parsed star combinations
2. **Indexing**: Index common number patterns
3. **Batch Processing**: Process multiple numbers efficiently
4. **Real-time**: Keep analysis under 100ms for UX

## Security & Privacy

1. **Input Sanitization**: Validate all number inputs
2. **Rate Limiting**: Prevent abuse
3. **Data Privacy**: Anonymize stored analyses
4. **Audit Logging**: Track all analysis requests
