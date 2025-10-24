# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **Claude Code plugin marketplace** - a JSON-based catalog for distributing Claude Code plugins. The marketplace is hosted at `mistakeknot/interagency-marketplace` and accessed via `/plugin marketplace add mistakeknot/interagency-marketplace`.

## Architecture

### Marketplace Structure

The marketplace has two key components:

1. **Marketplace Catalog** (`.claude-plugin/marketplace.json`)
   - Central registry defining marketplace identity and plugin listing
   - Contains: marketplace name, owner info, array of plugin entries
   - Each plugin entry has: `name`, `source`, `description`
   - Source can be: local path (`./plugins/name`), GitHub repo (`owner/repo`), or git URL

2. **Plugin Directories** (`plugins/*/`)
   - Plugins can be hosted directly in this repo under `plugins/`
   - Each plugin is self-contained with its own `.claude-plugin/plugin.json` manifest
   - Plugins can include: skills, commands, agents, hooks (optional directories)

### Plugin Anatomy

Each plugin in `plugins/` follows this structure:

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

**Critical**: The `plugin.json` manifest must reference all skills, commands, agents, or hooks by their relative paths within the plugin directory.

## Working with Plugins

### Adding a New Plugin to the Marketplace

When creating a new plugin:

1. Create plugin directory: `plugins/plugin-name/`
2. Create manifest: `plugins/plugin-name/.claude-plugin/plugin.json`
   - Set name, version, description, author
   - Reference any skills/commands/agents/hooks
3. Add plugin content (skills, commands, etc.)
4. Register in marketplace catalog: `.claude-plugin/marketplace.json`
   - Add entry to `plugins` array with name, source, description
   - Source should be `./plugins/plugin-name` for locally-hosted plugins
5. Create plugin README: `plugins/plugin-name/README.md`
6. Update main `README.md` with plugin details

### Plugin Manifest Requirements

`plugin.json` structure:
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": {
    "name": "Author Name",
    "email": "email@example.com"
  },
  "skills": ["./skills/skill-name"],
  "commands": ["./commands/command-name"],
  "agents": ["./agents/agent-name"],
  "hooks": ["./hooks/hook-name"]
}
```

### Creating Skills

Skills go in `plugins/plugin-name/skills/skill-name/SKILL.md` with this frontmatter:

```markdown
---
name: skill-name
description: Brief description of when Claude should use this skill
---

# Skill Title

[Skill implementation content]
```

The `description` field in frontmatter tells Claude when to automatically invoke the skill. Be specific about use cases.

## Marketplace Distribution

Users install the marketplace via:
```
/plugin marketplace add mistakeknot/interagency-marketplace
```

Then install individual plugins:
```
/plugin install plugin-name
```

The marketplace pulls from the GitHub repository at `https://github.com/mistakeknot/interagency-marketplace`.

## Current Plugins

### Interpeer
Cross-AI peer review plugin that integrates OpenAI Codex CLI for design/code feedback.

**Key implementation notes:**
- Skill requires external dependency: OpenAI Codex CLI must be installed
- Uses bash tool to pipe content to `codex exec --sandbox read-only`
- Implements 5-phase workflow: prepare, call Codex, present feedback, discuss, plan actions
- Emphasizes collaborative review (not automated acceptance of suggestions)

**Critical constraints (v1.1.0+):**
- **Always use `timeout`**: All Codex calls must use `timeout 180` (3 min max) to prevent runaway processes
- **Always include constraints in prompts**: TIME BUDGET, FILE LIMIT, OUTPUT REQUIRED
- **Phased reviews for complex projects**: Break into architecture → security → performance phases
- **Force early output**: Prompts must require "START RESPONSE NOW" to prevent analysis loops
- **Monitor for loops**: Watch for repeated file reads (>3 times) or lack of output after 2-3 minutes
- **Curated file lists**: Provide specific files to review instead of open exploration

**Lessons learned:**
- Without constraints, Codex can loop indefinitely re-reading files without producing output
- Open-ended prompts like "comprehensive review" encourage exhaustive exploration mode
- Must explicitly force synthesis with "OUTPUT REQUIRED: Respond immediately"
- Complex projects need phased approach: quick scan → targeted deep dive
- Recovery from loops: kill process, restart with narrower scope asking "what did you find so far?"

### Interdoc
Automatic CLAUDE.md maintenance plugin that keeps documentation current.

**Key implementation notes:**
- Dual detection system: SessionStart (3+ commits) and PostToolUse (10+ commits during session)
- Uses prompt injection hooks to automatically trigger documentation reviews
- Generates AGENTS.md redirects for Codex CLI compatibility
- Supports mono-repos with multiple CLAUDE.md files
- User approves all suggestions - fully ambient but human-controlled

**Version**: 2.1.0

## Plugin Distribution Strategy

The marketplace follows a **dual plugin model**:

1. **Interpeer**: External review and collaboration
   - Integrates OpenAI Codex CLI
   - Cross-AI peer review
   - Published at: `mistakeknot/interpeer`

2. **Interdoc**: Internal documentation maintenance
   - CLAUDE.md automation
   - Ambient operation via hooks
   - Published at: `mistakeknot/interdoc`

Both plugins use `source.source: "url"` format and are hosted in separate GitHub repositories referenced by the marketplace.

## Plugin Marketplace Schema

The marketplace.json schema has specific requirements that must be followed:

**Required top-level fields**:
```json
{
  "name": "marketplace-name",
  "owner": { "name": "...", "email": "..." },
  "metadata": {
    "description": "...",
    "version": "..."
  },
  "plugins": [...]
}
```

**Required plugin fields**:
```json
{
  "name": "plugin-name",
  "source": {
    "source": "url",
    "url": "https://github.com/owner/repo.git"
  },
  "description": "...",
  "version": "x.y.z",
  "keywords": ["tag1", "tag2"],
  "strict": true
}
```

**Critical lessons learned**:
- Source must be an object with `source: "url"` and `url` fields, not a simple string
- Cannot use shorthand like `"owner/repo"` - must use full git URL with `.git` extension
- All plugin fields (name, source, description, version, keywords, strict) are required for validation
- Metadata object is required at marketplace level
- Schema validation is strict - missing or incorrectly formatted fields will cause marketplace loading to fail

## Plugin Source Options

The `source` field in marketplace.json supports:
- **Local path**: `"./plugins/plugin-name"` - for plugins in this repo
- **GitHub shorthand**: `"owner/repo"` or `"github:owner/repo"`
- **Git URL**: `"https://github.com/owner/repo.git"`
- **Other git**: `"https://gitlab.com/owner/repo.git"`

## Repository Maintenance

When updating marketplace owner information, update both:
1. `.claude-plugin/marketplace.json` - `owner` field
2. Individual plugin manifests - `author` field

Current owner: MK <mistakeknot@vibeguider.org>
