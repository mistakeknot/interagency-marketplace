---
name: interpeer
description: Get expert feedback from OpenAI Codex CLI on designs, implementations, or approaches, then review and discuss that feedback with the user. Use when you want a second opinion on architecture, code quality, or technical decisions.
---

# Interpeer: Cross-AI Peer Review

## Purpose

Get expert technical feedback from OpenAI Codex CLI and collaboratively review it with the user. This provides a "second pair of eyes" on:
- Technical design documents
- Implementation approaches
- Code architecture
- System designs
- Code quality and best practices

## When to Use This Skill

**Use this skill when:**
- You've completed a design document and want expert validation
- You're unsure about a technical approach and want a second opinion
- You want to validate architectural decisions before implementation
- The user asks for external review of work
- You want to catch potential issues early

**Examples:**
- "Can you get Codex feedback on this design doc?"
- "Let's validate this approach with Codex"
- "I want a second opinion on this architecture"
- After completing a design: proactively offer "Would you like me to get Codex feedback on this design?"

## Workflow

### Phase 1: Prepare for Review

**1. Identify the Review Target**

Determine what needs review:
- Specific file path (e.g., `docs/technical/agent-daily-life-system.md`)
- Code implementation (e.g., `packages/core/src/domains/agent/DailyLife.ts`)
- Design approach (abstract concept, not a file)

**2. Ask User for Review Scope**

```
I can get Codex feedback on this [design/code/approach]. What specific aspects should I ask about?

Options:
- Overall architecture and design quality
- Performance implications and bottlenecks
- Missing edge cases or potential issues
- Best practices and code quality
- Alternative approaches or improvements
- All of the above (comprehensive review)
```

### Phase 2: Call Codex CLI

**For File Review:**

```bash
# Full file review - pipe file content to codex exec
cat <file-path> | codex exec --sandbox read-only "Please review this file. Provide feedback organized by: Strengths, Critical Concerns, Important Concerns, and Recommendations."

# Focused aspect review - specify focus areas in the prompt
cat <file-path> | codex exec --sandbox read-only "Please review this file focusing on:
1. Performance implications
2. Missing edge cases
3. Architectural patterns

Provide feedback organized by: Strengths, Critical Concerns, Important Concerns, and Recommendations."

# Save output to file (optional)
cat <file-path> | codex exec --sandbox read-only --output-last-message output.md "Review prompt here"
```

**For Approach/Concept Review:**

```bash
# Create temp file with approach description
cat > /tmp/codex-review-input.md << 'EOF'
# Technical Approach

[Describe the approach, architecture, or design decision]

## Context
[Background and constraints]

## Proposed Solution
[Your approach]

## Alternatives Considered
[Other options you evaluated]

## Questions
[Specific questions for review]
EOF

cat /tmp/codex-review-input.md | codex exec --sandbox read-only "Please review this technical approach. Focus on trade-offs, risks, and alternative considerations."
```

**For Code Review:**

```bash
# Review specific code file
cat <code-file-path> | codex exec --sandbox read-only "Please review this code for: correctness, performance, maintainability, and best practices."

# Compare implementations - create comparison file first
cat > /tmp/comparison.md << 'EOF'
# Approach Comparison

## Approach 1
[paste file1 content or describe]

## Approach 2
[paste file2 content or describe]

## Question
Which approach is better and why?
EOF

cat /tmp/comparison.md | codex exec --sandbox read-only "Please compare these approaches and recommend the best option with reasoning."
```

### Phase 3: Present Feedback to User

**Structure the presentation:**

1. **Executive Summary**
   ```
   Codex provided feedback on [file/approach]. Here are the key findings:

   ✅ Strengths:
   - [List positive aspects]

   ⚠️ Concerns:
   - [List issues or risks]

   💡 Suggestions:
   - [List recommendations]
   ```

2. **Detailed Feedback**
   Present Codex's full response organized by category

3. **Critical Issues First**
   Highlight any blocking issues or major concerns at the top

### Phase 4: Collaborative Review

**Discuss each point with the user:**

For each piece of feedback:

1. **Present the feedback point**
   ```
   Codex raised this concern: "[feedback quote]"
   ```

2. **Provide your analysis**
   ```
   I think this is [valid/questionable/contextual] because [reasoning]
   ```

3. **Ask user for input**
   ```
   What do you think about this feedback? Should we:
   - Address it now
   - Note it for later
   - Disagree and explain why
   ```

4. **Discuss implications**
   - How would addressing this change the design?
   - What's the trade-off?
   - Is it worth the complexity?

### Phase 5: Action Planning

**After reviewing all feedback:**

```
Based on Codex's feedback and our discussion, here's what I recommend:

Immediate Changes:
1. [Critical fix 1]
2. [Critical fix 2]

Future Enhancements:
1. [Nice to have 1]
2. [Nice to have 2]

Disagreements (with reasoning):
1. [Feedback we decided not to follow and why]

Would you like me to:
- Update the design document with these changes?
- Create a task list for addressing the feedback?
- Implement the critical changes now?
```

## Codex CLI Commands Reference

**Basic Review:**
```bash
# Review entire file - output to stdout
cat <file> | codex exec --sandbox read-only "Review this file"

# Save feedback to file
cat <file> | codex exec --sandbox read-only --output-last-message feedback.md "Review this file"

# Use different model
cat <file> | codex exec --sandbox read-only --model gpt-4 "Review this file"

# Get JSON output for programmatic processing
cat <file> | codex exec --sandbox read-only --json "Review this file"
```

**Focused Review:**
```bash
# Specify focus areas in the prompt
cat <file> | codex exec --sandbox read-only "Review this file focusing on:
- Performance and scalability
- Security vulnerabilities
- Best practices and code quality"

# Multiple aspects with detailed prompt
cat <file> | codex exec --sandbox read-only "Please review focusing on:
1. Architecture & design quality
2. Performance implications
3. Missing edge cases
4. Best practices

Provide feedback organized by: Strengths, Critical Concerns, Important Concerns, Recommendations."
```

**Context-Aware Review:**
```bash
# Include project context in the prompt
cat <file> | codex exec --sandbox read-only "Review this file.

Context: TypeScript + React project with focus on performance.

Provide feedback on architecture, performance, and React best practices."

# Performance-critical code review
cat <file> | codex exec --sandbox read-only "Review this WASM/TypeScript integration.

Context: Game simulation with 4,500 entities, 20ms performance budget.

Focus on: serialization overhead, threading, memory management."
```

**Available Sandbox Modes:**
- `read-only` - Safe for reviews (recommended)
- `workspace-write` - Allow file modifications (use with caution)
- `danger-full-access` - Full system access (not recommended for reviews)

## Critical Review Principles

### 1. Codex as Expert Consultant, Not Authority

**Remember:**
- Codex provides valuable input but doesn't know your full context
- You and the user make the final decisions
- Some feedback may not apply to your specific use case

**Pattern:**
```
Codex suggests: [feedback]

My analysis: [your interpretation with context]

Recommendation: [what you think should be done and why]

What do you think?
```

### 2. Balance Feedback with Project Constraints

**Consider:**
- Performance requirements (20ms budget)
- Existing architecture decisions (WASM/TypeScript split)
- Project scope (YAGNI vs future-proofing)
- Team expertise and maintainability

**Pattern:**
```
Codex recommends [X], which would improve [Y].

However, given our constraints:
- [Constraint 1]
- [Constraint 2]

I suggest [modified approach] instead because [reasoning].
```

### 3. Separate Categories of Feedback

**Critical (Must Address):**
- Correctness issues (bugs, logic errors)
- Security vulnerabilities
- Performance blockers
- Data loss risks

**Important (Should Address):**
- Architectural improvements
- Maintainability concerns
- Missing error handling
- Scalability issues

**Nice-to-Have (Consider):**
- Code style suggestions
- Alternative approaches
- Future optimizations
- Documentation improvements

### 4. Ask Clarifying Questions

If Codex feedback is unclear:

```bash
# Follow-up review with specific question
cat > /tmp/codex-followup.md << 'EOF'
Codex previously suggested: "[feedback quote]"

Can you clarify:
- What specific problem does this address?
- How would you recommend implementing this?
- What are the trade-offs?
EOF

cat /tmp/codex-followup.md | codex exec --sandbox read-only "Please clarify this feedback and provide implementation recommendations."
```

## Example Usage Patterns

### Pattern 1: Design Document Review

```
User: "Can you get Codex feedback on the Agent Daily Life design?"

You:
1. Read the design document
2. Call: cat docs/technical/agent-daily-life-system.md | codex exec --sandbox read-only "Please review this design focusing on architecture and scalability. Provide feedback organized by: Strengths, Critical Concerns, Important Concerns, Recommendations."
3. Present feedback organized by category
4. Discuss each point with user
5. Update document based on agreed changes
```

### Pattern 2: Pre-Implementation Validation

```
After completing design:

You: "I've completed the Agent Daily Life System design. Would you like me to get Codex feedback before we move to implementation?"

User: "Yes"

You:
1. Call: cat docs/technical/agent-daily-life-system.md | codex exec --sandbox read-only "Please provide comprehensive review of this design. Focus on: architecture, performance, edge cases, best practices. Organize by: Strengths, Critical Concerns, Important Concerns, Recommendations."
2. Present feedback
3. Discuss and resolve concerns
4. Update design if needed
5. Proceed to implementation with validated design
```

### Pattern 3: Code Review

```
User: "Review this implementation with Codex"

You:
1. Call: cat packages/core/src/domains/agent/DailyLife.ts | codex exec --sandbox read-only "Review this code for: performance, best practices, correctness, and maintainability."
2. Present code quality feedback
3. Discuss suggested improvements
4. Optionally refactor based on feedback
```

### Pattern 4: Architecture Decision Validation

```
You: "I'm considering two approaches for [X]. Let me get Codex's analysis."

1. Create comparison document with both approaches
2. Call: cat /tmp/approach-comparison.md | codex exec --sandbox read-only "Compare these approaches and suggest alternatives. Focus on: trade-offs, risks, implementation complexity, maintainability."
3. Present Codex's analysis of trade-offs
4. Discuss with user
5. Make informed decision together
```

## Integration with Other Skills

**Combine with brainstorming skill:**
```
1. Use brainstorming to create design
2. Use interpeer to validate design
3. Use writing-plans to create implementation plan
```

**Combine with code-review-expert:**
```
1. Use interpeer for external perspective
2. Use code-review-expert for project-specific review
3. Synthesize both sets of feedback
```

## Output Format

**Standard Review Output:**

```markdown
# Interpeer Review: [File/Approach Name]

## Executive Summary
[High-level findings]

## Strengths ✅
- [Positive aspect 1]
- [Positive aspect 2]

## Concerns ⚠️
### Critical
- [Critical issue 1]

### Important
- [Important issue 1]

### Minor
- [Minor suggestion 1]

## Recommendations 💡
1. [Recommendation 1]
2. [Recommendation 2]

## Alternative Approaches
[If requested]

## Discussion
[Your analysis of the feedback]

## Action Items
- [ ] [Action based on feedback 1]
- [ ] [Action based on feedback 2]
```

## Error Handling

**If Codex CLI fails:**
```bash
# Check Codex CLI is available
which codex || echo "Codex CLI not installed"

# Check file exists
test -f <file> || echo "File not found"

# Check for API errors
# Codex may fail due to API limits, network issues, or unsupported file types
```

**Fallback:**
If Codex unavailable:
1. Inform user
2. Offer to review manually using your knowledge
3. Suggest alternative review methods

## Best Practices

**DO:**
- Always provide your own analysis alongside Codex feedback
- Ask user which aspects to focus on
- Organize feedback by priority/severity
- Discuss trade-offs for each suggestion
- Make final decisions collaboratively

**DON'T:**
- Blindly implement all Codex suggestions without discussion
- Present feedback without context or analysis
- Skip discussing feedback that seems wrong
- Assume Codex knows your project constraints
- Use Codex as the sole decision-maker

## Quick Reference

```bash
# Standard design review
cat docs/technical/<design>.md | codex exec --sandbox read-only "Review this design"

# Performance-focused review
cat <file> | codex exec --sandbox read-only "Review focusing on performance and scalability"

# Code quality review
cat packages/core/src/<file>.ts | codex exec --sandbox read-only "Review for best practices and code quality"

# Comprehensive review with structure
cat <file> | codex exec --sandbox read-only "Review focusing on:
1. Architecture
2. Performance
3. Edge cases
4. Best practices

Organize by: Strengths, Critical Concerns, Important Concerns, Recommendations."

# With project context
cat <file> | codex exec --sandbox read-only "Review this file.

Context: TypeScript game simulation, 4500 agents, 20ms budget.

Focus on: serialization overhead, threading, memory management."

# Save output to file
cat <file> | codex exec --sandbox read-only --output-last-message feedback.md "Review this file"
```

## Remember

This skill is about **collaborative review**, not automated acceptance:
1. Get Codex's expert perspective
2. Add your contextual analysis
3. Discuss with user
4. Make informed decisions together
5. Document reasoning for accepted/rejected feedback

The goal is **better decisions through multiple perspectives**, not replacing human judgment.
