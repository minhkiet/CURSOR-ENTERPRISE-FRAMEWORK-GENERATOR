# Backward Compatibility Guide

> **Version:** 2.0.0  
> **Created:** 2026-08-03  
> **Purpose:** Maintain backward compatibility after renaming

## Overview

In v2.0, all skills and rules have been renamed with prefix system:
- Skills: ui_, code_, sec_, i_, doc_, db_, etc.
- Rules: ule_, proto_, ef_, meta_

For backward compatibility, aliases are maintained.

## Skill Aliases

| Old Name | New Name | Status |
|----------|----------|--------|
| landing-page-pro | ui_landing-page-pro | Alias maintained |
| dashboard-ui | ui_dashboard-ui | Alias maintained |
| rontend-taste | ui_frontend-taste | Alias maintained |
| hallmark | ui_hallmark | Alias maintained |
| rontend-redesign | ui_frontend-redesign | Alias maintained |
| rontend-review | ui_frontend-review | Alias maintained |
| karpathy-coding | code_karpathy | Alias maintained |
| ponytail | code_ponytail | Alias maintained |
| ull-output | code_full-output | Alias maintained |
| security-review | sec_security-review | Alias maintained |
| ietnam-payment-review | sec_vietnam-payment-review | Alias maintained |
| weknora-kb | i_weknora-kb | Alias maintained |
| ideo-generation | i_video-generation | Alias maintained |

## Rule Aliases

| Old Name | New Name | Status |
|----------|----------|--------|
| skill-registry | ule_skill-registry | Alias maintained |
| skill-integration | ule_skill-integration | Alias maintained |
| 	ask-analyzer | ule_task-analyzer | Alias maintained |
| intent-detection | ule_intent-detection | Alias maintained |

## Migration Path

### Old Way (v1)
`
.cursor/skills/landing-page-pro/SKILL.md
.cursor/skills/security-review/SKILL.md
.cursor/rules/skill-registry.mdc
`

### New Way (v2)
`
.cursor/skills/ui_landing-page-pro/SKILL.md
.cursor/skills/sec_security-review/SKILL.md
.cursor/rules/rule_skill-registry.mdc
`

## Auto-Detection

The skill-registry automatically handles both old and new names:
- Old names are aliased to new names
- References are auto-updated in skill-registry
- No code changes required for backward compatibility

## Deprecation Timeline

| Date | Change |
|------|--------|
| 2026-08-03 | v2.0 released with prefixes |
| 2026-10-01 | Alias warnings enabled |
| 2027-01-01 | Old names deprecated |
| 2027-06-01 | Old names removed |

## Benefits of New Naming

1. **Prefix-based discovery**: Easy to find skills by domain
2. **Auto-routing**: Keywords map directly to prefixes
3. **Namespace isolation**: No naming conflicts
4. **Scalability**: Add new domains without confusion

## Files Changed

- All skills renamed with prefix
- All rules renamed with prefix
- NAMING-CONVENTION.md created
- COMPATIBILITY.md (this file) created
- Alias links created for backward compatibility

## Support

For questions or issues with migration, see:
- NAMING-CONVENTION.md - Full naming guide
- .cursor/rules/rule_skill-registry.mdc - Skill definitions
- .cursor/INDEX.md - Skill index with new names
