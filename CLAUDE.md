# Interagency Marketplace

> See `AGENTS.md` for full development guide, schema details, and plugin creation workflows.

## Overview

Claude Code plugin marketplace - JSON-based catalog for distributing plugins. Hosted at `mistakeknot/interagency-marketplace`.

## Status: Production

40 plugins distributed.

## Quick Commands

```bash
# Users install marketplace
/plugin marketplace add mistakeknot/interagency-marketplace

# Users install plugins
/plugin install clavain
/plugin install interdoc
```

## Key Files

- `.claude-plugin/marketplace.json` — Central registry (source of truth)

Publishing runbook, schema details, and design decisions are in `AGENTS.md`.
