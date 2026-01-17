# Interagency Marketplace

> See `AGENTS.md` for full development guide, schema details, and plugin creation workflows.

## Overview

Claude Code plugin marketplace - JSON-based catalog for distributing plugins. Hosted at `mistakeknot/interagency-marketplace`.

## Status: Production

Two plugins distributed: Interpeer (v3.0.0), Interdoc (v2.1.0).

## Quick Commands

```bash
# Users install marketplace
/plugin marketplace add mistakeknot/interagency-marketplace

# Users install plugins
/plugin install interpeer
/plugin install interdoc
```

## Key Files

- `.claude-plugin/marketplace.json` - Central registry
- `plugins/*/` - Plugin directories (if locally hosted)

## Current Plugins

| Plugin | Version | Purpose |
|--------|---------|---------|
| Interpeer | 3.0.0 | Cross-AI peer review (3 skills) |
| Interdoc | 2.1.0 | Automatic CLAUDE.md maintenance |

## Design Decisions (Do Not Re-Ask)

- **External repos**: Both plugins in separate GitHub repos (mistakeknot/interpeer, mistakeknot/interdoc)
- **URL source format**: Must use `{ "source": "url", "url": "..." }` object, not shorthand
- **All fields required**: name, source, description, version, keywords, strict for validation
- **Git URLs with .git**: Full URLs like `https://github.com/owner/repo.git`
