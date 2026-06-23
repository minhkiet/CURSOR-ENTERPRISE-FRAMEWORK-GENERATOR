---
title: "Safety Filtering - Safety Settings và Content Filtering"
description: "Hướng dẫn toàn diện về safety settings trong Gemini API, bao gồm HarmBlockThreshold, HarmCategory, block thresholds, và cách configure safety cho production environments"
tags:
  - "gemini"
  - "safety"
  - "content-filtering"
  - "harm-block"
  - "safety-settings"
  - "moderation"
  - "harm-category"
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Safety Filtering - Safety Settings và Content Filtering

## Tổng Quan (Overview)

Safety filtering là một thành phần quan trọng trong bất kỳ hệ thống AI production nào. Gemini API cung cấp một hệ thống safety settings toàn diện cho phép developers kiểm soát loại nội dung nào được phép tạo ra và loại nào bị chặn. Hệ thống này dựa trên HarmCategory (các loại nội dung có hại) và HarmBlockThreshold (mức độ nghiêm trọng để chặn).

Việc hiểu và configure safety settings đúng cách là essential cho việc:

- Bảo vệ người dùng khỏi nội dung có hại
- Tuân thủ các quy định pháp luật và policies
- Xây dựng trust với người dùng
- Tránh các vấn đề pháp lý và reputation
- Tùy chỉnh mức độ filtering theo use case cụ thể

Trong tài liệu này, chúng ta sẽ đi sâu vào chi tiết kỹ thuật của safety system, cách interpret safety ratings, và các best practices để configure safety settings cho different scenarios.

## Mục Đích (Purpose)

**1. Hiểu Rõ Safety Rating System**

Cung cấp kiến thức chi tiết về HarmCategory và HarmBlockThreshold, cách safety ratings được calculated, và cách interpret các response từ safety system. Hiểu rõ system giúp developers make informed decisions về configuration.

**2. Nắm Vững Configuration Options**

Hướng dẫn chi tiết cách configure safety settings cho different use cases: từ strict filtering cho content platform đến permissive settings cho developer tools. Mỗi use case có yêu cầu khác nhau và cần configuration phù hợp.

**3. Xây Dựng Monitoring và Alerting Systems**

Cung cấp patterns để monitor safety-related events, track blocked content, và set up alerting cho các anomalies. Điều này quan trọng cho việc maintain compliance và respond to issues.

## Các Khái Niệm Cốt Lõi (Key Concepts)

### 1. HarmCategory - Các Loại Nội Dung Có Hại

Gemini xác định 4 HarmCategory chính, mỗi loại đại diện cho một loại nội dung có hại:

```python
# HarmCategory definitions (Python)
# Giá trị được định nghĩa trong google.generativeai.types

class HarmCategory:
    """
    Các loại harm categories được hỗ trợ bởi Gemini.
    """
    
    # Content có thể harassment hoặc bullying
    HARM_CATEGORY_HARASSMENT = "HARM_CATEGORY_HARASSMENT"
    
    # Content có thể hate speech hoặc discriminatory
    HARM_CATEGORY_HATE_SPEECH = "HARM_CATEGORY_HATE_SPEECH"
    
    # Content có thể sexually explicit
    HARM_CATEGORY_SEXUALLY_EXPLICIT = "HARM_CATEGORY_SEXUALLY_EXPLICIT"
    
    # Content có thể dangerous hoặc promote harm
    HARM_CATEGORY_DANGEROUS = "HARM_CATEGORY_DANGEROUS"


# Human-readable descriptions
HARM_CATEGORY_DESCRIPTIONS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: """
        Harassment content bao gồm các hành vi:
        - Bắt nạt, đe dọa, hoặc quấy rối một cá nhân hoặc nhóm
        - Ngôn từ lăng mạ, xúc phạm
        - Intimididation hoặc coercion
        - Discriminatory practices against protected groups
    """,
    
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: """
        Hate speech bao gồm:
        - Nội dung tấn công hoặc negative về một nhóm dựa trên:
          - Race, ethnicity, national origin
          - Religion
          - Sexual orientation, gender identity
          - Disability
          - Caste
        - Content that promotes exclusion or supremacy
        - Propaganda hoặc extremist content
    """,
    
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: """
        Sexually explicit content bao gồm:
        - Nội dung khiêu dâm
        - Descriptions of sexual acts
        - Adult content không phù hợp
        - Content liên quan đến exploitation
        - NSFW material
    """,
    
    HarmCategory.HARM_CATEGORY_DANGEROUS: """
        Dangerous content bao gồm:
        - Hướng dẫn tạo weapon
        - Content về self-harm hoặc suicide methods
        - Instructions cho harmful activities
        - Content promoting illegal activities
        - Terrorist or extremist propaganda
    """,
}
```

```typescript
// HarmCategory definitions (TypeScript)
import { HarmCategory, HarmBlockThreshold } from '@google/generative-ai';

enum HarmCategoryEnum {
  HARM_CATEGORY_HARASSMENT = 'HARM_CATEGORY_HARASSMENT',
  HARM_CATEGORY_HATE_SPEECH = 'HARM_CATEGORY_HATE_SPEECH',
  HARM_CATEGORY_SEXUALLY_EXPLICIT = 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
  HARM_CATEGORY_DANGEROUS = 'HARM_CATEGORY_DANGEROUS',
}

const HARM_CATEGORY_LABELS: Record<HarmCategory, string> = {
  [HarmCategory.HARM_CATEGORY_HARASSMENT]: 'Harassment',
  [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: 'Hate Speech',
  [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: 'Sexually Explicit',
  [HarmCategory.HARM_CATEGORY_DANGEROUS]: 'Dangerous Content',
};
```

### 2. HarmBlockThreshold - Mức Độ Chặn

HarmBlockThreshold xác định mức độ harm probability cần thiết để block content:

```python
# HarmBlockThreshold definitions
from enum import Enum


class HarmBlockThreshold(Enum):
    """
    Các mức độ block threshold.
    Mức độ được xếp theo thứ tự từ ít nghiêm ngặt đến nghiêm ngặt nhất.
    """
    
    # Không block any content (off)
    HARM_BLOCK_THRESHOLD_UNSPECIFIED = "HARM_BLOCK_THRESHOLD_UNSPECIFIED"
    
    # Block có harm probability >= NEGLIGIBLE
    # Negligible: gần như không có khả năng harmful
    HARM_BLOCK_THRESHOLD_NEGLIGIBLE = "HARM_BLOCK_THRESHOLD_NEGLIGIBLE"
    
    # Block có harm probability >= LOW
    # Low: có thể有害 nhưng không nghiêm trọng
    HARM_BLOCK_THRESHOLD_LOW = "HARM_BLOCK_THRESHOLD_LOW"
    
    # Block có harm probability >= MEDIUM
    # Medium: có khả năng harmful đáng kể
    HARM_BLOCK_THRESHOLD_MEDIUM = "HARM_BLOCK_THRESHOLD_MEDIUM"
    
    # Block có harm probability >= HIGH
    # High: có khả năng harmful cao
    HARM_BLOCK_THRESHOLD_HIGH = "HARM_BLOCK_THRESHOLD_HIGH"
    
    # Block có harm probability >= VERY_HIGH
    # Very High: gần như chắc chắn harmful
    HARM_BLOCK_THRESHOLD_VERY_HIGH = "HARM_BLOCK_THRESHOLD_VERY_HIGH"


class HarmProbability(Enum):
    """
    Harm probability levels - đây là output từ safety model.
    """
    HARM_PROBABILITY_UNSPECIFIED = "HARM_PROBABILITY_UNSPECIFIED"
    NEGLIGIBLE = "NEGLIGIBLE"      # 0-20%
    LOW = "LOW"                    # 20-40%
    MEDIUM = "MEDIUM"              # 40-60%
    HIGH = "HIGH"                 # 60-80%
    CRITICAL = "CRITICAL"         # 80-100%


# Block decision logic
def should_block(probability: HarmProbability, threshold: HarmBlockThreshold) -> bool:
    """
    Xác định xem content có nên bị block không.
    
    Block nếu probability >= threshold.
    """
    probability_order = {
        HarmProbability.HARM_PROBABILITY_UNSPECIFIED: 0,
        HarmProbability.NEGLIGIBLE: 1,
        HarmProbability.LOW: 2,
        HarmProbability.MEDIUM: 3,
        HarmProbability.HIGH: 4,
        HarmProbability.CRITICAL: 5,
    }
    
    threshold_order = {
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED: 0,
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_NEGLIGIBLE: 1,
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW: 2,
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM: 3,
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH: 4,
        HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH: 5,
    }
    
    return probability_order.get(probability, 0) >= threshold_order.get(threshold, 0)


# Test cases
test_cases = [
    # (probability, threshold, expected_block)
    (HarmProbability.NEGLIGIBLE, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_NEGLIGIBLE, True),
    (HarmProbability.LOW, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_NEGLIGIBLE, True),
    (HarmProbability.LOW, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW, True),
    (HarmProbability.MEDIUM, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW, True),
    (HarmProbability.MEDIUM, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM, True),
    (HarmProbability.LOW, HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM, False),
]

for prob, threshold, expected in test_cases:
    result = should_block(prob, threshold)
    status = "✓" if result == expected else "✗"
    print(f"{status} {prob.value} + {threshold.value} = {result}")
```

### 3. Safety Rating Structure

Mỗi content được đánh giá và trả về SafetyRating:

```python
# SafetyRating structure
from dataclasses import dataclass
from typing import Optional


@dataclass
class SafetyRating:
    """
    Safety rating cho một phần content.
    """
    category: str  # HarmCategory
    probability: str  # HarmProbability
    probability_score: float  # 0.0 - 1.0 (internal score)
    
    @property
    def blocked(self) -> bool:
        """Check nếu content bị blocked."""
        return self.probability in [
            "HARM_PROBABILITY_HIGH",
            "HARM_PROBABILITY_CRITICAL"
        ]
    
    def get_severity(self) -> str:
        """Get human-readable severity."""
        severity_map = {
            "HARM_PROBABILITY_UNSPECIFIED": "Not checked",
            "NEGLIGIBLE": "Very Low",
            "LOW": "Low",
            "MEDIUM": "Medium",
            "HIGH": "High",
            "CRITICAL": "Very High",
        }
        return severity_map.get(self.probability, "Unknown")


@dataclass
class PromptFeedback:
    """
    Feedback về prompt (input).
    """
    block_reason: Optional[str]
    safety_ratings: list[SafetyRating]
    
    @property
    def blocked(self) -> bool:
        """Check nếu prompt bị blocked."""
        return self.block_reason is not None


@dataclass
class CandidateSafetyRating:
    """
    Safety rating cho một candidate (output).
    """
    finish_reason: str
    safety_ratings: list[SafetyRating]
    
    @property
    def blocked(self) -> bool:
        """Check nếu candidate bị blocked."""
        return self.finish_reason in [
            "FINISH_REASON_SAFETY",
            "FINISH_REASON_RECITATION",
        ]
```

```typescript
// SafetyRating structure (TypeScript)
import { SafetyRating, HarmCategory, HarmProbability } from '@google/generative-ai';

interface SafetyRatingResult {
  category: HarmCategory;
  probability: HarmProbability;
  probabilityScore: number;
}

interface PromptFeedback {
  blockReason?: string;
  safetyRatings: SafetyRatingResult[];
}

interface CandidateSafetyRating {
  finishReason: string;
  safetyRatings: SafetyRatingResult[];
}

// Helper functions
function isContentBlocked(ratings: SafetyRatingResult[]): boolean {
  const highProbabilities = [
    HarmProbability.HARM_PROBABILITY_HIGH,
    HarmProbability.HARM_PROBABILITY_CRITICAL,
  ];
  
  return ratings.some(r => highProbabilities.includes(r.probability));
}

function getHighestProbability(ratings: SafetyRatingResult[]): HarmProbability {
  const probabilityOrder = [
    HarmProbability.NEGLIGIBLE,
    HarmProbability.LOW,
    HarmProbability.MEDIUM,
    HarmProbability.HIGH,
    HarmProbability.CRITICAL,
  ];
  
  let highest = HarmProbability.NEGLIGIBLE;
  
  for (const rating of ratings) {
    const currentIndex = probabilityOrder.indexOf(rating.probability);
    const highestIndex = probabilityOrder.indexOf(highest);
    
    if (currentIndex > highestIndex) {
      highest = rating.probability;
    }
  }
  
  return highest;
}
```

## Safety Configuration Patterns

### 1. Preset Configurations

```python
# src/safety/presets.py
"""
Preset safety configurations cho different use cases.
"""

from typing import Dict
from google.generativeai import types


class SafetyPreset(Enum):
    """Các preset safety configurations."""
    MINIMAL = "minimal"           # Almost no filtering
    STANDARD = "standard"         # Balanced filtering
    RESTRICTIVE = "restrictive"   # High filtering
    MAXIMUM = "maximum"           # Maximum filtering
    CUSTOM = "custom"             # Custom configuration


# Minimal filtering - cho developer tools, code generation
MINIMAL_SETTINGS: Dict[str, str] = {
    "HARASSMENT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
    "HATE_SPEECH": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
    "SEXUALLY_EXPLICIT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
    "DANGEROUS": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
}

# Standard filtering - cho general applications
STANDARD_SETTINGS: Dict[str, str] = {
    "HARASSMENT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
    "HATE_SPEECH": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
    "SEXUALLY_EXPLICIT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
    "DANGEROUS": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
}

# Restrictive filtering - cho content platforms
RESTRICTIVE_SETTINGS: Dict[str, str] = {
    "HARASSMENT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
    "HATE_SPEECH": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
    "SEXUALLY_EXPLICIT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
    "DANGEROUS": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
}

# Maximum filtering - cho sensitive applications
MAXIMUM_SETTINGS: Dict[str, str] = {
    "HARASSMENT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
    "HATE_SPEECH": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
    "SEXUALLY_EXPLICIT": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
    "DANGEROUS": types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
}


def get_safety_settings(preset: SafetyPreset) -> list:
    """
    Get safety settings theo preset.
    
    Returns:
        List of safety settings cho Gemini API
    """
    settings_map = {
        SafetyPreset.MINIMAL: MINIMAL_SETTINGS,
        SafetyPreset.STANDARD: STANDARD_SETTINGS,
        SafetyPreset.RESTRICTIVE: RESTRICTIVE_SETTINGS,
        SafetyPreset.MAXIMUM: MAXIMUM_SETTINGS,
    }
    
    if preset == SafetyPreset.CUSTOM:
        return []  # Caller phải provide custom settings
    
    settings = settings_map.get(preset, STANDARD_SETTINGS)
    
    return [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=settings["HARASSMENT"]
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=settings["HATE_SPEECH"]
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=settings["SEXUALLY_EXPLICIT"]
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS,
            threshold=settings["DANGEROUS"]
        ),
    ]
```

```typescript
// src/safety/presets.ts
/**
 * Safety preset configurations (TypeScript)
 */

import { 
  HarmCategory, 
  HarmBlockThreshold, 
  SafetySetting,
  HarmProbability 
} from '@google/generative-ai';

export enum SafetyPreset {
  MINIMAL = 'minimal',
  STANDARD = 'standard',
  RESTRICTIVE = 'restrictive',
  MAXIMUM = 'maximum',
  CUSTOM = 'custom',
}

const MINIMAL_SETTINGS: Record<string, HarmBlockThreshold> = {
  [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
};

const STANDARD_SETTINGS: Record<string, HarmBlockThreshold> = {
  [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
};

const RESTRICTIVE_SETTINGS: Record<string, HarmBlockThreshold> = {
  [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_HIGH_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_HIGH_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_HIGH_AND_ABOVE,
  [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_HIGH_AND_ABOVE,
};

const MAXIMUM_SETTINGS: Record<string, HarmBlockThreshold> = {
  [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_ONLY_HIGH,
};

export function getSafetySettings(preset: SafetyPreset): SafetySetting[] {
  const settingsMap: Record<string, Record<string, HarmBlockThreshold>> = {
    [SafetyPreset.MINIMAL]: MINIMAL_SETTINGS,
    [SafetyPreset.STANDARD]: STANDARD_SETTINGS,
    [SafetyPreset.RESTRICTIVE]: RESTRICTIVE_SETTINGS,
    [SafetyPreset.MAXIMUM]: MAXIMUM_SETTINGS,
  };
  
  if (preset === SafetyPreset.CUSTOM) {
    return [];
  }
  
  const settings = settingsMap[preset] || STANDARD_SETTINGS;
  
  return [
    { category: HarmCategory.HARM_CATEGORY_HARASSMENT, threshold: settings[HarmCategory.HARM_CATEGORY_HARASSMENT] },
    { category: HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold: settings[HarmCategory.HARM_CATEGORY_HATE_SPEECH] },
    { category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold: settings[HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT] },
    { category: HarmCategory.HARM_CATEGORY_DANGEROUS, threshold: settings[HarmCategory.HARM_CATEGORY_DANGEROUS] },
  ];
}
```

### 2. Dynamic Safety Configuration

```python
# src/safety/dynamic_config.py
"""
Dynamic safety configuration dựa trên context và user.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from google.generativeai import types


class UserTrustLevel(Enum):
    """Trust levels cho users."""
    ANONYMOUS = "anonymous"
    VERIFIED = "verified"
    PREMIUM = "premium"
    INTERNAL = "internal"


class ContentType(Enum):
    """Loại content được tạo."""
    GENERAL = "general"
    CREATIVE = "creative"
    TECHNICAL = "technical"
    SENSITIVE = "sensitive"


@dataclass
class SafetyContext:
    """Context cho safety decision."""
    user_trust_level: UserTrustLevel = UserTrustLevel.ANONYMOUS
    content_type: ContentType = ContentType.GENERAL
    age_group: Optional[str] = None  # "children", "teen", "adult"
    domain: Optional[str] = None  # "education", "entertainment", "business"


class DynamicSafetyConfigurator:
    """
    Dynamic safety configurator dựa trên context.
    """
    
    # Trust level multipliers (higher = more permissive)
    TRUST_MULTIPLIERS = {
        UserTrustLevel.ANONYMOUS: 0.5,    # Most restrictive
        UserTrustLevel.VERIFIED: 0.75,
        UserTrustLevel.PREMIUM: 1.0,
        UserTrustLevel.INTERNAL: 1.25,    # Most permissive
    }
    
    # Content type adjustments
    CONTENT_TYPE_ADJUSTMENTS = {
        ContentType.GENERAL: 0.0,       # Baseline
        ContentType.CREATIVE: 0.5,       # Allow more creative content
        ContentType.TECHNICAL: 0.25,     # Slightly more permissive for technical
        ContentType.SENSITIVE: -0.5,     # More restrictive
    }
    
    # Age group adjustments
    AGE_ADJUSTMENTS = {
        "children": -1.0,    # Maximum restriction
        "teen": -0.5,        # Strong restriction
        "adult": 0.0,        # Baseline
    }
    
    def get_safety_settings(
        self,
        context: SafetyContext
    ) -> List[types.SafetySetting]:
        """
        Generate safety settings dựa trên context.
        """
        # Calculate adjustments
        trust_multiplier = self.TRUST_MULTIPLIERS.get(
            context.user_trust_level, 1.0
        )
        content_adjustment = self.CONTENT_TYPE_ADJUSTMENTS.get(
            context.content_type, 0.0
        )
        age_adjustment = 0.0
        if context.age_group:
            age_adjustment = self.AGE_ADJUSTMENTS.get(context.age_group, 0.0)
        
        total_adjustment = (
            (trust_multiplier - 1.0) * 0.5 +
            content_adjustment * 0.3 +
            age_adjustment * 0.2
        )
        
        # Determine base threshold
        base_threshold = self._adjust_threshold(
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            total_adjustment
        )
        
        # Generate settings for all categories
        return self._generate_settings(base_threshold, context)
    
    def _adjust_threshold(
        self,
        base: types.HarmBlockThreshold,
        adjustment: float
    ) -> types.HarmBlockThreshold:
        """
        Adjust threshold dựa trên adjustment value.
        """
        thresholds = [
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_NEGLIGIBLE,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
        ]
        
        base_index = thresholds.index(base) if base in thresholds else 3
        new_index = max(0, min(len(thresholds) - 1, base_index + int(adjustment)))
        
        return thresholds[new_index]
    
    def _generate_settings(
        self,
        base_threshold: types.HarmBlockThreshold,
        context: SafetyContext
    ) -> List[types.SafetySetting]:
        """
        Generate safety settings for all categories.
        """
        # Adjust based on category sensitivity
        category_thresholds = {
            types.HarmCategory.HARM_CATEGORY_DANGEROUS: -1,  # Always more restrictive
            types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: 0,
            types.HarmCategory.HARM_CATEGORY_HARASSMENT: 0,
            types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: 1,  # Allow slightly more
        }
        
        settings = []
        for category, adjustment in category_thresholds.items():
            threshold = self._adjust_threshold(base_threshold, adjustment)
            settings.append(types.SafetySetting(
                category=category,
                threshold=threshold
            ))
        
        return settings
```

### 3. Safety Response Handler

```python
# src/safety/safety_handler.py
"""
Handler để process safety responses và make decisions.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from google.generativeai import types
import logging

logger = logging.getLogger(__name__)


@dataclass
class SafetyAnalysis:
    """Phân tích safety của một response."""
    is_blocked: bool
    block_reason: Optional[str]
    highest_probability: str
    highest_category: str
    all_ratings: List[Dict[str, Any]]
    severity_score: float  # 0.0 - 1.0


class SafetyResponseHandler:
    """
    Handler để process và analyze safety responses.
    """
    
    def __init__(self, callback: Optional[callable] = None):
        """
        Initialize handler.
        
        Args:
            callback: Optional callback được gọi khi content bị blocked
        """
        self.callback = callback
    
    def analyze_response(self, response) -> SafetyAnalysis:
        """
        Analyze safety của một Gemini response.
        
        Args:
            response: Response từ Gemini API
            
        Returns:
            SafetyAnalysis object
        """
        all_ratings = []
        highest_probability = "NEGLIGIBLE"
        highest_category = ""
        is_blocked = False
        block_reason = None
        
        # Check prompt feedback (input)
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
            pf = response.prompt_feedback
            
            if pf.block_reason:
                is_blocked = True
                block_reason = f"PROMPT: {pf.block_reason}"
                
                # Get ratings from prompt
                for rating in pf.safety_ratings:
                    all_ratings.append({
                        "type": "prompt",
                        "category": rating.category,
                        "probability": rating.probability,
                    })
            
            # Check if any rating is high
            for rating in pf.safety_ratings:
                if self._is_high_probability(rating.probability):
                    if self._compare_probability(rating.probability, highest_probability) > 0:
                        highest_probability = rating.probability
                        highest_category = rating.category
        
        # Check candidates (output)
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                # Check finish reason
                if hasattr(candidate, 'finish_reason'):
                    if candidate.finish_reason == "FINISH_REASON_SAFETY":
                        is_blocked = True
                        block_reason = "OUTPUT: Safety"
                    elif candidate.finish_reason == "FINISH_REASON_RECITATION":
                        is_blocked = True
                        block_reason = "OUTPUT: Recitation"
                
                # Get output ratings
                if hasattr(candidate, 'safety_ratings'):
                    for rating in candidate.safety_ratings:
                        all_ratings.append({
                            "type": "output",
                            "category": rating.category,
                            "probability": rating.probability,
                        })
                        
                        if self._is_high_probability(rating.probability):
                            if self._compare_probability(rating.probability, highest_probability) > 0:
                                highest_probability = rating.probability
                                highest_category = rating.category
        
        # Calculate severity score
        severity_score = self._calculate_severity_score(all_ratings)
        
        return SafetyAnalysis(
            is_blocked=is_blocked,
            block_reason=block_reason,
            highest_probability=highest_probability,
            highest_category=highest_category,
            all_ratings=all_ratings,
            severity_score=severity_score,
        )
    
    def handle_blocked_content(
        self,
        analysis: SafetyAnalysis,
        original_request: str
    ) -> str:
        """
        Handle khi content bị blocked.
        """
        logger.warning(
            f"Content blocked: {analysis.block_reason} "
            f"(probability: {analysis.highest_probability}, "
            f"category: {analysis.highest_category})"
        )
        
        # Call callback if configured
        if self.callback:
            try:
                self.callback(analysis, original_request)
            except Exception as e:
                logger.error(f"Error in safety callback: {e}")
        
        # Return appropriate message
        return self._get_blocked_message(analysis)
    
    def _is_high_probability(self, probability: str) -> bool:
        """Check nếu probability là HIGH hoặc CRITICAL."""
        return probability in [
            "HARM_PROBABILITY_HIGH",
            "HARM_PROBABILITY_CRITICAL",
        ]
    
    def _compare_probability(self, p1: str, p2: str) -> int:
        """Compare hai probabilities. Return positive if p1 > p2."""
        order = [
            "HARM_PROBABILITY_UNSPECIFIED",
            "NEGLIGIBLE",
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        ]
        
        idx1 = order.index(p1) if p1 in order else 0
        idx2 = order.index(p2) if p2 in order else 0
        
        return idx1 - idx2
    
    def _calculate_severity_score(self, ratings: List[Dict[str, Any]]) -> float:
        """
        Calculate overall severity score (0.0 - 1.0).
        """
        if not ratings:
            return 0.0
        
        score_map = {
            "HARM_PROBABILITY_UNSPECIFIED": 0.0,
            "NEGLIGIBLE": 0.1,
            "LOW": 0.25,
            "MEDIUM": 0.5,
            "HIGH": 0.75,
            "CRITICAL": 1.0,
        }
        
        max_score = 0.0
        for rating in ratings:
            score = score_map.get(rating.get('probability', ''), 0.0)
            max_score = max(max_score, score)
        
        return max_score
    
    def _get_blocked_message(self, analysis: SafetyAnalysis) -> str:
        """
        Get user-friendly message khi content bị blocked.
        """
        category_messages = {
            "HARM_CATEGORY_HARASSMENT": "nội dung quấy rối hoặc lăng mạ",
            "HARM_CATEGORY_HATE_SPEECH": "nội dung phân biệt đối xử",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "nội dung nhạy cảm",
            "HARM_CATEGORY_DANGEROUS": "nội dung có thể gây hại",
        }
        
        category = analysis.highest_category
        category_text = category_messages.get(category, "có vấn đề")
        
        return (
            "Xin lỗi, tôi không thể hoàn thành yêu cầu này vì nội dung "
            f"có vấn đề về: {category_text}. "
            "Vui lòng thử lại với nội dung khác."
        )


class SafetyAuditLogger:
    """
    Logger để audit safety-related events.
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file
        self.stats = {
            "total_requests": 0,
            "blocked_requests": 0,
            "blocked_by_category": {
                "HARASSMENT": 0,
                "HATE_SPEECH": 0,
                "SEXUALLY_EXPLICIT": 0,
                "DANGEROUS": 0,
            },
        }
    
    def log_request(
        self,
        request: str,
        analysis: SafetyAnalysis,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log một request cho audit.
        """
        self.stats["total_requests"] += 1
        
        if analysis.is_blocked:
            self.stats["blocked_requests"] += 1
            
            # Update category stats
            category = analysis.highest_category.replace("HARM_CATEGORY_", "")
            if category in self.stats["blocked_by_category"]:
                self.stats["blocked_by_category"][category] += 1
            
            # Log to file
            if self.log_file:
                self._write_to_file(request, analysis, user_id)
    
    def _write_to_file(
        self,
        request: str,
        analysis: SafetyAnalysis,
        user_id: Optional[str]
    ) -> None:
        """Write blocked request to log file."""
        import json
        from datetime import datetime
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "request": request[:500],  # Truncate
            "blocked": True,
            "block_reason": analysis.block_reason,
            "probability": analysis.highest_probability,
            "category": analysis.highest_category,
            "severity_score": analysis.severity_score,
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            logger.error(f"Error writing to safety log: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get safety statistics."""
        return {
            **self.stats,
            "block_rate": (
                self.stats["blocked_requests"] / max(1, self.stats["total_requests"])
            ) * 100
        }
```

## Best Practices

### 1. Production Safety Configuration

```python
# Best practices cho production safety

class ProductionSafetyManager:
    """
    Manager cho production safety configuration.
    """
    
    @staticmethod
    def get_recommended_settings() -> List[types.SafetySetting]:
        """
        Get recommended settings cho production.
        """
        return [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            ),
        ]
    
    @staticmethod
    def get_permissive_settings() -> List[types.SafetySetting]:
        """
        Get permissive settings (cho internal tools).
        """
        return [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS,
                threshold=types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
            ),
        ]
    
    @staticmethod
    def validate_safety_settings(settings: List[types.SafetySetting]) -> bool:
        """
        Validate safety settings configuration.
        """
        required_categories = {
            types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            types.HarmCategory.HARM_CATEGORY_DANGEROUS,
        }
        
        configured_categories = {s.category for s in settings}
        
        # Check all categories are configured
        if required_categories != configured_categories:
            missing = required_categories - configured_categories
            logger.warning(f"Missing safety categories: {missing}")
            return False
        
        # Check no category is set to UNSPECIFIED
        for setting in settings:
            if setting.threshold == types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED:
                logger.warning(f"Category {setting.category} has UNSPECIFIED threshold")
                return False
        
        return True
```

### 2. Graceful Degradation

```python
# Graceful degradation khi safety blocks content

class SafeContentGenerator:
    """
    Generator với graceful degradation khi content bị blocked.
    """
    
    def __init__(self, model, safety_handler: SafetyResponseHandler):
        self.model = model
        self.safety_handler = safety_handler
    
    async def generate_with_fallback(
        self,
        prompt: str,
        safety_settings: List[types.SafetySetting],
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Generate content với fallback nếu bị blocked.
        """
        current_settings = safety_settings.copy()
        
        for attempt in range(max_retries + 1):
            try:
                # Generate content
                response = self.model.generate_content(
                    prompt,
                    safety_settings=current_settings
                )
                
                # Analyze response
                analysis = self.safety_handler.analyze_response(response)
                
                if analysis.is_blocked:
                    if attempt < max_retries:
                        # Make settings more restrictive and retry
                        logger.info(f"Content blocked, attempt {attempt + 1}. Making more restrictive.")
                        current_settings = self._make_more_restrictive(current_settings)
                        continue
                    else:
                        # Max retries reached
                        return {
                            "success": False,
                            "blocked": True,
                            "message": self.safety_handler.handle_blocked_content(
                                analysis, prompt
                            ),
                            "analysis": analysis,
                        }
                else:
                    # Success
                    return {
                        "success": True,
                        "blocked": False,
                        "response": response,
                        "analysis": analysis,
                    }
                    
            except Exception as e:
                logger.error(f"Error generating content: {e}")
                return {
                    "success": False,
                    "error": str(e),
                }
        
        return {
            "success": False,
            "blocked": True,
            "message": "Unable to generate safe content after multiple attempts.",
        }
    
    def _make_more_restrictive(
        self,
        settings: List[types.SafetySetting]
    ) -> List[types.SafetySetting]:
        """
        Make safety settings more restrictive.
        """
        threshold_order = [
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_NEGLIGIBLE,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_LOW,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_MEDIUM,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_HIGH,
            types.HarmBlockThreshold.HARM_BLOCK_THRESHOLD_VERY_HIGH,
        ]
        
        new_settings = []
        for setting in settings:
            current_idx = threshold_order.index(setting.threshold) if setting.threshold in threshold_order else 3
            
            # Move to more restrictive (higher index)
            new_idx = min(len(threshold_order) - 1, current_idx + 1)
            
            new_settings.append(types.SafetySetting(
                category=setting.category,
                threshold=threshold_order[new_idx]
            ))
        
        return new_settings
```

### 3. Safety Monitoring Dashboard Data

```python
# Safety monitoring data structure

@dataclass
class SafetyMetrics:
    """Metrics cho safety monitoring."""
    
    timestamp: datetime
    total_requests: int
    blocked_requests: int
    block_rate: float
    
    # By category
    harassment_blocks: int
    hate_speech_blocks: int
    explicit_blocks: int
    dangerous_blocks: int
    
    # Severity distribution
    negligible_count: int
    low_count: int
    medium_count: int
    high_count: int
    critical_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage/reporting."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "total_requests": self.total_requests,
            "blocked_requests": self.blocked_requests,
            "block_rate": self.block_rate,
            "by_category": {
                "harassment": self.harassment_blocks,
                "hate_speech": self.hate_speech_blocks,
                "explicit": self.explicit_blocks,
                "dangerous": self.dangerous_blocks,
            },
            "severity_distribution": {
                "negligible": self.negligible_count,
                "low": self.low_count,
                "medium": self.medium_count,
                "high": self.high_count,
                "critical": self.critical_count,
            },
        }


class SafetyMetricsCollector:
    """
    Collector để aggregate safety metrics.
    """
    
    def __init__(self):
        self.reset_period = datetime.utcnow()
        self.requests = []
        self.blocked = []
    
    def record_request(
        self,
        request: str,
        analysis: SafetyAnalysis
    ) -> None:
        """Record một request."""
        self.requests.append({
            "timestamp": datetime.utcnow(),
            "analysis": analysis,
        })
        
        if analysis.is_blocked:
            self.blocked.append({
                "timestamp": datetime.utcnow(),
                "request": request,
                "analysis": analysis,
            })
    
    def get_metrics(self) -> SafetyMetrics:
        """Get current metrics."""
        now = datetime.utcnow()
        
        # Calculate counts by category
        category_counts = {
            "HARASSMENT": 0,
            "HATE_SPEECH": 0,
            "SEXUALLY_EXPLICIT": 0,
            "DANGEROUS": 0,
        }
        
        severity_counts = {
            "NEGLIGIBLE": 0,
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0,
        }
        
        for req in self.requests:
            analysis = req["analysis"]
            
            # Category counts (only for blocked)
            if analysis.is_blocked:
                cat = analysis.highest_category.replace("HARM_CATEGORY_", "")
                if cat in category_counts:
                    category_counts[cat] += 1
            
            # Severity counts
            prob = analysis.highest_probability.replace("HARM_PROBABILITY_", "")
            if prob in severity_counts:
                severity_counts[prob] += 1
        
        total = len(self.requests)
        blocked_count = len(self.blocked)
        
        return SafetyMetrics(
            timestamp=now,
            total_requests=total,
            blocked_requests=blocked_count,
            block_rate=(blocked_count / max(1, total)) * 100,
            harassment_blocks=category_counts["HARASSMENT"],
            hate_speech_blocks=category_counts["HATE_SPEECH"],
            explicit_blocks=category_counts["SEXUALLY_EXPLICIT"],
            dangerous_blocks=category_counts["DANGEROUS"],
            negligible_count=severity_counts["NEGLIGIBLE"],
            low_count=severity_counts["LOW"],
            medium_count=severity_counts["MEDIUM"],
            high_count=severity_counts["HIGH"],
            critical_count=severity_counts["CRITICAL"],
        )
    
    def reset(self) -> None:
        """Reset metrics."""
        self.reset_period = datetime.utcnow()
        self.requests = []
        self.blocked = []
```

## Common Patterns

### 1. Content Moderation Pipeline

```python
# src/safety/moderation_pipeline.py
"""
Content Moderation Pipeline
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ModerationDecision(Enum):
    """Decision từ moderation."""
    APPROVE = "approve"
    FLAG = "flag"
    REJECT = "reject"
    MANUAL_REVIEW = "manual_review"


@dataclass
class ModerationResult:
    """Result của moderation."""
    decision: ModerationDecision
    confidence: float
    reasons: List[str]
    category_scores: Dict[str, float]


class ContentModerationPipeline:
    """
    Pipeline để moderate content với multiple stages.
    """
    
    def __init__(self, gemini_model, config: Dict[str, Any]):
        self.model = gemini_model
        self.config = config
        
        # Safety thresholds
        self.auto_reject_threshold = config.get("auto_reject_threshold", 0.8)
        self.flag_threshold = config.get("flag_threshold", 0.5)
        self.manual_review_threshold = config.get("manual_review_threshold", 0.3)
    
    async def moderate(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> ModerationResult:
        """
        Moderate content through multiple stages.
        """
        # Stage 1: Quick keyword check
        keyword_result = self._keyword_check(content)
        if keyword_result["match"]:
            return ModerationResult(
                decision=ModerationDecision.AUTO_REJECT,
                confidence=0.95,
                reasons=keyword_result["reasons"],
                category_scores=keyword_result["scores"],
            )
        
        # Stage 2: Gemini safety check
        gemini_result = await self._gemini_safety_check(content)
        
        # Stage 3: Decision based on scores
        return self._make_decision(gemini_result, context)
    
    def _keyword_check(self, content: str) -> Dict[str, Any]:
        """
        Quick keyword-based check.
        """
        # Define blocked keywords (simplified)
        blocked_patterns = {
            "HARASSMENT": ["threat", "kill", "hurt"],
            "HATE_SPEECH": ["hate", "slur"],
            "DANGEROUS": ["bomb", "weapon", "attack"],
        }
        
        content_lower = content.lower()
        reasons = []
        scores = {}
        
        for category, keywords in blocked_patterns.items():
            matches = [kw for kw in keywords if kw in content_lower]
            if matches:
                scores[category] = len(matches) / len(keywords)
                reasons.append(f"Found blocked keywords: {', '.join(matches)}")
            else:
                scores[category] = 0.0
        
        return {
            "match": any(scores.values()),
            "reasons": reasons,
            "scores": scores,
        }
    
    async def _gemini_safety_check(self, content: str) -> Dict[str, Any]:
        """
        Use Gemini để check safety.
        """
        prompt = f"""
Evaluate the following content for safety issues.
Content: {content}

Categories to check:
- HARASSMENT: Bullying, threatening, harassing language
- HATE_SPEECH: Discriminatory or hateful content
- SEXUALLY_EXPLICIT: Adult or explicit content
- DANGEROUS: Content promoting harm or illegal activities

Return a JSON with:
{{
  "scores": {{
    "HARASSMENT": 0.0-1.0,
    "HATE_SPEECH": 0.0-1.0,
    "SEXUALLY_EXPLICIT": 0.0-1.0,
    "DANGEROUS": 0.0-1.0
  }},
  "summary": "brief summary",
  "reasons": ["list of specific issues if any"]
}}
"""
        
        response = self.model.generate_content(prompt)
        
        # Parse response (simplified)
        # In production, use structured output
        return {"scores": {}, "summary": response.text, "reasons": []}
    
    def _make_decision(
        self,
        safety_result: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> ModerationResult:
        """
        Make moderation decision based on scores.
        """
        scores = safety_result.get("scores", {})
        
        # Get max score across categories
        max_score = max(scores.values()) if scores else 0.0
        
        # Decision logic
        if max_score >= self.auto_reject_threshold:
            return ModerationResult(
                decision=ModerationDecision.REJECT,
                confidence=max_score,
                reasons=safety_result.get("reasons", []),
                category_scores=scores,
            )
        
        if max_score >= self.flag_threshold:
            return ModerationResult(
                decision=ModerationDecision.FLAG,
                confidence=max_score,
                reasons=safety_result.get("reasons", []),
                category_scores=scores,
            )
        
        if max_score >= self.manual_review_threshold:
            return ModerationResult(
                decision=ModerationDecision.MANUAL_REVIEW,
                confidence=max_score,
                reasons=safety_result.get("reasons", []),
                category_scores=scores,
            )
        
        return ModerationResult(
            decision=ModerationDecision.APPROVE,
            confidence=1.0 - max_score,
            reasons=[],
            category_scores=scores,
        )
```

### 2. Age-Appropriate Content Filter

```typescript
// src/safety/age-filter.ts
/**
 * Age-appropriate content filter (TypeScript)
 */

import { HarmCategory, HarmBlockThreshold, SafetySetting } from '@google/generative-ai';

export enum AgeGroup {
  CHILDREN = 'children',      // Under 13
  TEEN = 'teen',              // 13-17
  YOUNG_ADULT = 'young_adult', // 18-24
  ADULT = 'adult',            // 25+
}

interface AgeAppropriateConfig {
  ageGroup: AgeGroup;
  contentType: 'general' | 'educational' | 'creative';
}

export class AgeAppropriateFilter {
  /**
   * Get safety settings cho age-appropriate filtering
   */
  static getSettings(config: AgeAppropriateConfig): SafetySetting[] {
    const { ageGroup, contentType } = config;
    
    // Base threshold varies by age
    const baseThresholds = this.getBaseThresholds(ageGroup);
    
    // Adjust for content type
    const adjustments = this.getContentTypeAdjustments(contentType);
    
    // Generate settings
    const categories = [
      HarmCategory.HARM_CATEGORY_HARASSMENT,
      HarmCategory.HARM_CATEGORY_HATE_SPEECH,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
      HarmCategory.HARM_CATEGORY_DANGEROUS,
    ];
    
    return categories.map(category => ({
      category,
      threshold: this.adjustThreshold(
        baseThresholds[category],
        adjustments[category]
      ),
    }));
  }
  
  private static getBaseThresholds(ageGroup: AgeGroup): Record<HarmCategory, HarmBlockThreshold> {
    const thresholdsByAge: Record<AgeGroup, Record<HarmCategory, HarmBlockThreshold>> = {
      [AgeGroup.CHILDREN]: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
      },
      [AgeGroup.TEEN]: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
      },
      [AgeGroup.YOUNG_ADULT]: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      },
      [AgeGroup.ADULT]: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      },
    };
    
    return thresholdsByAge[ageGroup];
  }
  
  private static getContentTypeAdjustments(contentType: string): Record<HarmCategory, number> {
    // Adjustment values: positive = more permissive, negative = more restrictive
    const adjustments: Record<string, Record<HarmCategory, number>> = {
      general: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: 0,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: 0,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: 0,
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: 0,
      },
      educational: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: 0,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: 0,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: -1, // More restrictive
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: 0,
      },
      creative: {
        [HarmCategory.HARM_CATEGORY_HARASSMENT]: 0,
        [HarmCategory.HARM_CATEGORY_HATE_SPEECH]: 0,
        [HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT]: 1, // More permissive for creative
        [HarmCategory.HARM_CATEGORY_DANGEROUS]: -1, // More restrictive
      },
    };
    
    return adjustments[contentType] || adjustments.general;
  }
  
  private static adjustThreshold(
    base: HarmBlockThreshold,
    adjustment: number
  ): HarmBlockThreshold {
    const thresholdOrder = [
      HarmBlockThreshold.HARM_BLOCK_THRESHOLD_UNSPECIFIED,
      HarmBlockThreshold.BLOCK_NONE,
      HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
      HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      HarmBlockThreshold.BLOCK_HIGH_AND_ABOVE,
      HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ];
    
    const baseIndex = thresholdOrder.indexOf(base);
    const newIndex = Math.max(0, Math.min(thresholdOrder.length - 1, baseIndex + adjustment));
    
    return thresholdOrder[newIndex];
  }
}
```

## Examples

### 1. Complete Safety System - Python

```python
# src/examples/safety_system.py
"""
Complete Safety System Example
"""

import asyncio
from typing import List, Dict, Any, Optional
from google.generativeai import GenerativeModel, types
from src.config.gemini_config import GeminiConfig, initialize_gemini, create_model
from src.safety.presets import get_safety_settings, SafetyPreset
from src.safety.safety_handler import SafetyResponseHandler, SafetyAuditLogger
from src.safety.dynamic_config import DynamicSafetyConfigurator, SafetyContext, UserTrustLevel


class SafeGeminiService:
    """
    Complete service với safety integration.
    """
    
    def __init__(self, config: GeminiConfig):
        # Initialize Gemini
        initialize_gemini(config)
        self.model = create_model(config)
        
        # Initialize safety components
        self.safety_handler = SafetyResponseHandler(callback=self._on_blocked)
        self.audit_logger = SafetyAuditLogger(log_file="safety_audit.jsonl")
        self.dynamic_config = DynamicSafetyConfigurator()
    
    def _on_blocked(self, analysis, request: str) -> None:
        """
        Callback khi content bị blocked.
        """
        print(f"Blocked request detected: {analysis.block_reason}")
    
    async def generate(
        self,
        prompt: str,
        safety_preset: SafetyPreset = SafetyPreset.STANDARD,
        context: Optional[SafetyContext] = None
    ) -> Dict[str, Any]:
        """
        Generate content với safety handling.
        """
        # Get safety settings
        if context:
            safety_settings = self.dynamic_config.get_safety_settings(context)
        else:
            safety_settings = get_safety_settings(safety_preset)
        
        try:
            # Generate content
            response = self.model.generate_content(
                prompt,
                safety_settings=safety_settings
            )
            
            # Analyze response
            analysis = self.safety_handler.analyze_response(response)
            
            # Log for audit
            self.audit_logger.log_request(prompt, analysis)
            
            if analysis.is_blocked:
                return {
                    "success": False,
                    "blocked": True,
                    "message": self.safety_handler.handle_blocked_content(
                        analysis, prompt
                    ),
                    "analysis": analysis,
                }
            
            return {
                "success": True,
                "blocked": False,
                "response": response.text,
                "analysis": analysis,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    def get_safety_stats(self) -> Dict[str, Any]:
        """Get safety statistics."""
        return self.audit_logger.get_stats()


async def main():
    """Example usage."""
    
    # Initialize service
    config = GeminiConfig.from_env()
    service = SafeGeminiService(config)
    
    # Example 1: Standard request
    print("=" * 50)
    print("Example 1: Normal Request")
    print("=" * 50)
    
    result = await service.generate(
        "Explain quantum computing in simple terms.",
        safety_preset=SafetyPreset.STANDARD
    )
    
    if result["success"]:
        print(f"Response: {result['response'][:200]}...")
        print(f"Safety analysis: {result['analysis'].severity_score}")
    else:
        print(f"Error: {result.get('error') or result.get('message')}")
    
    # Example 2: Request with context
    print("\n" + "=" * 50)
    print("Example 2: Context-Aware Request")
    print("=" * 50)
    
    context = SafetyContext(
        user_trust_level=UserTrustLevel.PREMIUM,
        content_type="creative",
        age_group="adult"
    )
    
    result = await service.generate(
        "Write a creative story with some tension.",
        context=context
    )
    
    if result["success"]:
        print(f"Response: {result['response'][:200]}...")
        print(f"Safety analysis: {result['analysis'].severity_score}")
    else:
        print(f"Blocked: {result.get('message')}")
    
    # Example 3: Get stats
    print("\n" + "=" * 50)
    print("Safety Statistics")
    print("=" * 50)
    
    stats = service.get_safety_stats()
    print(f"Total requests: {stats['total_requests']}")
    print(f"Blocked: {stats['blocked_requests']}")
    print(f"Block rate: {stats['block_rate']:.2f}%")


if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Complete Safety System - TypeScript

```typescript
// src/examples/safety-system.ts
/**
 * Complete Safety System (TypeScript)
 */

import { 
  GoogleGenerativeAI, 
  HarmCategory, 
  HarmBlockThreshold, 
  SafetySetting,
  GenerateContentResult 
} from '@google/generative-ai';
import { SafetyPreset, getSafetySettings } from '../safety/presets';
import { 
  SafetyResponseHandler, 
  SafetyAuditLogger, 
  SafetyAnalysis 
} from '../safety/safety-handler';
import { 
  DynamicSafetyConfigurator, 
  SafetyContext as DynamicSafetyContext, 
  UserTrustLevel,
  ContentType 
} from '../safety/dynamic-config';

interface GenerationResult {
  success: boolean;
  blocked?: boolean;
  response?: string;
  message?: string;
  analysis?: SafetyAnalysis;
  error?: string;
}

export class SafeGeminiService {
  private client: GoogleGenerativeAI;
  private model: ReturnType<GoogleGenerativeAI['getGenerativeModel']>;
  private safetyHandler: SafetyResponseHandler;
  private auditLogger: SafetyAuditLogger;
  private dynamicConfig: DynamicSafetyConfigurator;
  
  constructor(apiKey: string) {
    this.client = new GoogleGenerativeAI(apiKey);
    this.model = this.client.getGenerativeModel({
      model: 'gemini-2.0-flash',
    });
    
    this.safetyHandler = new SafetyResponseHandler(
      this.handleBlocked.bind(this)
    );
    this.auditLogger = new SafetyAuditLogger('safety_audit.jsonl');
    this.dynamicConfig = new DynamicSafetyConfigurator();
  }
  
  private handleBlocked(analysis: SafetyAnalysis, request: string): void {
    console.log(`Blocked request detected: ${analysis.blockReason}`);
  }
  
  async generate(
    prompt: string,
    safetyPreset: SafetyPreset = SafetyPreset.STANDARD,
    context?: DynamicSafetyContext
  ): Promise<GenerationResult> {
    // Get safety settings
    let safetySettings: SafetySetting[];
    
    if (context) {
      safetySettings = this.dynamicConfig.getSafetySettings(context);
    } else {
      safetySettings = getSafetySettings(safetyPreset);
    }
    
    try {
      // Generate content
      const response = await this.model.generateContent({
        contents: [{ role: 'user', parts: [{ text: prompt }] }],
        safetySettings,
      });
      
      // Analyze response
      const analysis = this.safetyHandler.analyzeResponse(response);
      
      // Log for audit
      this.auditLogger.logRequest(prompt, analysis);
      
      if (analysis.isBlocked) {
        return {
          success: false,
          blocked: true,
          message: this.safetyHandler.handleBlockedContent(analysis, prompt),
          analysis,
        };
      }
      
      // Extract text
      const text = response.response?.text() || '';
      
      return {
        success: true,
        blocked: false,
        response: text,
        analysis,
      };
      
    } catch (error) {
      return {
        success: false,
        error: String(error),
      };
    }
  }
  
  getSafetyStats(): Record<string, any> {
    return this.auditLogger.getStats();
  }
}

// Usage
async function main() {
  const service = new SafeGeminiService(process.env.GEMINI_API_KEY!);
  
  // Normal request
  const result1 = await service.generate(
    'Explain machine learning in simple terms.'
  );
  
  if (result1.success) {
    console.log('Response:', result1.response?.substring(0, 200));
  }
  
  // Get stats
  const stats = service.getSafetyStats();
  console.log('Stats:', stats);
}

main().catch(console.error);
```

## Troubleshooting

### Các Vấn Đề Thường Gặp

**1. "Content unexpectedly blocked"**

```
Nguyên nhân: Safety threshold quá restrictive
Giải pháp:
- Kiểm tra safety settings configuration
- Xem xét giảm threshold cho một số categories
- Test với different thresholds
- Kiểm tra prompt có chứa từ ngữ sensitive không
```

**2. "Safety callback not called"**

```
Nguyên nhân: Callback không được registered hoặc có lỗi
Giải pháp:
- Verify callback được truyền vào constructor
- Check callback không throw exceptions
- Verify response actually triggers safety block
```

**3. "Inconsistent blocking behavior"**

```
Nguyên nhân: Settings không được applied đúng
Giải pháp:
- Verify safety_settings được truyền đúng cho mỗi request
- Check model không override settings
- Log settings được sử dụng để debug
```

**4. "Safety logs not writing"**

```
Nguyên nhân: File permissions hoặc path issue
Giải pháp:
- Check directory tồn tại và có write permissions
- Verify log file path đúng
- Check disk space
- Implement fallback logging
```

**5. "High false positive rate"**

```
Nguyên nhân: Threshold quá low hoặc content patterns trigger false positives
Giải pháp:
- Analyze blocked content patterns
- Consider using more permissive settings
- Implement human review queue
- Tune thresholds based on false positive analysis
```

## References

### Official Documentation

- [Safety Settings Documentation](https://ai.google.dev/docs/safety_settings)
- [Safety Ratings Guide](https://ai.google.dev/docs/safety_ratings)
- [Content Filtering Best Practices](https://ai.google.dev/docs/content_filtering)

### Related Documents

- `@gemini-api-setup.md` - Setup và configuration
- `@security.mdc` - Security principles
- `@monitoring.mdc` - Monitoring và logging
- `@authentication.mdc` - Authentication patterns
