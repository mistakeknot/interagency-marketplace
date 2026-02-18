# Interagency Marketplace

A Claude Code plugin marketplace — 32 plugins for building software with agents, across coordination, review, documentation, observability, and workflow.

## Installation

```bash
/plugin marketplace add mistakeknot/interagency-marketplace
```

Once added, browse and install any plugin below:

```bash
/plugin install <plugin-name>
```

## Plugins

### Clavain

General-purpose engineering discipline plugin. 5 agents, 37 commands, 27 skills, 1 MCP server — the hub that ties together workflow discipline, Codex dispatch, cross-AI review, and structured debate. Most of the companion plugins below were extracted from Clavain as they grew complex enough to deserve their own repos.

```bash
/plugin install clavain
```

### interdoc

Recursive AGENTS.md generator with parallel subagents. Point it at a project and it produces cross-AI compatible documentation — works with Claude Code, Codex CLI, whatever comes next. Handles CLAUDE.md harmonization (migrates content to AGENTS.md, slims CLAUDE.md to settings only), incremental updates, unified diff previews, and smart monorepo scoping.

```bash
/plugin install interdoc
```

### interfluence

Analyze your writing style and get Claude to actually sound like you. Ingest writing samples, build a prose voice profile, and apply it to any human-facing documentation or copy. The profile is natural language (not numeric scores) because Claude follows prose instructions better than parameter tuning.

```bash
/plugin install interfluence
```

### interflux

Multi-agent document review engine — scored triage picks the right domain agents, content slicing keeps each agent focused, and knowledge injection gives them project context. 7 specialized review agents covering architecture, safety, correctness, performance, quality, game design, and user/product. Also powers the `flux-research` multi-agent research workflow.

```bash
/plugin install interflux
```

### intersynth

The synthesis layer for multi-agent workflows. When interflux (or any parallel agent pattern) produces findings from multiple agents, intersynth collects them, deduplicates across agents, writes structured verdicts, and produces a compact summary. The glue that turns parallel agent output into something coherent.

```bash
/plugin install intersynth
```

### interpeer

Cross-AI peer review with 4 escalation modes: quick (Claude/Codex for fast feedback), deep (Oracle/GPT for large context), council (multi-model consensus for critical decisions), and mine (extract disagreements between models and convert them into tests and specs). The disagreement-driven development workflow is genuinely useful — models disagree about interesting things.

```bash
/plugin install interpeer
```

### intertest

Engineering quality disciplines — three skills that enforce process when it matters most. Systematic debugging (4-phase root-cause investigation, no guessing), test-driven development (strict RED-GREEN-REFACTOR, no skipping), and verification gates (evidence-based checks before claiming something works).

```bash
/plugin install intertest
```

### interphase

Phase tracking and gate validation for the Beads issue tracker. Adds lifecycle state management — discovery, planning, building, review, shipping — on top of the core beads workflow. Enforces gates between phases so work doesn't skip steps.

```bash
/plugin install interphase
```

### interpath

Product artifact generator. Pulls from beads state, brainstorms, and project context to produce roadmaps, PRDs, vision docs, changelogs, and status reports. The artifacts stay connected to the actual work state rather than drifting into aspirational fiction.

```bash
/plugin install interpath
```

### interwatch

Documentation freshness monitoring. Runs drift detection across product artifacts and code docs, scores confidence, and orchestrates auto-refresh when things get stale. Solves the perennial problem of docs that were accurate three weeks ago.

```bash
/plugin install interwatch
```

### interline

Dynamic statusline for Claude Code — shows active beads with priority and title, workflow phase, coordination status, and Codex dispatch state. Integrates with Clavain, interphase, interlock, and beads to give you a persistent awareness of what's happening without checking manually.

```bash
/plugin install interline
```

### interlock

Multi-agent file coordination via MCP. Reserve files before editing, detect conflicts, exchange messages between agents. Wraps the intermute coordination service with hooks, commands, skills, and git pre-commit enforcement. The thing that prevents two agents from editing the same file simultaneously and producing a mess.

```bash
/plugin install interlock
```

### intermux

Agent activity visibility — monitors tmux sessions, provides activity feeds, detects health issues. 7 MCP tools for cross-agent observability. When you have multiple agents running in tmux panes, intermux tells you what each one is doing without switching panes.

```bash
/plugin install intermux
```

### intermap

Project-level code mapping MCP server. Maintains a project registry, generates call graphs, runs impact analysis, and provides an agent overlay so Claude understands the codebase topology. Go backend with a Python bridge for the analysis layer.

```bash
/plugin install intermap
```

### interject

Ambient discovery and research engine. Scans arXiv, Hacker News, GitHub, Anthropic docs, and Exa for new capabilities relevant to your projects. MCP server with an embedding-based recommendation engine, confidence-tiered output, and learned interest profiles that improve over time.

```bash
/plugin install interject
```

### interserve

Codex spark classifier and context compression. MCP server exposing `classify_sections`, `extract_sections`, and `codex_query` tools for token-efficient document handling. Useful when you need to route large documents to the right processing pipeline without reading everything.

```bash
/plugin install interserve
```

### interkasten

Bidirectional Notion sync for Claude Code. Three-way merge conflict resolution, beads issue tracking integration, and 21 MCP tools for project lifecycle management. The bridge between your Notion workspace and your codebase — changes flow both directions.

```bash
/plugin install interkasten
```

### intercheck

Code quality guards and session health monitoring. Tracks context pressure with time-decay scoring, validates syntax for 8 languages, and auto-formats via ruff/shfmt/gofmt/jq/prettier. Catches the kind of problems that compound when you're deep in a long coding session.

```bash
/plugin install intercheck
```

### interstat

Token efficiency benchmarking. PostToolUse hooks capture real-time events to SQLite, SessionEnd hooks backfill token data from JSONL transcripts, and the report shows percentiles with a decision gate. Answers the question "am I actually using tokens efficiently or just burning through context?"

```bash
/plugin install interstat
```

### internext

Work prioritization and next-task analysis. Reads beads state and project context, scores candidates on impact/effort/risk, identifies dependency leverage (a P2 that unblocks three P1s beats a standalone P1), and gives an opinionated recommendation — not a menu.

```bash
/plugin install internext
```

### intermem

Memory synthesis — graduates stable auto-memory facts to AGENTS.md and CLAUDE.md. Detects stability (a fact confirmed across multiple sessions), deduplicates against existing docs, presents changes for interactive approval, and prunes the source. Prevents the memory directory from growing without bound while preserving what matters.

```bash
/plugin install intermem
```

### interpub

Safe plugin publishing. Bumps all version locations (plugin.json, package.json, marketplace entry), validates sync, then commits and pushes with confirmation. Exists because manually keeping three version strings in sync across two repos is exactly the kind of thing humans mess up.

```bash
/plugin install interpub
```

### interdev

Developer tooling for Claude Code — MCP CLI interaction, skill authoring, plugin development scaffolding, and Claude Code reference docs. The meta-plugin for building plugins.

```bash
/plugin install interdev
```

### intercraft

Agent-native architecture patterns. Design, review, and audit applications where agents are first-class citizens — ensuring that any action a user can take, an agent can also take. Includes a scored audit skill for evaluating agent-native parity.

```bash
/plugin install intercraft
```

### interform

Design patterns and visual quality for Claude Code interfaces. Provides guidance for building distinctive, production-grade UIs rather than the default "it works but looks like a prototype" aesthetic.

```bash
/plugin install interform
```

### interslack

Slack integration for Claude Code. Send messages, read channels, test webhook integrations. Straightforward plumbing.

```bash
/plugin install interslack
```

### interlens

288 FLUX cognitive lenses for structured thinking. MCP server with lens search, thinking mode workflows, belief statement generation, quality evaluation, and solution synthesis. When you want to examine a problem through a specific analytical frame — systems dynamics, game theory, cognitive biases — this gives you the vocabulary.

```bash
/plugin install interlens
```

### interleave

Deterministic Skeleton with LLM Islands — a token-efficient document generation pattern where scripts render the predictable parts and LLM subagents fill only the semantic sections. Spec + library plugin with a reference implementation (roadmap generation from beads data). Inspired by Skeleton-of-Thought (ICLR 2024) and Astro's Islands Architecture.

```bash
/plugin install interleave
```

### intersearch

Shared embedding and search infrastructure. Sentence-transformer embeddings and Exa web search, used by interject and interflux as a common dependency. Not something you'd install directly unless you're building on top of the search layer.

```bash
/plugin install intersearch
```

### tldr-swinton

Token-efficient code reconnaissance for LLMs. Autonomous skills save 48-85% tokens via diff-context, semantic search, structural patterns, and symbol analysis. Includes an MCP server for direct tool integration. The name is a Tilda Swinton pun, which is exactly the level of whimsy you'd expect.

```bash
/plugin install tldr-swinton
```

### tuivision

TUI automation and visual testing — Playwright for terminal applications. Spawn TUI apps in virtual terminals, send keystrokes, capture screenshots as PNG/SVG, and manage multiple concurrent sessions. MCP server with xterm.js headless rendering. Requires Node.js 20+ and Cairo/Pango.

```bash
/plugin install tuivision
```

### tool-time

Tool usage analytics for Claude Code and Codex CLI. Tracks tool patterns via hooks, detects inefficiencies, and offers opt-in community comparison with anonymized data. Useful for figuring out where your workflow is actually spending tokens.

```bash
/plugin install tool-time
```

---

## Adding Plugins

To add a plugin to this marketplace:

1. Fork this repository
2. Add an entry to `.claude-plugin/marketplace.json`
3. Submit a pull request

See the [marketplace.json schema](.claude-plugin/marketplace.json) for the required fields.
