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

Get a second opinion in the form of expert feedback from OpenAI Codex CLI on designs, implementations, or approaches, then review and discuss that feedback with the user.

**Features:**
- Design document review and validation
- Code quality and architecture feedback
- Cross-AI peer review workflow
- Collaborative discussion of feedback
- Multi-perspective technical analysis

**Prerequisites:** Requires [OpenAI Codex CLI](https://github.com/openai/codex-cli) installed and configured.

**Installation:**
```bash
/plugin install interpeer
```

**Learn more:** [Interpeer Plugin Documentation](plugins/interpeer/README.md)

### Interdoc

Automatic, ambient CLAUDE.md maintenance - detects changes when you start a session and proactively suggests documentation updates without manual invocation.

**Features:**
- Fully automatic activation on session start
- Ambient operation - analyzes and suggests without manual invocation
- Smart categorization (Architecture, Implementation, Dependencies, Conventions)
- Adaptive to your existing CLAUDE.md structure
- Mono-repo support with multiple CLAUDE.md files
- AGENTS.md redirect generation for Codex CLI compatibility

**Installation:**
```bash
/plugin install interdoc
```

**Learn more:** [Interdoc Plugin Repository](https://github.com/mistakeknot/interdoc)

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
