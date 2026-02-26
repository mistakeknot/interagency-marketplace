# Batch Update: README.md Installation Sections with Marketplace Instructions

**Date:** 2026-02-23
**Scope:** 34 Interverse plugin README.md files
**Script:** `/tmp/update-readmes.py`

## Summary

Updated 31 of 34 Interverse plugin README.md files to include interagency marketplace setup instructions before the `/plugin install` command. Three files were skipped (with reasons). The update was applied using a Python script that handles four distinct README patterns.

## Changes Made

Each modified README's installation section now follows a two-step pattern:

```markdown
First, add the [interagency marketplace](https://github.com/mistakeknot/interagency-marketplace) (one-time setup):

```bash
/plugin marketplace add mistakeknot/interagency-marketplace
```

Then install the plugin:

```bash
/plugin install <name>
```
```

## Pattern Classification

### Pattern 1: Standard `## Installation` (27 plugins)

Most common pattern. A `## Installation` header followed immediately by a code block containing `/plugin install <name>`.

**Plugins:** intercheck, intercraft, interdev, interfin, interflux, interform, interleave, interline, intermap, intermem, intermux, internext, interpub, interstat, intersynth, intertest, tool-time (simple code block); interject, interkasten, interlock, interpath, interwatch, interpeer, interserve, interslack, intersearch, tuivision (code block + post-install notes preserved).

**Transformation:** Inserted marketplace block between `## Installation` header and existing code block. Post-install notes (e.g., "Requires Node.js for the MCP server", "Requires the intermute service running", "Companion plugin for Clavain") were preserved.

### Pattern 2: `## Installation` with "Or manually:" Alternative (1 plugin)

**Plugin:** interdoc

**Before:**
```markdown
## Installation

```bash
/plugin install interdoc
```

Or manually:

```bash
git clone https://github.com/mistakeknot/interdoc.git
cd interdoc && /plugin install .
```
```

**Transformation:** Inserted marketplace block before both install options. The "Or manually:" alternative was preserved intact.

### Pattern 3: `## Getting Started` with Install Paragraph (2 plugins)

**Plugins:** interfluence, interlearn

**interfluence before:**
```markdown
## Getting Started

Install from the interagency marketplace:

```
/plugin install interfluence
```
```

**interlearn before (different install command format):**
```markdown
## Getting Started

Install from the interagency marketplace:

```bash
claude plugins install interlearn@interagency-marketplace
```
```

**Transformation:** Replaced "Install from the interagency marketplace:" paragraph + code block with the two-step marketplace pattern. For interlearn, also normalized the install command from `claude plugins install interlearn@interagency-marketplace` to `/plugin install interlearn`. Preserved the "Then:" continuation text that follows in both cases.

### Skipped Files (3 plugins)

| Plugin | Reason | Detail |
|--------|--------|--------|
| **interchart** | No plugin install line | Visualization tool, not a Claude Code plugin; uses `bash scripts/generate.sh` |
| **interlens** | No plugin install line | Monorepo (`pnpm -r install`), not a `/plugin install` target |
| **tldr-swinton** | Already has marketplace | `## Agent Integration > ### Claude Code Plugin` section already contains `marketplace add` |

## Plugins with Post-Install Notes (Preserved)

These plugins have text between the install code block and the next `##` header that was preserved:

| Plugin | Note |
|--------|------|
| interkasten | "Requires Node.js for the MCP server." |
| interlock | "Requires the intermute service running (the Go coordination backend)." |
| interject | "Requires `intersearch` as a dependency (shared embedding infrastructure)." |
| interpeer | "Requires Codex CLI for quick mode and Oracle CLI for deep mode." |
| interserve | "Requires Clavain's `dispatch.sh` for Codex spark dispatch." |
| interslack | "Requires slackcli installed and configured with your Slack session tokens." |
| tuivision | System dependency instructions (apt/brew install for canvas rendering) |
| interpath | "Companion plugin for Clavain." |
| interwatch | "Companion plugin for Clavain." |
| interphase | "Companion plugin for Clavain -- most useful when installed alongside the core engineering plugin." |
| interline | Setup command instructions after install block |
| interfin | Separate CLI install instructions after plugin install |
| interdoc | "Or manually:" alternative install block |
| intersearch | "Typically installed automatically as a dependency." |

## Script Details

**Location:** `/tmp/update-readmes.py`

**Usage:**
```bash
python3 /tmp/update-readmes.py --dry-run   # Preview changes (no writes)
python3 /tmp/update-readmes.py              # Apply changes
```

**Approach:**
1. Globs all `README.md` files in `/home/mk/projects/Demarch/interverse/*/README.md`
2. Skips files that already contain `marketplace add`
3. Skips files without any `/plugin install` or `claude plugins install` line
4. Routes to the correct handler based on plugin name and content patterns
5. Uses regex to find and replace the installation section
6. Preserves all content after the install code block (notes, companion plugin references)
7. Prints unified diffs for all changes

**Idempotency:** Running the script a second time would skip all 34 files (31 already have `marketplace add`, 3 were already skipped for other reasons).

## Verification

Spot-checked four representative files after modification:

1. **intercheck** (standard): Clean two-step install, proper section separation
2. **interfluence** (Getting Started): Marketplace block + preserved "Then:" continuation
3. **interlearn** (Getting Started, old format): Normalized install command + preserved continuation
4. **interkasten** (post-install note): "Requires Node.js" preserved after install block

## Files Not Committed

No git commits or pushes were made. The 31 modified README files are sitting as uncommitted changes across their respective plugin directories in the monorepo at `/home/mk/projects/Demarch/interverse/`.
