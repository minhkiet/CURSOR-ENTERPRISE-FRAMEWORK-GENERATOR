# Task Analyzer Python Integration
# Advanced task analysis with full language support

import json
import re
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════════════════════════

@dataclass
class LanguageDetection:
    language: str
    confidence: float
    scores: Dict[str, float]
    is_translated: bool
    original_text: str
    translated_text: str

@dataclass
class IntentAnalysis:
    primary_intent: str
    intent_scores: Dict[str, float]
    intent_confidence: float
    domains: List[str]
    primary_domain: str

@dataclass
class SkillMatch:
    skill_id: str
    skill_name: str
    confidence: float
    role: str  # primary, secondary, mandatory, overlay

@dataclass
class SkillDetection:
    matched_skills: List[str]
    skill_confidences: Dict[str, float]
    primary_skill: Optional[str]
    mandatory_skills: List[SkillMatch]
    total_detected: int

@dataclass
class DependencyCheck:
    python: List[str]
    npm: List[str]
    system: List[str]
    missing: List[str]
    installed: List[str]

@dataclass
class TaskManifest:
    version: str
    generated_at: str
    request_id: str
    input: Dict[str, Any]
    analysis: Dict[str, Any]
    tasks: List[Dict[str, Any]]
    execution_order: List[str]
    output: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════════════════════════════
# LANGUAGE DETECTION
# ═══════════════════════════════════════════════════════════════════════════════════════

class LanguageDetector:
    """Detects source language of requests"""
    
    SIGNALS = {
        "vietnamese": {
            "keywords": ["tạo", "xây dựng", "cải thiện", "sửa lỗi", "thiết kế", "app", "web", "trang", "code", "lập trình", "của", "là", "được", "với", "và"],
            "patterns": ["^tạo ", "^xây ", "^cải ", "^sửa ", "^thiết kế"]
        },
        "chinese": {
            "has_chars": "[\u4e00-\u9fff]",
            "keywords": ["创建", "构建", "改进", "修复", "设计", "应用", "网站", "代码"]
        },
        "japanese": {
            "has_chars": "[\u3040-\u309f\u30a0-\u30ff]",
            "keywords": ["作成", "構築", "開発", "設計", "アプリ"]
        },
        "korean": {
            "has_chars": "[\uac00-\ud7af]",
            "keywords": ["생성", "구축", "개발", "설계", "앱"]
        },
        "english": {
            "keywords": ["create", "build", "improve", "fix", "design", "app", "web", "page", "code", "with", "and", "for"]
        }
    }
    
    @classmethod
    def detect(cls, text: str) -> LanguageDetection:
        scores = {}
        text_lower = text.lower()
        
        # Check Vietnamese
        score = 0
        for kw in cls.SIGNALS["vietnamese"]["keywords"]:
            if kw in text_lower:
                score += 2
        for pattern in cls.SIGNALS["vietnamese"]["patterns"]:
            if re.search(pattern, text_lower):
                score += 3
        scores["vietnamese"] = score
        
        # Check English
        score = 0
        for kw in cls.SIGNALS["english"]["keywords"]:
            if kw in text_lower:
                score += 1
        scores["english"] = score
        
        # Check CJK characters
        for lang, pattern in [("chinese", "[\u4e00-\u9fff]"), ("japanese", "[\u3040-\u309f\u30a0-\u30ff]"), ("korean", "[\uac00-\ud7af]")]:
            if re.search(pattern, text):
                scores[lang] = 10
        
        # Find best match
        best_lang = max(scores, key=scores.get)
        confidence = min(1.0, scores[best_lang] / 10)
        
        return LanguageDetection(
            language=best_lang,
            confidence=confidence,
            scores=scores,
            is_translated=False,
            original_text=text,
            translated_text=text
        )

# ═══════════════════════════════════════════════════════════════════════════════════════
# TRANSLATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════════════

class Translator:
    """Translates requests to English"""
    
    VI_TO_EN = {
        # Intent verbs
        "tạo": "create",
        "xây dựng": "build",
        "cải thiện": "improve",
        "sửa lỗi": "fix bug",
        "sửa": "fix",
        "thiết kế": "design",
        "phát triển": "develop",
        "thêm": "add",
        "xóa": "delete",
        "thay đổi": "change",
        "cập nhật": "update",
        "nâng cấp": "upgrade",
        "tối ưu": "optimize",
        
        # Tech terms
        "trang web": "website",
        "trang": "page",
        "app": "app",
        "ứng dụng": "application",
        "hệ thống": "system",
        "component": "component",
        "thành phần": "component",
        "chức năng": "feature",
        "tính năng": "feature",
        "giao diện": "UI",
        "database": "database",
        "cơ sở dữ liệu": "database",
        "backend": "backend",
        "frontend": "frontend",
        "code": "code",
        "lập trình": "programming",
        "mã nguồn": "source code",
        "api": "API",
        
        # UI terms
        "nút": "button",
        "nút bấm": "button",
        "ô nhập": "input field",
        "trường nhập": "input field",
        "biểu mẫu": "form",
        "bảng": "table",
        "menu": "menu",
        "thanh điều hướng": "navigation bar",
        "popup": "popup",
        "modal": "modal",
        "thông báo": "notification",
        
        # Project types
        "landing page": "landing page",
        "trang đích": "landing page",
        "portfolio": "portfolio",
        "danh mục": "portfolio",
        "blog": "blog",
        "dashboard": "dashboard",
        "trang quản trị": "admin dashboard",
        "cửa hàng": "store",
        "thương mại điện tử": "e-commerce",
        
        # Quality terms
        "đẹp": "beautiful",
        "hiện đại": "modern",
        "nhanh": "fast",
        "bảo mật": "secure",
        "an toàn": "safe",
        "dễ sử dụng": "easy to use",
        
        # Connectors
        "với": "with",
        "và": "and",
        "hoặc": "or",
        "để": "to",
        "cho": "for",
        "của": "of",
        "là": "is",
        "được": "is",
        "này": "this",
        "đó": "that",
        "các": "these",
        "những": "those",
        
        # Payment
        "thanh toán": "payment",
        "ví điện tử": "e-wallet",
        "VNPay": "VNPay",
        "MoMo": "MoMo",
        "SePay": "SePay",
        "PayOS": "PayOS",
        "ZaloPay": "ZaloPay",
        "VietQR": "VietQR",
        
        # Address
        "địa chỉ": "address",
        "địa chỉ Việt Nam": "Vietnam address",
        "tỉnh": "province",
        "thành phố": "city",
        "quận": "district",
        "huyện": "district",
        "phường": "ward",
        "xã": "commune"
    }
    
    @classmethod
    def translate(cls, text: str, source_lang: str) -> str:
        if source_lang != "vietnamese":
            return text
        
        result = text
        
        # Apply translations (longer phrases first)
        sorted_phrases = sorted(cls.VI_TO_EN.keys(), key=len, reverse=True)
        
        for phrase in sorted_phrases:
            pattern = r'\b' + re.escape(phrase) + r'\b'
            result = re.sub(pattern, cls.VI_TO_EN[phrase], result, flags=re.IGNORECASE)
        
        return result

# ═══════════════════════════════════════════════════════════════════════════════════════
# INTENT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════════════

class IntentAnalyzer:
    """Analyzes request intent"""
    
    INTENTS = {
        "build": {
            "keywords": ["create", "build", "make", "add", "implement", "develop", "generate", "tạo", "xây dựng", "创建", "構築"],
            "weight": 0.25
        },
        "redesign": {
            "keywords": ["improve", "upgrade", "redesign", "modernize", "enhance", "refresh", "cải thiện", "改进", "改善"],
            "weight": 0.20
        },
        "fix": {
            "keywords": ["fix", "bug", "error", "issue", "problem", "repair", "debug", "patch", "sửa lỗi", "修复"],
            "weight": 0.20
        },
        "review": {
            "keywords": ["review", "check", "audit", "inspect", "analyze", "assess", "evaluate", "kiểm tra", "审查"],
            "weight": 0.15
        },
        "explain": {
            "keywords": ["explain", "how", "what", "why", "understand", "clarify", "describe", "giải thích", "解释"],
            "weight": 0.10
        },
        "security": {
            "keywords": ["security", "vulnerability", "auth", "JWT", "OAuth", "bảo mật", "安全", "penetration", "pentest"],
            "weight": 0.10
        }
    }
    
    DOMAINS = {
        "frontend": ["frontend", "UI", "UX", "landing", "page", "component", "button", "form", "react", "vue", "angular", "next", "nuxt"],
        "backend": ["backend", "API", "server", "endpoint", "database", "REST", "GraphQL"],
        "security": ["security", "auth", "login", "password", "JWT", "OAuth", "XSS", "vulnerability"],
        "payment": ["payment", "checkout", "stripe", "MoMo", "SePay", "PayOS", "VNPay", "ZaloPay", "VietQR", "thanh toán"],
        "mobile": ["mobile", "app", "iOS", "Android", "react native", "flutter"],
        "database": ["database", "SQL", "PostgreSQL", "MySQL", "MongoDB", "migration"],
        "devops": ["docker", "kubernetes", "CI/CD", "deployment", "AWS", "Azure", "GCP"],
        "knowledge": ["knowledge base", "RAG", "document", "wiki", "FAQ", "weknora", "rag"],
        "ocr": ["ocr", "text extraction", "image to text", "scanned"]
    }
    
    @classmethod
    def analyze(cls, text: str) -> IntentAnalysis:
        text_lower = text.lower()
        scores = {}
        
        for intent_name, intent_data in cls.INTENTS.items():
            score = 0
            for kw in intent_data["keywords"]:
                if kw in text_lower:
                    score += 1
            scores[intent_name] = score
        
        max_score = max(scores.values()) if scores else 0
        primary_intent = max(scores, key=scores.get) if scores else "build"
        confidence = min(1.0, max_score / 3) if max_score > 0 else 0.5
        
        # Detect domains
        domains = []
        for domain_name, patterns in cls.DOMAINS.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    if domain_name not in domains:
                        domains.append(domain_name)
                    break
        
        return IntentAnalysis(
            primary_intent=primary_intent,
            intent_scores=scores,
            intent_confidence=confidence,
            domains=domains,
            primary_domain=domains[0] if domains else "general"
        )

# ═══════════════════════════════════════════════════════════════════════════════════════
# SKILL DETECTION
# ═══════════════════════════════════════════════════════════════════════════════════════

class SkillDetector:
    """Detects skills based on request content"""
    
    SKILLS = {
        "frontend-taste": {
            "name": "Frontend Taste",
            "keywords": ["landing page", "portfolio", "homepage", "marketing site", "SaaS landing", "greenfield", "beautiful", "premium", "trang đích", "danh mục"],
            "confidence_threshold": 0.75,
            "mandatory": False,
            "always_with_frontend": True
        },
        "frontend-redesign": {
            "name": "Frontend Redesign",
            "keywords": ["redesign", "upgrade", "improve existing", "modernize", "enhance", "refresh", "cải thiện", "hiện tại", "现有"],
            "confidence_threshold": 0.75,
            "mandatory": False,
            "always_with_frontend": True
        },
        "full-output": {
            "name": "Full Output",
            "keywords": ["full implementation", "complete", "not skeleton", "no TODO", "entire", "triển khai đầy đủ", "hoàn chỉnh", "toàn bộ"],
            "confidence_threshold": 0.80,
            "mandatory": False,
            "always_with_frontend": False
        },
        "frontend-review": {
            "name": "Frontend Review",
            "keywords": ["review", "quality check", "audit", "taste check", "kiểm tra", "đánh giá", "chất lượng"],
            "confidence_threshold": 0.70,
            "mandatory": True,
            "always_with_frontend": True
        },
        "security-review": {
            "name": "Security Review",
            "keywords": ["security", "vulnerability", "XSS", "SQL injection", "auth", "JWT", "OAuth", "pentest", "OWASP", "bảo mật", "安全"],
            "confidence_threshold": 0.85,
            "mandatory": False,
            "always_with_frontend": False
        },
        "vietnam-payment-review": {
            "name": "Vietnam Payment Review",
            "keywords": ["MoMo", "SePay", "PayOS", "VNPay", "ZaloPay", "VietQR", "thanh toán Việt Nam", "payment Vietnam"],
            "confidence_threshold": 0.90,
            "mandatory": False,
            "always_with_frontend": False
        },
        "karpathy-coding": {
            "name": "Karpathy Coding",
            "keywords": ["vibe code", "just do it", "simple", "straightforward", "don't overthink", "minimal"],
            "confidence_threshold": 0.70,
            "mandatory": True,
            "always_with_frontend": False
        },
        "ponytail": {
            "name": "Ponytail",
            "keywords": ["less code", "yagni", "over-engineering", "minimal", "simple", "đơn giản", "ít code"],
            "confidence_threshold": 0.80,
            "mandatory": False,
            "always_with_frontend": False
        },
        "visual-explainer": {
            "name": "Visual Explainer",
            "keywords": ["diagram", "architecture overview", "flowchart", "diff review", "visual", "sơ đồ", "lưu đồ"],
            "confidence_threshold": 0.85,
            "mandatory": False,
            "always_with_frontend": False
        },
        "weknora-kb": {
            "name": "WeKnora Knowledge Base",
            "keywords": ["knowledge base", "RAG", "document q&a", "wiki", "FAQ", "weknora", "rag", "cơ sở tri thức"],
            "confidence_threshold": 0.90,
            "mandatory": False,
            "always_with_frontend": False
        },
        "pixelrag": {
            "name": "PixelRAG",
            "keywords": ["pixelrag", "visual rag", "screenshot rag", "table extraction", "chart extraction", "đọc bảng", "đọc biểu đồ"],
            "confidence_threshold": 0.90,
            "mandatory": False,
            "always_with_frontend": False
        },
        "document-ocr": {
            "name": "Document OCR",
            "keywords": ["ocr", "text extraction", "image to text", "scanned document", "đọc text", "trích xuất text"],
            "confidence_threshold": 0.90,
            "mandatory": False,
            "always_with_frontend": False
        },
        "vietnam-address": {
            "name": "Vietnam Address",
            "keywords": ["vietnam address", "province", "district", "ward", "địa chỉ Việt Nam", "tỉnh", "thành phố", "quận", "huyện"],
            "confidence_threshold": 0.90,
            "mandatory": False,
            "always_with_frontend": False
        }
    }
    
    @classmethod
    def detect(cls, text: str, intent_analysis: IntentAnalysis) -> SkillDetection:
        text_lower = text.lower()
        matched_skills = []
        skill_confidences = {}
        mandatory_skills = []
        
        for skill_id, skill_data in cls.SKILLS.items():
            score = 0
            for kw in skill_data["keywords"]:
                if kw.lower() in text_lower:
                    score += 1
            
            confidence = score / len(skill_data["keywords"]) if skill_data["keywords"] else 0
            
            # Check if mandatory
            if skill_data["mandatory"]:
                mandatory_skills.append(SkillMatch(
                    skill_id=skill_id,
                    skill_name=skill_data["name"],
                    confidence=1.0,
                    role="mandatory"
                ))
                matched_skills.append(skill_id)
                skill_confidences[skill_id] = 1.0
            # Check threshold
            elif confidence >= skill_data["confidence_threshold"]:
                # Check if always_with_frontend
                if skill_data["always_with_frontend"] and "frontend" in intent_analysis.domains:
                    matched_skills.append(skill_id)
                    skill_confidences[skill_id] = confidence
                elif not skill_data["always_with_frontend"]:
                    matched_skills.append(skill_id)
                    skill_confidences[skill_id] = confidence
        
        # Determine primary skill
        primary_skill = None
        highest_confidence = 0
        for skill_id in matched_skills:
            if skill_id not in ["karpathy-coding", "frontend-review"]:
                if skill_confidences.get(skill_id, 0) > highest_confidence:
                    highest_confidence = skill_confidences[skill_id]
                    primary_skill = skill_id
        
        return SkillDetection(
            matched_skills=matched_skills,
            skill_confidences=skill_confidences,
            primary_skill=primary_skill,
            mandatory_skills=mandatory_skills,
            total_detected=len(matched_skills)
        )

# ═══════════════════════════════════════════════════════════════════════════════════════
# TASK GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════════════

class TaskGenerator:
    """Generates task manifests based on detected skills"""
    
    GATE_MAPPING = {
        "karpathy-coding": {"pre": ["karpathy-pre"], "post": ["karpathy-post"]},
        "frontend-taste": {"pre": ["taste-pre"], "post": ["taste-post"]},
        "frontend-redesign": {"pre": ["redesign-pre"], "post": ["redesign-post"]},
        "full-output": {"pre": ["fulloutput-pre"], "post": ["fulloutput-post"]},
        "frontend-review": {"pre": ["review-pre"], "post": ["review-post"]},
        "security-review": {"pre": ["security-pre"], "post": ["security-post"]},
        "vietnam-payment-review": {"pre": ["payment-pre"], "post": ["payment-post"]},
        "weknora-kb": {"pre": ["weknora-pre"], "post": ["weknora-post"]},
        "pixelrag": {"pre": ["pixelrag-pre"], "post": ["pixelrag-post"]},
        "document-ocr": {"pre": ["ocr-pre"], "post": ["ocr-post"]}
    }
    
    @classmethod
    def generate(cls, request: str, language: LanguageDetection, intent: IntentAnalysis, skills: SkillDetection) -> TaskManifest:
        tasks = []
        execution_order = []
        task_id = 0
        
        # Collect all required gates
        pre_gates = set()
        post_gates = set()
        
        for skill_id in skills.matched_skills:
            if skill_id in cls.GATE_MAPPING:
                pre_gates.update(cls.GATE_MAPPING[skill_id]["pre"])
                post_gates.update(cls.GATE_MAPPING[skill_id]["post"])
        
        # Pre-gate task
        if pre_gates:
            task_id += 1
            pre_gate_task = {
                "task_id": f"task-{task_id}",
                "task_name": "Pre-Review Gates",
                "task_type": "pre-gate",
                "description": "Run all pre-review gates before implementation",
                "estimated_time": "10 minutes",
                "skills_applied": skills.matched_skills,
                "subtasks": [
                    {
                        "subtask_id": f"sub-{task_id}-{gate}",
                        "name": f"{gate.replace('-pre', '').replace('-', ' ').title()} Pre-Gate",
                        "checkpoints": ["Gate initialized", "Checklist reviewed", "Gate passed"]
                    }
                    for gate in sorted(pre_gates)
                ],
                "dependencies": [],
                "status": "pending"
            }
            tasks.append(pre_gate_task)
            execution_order.append(pre_gate_task["task_id"])
        
        # Implementation task
        task_id += 1
        impl_task = {
            "task_id": f"task-{task_id}",
            "task_name": "Implementation",
            "task_type": "implementation",
            "description": f"Implement: {request[:100]}...",
            "estimated_time": "30 minutes",
            "skills_applied": skills.matched_skills,
            "subtasks": [
                {
                    "subtask_id": "sub-impl-1",
                    "name": "Environment Setup",
                    "checkpoints": ["Dependencies installed", "Environment configured"]
                },
                {
                    "subtask_id": "sub-impl-2",
                    "name": "Core Implementation",
                    "checkpoints": ["Main logic implemented", "Code follows style guide"]
                },
                {
                    "subtask_id": "sub-impl-3",
                    "name": "Testing",
                    "checkpoints": ["Tests written", "Tests pass"]
                }
            ],
            "dependencies": [tasks[-1]["task_id"]] if tasks else [],
            "status": "pending"
        }
        tasks.append(impl_task)
        execution_order.append(impl_task["task_id"])
        
        # Post-gate task
        if post_gates:
            task_id += 1
            post_gate_task = {
                "task_id": f"task-{task_id}",
                "task_name": "Post-Review Gates",
                "task_type": "post-gate",
                "description": "Run all post-review gates after implementation",
                "estimated_time": "15 minutes",
                "skills_applied": skills.matched_skills,
                "subtasks": [
                    {
                        "subtask_id": f"sub-{task_id}-{gate}",
                        "name": f"{gate.replace('-post', '').replace('-', ' ').title()} Post-Gate",
                        "checkpoints": ["Gate initialized", "Checklist reviewed", "Gate passed"]
                    }
                    for gate in sorted(post_gates)
                ],
                "dependencies": [impl_task["task_id"]],
                "status": "pending"
            }
            tasks.append(post_gate_task)
            execution_order.append(post_gate_task["task_id"])
        
        # Delivery task
        task_id += 1
        delivery_task = {
            "task_id": f"task-{task_id}",
            "task_name": "Delivery",
            "task_type": "delivery",
            "description": "Deliver final code to user",
            "estimated_time": "5 minutes",
            "skills_applied": [],
            "subtasks": [
                {
                    "subtask_id": "sub-del-1",
                    "name": "Code Review",
                    "checkpoints": ["Code reviewed", "Changes documented"]
                },
                {
                    "subtask_id": "sub-del-2",
                    "name": "Deliver",
                    "checkpoints": ["Code delivered", "Summary provided"]
                }
            ],
            "dependencies": [tasks[-1]["task_id"]] if tasks else [],
            "status": "pending"
        }
        tasks.append(delivery_task)
        execution_order.append(delivery_task["task_id"])
        
        # Build analysis
        analysis = {
            "skills_selected": [
                {
                    "skill_id": skill_id,
                    "confidence": skills.skill_confidences.get(skill_id, 0),
                    "role": "primary" if skill_id == skills.primary_skill else "secondary"
                }
                for skill_id in skills.matched_skills
            ],
            "rules_matched": cls._get_matched_rules(intent),
            "gates_required": {
                "pre": sorted(list(pre_gates)),
                "post": sorted(list(post_gates))
            },
            "dependencies": {
                "python": cls._get_python_deps(skills),
                "npm": cls._get_npm_deps(skills),
                "system": cls._get_system_deps(skills)
            }
        }
        
        return TaskManifest(
            version="1.0.0",
            generated_at=datetime.now().isoformat(),
            request_id=str(uuid.uuid4()),
            input={
                "original_request": request,
                "detected_language": language.language,
                "translated_request": language.translated_text,
                "primary_intent": intent.primary_intent,
                "primary_domain": intent.primary_domain
            },
            analysis=analysis,
            tasks=tasks,
            execution_order=execution_order,
            output={
                "summary": f"Task manifest for: {request[:100]}...",
                "deliverables": cls._get_deliverables(skills),
                "warnings": [],
                "next_steps": ["Run pre-review gates", "Implement feature", "Run post-review gates", "Deliver code"]
            }
        )
    
    @classmethod
    def _get_matched_rules(cls, intent: IntentAnalysis) -> List[str]:
        rules = []
        if "frontend" in intent.domains:
            rules.extend(["frontend-architecture", "ui-visual-design", "coding-standards"])
        if "security" in intent.domains:
            rules.append("web-security")
        if "payment" in intent.domains:
            rules.append("billing")
        return rules
    
    @classmethod
    def _get_python_deps(cls, skills: SkillDetection) -> List[str]:
        # This would be populated from skill-dependencies.json
        return []
    
    @classmethod
    def _get_npm_deps(cls, skills: SkillDetection) -> List[str]:
        return []
    
    @classmethod
    def _get_system_deps(cls, skills: SkillDetection) -> List[str]:
        return []
    
    @classmethod
    def _get_deliverables(cls, skills: SkillDetection) -> List[str]:
        deliverables = []
        if "frontend-taste" in skills.matched_skills or "frontend-redesign" in skills.matched_skills:
            deliverables.append("Frontend implementation")
        if "full-output" in skills.matched_skills:
            deliverables.append("Complete implementation")
        return deliverables

# ═══════════════════════════════════════════════════════════════════════════════════════
# MAIN ANALYZER
# ═══════════════════════════════════════════════════════════════════════════════════════

class TaskAnalyzer:
    """Main task analyzer orchestrator"""
    
    def __init__(self, dependencies_path: Optional[str] = None):
        self.dependencies_path = dependencies_path
        self.manifest = self._load_dependencies()
    
    def _load_dependencies(self) -> Dict:
        if self.dependencies_path and os.path.exists(self.dependencies_path):
            with open(self.dependencies_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def analyze(self, request: str) -> TaskManifest:
        """Full analysis pipeline"""
        
        # Step 1: Language Detection
        lang = LanguageDetector.detect(request)
        
        # Step 2: Translation
        if lang.language != "english":
            lang.translated_text = Translator.translate(request, lang.language)
        
        # Step 3: Intent Analysis
        intent = IntentAnalyzer.analyze(lang.translated_text)
        
        # Step 4: Skill Detection
        skills = SkillDetector.detect(lang.translated_text, intent)
        
        # Step 5: Task Generation
        manifest = TaskGenerator.generate(request, lang, intent, skills)
        
        return manifest
    
    def to_dict(self, manifest: TaskManifest) -> Dict:
        """Convert manifest to dictionary"""
        return asdict(manifest)
    
    def to_json(self, manifest: TaskManifest, indent: int = 2) -> str:
        """Convert manifest to JSON string"""
        return json.dumps(self.to_dict(manifest), indent=indent, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Task Analyzer - Cursor Enterprise Framework")
    parser.add_argument("request", nargs="*", help="Request to analyze")
    parser.add_argument("-f", "--file", help="Read request from file")
    parser.add_argument("-o", "--output", help="Output file for manifest")
    parser.add_argument("-j", "--json", action="store_true", help="Output as JSON")
    parser.add_argument("-d", "--dependencies", help="Path to skill-dependencies.json")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Get request
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            request = f.read().strip()
    elif args.request:
        request = " ".join(args.request)
    else:
        print("Error: Please provide a request or use --file")
        sys.exit(1)
    
    # Analyze
    analyzer = TaskAnalyzer(dependencies_path=args.dependencies)
    manifest = analyzer.analyze(request)
    
    # Output
    if args.json or args.output:
        output = analyzer.to_json(manifest)
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Manifest saved to: {args.output}")
        else:
            print(output)
    else:
        # Pretty print
        print("\n" + "=" * 80)
        print("TASK ANALYSIS RESULT")
        print("=" * 80)
        print(f"\nOriginal Request: {request[:100]}...")
        print(f"Detected Language: {manifest.input['detected_language']}")
        print(f"Translated: {manifest.input['translated_request'][:100]}...")
        print(f"Primary Intent: {manifest.input['primary_intent']}")
        print(f"Primary Domain: {manifest.input['primary_domain']}")
        
        print("\n--- Skills Detected ---")
        for skill in manifest.analysis['skills_selected']:
            print(f"  - {skill['skill_id']} ({skill['confidence']:.0%}) [{skill['role']}]")
        
        print("\n--- Tasks Generated ---")
        for task in manifest.tasks:
            print(f"  [{task['task_id']}] {task['task_name']}")
            for subtask in task['subtasks']:
                print(f"       └─ {subtask['name']}")
        
        print("\n--- Gates Required ---")
        print(f"  Pre: {', '.join(manifest.analysis['gates_required']['pre']) or 'none'}")
        print(f"  Post: {', '.join(manifest.analysis['gates_required']['post']) or 'none'}")

if __name__ == "__main__":
    main()
