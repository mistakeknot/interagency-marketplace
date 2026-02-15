# Interagency Marketplace - Development Guide

> Claude Code plugin marketplace - JSON-based catalog for distributing Claude Code plugins.

## Overview

Hosted at `mistakeknot/interagency-marketplace`, accessed via `/plugin marketplace add mistakeknot/interagency-marketplace`.

## Architecture

### Marketplace Structure

1. **Marketplace Catalog** (`.claude-plugin/marketplace.json`)
   - Central registry with marketplace identity and plugin listing
   - Contains: marketplace name, owner info, array of plugin entries
   - Each plugin entry: `name`, `source`, `description`, `version`, `keywords`, `strict`

2. **Plugin Directories** (`plugins/*/`)
   - Self-contained plugins with `.claude-plugin/plugin.json` manifest
   - Can include: skills, commands, agents, hooks

### Plugin Anatomy

```
plugins/plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── skills/                  # Optional: agent skills
│   └── skill-name/
│       └── SKILL.md
├── commands/                # Optional: slash commands
├── agents/                  # Optional: specialized agents
└── hooks/                   # Optional: lifecycle hooks
```

## Current Plugins

### Interpeer (v3.0.0)
Cross-AI peer review plugin with three focused skills:

| Skill | Tool | Use Case |
|-------|------|----------|
| `/qinterpeer` | Codex CLI | Quick reviews, fast feedback |
| `/interpeer` | Oracle (ChatGPT 5.2 Pro) | Deep reasoning, large context |
| `/winterpeer` | LLM Council | Multi-model consensus for critical decisions |

**External dependencies:**
- Codex CLI (`npm install -g @openai/codex`)
- Oracle (`npm install -g @steipete/oracle`)

**Repository:** `mistakeknot/interpeer`

### interdoc (v2.1.0)
Automatic CLAUDE.md maintenance plugin:
- Dual detection: SessionStart (3+ commits), PostToolUse (10+ commits)
- Uses prompt injection hooks for automatic documentation reviews
- Generates AGENTS.md redirects for Codex CLI compatibility
- Supports mono-repos with multiple CLAUDE.md files

## Plugin Manifest Schema

### plugin.json Structure
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": { "name": "...", "email": "..." },
  "skills": ["./skills/skill-name"],
  "commands": ["./commands/command-name"],
  "agents": ["./agents/agent-name"],
  "hooks": ["./hooks/hook-name"]
}
```

### marketplace.json Schema
```json
{
  "name": "marketplace-name",
  "owner": { "name": "...", "email": "..." },
  "metadata": { "description": "...", "version": "..." },
  "plugins": [
    {
      "name": "plugin-name",
      "source": { "source": "url", "url": "https://github.com/owner/repo.git" },
      "description": "...",
      "version": "x.y.z",
      "keywords": ["tag1", "tag2"],
      "strict": true
    }
  ]
}
```

**Critical:** Source must be object with `source: "url"` and `url` fields, not simple string.

## Adding a New Plugin

1. Create plugin directory: `plugins/plugin-name/`
2. Create manifest: `plugins/plugin-name/.claude-plugin/plugin.json`
3. Add plugin content (skills, commands, etc.)
4. Register in `.claude-plugin/marketplace.json`
5. Create README: `plugins/plugin-name/README.md`
6. Update main `README.md`

## Creating Skills

Skills go in `plugins/plugin-name/skills/skill-name/SKILL.md`:

```markdown
---
name: skill-name
description: Brief description of when Claude should use this skill
---

# Skill Title

[Skill implementation content]
```

The `description` field tells Claude when to automatically invoke the skill.

## Plugin Source Options

- **Local path**: `"./plugins/plugin-name"`
- **GitHub shorthand**: `"owner/repo"` or `"github:owner/repo"`
- **Git URL**: `"https://github.com/owner/repo.git"`
- **Other git**: `"https://gitlab.com/owner/repo.git"`

## User Installation

```bash
# Add marketplace
/plugin marketplace add mistakeknot/interagency-marketplace

# Install plugin
/plugin install plugin-name
```

## Marketplace Owner

Current: MK <mistakeknot@vibeguider.org>

Update in both:
1. `.claude-plugin/marketplace.json` - `owner` field
2. Individual plugin manifests - `author` field
