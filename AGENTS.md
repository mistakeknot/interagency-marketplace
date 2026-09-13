# Interagency Marketplace - Development Guide

## Canonical References
1. [`PHILOSOPHY.md`](../../PHILOSOPHY.md) — direction for ideation and planning decisions.
2. `CLAUDE.md` — implementation details, architecture, testing, and release workflow.

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

## Writing to main

`main` rejects a direct push whose `structural` check has not already passed. This is deliberate and it binds administrators too, so there is no bypass to lean on (mk-0y69).

`.claude-plugin/marketplace.json` is read by every `claude plugin install` across the fleet. Before this gate, main's only rule demanded an approving review from a pool containing exactly one person: unsatisfiable by construction, bypassed on every publish, and printing `Bypassed rule violations` often enough that a genuine warning would not have stood out.

Validate locally first — it is the same script CI runs:

```bash
python3 scripts/validate-marketplace.py                      # offline, the required check
python3 scripts/validate-marketplace.py --check-sources      # resolve every plugin source
```

Add `--require-visible` when your token can see all 65 sources; it turns any entry the run could not resolve into an error rather than a warning. A run that could not look at something must not report that it looked.

### The two-step push

A fresh commit has no checks yet, so pushing it straight at `main` is refused. Land the SHA on a candidate ref, let the check run there, then advance `main` to that same SHA:

```bash
git push origin HEAD:refs/heads/publish-candidate
gh run watch "$(gh run list --branch publish-candidate --limit 1 --json databaseId --jq '.[0].databaseId')"
git push origin HEAD:main          # the SHA already passed; accepted without a PR
git push origin --delete publish-candidate
```

No pull request is involved. GitHub permits a direct push of a commit whose required checks have already succeeded, and the SHA must be **identical** — rebasing or amending between the two steps produces a new SHA with no checks, and the push is refused again.

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
