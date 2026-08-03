# update-skill-registry.py
# Script to update skill-registry.mdc with new prefixed paths
# Version: 2.0.0 - 2026-08-03

import re
import os
from pathlib import Path

def get_mappings():
    """Return skill and rule mappings"""
    skill_mappings = {
        # UI & Visual Design
        "landing-page-pro": "ui_landing-page-pro",
        "dashboard-ui": "ui_dashboard-ui",
        "frontend-taste": "ui_frontend-taste",
        "hallmark": "ui_hallmark",
        "frontend-redesign": "ui_frontend-redesign",
        "frontend-review": "ui_frontend-review",
        "visual-explainer": "ui_visual-explainer",
        "canvas-design": "ui_canvas-design",
        "theme-factory": "ui_theme-factory",
        "open-design": "ui_open-design",
        "web-design-guidelines": "ui_web-design-guidelines",
        
        # Code & Development
        "karpathy-coding": "code_karpathy",
        "ponytail": "code_ponytail",
        "full-output": "code_full-output",
        "vibe-coding": "code_vibe-coding",
        
        # Document & Writing
        "ai-copywriter": "doc_ai-copywriter",
        "book-to-skill": "doc_book-to-skill",
        "simple-english": "doc_simple-english",
        "microsoft-docs": "doc_microsoft-docs",
        
        # Database
        "mysql": "db_mysql",
        "mysql-patterns": "db_mysql-patterns",
        "sql-server-table-reconciliation": "db_sql-server-table-reconciliation",
        "adbc": "db_adbc",
        "redis-observability": "db_redis-observability",
        
        # Infrastructure
        "deploy-to-vercel": "infra_deploy-vercel",
        "docker": "infra_docker",
        "prefect": "infra_prefect",
        
        # Security
        "security-review": "sec_security-review",
        "vietnam-payment-review": "sec_vietnam-payment-review",
        
        # Performance
        "vercel-react-best-practices": "perf_react-best-practices",
        "vercel-composition-patterns": "perf_composition-patterns",
        
        # AI & Agent
        "weknora-kb": "ai_weknora-kb",
        "weknora-agent": "ai_weknora-agent",
        "pixelrag": "ai_pixelrag",
        "video-generation": "ai_video-generation",
        "chatbotx-feature": "ai_chatbotx-feature",
        "chatbotx-database": "ai_chatbotx-database",
        "chatbotx-worker": "ai_chatbotx-worker",
        
        # Special
        "bazi": "special_bazi",
        "vietnam-address": "special_vietnam-address",
        
        # Utilities
        "skill-installer": "util_skill-installer",
        "create-pull-request": "util_create-pull-request",
        "csv-wrangling": "util_csv-wrangling",
        "document-ocr": "util_document-ocr",
        "webapp-testing": "util_webapp-testing",
    }
    
    rule_mappings = {
        # Core Rules
        "skill-registry": "rule_skill-registry",
        "skill-integration": "rule_skill-integration",
        "task-analyzer": "rule_task-analyzer",
        "intent-detection": "rule_intent-detection",
        
        # Protocols
        "multi-language-processing": "proto_multi-language-processing",
        "multi-language-vibe-code": "proto_multi-language-vibe-code",
        "context-router": "proto_context-router",
        "memory-first": "proto_memory-first",
        
        # References
        "architecture-patterns": "ref_architecture-patterns",
        "frontend-frameworks": "ref_frontend-frameworks",
        "backend-frameworks": "ref_backend-frameworks",
        "enterprise-patterns": "ref_enterprise-patterns",
        "api-patterns": "ref_api-patterns",
    }
    
    return skill_mappings, rule_mappings


def update_skill_registry(input_path, output_path=None):
    """Update skill-registry.mdc with new prefixed paths"""
    
    if output_path is None:
        output_path = input_path
    
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    skill_mappings, rule_mappings = get_mappings()
    
    # Update skill paths in content
    for old_name, new_name in skill_mappings.items():
        # Pattern: .cursor/skills/OLD-NAME/SKILL.md
        pattern = rf"\.cursor/skills/{old_name}/SKILL\.md"
        replacement = f".cursor/skills/{new_name}/SKILL.md"
        content = re.sub(pattern, replacement, content)
        
        # Pattern: skills/OLD-NAME/SKILL.md
        pattern = rf"skills/{old_name}/SKILL\.md"
        replacement = f"skills/{new_name}/SKILL.md"
        content = re.sub(pattern, replacement, content)
        
        # Pattern: | `OLD-NAME` | (skill ID column in tables)
        pattern = rf"\|\s*`{old_name}`\s*\|"
        replacement = f"| `{new_name}` |"
        content = re.sub(pattern, replacement, content)
    
    # Update rule paths
    for old_name, new_name in rule_mappings.items():
        # Pattern: .cursor/rules/OLD-NAME.mdc
        pattern = rf"\.cursor/rules/{old_name}\.mdc"
        replacement = f".cursor/rules/{new_name}.mdc"
        content = re.sub(pattern, replacement, content)
        
        # Pattern: [[OLD-NAME]]
        pattern = rf"\[\[{old_name}\]\]"
        replacement = f"[[{new_name}]]"
        content = re.sub(pattern, replacement, content)
        
        # Pattern: OLD-NAME in target paths
        pattern = rf"target.*OLD-NAME/{old_name}/"
        # Skip this pattern as it's not a simple replacement
    
    # Count changes
    changes = content.count(new_name) - original_content.count(new_name)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return changes


def create_new_skill_registry_template():
    """Create a template for the new skill-registry with prefix updates"""
    
    template = """# Skill Registry v2 - Single Source of Truth

> **Version:** 2.0.0  
> **Updated:** 2026-08-03  
> **Changes:** All skills and rules renamed with prefix system

## Prefix System

| Prefix | Domain | Examples |
|--------|--------|----------|
| `ui_` | UI & Visual Design | ui_landing-page-pro, ui_dashboard-ui |
| `code_` | Code & Development | code_karpathy, code_ponytail |
| `sec_` | Security | sec_security-review, sec_vietnam-payment |
| `ai_` | AI & Agent | ai_weknora-kb, ai_video-generation |
| `doc_` | Document & Writing | doc_book-to-skill, doc_ai-copywriter |
| `db_` | Database | db_mysql, db_adbc |
| `infra_` | Infrastructure | infra_deploy-vercel, infra_docker |
| `perf_` | Performance | perf_react-best-practices |
| `special_` | Special | special_bazi, special_vietnam-address |
| `util_` | Utilities | util_skill-installer, util_document-ocr |

## Migration Status

All skills have been renamed with prefix system. See `NAMING-CONVENTION.md` for full mapping.

### Skill ID Changes (Summary)

| Old ID | New ID | Path |
|--------|--------|------|
| frontend-taste | ui_frontend-taste | .cursor/skills/ui_frontend-taste/ |
| frontend-redesign | ui_frontend-redesign | .cursor/skills/ui_frontend-redesign/ |
| frontend-review | ui_frontend-review | .cursor/skills/ui_frontend-review/ |
| landing-page-pro | ui_landing-page-pro | .cursor/skills/ui_landing-page-pro/ |
| dashboard-ui | ui_dashboard-ui | .cursor/skills/ui_dashboard-ui/ |
| hallmark | ui_hallmark | .cursor/skills/ui_hallmark/ |
| karpathy-coding | code_karpathy | .cursor/skills/code_karpathy/ |
| ponytail | code_ponytail | .cursor/skills/code_ponytail/ |
| full-output | code_full-output | .cursor/skills/code_full-output/ |
| security-review | sec_security-review | .cursor/skills/sec_security-review/ |
| vietnam-payment-review | sec_vietnam-payment-review | .cursor/skills/sec_vietnam-payment-review/ |
| weknora-kb | ai_weknora-kb | .cursor/skills/ai_weknora-kb/ |
| weknora-agent | ai_weknora-agent | .cursor/skills/ai_weknora-agent/ |
| pixelrag | ai_pixelrag | .cursor/skills/ai_pixelrag/ |
| video-generation | ai_video-generation | .cursor/skills/ai_video-generation/ |
| book-to-skill | doc_book-to-skill | .cursor/skills/doc_book-to-skill/ |
| ai-copywriter | doc_ai-copywriter | .cursor/skills/doc_ai-copywriter/ |
| simple-english | doc_simple-english | .cursor/skills/doc_simple-english/ |
| mysql | db_mysql | .cursor/skills/db_mysql/ |
| adbc | db_adbc | .cursor/skills/db_adbc/ |
| deploy-to-vercel | infra_deploy-vercel | .cursor/skills/infra_deploy-vercel/ |
| vercel-react-best-practices | perf_react-best-practices | .cursor/skills/perf_react-best-practices/ |
| bazi | special_bazi | .cursor/skills/special_bazi/ |
| vietnam-address | special_vietnam-address | .cursor/skills/special_vietnam-address/ |
| skill-installer | util_skill-installer | .cursor/skills/util_skill-installer/ |
| document-ocr | util_document-ocr | .cursor/skills/util_document-ocr/ |

## Usage

### Auto-Detection

Skills are automatically selected based on request keywords:

```
"build landing page" → ui_landing-page-pro
"security audit" → sec_security-review
"knowledge base" → ai_weknora-kb
```

### Manual Selection

Use the new prefixed names:

```
.cursor/skills/ui_landing-page-pro/SKILL.md
.cursor/skills/sec_security-review/SKILL.md
.cursor/skills/code_karpathy/SKILL.md
```

## Full Documentation

See `NAMING-CONVENTION.md` for complete naming guide and migration instructions.
"""
    
    return template


def main():
    """Main function"""
    script_dir = Path(__file__).parent.parent
    registry_path = script_dir / ".cursor" / "rules" / "skill-registry.mdc"
    
    print("=" * 60)
    print("SKILL REGISTRY UPDATE SCRIPT v2.0")
    print("=" * 60)
    print()
    
    if not registry_path.exists():
        print(f"ERROR: skill-registry.mdc not found at {registry_path}")
        print("Run rename-skills-rules.ps1 first to rename folders")
        return
    
    print(f"Updating: {registry_path}")
    print()
    
    # Update the registry
    changes = update_skill_registry(str(registry_path))
    
    print(f"✓ Updated skill-registry.mdc with {changes} changes")
    print()
    print("Changes made:")
    print("  - All skill paths updated with new prefixes")
    print("  - All skill IDs updated with new prefixes")
    print("  - All rule references updated with new prefixes")
    print()
    print("Next steps:")
    print("  1. Review the updated skill-registry.mdc")
    print("  2. Update .cursorrules references")
    print("  3. Update AGENTS.md references")
    print("  4. Update INDEX.md and INDEX.json")
    print("  5. Run create-compatibility-layer.ps1 for aliases")


if __name__ == "__main__":
    main()
