# Interagency Marketplace

> See `AGENTS.md` for full development guide, schema details, and plugin creation workflows.

## Overview

Claude Code plugin marketplace - JSON-based catalog for distributing plugins. Hosted at `mistakeknot/interagency-marketplace`.

## Status: Production

32 plugins distributed.

## Quick Commands

```bash
# Users install marketplace
/plugin marketplace add mistakeknot/interagency-marketplace

# Users install plugins
/plugin install clavain
/plugin install interdoc
```

## Key Files

- `.claude-plugin/marketplace.json` - Central registry (source of truth)

## Plugin Publishing Runbook

### Adding a New Plugin

1. **Ensure plugin repo has `.claude-plugin/plugin.json`**:
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What it does",
     "author": { "name": "...", "email": "..." },
     "repository": "https://github.com/owner/repo",
     "license": "MIT",
     "skills": ["./skills/my-skill"],
     "commands": ["./commands/my-command.md"],
     "hooks": "./hooks/hooks.json"
   }
   ```

2. **Add entry to marketplace.json**:
   ```json
   {
     "name": "my-plugin",
     "source": {
       "source": "url",
       "url": "https://github.com/owner/repo.git"
     },
     "description": "Short description for marketplace listing",
     "version": "1.0.0",
     "keywords": ["relevant", "keywords"],
     "strict": true
   }
   ```

3. **Update README.md** with plugin documentation

4. **Commit and push**:
   ```bash
   git add .claude-plugin/marketplace.json README.md
   git commit -m "feat: add my-plugin to marketplace"
   git push
   ```

### Updating an Existing Plugin

```bash
# 1. Plugin author bumps version in their repo
#    (edit .claude-plugin/plugin.json, commit, push)

# 2. Update marketplace to match
edit .claude-plugin/marketplace.json  # bump version
git add .claude-plugin/marketplace.json
git commit -m "chore: bump my-plugin to vX.Y.Z"
git push
```

### marketplace.json Schema

```json
{
  "name": "interagency-marketplace",
  "owner": { "name": "...", "email": "..." },
  "metadata": { "description": "...", "version": "1.0.0" },
  "plugins": [
    {
      "name": "plugin-name",           // Required: matches plugin.json name
      "source": {                      // Required: where to fetch
        "source": "url",
        "url": "https://github.com/owner/repo.git"
      },
      "description": "...",            // Required: marketplace listing
      "version": "X.Y.Z",              // Required: must match plugin.json
      "keywords": ["..."],             // Required: for search/discovery
      "strict": true                   // Required: enables validation
    }
  ]
}
```

## Design Decisions (Do Not Re-Ask)

- **External repos**: All plugins in separate GitHub repos under mistakeknot/
- **URL source format**: Must use `{ "source": "url", "url": "..." }` object, not shorthand
- **All fields required**: name, source, description, version, keywords, strict for validation
- **Git URLs with .git**: Full URLs like `https://github.com/owner/repo.git`
