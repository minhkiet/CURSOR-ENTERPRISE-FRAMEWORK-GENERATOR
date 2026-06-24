---
title: "Enterprise Security và Data Handling"
description: "Hướng dẫn Enterprise Security cho Claude API - data handling, privacy considerations, compliance, API security, key rotation, audit logging"
tags: ["claude", "security", "enterprise", "compliance", "privacy", "audit", "data-handling"]
created: "2026-06-23"
version: "1.0.0"
framework: "cursor-enterprise-framework"
---

# Enterprise Security và Data Handling

## Tổng quan (Overview)

Trong môi trường enterprise, việc sử dụng AI APIs như Claude đặt ra nhiều thách thức về bảo mật và tuân thủ quy định. Dữ liệu được gửi đến Claude API có thể bao gồm thông tin nhạy cảm như dữ liệu khách hàng, bí mật thương mại, hoặc thông tin tài chính. Việc bảo vệ dữ liệu này không chỉ là yêu cầu pháp lý mà còn là trách nhiệm đạo đức và chiến lược kinh doanh.

Tài liệu này cung cấp hướng dẫn toàn diện về các best practices bảo mật khi sử dụng Claude API trong môi trường enterprise, bao gồm quản lý API keys, xử lý dữ liệu, tuân thủ compliance, và triển khai audit logging.

## Mục đích (Purpose)

Mục tiêu chính của tài liệu này bao gồm:

1. **API Key Security** - Quản lý và bảo vệ API credentials
2. **Data Handling** - Xử lý dữ liệu nhạy cảm an toàn
3. **Compliance** - Tuân thủ GDPR, SOC 2, HIPAA và các regulations khác
4. **Audit Logging** - Ghi log và monitoring cho security
5. **Network Security** - Bảo mật kết nối và infrastructure
6. **Incident Response** - Xử lý security incidents

## Khái niệm cốt lõi (Key Concepts)

### 1. Data Classification

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA CLASSIFICATION                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              PUBLIC DATA                                 │   │
│  │  • Marketing materials                                   │   │
│  │  • Public documentation                                 │   │
│  │  Risk: Low - Có thể gửi lên API freely                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │            INTERNAL DATA                                 │   │
│  │  • Business processes                                   │   │
│  │  • Internal communications                              │   │
│  │  Risk: Medium - Cần access controls                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │          CONFIDENTIAL DATA                               │   │
│  │  • Customer PII                                         │   │
│  │  • Financial records                                    │   │
│  │  Risk: High - Cần encryption, access logging            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                     │
│                            ▼                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           RESTRICTED DATA                               │   │
│  │  • PHI (Protected Health Information)                   │   │
│  │  • Authentication credentials                           │   │
│  │  Risk: Critical - Không nên gửi lên external API       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE SECURITY ARCHITECTURE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│   │   Client     │──────│   API       │──────│   Claude    │ │
│   │  Application │      │   Gateway   │      │   API       │ │
│   └──────────────┘      └──────────────┘      └──────────────┘ │
│         │                      │                      │          │
│         │                      │                      │          │
│         ▼                      ▼                      ▼          │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│   │  Secrets    │      │  Audit      │      │  Data       │ │
│   │  Manager    │      │  Logging    │      │  Processor  │ │
│   └──────────────┘      └──────────────┘      └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## API Key Management

### 1. Secure Key Storage

```python
import os
from typing import Optional
from dataclasses import dataclass

# DON'T: Hardcode API keys (BAD)
BAD_EXAMPLE = """
client = Anthropic(api_key="sk-ant-api03-xxxxx...")
"""

# DO: Use environment variables (GOOD)
GOOD_EXAMPLE = """
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
"""


class SecureAPIClient:
    """Secure API client với proper key management."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        key_source: str = "environment"  # environment, aws, azure, vault
    ):
        self.api_key = self._load_api_key(api_key, key_source)
        self.client = Anthropic(api_key=self.api_key)
    
    def _load_api_key(
        self,
        explicit_key: Optional[str],
        source: str
    ) -> str:
        """Load API key from secure source."""
        
        # Priority 1: Explicitly provided key
        if explicit_key:
            return explicit_key
        
        # Priority 2: Environment variable
        if source == "environment":
            key = os.environ.get("ANTHROPIC_API_KEY")
            if key:
                return key
        
        # Priority 3: AWS Secrets Manager
        if source == "aws":
            return self._load_from_aws_secrets()
        
        # Priority 4: Azure Key Vault
        if source == "azure":
            return self._load_from_azure_vault()
        
        # Priority 5: HashiCorp Vault
        if source == "vault":
            return self._load_from_vault()
        
        raise ValueError("No API key found in any source")
    
    def _load_from_aws_secrets(self) -> str:
        """Load API key from AWS Secrets Manager."""
        import boto3
        
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(
            SecretId='prod/anthropic-api-key'
        )
        return response['SecretString']
    
    def _load_from_azure_vault(self) -> str:
        """Load API key from Azure Key Vault."""
        from azure.keyvault.secrets import SecretClient
        from azure.identity import DefaultAzureCredential
        
        credential = DefaultAzureCredential()
        client = SecretClient(
            vault_url="https://your-keyvault.vault.azure.net/",
            credential=credential
        )
        return client.get_secret("anthropic-api-key").value
    
    def _load_from_vault(self) -> str:
        """Load API key from HashiCorp Vault."""
        import hvac
        
        client = hvac.Client()
        response = client.secrets.kv.v2.read_secret_version(
            path='anthropic-api-key'
        )
        return response['data']['data']['api_key']
```

### 2. Key Rotation

```python
import asyncio
from datetime import datetime, timedelta
from typing import Optional

class APIKeyRotation:
    """Automated API key rotation manager."""
    
    def __init__(
        self,
        current_key_id: str,
        rotation_days: int = 90
    ):
        self.current_key_id = current_key_id
        self.rotation_days = rotation_days
        self.rotation_scheduled = False
    
    async def check_rotation_needed(self) -> bool:
        """Check if key rotation is needed."""
        
        # Get key metadata from Anthropic console
        key_info = await self._get_key_metadata(self.current_key_id)
        
        created_date = datetime.fromisoformat(key_info['created_at'])
        days_since_creation = (datetime.now() - created_date).days
        
        return days_since_creation >= self.rotation_days
    
    async def rotate_key(self) -> dict:
        """Rotate API key."""
        
        # 1. Create new key
        new_key = await self._create_new_key()
        
        # 2. Update secrets manager
        await self._update_secrets_manager(new_key)
        
        # 3. Notify systems to use new key
        await self._notify_key_change()
        
        # 4. Revoke old key (with grace period)
        await self._schedule_old_key_revocation()
        
        self.current_key_id = new_key['id']
        
        return {
            "new_key_id": new_key['id'],
            "old_key_id": self.current_key_id,
            "revocation_date": datetime.now() + timedelta(days=7)
        }
    
    async def _create_new_key(self) -> dict:
        """Create new API key via Anthropic console API."""
        # Implementation depends on Anthropic's API
        pass
    
    async def _update_secrets_manager(self, new_key: dict):
        """Update key in secrets manager."""
        pass
    
    async def _notify_key_change(self):
        """Notify services about key change."""
        pass
    
    async def _schedule_old_key_revocation(self):
        """Schedule old key revocation."""
        # Revoke after grace period
        pass
```

### 3. Multi-Environment Key Management

```python
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"


class EnvironmentKeyManager:
    """Manage API keys across environments."""
    
    def __init__(self):
        self.keys = {
            Environment.DEVELOPMENT: os.environ.get("ANTHROPIC_API_KEY_DEV"),
            Environment.STAGING: os.environ.get("ANTHROPIC_API_KEY_STAGING"),
            Environment.PRODUCTION: os.environ.get("ANTHROPIC_API_KEY_PROD"),
        }
    
    def get_client(self, env: Environment) -> Anthropic:
        """Get API client for specific environment."""
        
        key = self.keys.get(env)
        if not key:
            raise ValueError(f"No API key for environment: {env}")
        
        # Validate environment match
        self._validate_environment(env, key)
        
        return Anthropic(api_key=key)
    
    def _validate_environment(self, env: Environment, key: str):
        """Validate key is being used in correct environment."""
        
        # Add environment-specific validation
        if env == Environment.PRODUCTION:
            if self._is_development_key(key):
                raise SecurityError(
                    "Production environment using development API key!"
                )
    
    def _is_development_key(self, key: str) -> bool:
        """Check if key is a development key."""
        return "dev" in key.lower() or "test" in key.lower()
```

## Data Handling

### 1. PII Detection và Redaction

```python
import re
from dataclasses import dataclass
from typing import Literal

@dataclass
class RedactionConfig:
    """Configuration cho PII redaction."""
    redact_email: bool = True
    redact_phone: bool = True
    redact_ssn: bool = True
    redact_credit_card: bool = True
    redact_address: bool = True
    redact_name: bool = False  # Names often needed for context


class PIIDetector:
    """Detect PII in text."""
    
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone_vietnam": r'(?:0[0-9]{9,10}|0[0-9]{2}[0-9]{7,8})',
        "phone_us": r'\b(?:\+1)?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
        "ssn": r'\b[0-9]{3}[-\s]?[0-9]{2}[-\s]?[0-9]{4}\b',
        "credit_card": r'\b(?:[0-9]{4}[-\s]?){3}[0-9]{4}\b',
        "date_of_birth": r'\b(?:DOB|Date of Birth|Birthday)[:\s]+[\d/:-]+\b',
    }
    
    def detect(self, text: str) -> list[dict]:
        """Detect PII in text."""
        
        findings = []
        
        for pii_type, pattern in self.PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                findings.append({
                    "type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        return findings
    
    def redact(self, text: str, config: RedactionConfig) -> tuple[str, list[dict]]:
        """Redact PII from text."""
        
        findings = self.detect(text)
        redaction_log = []
        
        # Sort in reverse order to maintain positions
        findings.sort(key=lambda x: x['start'], reverse=True)
        
        redacted_text = text
        
        for finding in findings:
            pii_type = finding['type']
            
            # Check if should redact based on config
            if not self._should_redact(pii_type, config):
                continue
            
            # Create redaction mask
            mask = f"[REDACTED-{pii_type.upper()}]"
            
            # Replace in text
            redacted_text = (
                redacted_text[:finding['start']] +
                mask +
                redacted_text[finding['end']:]
            )
            
            # Log redaction
            redaction_log.append({
                "original": finding['value'],
                "type": pii_type,
                "position": finding['start']
            })
        
        return redacted_text, redaction_log
    
    def _should_redact(self, pii_type: str, config: RedactionConfig) -> bool:
        """Check if PII type should be redacted."""
        
        redaction_map = {
            "email": config.redact_email,
            "phone_vietnam": config.redact_phone,
            "phone_us": config.redact_phone,
            "ssn": config.redact_ssn,
            "credit_card": config.redact_credit_card,
            "date_of_birth": config.redact_email,  # Treat as sensitive
        }
        
        return redaction_map.get(pii_type, False)
```

### 2. Data Processing Pipeline

```python
from typing import Optional
from dataclasses import dataclass
from enum import Enum

class ProcessingMode(Enum):
    FULL_SEND = "full"      # Send all data
    REDACTED = "redacted"   # Redact PII
    SANITIZED = "sanitized" # Replace with synthetic data
    LOCAL_ONLY = "local"    # Never send to external API


@dataclass
class ProcessingConfig:
    """Configuration cho data processing."""
    mode: ProcessingMode = ProcessingMode.REDACTED
    preserve_context: bool = True
    preserve_entities: bool = False  # Replace names with placeholders
    log_processing: bool = True


class DataProcessor:
    """Process data before sending to Claude API."""
    
    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.pii_detector = PIIDetector()
        self.redaction_config = RedactionConfig()
    
    def process(self, text: str, metadata: dict | None = None) -> dict:
        """Process text according to configuration."""
        
        processing_log = {
            "original_length": len(text),
            "mode": self.config.mode.value,
            "redactions": []
        }
        
        if self.config.mode == ProcessingMode.FULL_SEND:
            processed_text = text
            
        elif self.config.mode == ProcessingMode.REDACTED:
            processed_text, redactions = self.pii_detector.redact(
                text, self.redaction_config
            )
            processing_log["redactions"] = redactions
            
        elif self.config.mode == ProcessingMode.SANITIZED:
            processed_text, redactions = self._sanitize(text)
            processing_log["redactions"] = redactions
            
        elif self.config.mode == ProcessingMode.LOCAL_ONLY:
            # Never send to external API - return empty
            return {
                "processed_text": "",
                "should_send": False,
                "log": processing_log
            }
        
        processing_log["processed_length"] = len(processed_text)
        
        return {
            "processed_text": processed_text,
            "should_send": True,
            "log": processing_log
        }
    
    def _sanitize(self, text: str) -> tuple[str, list[dict]]:
        """Replace sensitive data with synthetic alternatives."""
        
        findings = self.pii_detector.detect(text)
        sanitized_text = text
        sanitizations = []
        
        # Sort in reverse order
        findings.sort(key=lambda x: x['start'], reverse=True)
        
        replacements = {
            "email": "[user@email.com]",
            "phone_vietnam": "[PHONE_NUMBER]",
            "phone_us": "[PHONE_NUMBER]",
            "ssn": "[SSN_XXX-XX-XXXX]",
            "credit_card": "[CREDIT_CARD_XXXX]",
        }
        
        for finding in findings:
            pii_type = finding['type']
            if pii_type in replacements:
                sanitized_text = (
                    sanitized_text[:finding['start']] +
                    replacements[pii_type] +
                    sanitized_text[finding['end']:]
                )
                sanitizations.append({
                    "type": pii_type,
                    "original": finding['value'],
                    "replacement": replacements[pii_type]
                })
        
        return sanitized_text, sanitizations
```

### 3. Secure Request Handler

```python
import asyncio
import hashlib
from typing import Optional

class SecureRequestHandler:
    """Secure handler cho Claude API requests."""
    
    def __init__(
        self,
        client: Anthropic,
        data_processor: DataProcessor,
        audit_logger: 'AuditLogger'
    ):
        self.client = client
        self.data_processor = data_processor
        self.audit_logger = audit_logger
    
    async def send_message(
        self,
        messages: list[dict],
        system: Optional[str] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        **kwargs
    ) -> dict:
        """Send message with security controls."""
        
        request_id = request_id or self._generate_request_id()
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Process messages
            processed_messages = []
            for msg in messages:
                processed = self.data_processor.process(
                    str(msg.get("content", "")),
                    {"request_id": request_id, "user_id": user_id}
                )
                
                processed_messages.append({
                    **msg,
                    "content": processed["processed_text"],
                    "_processing_log": processed["log"]
                })
            
            # Process system prompt
            processed_system = None
            if system:
                processed = self.data_processor.process(
                    system,
                    {"request_id": request_id, "user_id": user_id, "type": "system"}
                )
                processed_system = processed["processed_text"]
            
            # Check if should send
            should_send = all(
                m.get("_processing_log", {}).get("should_send", True)
                for m in processed_messages
            )
            
            if not should_send:
                return {
                    "status": "blocked",
                    "reason": "Data policy violation",
                    "request_id": request_id
                }
            
            # Send request
            response = await self.client.messages.create(
                model=kwargs.get("model", "claude-3-5-sonnet-20241022"),
                system=processed_system,
                messages=[{
                    "role": m["role"],
                    "content": m["content"]
                } for m in processed_messages],
                max_tokens=kwargs.get("max_tokens", 1024),
            )
            
            # Log successful request
            await self.audit_logger.log_request(
                request_id=request_id,
                user_id=user_id,
                success=True,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                duration_ms=int((asyncio.get_event_loop().time() - start_time) * 1000)
            )
            
            return {
                "status": "success",
                "response": response.content[0].text,
                "request_id": request_id,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
            
        except Exception as e:
            # Log failed request
            await self.audit_logger.log_request(
                request_id=request_id,
                user_id=user_id,
                success=False,
                error=str(e)
            )
            
            raise
    
    def _generate_request_id(self) -> str:
        """Generate unique request ID."""
        import uuid
        return str(uuid.uuid4())
```

## Audit Logging

### 1. Audit Logger Implementation

```python
from datetime import datetime
from typing import Optional
import json
import asyncio

class AuditLogger:
    """Comprehensive audit logging for Claude API usage."""
    
    def __init__(
        self,
        storage: str = "database",  # database, file, cloudwatch
        log_level: str = "info"
    ):
        self.storage = storage
        self.log_level = log_level
        self._setup_storage()
    
    def _setup_storage(self):
        """Setup logging storage based on configuration."""
        
        if self.storage == "database":
            # Setup database connection
            pass
        elif self.storage == "cloudwatch":
            # Setup CloudWatch client
            pass
    
    async def log_request(
        self,
        request_id: str,
        user_id: Optional[str],
        success: bool,
        input_tokens: int = 0,
        output_tokens: int = 0,
        duration_ms: int = 0,
        error: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        """Log an API request."""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "claude_api_request",
            "request_id": request_id,
            "user_id": user_id,
            "success": success,
            "metrics": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "duration_ms": duration_ms,
                "total_tokens": input_tokens + output_tokens
            },
            "metadata": metadata or {}
        }
        
        if error:
            log_entry["error"] = {
                "message": str(error),
                "type": type(error).__name__
            }
        
        await self._write_log(log_entry)
    
    async def log_data_access(
        self,
        request_id: str,
        user_id: str,
        data_type: str,
        action: str,  # read, write, delete
        data_hash: Optional[str] = None
    ):
        """Log data access for compliance."""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "data_access",
            "request_id": request_id,
            "user_id": user_id,
            "data_type": data_type,
            "action": action,
            "data_hash": data_hash
        }
        
        await self._write_log(log_entry)
    
    async def log_security_event(
        self,
        event_type: str,
        severity: str,  # low, medium, high, critical
        description: str,
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        metadata: Optional[dict] = None
    ):
        """Log security-related events."""
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": "security",
            "severity": severity,
            "description": description,
            "user_id": user_id,
            "ip_address": ip_address,
            "metadata": metadata or {}
        }
        
        await self._write_log(log_entry)
        
        # Alert for high/critical events
        if severity in ["high", "critical"]:
            await self._send_alert(log_entry)
    
    async def _write_log(self, log_entry: dict):
        """Write log entry to storage."""
        
        if self.storage == "database":
            await self._write_to_database(log_entry)
        elif self.storage == "cloudwatch":
            await self._write_to_cloudwatch(log_entry)
        elif self.storage == "file":
            await self._write_to_file(log_entry)
    
    async def _send_alert(self, log_entry: dict):
        """Send alert for critical security events."""
        # Implement alert notification
        pass
```

### 2. Compliance Reporting

```python
from datetime import datetime, timedelta
from typing import Optional

class ComplianceReporter:
    """Generate compliance reports for audit requirements."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
    
    async def generate_monthly_report(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Generate monthly compliance report."""
        
        # Query logs for period
        logs = await self._query_logs(start_date, end_date)
        
        # Calculate metrics
        total_requests = len(logs)
        successful_requests = sum(1 for l in logs if l.get("success"))
        failed_requests = total_requests - successful_requests
        
        total_input_tokens = sum(
            l.get("metrics", {}).get("input_tokens", 0)
            for l in logs
        )
        total_output_tokens = sum(
            l.get("metrics", {}).get("output_tokens", 0)
            for l in logs
        )
        
        # Identify security events
        security_events = [
            l for l in logs
            if l.get("event_type") == "security"
        ]
        
        # Unique users
        unique_users = set(
            l.get("user_id")
            for l in logs
            if l.get("user_id")
        )
        
        return {
            "report_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "usage_summary": {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": successful_requests / total_requests if total_requests else 0,
                "total_input_tokens": total_input_tokens,
                "total_output_tokens": total_output_tokens,
                "unique_users": len(unique_users)
            },
            "security_summary": {
                "total_security_events": len(security_events),
                "high_severity_events": sum(
                    1 for e in security_events
                    if e.get("severity") == "high"
                ),
                "critical_events": sum(
                    1 for e in security_events
                    if e.get("severity") == "critical"
                )
            },
            "generated_at": datetime.utcnow().isoformat()
        }
    
    async def generate_user_activity_report(
        self,
        user_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Generate activity report for specific user."""
        
        logs = await self._query_logs(
            start_date,
            end_date,
            filters={"user_id": user_id}
        )
        
        return {
            "user_id": user_id,
            "report_period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "activity": {
                "total_requests": len(logs),
                "data_accesses": sum(
                    1 for l in logs
                    if l.get("event_type") == "data_access"
                ),
                "security_events": sum(
                    1 for l in logs
                    if l.get("event_type") == "security"
                )
            },
            "generated_at": datetime.utcnow().isoformat()
        }
```

## Network Security

### 1. Secure Connection Configuration

```python
import ssl
from urllib3.util.url import parse_url

class SecureConnectionConfig:
    """Configure secure connections to Claude API."""
    
    @staticmethod
    def create_ssl_context() -> ssl.SSLContext:
        """Create SSL context for secure connections."""
        
        context = ssl.create_default_context()
        
        # Require TLS 1.2 or higher
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        
        # Verify certificates
        context.verify_mode = ssl.CERT_REQUIRED
        
        # Load system CA certificates
        context.load_default_certs()
        
        return context
    
    @staticmethod
    def validate_api_endpoint(endpoint: str) -> bool:
        """Validate API endpoint is trusted."""
        
        trusted_domains = [
            "api.anthropic.com",
            "console.anthropic.com",
        ]
        
        parsed = parse_url(endpoint)
        
        return parsed.host in trusted_domains
```

### 2. Rate Limiting và Quota Enforcement

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class RateLimitConfig:
    """Rate limiting configuration."""
    requests_per_minute: int = 50
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    tokens_per_minute: int = 80000
    tokens_per_day: int = 1000000


class RateLimiter:
    """Enforce rate limits cho API usage."""
    
    def __init__(self, config: RateLimitConfig):
        self.config = config
        self._requests: dict[str, list[datetime]] = defaultdict(list)
        self._token_usage: dict[str, list[tuple[datetime, int]]] = defaultdict(list)
    
    async def check_limit(
        self,
        user_id: str,
        estimated_tokens: int
    ) -> tuple[bool, dict]:
        """Check if request is within limits.
        
        Returns: (allowed, limit_info)
        """
        
        now = datetime.utcnow()
        requests = self._requests[user_id]
        token_usage = self._token_usage[user_id]
        
        # Clean old entries
        self._cleanup_old_entries(user_id, now)
        
        # Check rate limits
        limits_check = {
            "requests_per_minute": {
                "limit": self.config.requests_per_minute,
                "used": self._count_requests_in_period(requests, now, timedelta(minutes=1)),
                "allowed": True  # Will be updated
            },
            "requests_per_hour": {
                "limit": self.config.requests_per_hour,
                "used": self._count_requests_in_period(requests, now, timedelta(hours=1)),
                "allowed": True
            },
            "requests_per_day": {
                "limit": self.config.requests_per_day,
                "used": self._count_requests_in_period(requests, now, timedelta(days=1)),
                "allowed": True
            },
            "tokens_per_minute": {
                "limit": self.config.tokens_per_minute,
                "used": self._count_tokens_in_period(token_usage, now, timedelta(minutes=1)),
                "allowed": True
            },
        }
        
        # Calculate if allowed
        allowed = all(
            check["used"] < check["limit"]
            for check in limits_check.values()
        )
        
        # Add estimated tokens to minute check
        if allowed:
            limits_check["tokens_per_minute"]["used"] += estimated_tokens
            if limits_check["tokens_per_minute"]["used"] >= self.config.tokens_per_minute:
                allowed = False
        
        return allowed, limits_check
    
    async def record_request(
        self,
        user_id: str,
        tokens_used: int
    ):
        """Record completed request for rate limiting."""
        
        now = datetime.utcnow()
        self._requests[user_id].append(now)
        self._token_usage[user_id].append((now, tokens_used))
    
    def _cleanup_old_entries(self, user_id: str, now: datetime):
        """Remove old entries to prevent memory growth."""
        
        cutoff_day = now - timedelta(days=1)
        cutoff_minute = now - timedelta(minutes=1)
        
        # Clean requests
        self._requests[user_id] = [
            t for t in self._requests[user_id]
            if t > cutoff_day
        ]
        
        # Clean token usage
        self._token_usage[user_id] = [
            (t, tokens) for t, tokens in self._token_usage[user_id]
            if t > cutoff_day
        ]
    
    def _count_requests_in_period(
        self,
        requests: list[datetime],
        now: datetime,
        period: timedelta
    ) -> int:
        """Count requests within time period."""
        
        cutoff = now - period
        return sum(1 for t in requests if t > cutoff)
    
    def _count_tokens_in_period(
        self,
        token_usage: list[tuple[datetime, int]],
        now: datetime,
        period: timedelta
    ) -> int:
        """Count tokens used within time period."""
        
        cutoff = now - period
        return sum(
            tokens for t, tokens in token_usage
            if t > cutoff
        )
```

## Compliance Implementation

### 1. GDPR Compliance

```python
class GDPRCompliance:
    """GDPR compliance helpers for Claude API usage."""
    
    @staticmethod
    def should_process_data(personal_data: dict, purpose: str) -> bool:
        """Check if data processing is allowed under GDPR."""
        
        # Legal basis mapping
        legal_basis = {
            "consent": ["marketing", "profiling"],
            "contract": ["service_delivery", "account_management"],
            "legitimate_interest": ["fraud_prevention", "security"],
            "legal_obligations": ["regulatory_compliance", "tax"]
        }
        
        # Check if purpose is covered
        for basis, purposes in legal_basis.items():
            if purpose in purposes:
                return True
        
        return False
    
    @staticmethod
    def anonymize_for_processing(data: dict) -> dict:
        """Anonymize data for processing."""
        
        # PII fields to remove/replace
        pii_fields = [
            "name", "email", "phone", "address",
            "date_of_birth", "id_number"
        ]
        
        anonymized = data.copy()
        
        for field in pii_fields:
            if field in anonymized:
                if field == "email":
                    # Keep partial email for debugging
                    anonymized[field] = "***@***.**"
                else:
                    anonymized[field] = "[REDACTED]"
        
        return anonymized
```

### 2. HIPAA Compliance Helpers

```python
class HIPAACompliance:
    """HIPAA compliance helpers for PHI data."""
    
    # PHI (Protected Health Information) fields
    PHI_FIELDS = [
        "patient_name", "dates", "phone", "fax", "email",
        "ssn", "medical_record", "health_plan",
        "account", "biometric", "photo", "any_unique_identifier"
    ]
    
    @staticmethod
    def is_phi_present(data: dict) -> bool:
        """Check if data contains PHI."""
        
        data_str = str(data).lower()
        
        phi_indicators = [
            "patient", "diagnosis", "treatment", "prescription",
            "medical", "health", "doctor", "hospital"
        ]
        
        return any(indicator in data_str for indicator in phi_indicators)
    
    @staticmethod
    def safe_for_external_processing(data: dict) -> tuple[bool, str]:
        """Check if data can be safely sent to external API.
        
        Returns: (safe, reason)
        """
        
        if HIPAACompliance.is_phi_present(data):
            return False, "PHI detected - cannot send to external API"
        
        # Check for common PHI patterns
        detector = PIIDetector()
        findings = detector.detect(str(data))
        
        if findings:
            return False, f"PII detected: {[f['type'] for f in findings]}"
        
        return True, "Data appears safe for processing"
```

## Best Practices

### 1. Security Checklist

```python
SECURITY_CHECKLIST = """
# Claude API Security Checklist

## API Key Management
[ ] API keys stored in secure vault (not code, not env files in repo)
[ ] API keys rotated every 90 days
[ ] Different keys for different environments
[ ] Keys have minimal necessary permissions
[ ] Old keys revoked promptly after rotation

## Data Handling
[ ] PII detection and redaction in place
[ ] Data classification policy implemented
[ ] Sensitive data never logged
[ ] Data retention policies defined and enforced
[ ] Encryption in transit (TLS 1.2+)
[ ] Encryption at rest for stored data

## Access Control
[ ] API access limited to authorized services
[ ] Rate limiting implemented
[ ] User/service authentication in place
[ ] Principle of least privilege applied

## Monitoring & Logging
[ ] All API calls logged with request/response metadata
[ ] Logs include: timestamp, user, tokens, success/failure, duration
[ ] Security events logged and alerted
[ ] Log integrity protected (immutable storage)
[ ] Regular log review process

## Compliance
[ ] GDPR requirements documented and implemented
[ ] Data processing agreements in place
[ ] Privacy impact assessments conducted
[ ] Right to deletion (erasure) capability
[ ] Data portability support

## Incident Response
[ ] Security incident response plan documented
[ ] Key rotation procedure documented
[ ] Data breach notification procedure documented
[ ] Regular security audits conducted
"""
```

### 2. Environment Configuration

```python
# Production environment configuration
PRODUCTION_SECURITY_CONFIG = {
    # API Keys
    "api_key_source": "aws_secrets_manager",  # or azure_key_vault, hashicorp_vault
    "api_key_rotation_days": 90,
    
    # Data Processing
    "pii_redaction_enabled": True,
    "data_classification_required": True,
    "allow_full_data_send": False,  # Always process
    
    # Network
    "verify_ssl": True,
    "allowed_domains": ["api.anthropic.com"],
    "timeout_seconds": 60,
    
    # Rate Limiting
    "rate_limit_requests_per_minute": 50,
    "rate_limit_tokens_per_minute": 80000,
    
    # Logging
    "log_level": "info",
    "log_requests": True,
    "log_responses": False,  # Don't log sensitive responses
    "log_security_events": True,
    
    # Compliance
    "gdpr_compliant": True,
    "hipaa_compliant": False,  # Set True if handling PHI
    "data_retention_days": 90,
}
```

## Troubleshooting

### Common Security Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| API key exposed | Keys in code/repository | Immediate rotation, review git history |
| Excessive token usage | No rate limiting | Implement rate limits per user/service |
| PII in logs | Missing redaction | Implement PII detection in logging |
| Unauthorized access | Weak access controls | Review IAM policies, add authentication |
| Data leakage | No data classification | Implement classification, filter before send |

### Incident Response Steps

```python
INCIDENT_RESPONSE_STEPS = """
# Security Incident Response

## 1. Identify (Within 15 minutes)
- Determine scope of incident
- Identify affected systems/users
- Preserve evidence

## 2. Contain (Within 30 minutes)
- Revoke compromised API keys
- Isolate affected systems
- Block unauthorized access

## 3. Eradicate
- Remove threat vectors
- Reset compromised credentials
- Patch vulnerabilities

## 4. Recover
- Restore from clean backups
- Verify systems are secure
- Monitor for recurrence

## 5. Post-Incident
- Document lessons learned
- Update security controls
- Notify affected parties (if required)
- Report to authorities (if required)
"""
```

## References

- [Anthropic Security Practices](https://www.anthropic.com/security)
- [GDPR Guidelines](https://gdpr.eu/)
- [HIPAA Journal](https://www.hipaajournal.com/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
