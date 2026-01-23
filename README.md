# Interagency Marketplace

A Claude Code plugin marketplace for discovering and installing plugins that help with interoperability between different coding agents like Claude Code and Codex CLI.

## What is this?

This is a plugin marketplace for [Claude Code](https://claude.com/claude-code) - a centralized catalog that lists available plugins and describes where to find them.

## Installation

To add this marketplace to your Claude Code installation:

```bash
/plugin marketplace add mistakeknot/interagency-marketplace
```

Once added, you can browse and install plugins from this marketplace using Claude Code.

## Available Plugins

### Interpeer

Cross-AI peer review with multiple modes for different use cases.

**Skills:**
- `qinterpeer` - Quick peer review using Codex CLI for fast feedback
- `interpeer` - Deep peer review using Oracle (ChatGPT 5.2 Pro) with large context
- `winterpeer` - LLM Council review for critical decisions (GPT + Claude consensus)
- `splinterpeer` - Extract disagreements and convert into actionable artifacts

**Features:**
- Auto-detects available AI tools (Codex CLI, Oracle)
- Large context support (~200k tokens with Oracle)
- Disagreement-driven development workflow
- Multi-perspective technical analysis

**Prerequisites:** Requires [Codex CLI](https://github.com/openai/codex) or [Oracle CLI](https://github.com/anthropics/oracle) installed.

**Installation:**
```bash
/plugin install interpeer
```

**Learn more:** [Interpeer Plugin Documentation](https://github.com/mistakeknot/interpeer)

### Interdoc

Recursive AGENTS.md generator using parallel subagents. Generates cross-AI compatible documentation that works with Claude Code, Codex CLI, and other AI tools.

**Features:**
- Parallel subagents for fast analysis across directories
- CLAUDE.md harmonization - migrates docs to AGENTS.md, slims CLAUDE.md to settings only
- Incremental updates - appends new content, preserves existing documentation
- Unified diff previews with individual file review option
- Smart monorepo scoping for large projects
- Git-aware updates using commit history and diffs
- Subagent verification before committing

**Skill:** `interdoc` - Triggered by natural language ("generate documentation", "update AGENTS.md") or automatically via hooks.

**Installation:**
```bash
/plugin install interdoc
```

**Learn more:** [Interdoc Plugin Repository](https://github.com/mistakeknot/interdoc)

### tldrs

Token-efficient code reconnaissance for LLMs with 85%+ token savings.

**Commands:**
- `/tldrs-diff` - Diff-focused context for recent changes
- `/tldrs-find <query>` - Semantic code search by concept
- `/tldrs-context <symbol>` - Symbol-level context with call graph
- `/tldrs-quickstart` - Quick reference guide

**Features:**
- Diff-first workflow (prioritizes recent changes)
- Semantic search using Ollama/sentence-transformers embeddings
- Delta mode for multi-turn conversations (~60% additional savings)
- Token budgets to prevent context blowup
- VHS refs for large output storage

**Prerequisites:** Requires the `tldrs` CLI installed in the environment.

```bash
curl -fsSL https://raw.githubusercontent.com/mistakeknot/tldr-swinton/main/scripts/install.sh | bash
```

**Installation:**
```bash
/plugin install tldrs
```

**Learn more:** [tldr-swinton](https://github.com/mistakeknot/tldr-swinton) · [tldrs-vhs](https://github.com/mistakeknot/tldrs-vhs)

---

See [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) for the complete catalog.

## Adding Plugins to this Marketplace

To add a new plugin to this marketplace:

1. Fork this repository
2. Edit `.claude-plugin/marketplace.json`
3. Add your plugin entry:
   ```json
   {
     "name": "your-plugin-name",
     "source": "github-username/repo-name",
     "description": "What your plugin does"
   }
   ```
4. Submit a pull request

### Plugin Source Options

The `source` field supports multiple formats:

- **GitHub repo**: `"owner/repo"` or `"github:owner/repo"`
- **Git URL**: `"https://github.com/owner/repo.git"`
- **Local path**: `"./plugins/my-plugin"` (for plugins in this repo)
- **Other git services**: `"https://gitlab.com/owner/repo.git"`

## Marketplace Structure

```
.
├── .claude-plugin/
│   └── marketplace.json    # Plugin catalog
├── plugins/                # Plugins hosted in this repo
│   └── interpeer/          # Interpeer plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── interpeer/
│       │       └── SKILL.md
│       └── README.md
└── README.md
```

## Usage

After adding this marketplace, users can:

```bash
# Browse available plugins
/plugin marketplace browse

# Install a plugin from this marketplace
/plugin install plugin-name

# Update plugins from marketplaces
/plugin marketplace update
```

## Learn More

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Plugin Marketplaces Guide](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces)
