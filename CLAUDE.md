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
