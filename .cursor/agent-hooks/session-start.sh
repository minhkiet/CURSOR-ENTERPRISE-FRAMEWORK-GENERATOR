#!/bin/bash
# agent-skills session start hook
# Injects skills awareness into every new session

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/agent-skills"
META_SKILL="$SKILLS_DIR/using-agent-skills/SKILL.md"

if ! command -v jq >/dev/null 2>&1; then
  echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "agent-skills: jq not found. Skills available in .cursor/agent-skills/"}}'
  exit 0
fi

if [ -f "$META_SKILL" ]; then
  CONTENT=$(cat "$META_SKILL")
  jq -cn \
    --arg context "agent-skills loaded. Available skills in .cursor/agent-skills/

$CONTENT" \
    '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $context}}'
else
  echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "agent-skills: Skills available in .cursor/agent-skills/"}}'
fi
