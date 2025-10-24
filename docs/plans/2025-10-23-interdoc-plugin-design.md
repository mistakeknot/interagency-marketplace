# Interdoc Plugin Design

**Date**: 2025-10-23
**Status**: Design Complete
**Target**: Claude Code Plugin for interagency-marketplace

## Overview

**Purpose**: Claude Code plugin that keeps CLAUDE.md documentation up-to-date by detecting significant code changes and suggesting relevant documentation updates.

**Key Insight**: CLAUDE.md files serve as crucial context for Claude Code sessions. Keeping them current is important but tedious. Interdoc automates detection and drafting while keeping humans in control.

## Requirements

### Tracked Change Categories

Interdoc monitors and suggests documentation for:
- **Architecture changes**: New patterns, structural changes, component additions/removals
- **Critical implementation details**: Lessons learned, gotchas, non-obvious constraints
- **Plugin/dependency changes**: New tools added, removed, or significantly changed
- **Repository conventions**: Naming patterns, file organization, workflow changes

### User Experience Principles

- **Review and approve**: User approves all suggestions before updating CLAUDE.md
- **Non-intrusive**: Don't interrupt during rapid iteration
- **Context-aware**: Adapt to existing CLAUDE.md structure and style
- **Helpful defaults**: Create CLAUDE.md if missing, handle mono-repos intelligently

## Architecture

### Dual Invocation Model

**Path A: Automatic (Post-Commit Hook)**
- Runs silently after each commit
- Smart detection identifies significant changes
- Logs pending suggestions to `.git/interdoc-pending`
- Shows one-line reminder if suggestions accumulate: `💡 Tip: 3 commits may need CLAUDE.md updates`
- Does NOT interrupt flow - user decides when to review

**Path B: Manual (Skill Invocation)**
- User requests: "update CLAUDE.md" or "review documentation"
- Processes all commits since last CLAUDE.md update
- Useful for: batch reviews, branch work, after feature completion

### Smart Detection Heuristics

**Trigger conditions** (any one flags as significant):
1. New directories created
2. File moves/renames (indicates refactoring)
3. Changes to config files: `package.json`, `tsconfig.json`, `.claude-plugin/*`, etc.
4. 3+ files changed in single commit (feature work)
5. New file types introduced (first `.rs`, `.py`, etc.)

**Skip conditions** (all must be true to skip):
1. Single file changed
2. File is markdown (likely docs)
3. Diff < 50 lines
4. No new files/directories

### Core Workflow

When invoked (manually or after accumulation):

1. **Detect baseline**: Find last CLAUDE.md modification via `git log CLAUDE.md`
2. **Analyze commits**: Get all commits since baseline
3. **Extract changes**: Analyze diffs for each commit
4. **Categorize changes**: Group into Architecture / Implementation / Dependencies / Conventions
5. **Generate suggestions**: Create proposed documentation updates with commit context
6. **Present for review**: Show suggestions with "approve all" or "review individually"
7. **Apply approved**: Update CLAUDE.md with user-approved changes
8. **Commit update**: Create documentation commit

### Categorization Logic

Claude applies judgment to categorize changes:

**Architecture** - Structural changes:
- New directories or major reorganization
- File moves affecting multiple files
- Changes to build/config files

**Implementation Details** - Important lessons:
- Bug fixes with non-obvious solutions
- Complex logic (>200 lines changed in one file)
- New error handling patterns

**Dependencies** - External tools:
- `package.json`, `Cargo.toml`, `requirements.txt` changes
- `.claude-plugin/*` modifications

**Conventions** - Repeated patterns:
- Consistent changes across 3+ files
- New naming or structure patterns
- Workflow additions

### Suggestion Format

For each category:
```markdown
## [Category]: [Brief Description]

**Triggered by**:
- [commit hash] [commit message]
- [commit hash] [commit message]

**Proposed documentation**:

[Text formatted to fit existing CLAUDE.md structure]

**Why this matters**: [Context for significance]
```

### Adaptive Structure

Claude reads existing CLAUDE.md to:
- Identify section hierarchy and headers
- Match tone and style
- Insert suggestions in appropriate sections
- Maintain consistent formatting

If CLAUDE.md doesn't have relevant sections, Claude suggests where to add them.

## Edge Case Behaviors

### Missing CLAUDE.md

When Interdoc detects changes but no CLAUDE.md exists:

```
I detected significant changes but CLAUDE.md doesn't exist.

Let me create one with a basic template:
- Repository Purpose
- Architecture
- Current Status
- Key Conventions

You can customize after I create it.
```

**Behavior**:
- Create CLAUDE.md with minimal template
- Apply current suggestions to new file
- Commit creation + initial documentation together

### Mono-repos

When multiple packages/modules exist:

```
I detected this is a mono-repo structure.

Your recent commits affected:
- packages/api/
- packages/shared/

I'll create CLAUDE.md files for each package:
- packages/api/CLAUDE.md (API-specific docs)
- packages/shared/CLAUDE.md (shared code docs)
- ./CLAUDE.md (root - overall architecture)

Updates will target the appropriate package-level files.
```

**Behavior**:
- Detect mono-repo structure (multiple `package.json`, workspace config, etc.)
- Create CLAUDE.md per package/module
- Root CLAUDE.md documents overall architecture
- Suggestions target the CLAUDE.md closest to changed files
- If changes span packages, suggest updates to multiple files

### Merge Commits

**Behavior**:
- Analyze merge commit's combined diff
- Attribute to the merge (not individual commits being merged)
- Flag large merges: "This merge includes X files - review major changes?"

### Large Refactors (>50 files)

**Behavior**:
- Group changes by directory/module
- Present high-level summary: "Architectural shift: [description]"
- Limit to top 3 most significant categories
- Suggest: "Large refactor detected - I'll focus on architectural patterns"

### Cross-AI Compatibility (AGENTS.md)

**Problem**: Users may want to use both Codex CLI (reads AGENTS.md) and Claude Code (reads CLAUDE.md) on the same codebase without maintaining duplicate documentation.

**Solution**: Generate minimal AGENTS.md files that redirect to CLAUDE.md:

```markdown
# Agent Context

For complete project documentation, read CLAUDE.md in this directory.

This file exists for Codex CLI compatibility. All project guidance, architecture, conventions, and lessons learned are maintained in CLAUDE.md.
```

**Behavior**:
- When creating/updating CLAUDE.md, check if AGENTS.md exists
- If missing, create AGENTS.md with redirect template
- Single source of truth maintained in CLAUDE.md
- Works for both root and mono-repo package directories

**Benefits**:
- Zero sync complexity
- Single file to maintain (CLAUDE.md)
- Both AI tools work seamlessly
- No duplicate or conflicting documentation

## Plugin Structure

```
interdoc/
├── .claude-plugin/
│   └── plugin.json           # Manifest referencing skill and hook
├── skills/
│   └── interdoc/
│       └── SKILL.md          # Main skill with workflow
├── hooks/
│   └── post-commit           # Shell script for detection
└── README.md                 # Plugin documentation
```

### Skill Frontmatter

```yaml
---
name: interdoc
description: Use when user requests CLAUDE.md updates or when documentation needs review after code changes. Analyzes git commits to suggest documentation updates for architecture, implementation details, dependencies, and conventions.
---
```

This description catches:
- "update CLAUDE.md"
- "review documentation"
- "add this to CLAUDE.md"
- "document recent changes"

### Post-Commit Hook

Simple shell script:
```bash
#!/bin/bash
# Log commit for later review
echo "$(git rev-parse HEAD)" >> .git/interdoc-pending

# Check if significant (run heuristics)
# If significant and pending count > threshold, show reminder
```

Hook stays lightweight - main logic lives in the skill.

## Success Criteria

**Primary**:
- Reduces manual CLAUDE.md maintenance burden by 80%
- Catches significant changes that should be documented
- Low false positive rate (doesn't trigger on trivial changes)

**Secondary**:
- Users approve 50%+ of suggestions (signal/noise ratio)
- CLAUDE.md stays current within 1 week of major changes
- Hook doesn't feel annoying or interruptive

## Future Enhancements (Out of Scope for v1)

- Learn from user acceptance/rejection patterns
- Suggest removing outdated sections
- Integration with PR descriptions
- Template library for common documentation patterns
- Cross-reference with existing docs

## Implementation Notes

- Written as Claude Code skill (high-level instructions)
- Claude determines specific git commands and parsing
- Focus on workflow clarity and edge case guidance
- Let Claude apply judgment for categorization

## Distribution

1. Create plugin in separate repo: `mistakeknot/interdoc`
2. Publish to GitHub
3. Add to interagency-marketplace via:
   ```json
   {
     "name": "interdoc",
     "source": "mistakeknot/interdoc",
     "description": "Keep CLAUDE.md documentation up-to-date automatically"
   }
   ```

## Review Notes

**Interpeer feedback** (2025-10-23):
- ✅ Design is appropriately high-level for Claude Code plugin
- ✅ Edge case behaviors specified
- ✅ UX considerations addressed (batching, non-intrusive)
- ✅ Mono-repo handling clarified
