# AI Agent Skills

eigenhelm publishes agent skills for coding assistants. When an agent loads the skill, it gains a structured protocol for evaluating and improving code quality.

## Install the skill

=== "npx skills"

    ```bash
    npx skills add metacogdev/skills --skill eigenhelm
    ```

=== "Manual (opencode)"

    Copy the skill to your project:

    ```bash
    mkdir -p .opencode/skills/eigenhelm
    # Copy SKILL.md from https://github.com/metacogdev/skills/tree/main/eigenhelm
    ```

=== "Manual (Claude Code)"

    ```bash
    mkdir -p .claude/skills/eigenhelm
    # Copy SKILL.md
    ```

## What the skill provides

The skill teaches agents to:

1. Run `eh evaluate --classify --format human <file>` after writing code
2. Interpret scores, decisions, and directives
3. Follow an **iteration protocol** with strict limits to prevent infinite refinement loops

## Iteration protocol

The skill enforces these rules:

| Decision | Action | Max attempts |
|----------|--------|-------------|
| **reject** | Address `[high]` directives, re-evaluate | 3 |
| **marginal** | Address `[high]` directives if straightforward | 2 |
| **accept** | Stop | — |

**Stop rule**: If the score doesn't improve by ≥ 0.03 between attempts, stop immediately.

**Small file caveat**: Files under ~80 lines will show `[medium] improve_compression` and `[medium] review_structure` — these are expected and should be ignored. Only PCA-derived directives (`reduce_complexity`, `extract_repeated_logic`) are actionable on small files.

## Example agent prompt

You can also add eigenhelm to any agent by including this in your system prompt or project instructions:

```
After writing or modifying code, evaluate it with:
  eh evaluate --classify --format human <file>

If the decision is "reject", address [high] severity directives and re-evaluate (max 3 attempts).
If "marginal", address [high] directives if straightforward (max 2 attempts).
If "accept", move on.

Stop iterating if the score doesn't improve by 0.03 between attempts.
```
