---
name: eigenhelm
description: Evaluate code quality using eigenhelm aesthetic scoring. Run after writing or modifying code files to get actionable improvement directives with automatic iteration limits.
---

# eigenhelm — Agent Skill

Evaluate code quality using eigenhelm aesthetic scoring. Run after writing or modifying code files to get actionable improvement directives.

## When to use

- After writing or substantially modifying a source file
- After all tests pass — eigenhelm is a post-test tool, not a substitute for tests
- During code review to identify structural issues

## When NOT to use

- As a loop target — do NOT rewrite working code to chase a score
- Before tests pass — fix correctness first, aesthetics second
- On generated code, config files, or test fixtures

## How to evaluate

```bash
eh evaluate <file-or-directory> --classify
```

## How to interpret results

- **accept** (score < 0.4): Code is structurally sound. Move on.
- **marginal** (score 0.4-0.6): Code is fine. Read directives if curious, but do not iterate to improve the score. Marginal is an acceptable end state.
- **reject** (score > 0.6): Worth reviewing. Read the directives — they identify specific structural issues. Apply fixes that make sense, skip ones that don't.

## Rules for agents

1. **One pass, not a loop.** Evaluate once after writing a file. If reject, read the directives, apply what's obviously correct, re-evaluate once. If still reject or marginal, stop. Two passes maximum.

2. **Never sacrifice correctness for score.** If a directive suggests refactoring that would change behavior, skip it. A working reject is better than a broken marginal.

3. **Directives are suggestions, not commands.** `extract_repeated_logic` means "this region has structural repetition" — it doesn't mean you must extract. Sometimes repetition is the right choice (data tables, exhaustive matching, protocol conformance).

4. **Tests gate, eigenhelm advises.** Run tests before and after any eigenhelm-motivated change. If a change breaks tests, revert it immediately regardless of what it does to the score.

5. **Skip barrel and type-definition files.** Files that are primarily imports/exports or type definitions (dataclasses, interfaces, structs) are automatically skipped by eigenhelm. Don't manually evaluate them.

## Directive reference

| Category | Meaning | Action |
|----------|---------|--------|
| `extract_repeated_logic` | Structural repetition detected in AST | Look for shared abstractions, but only if the repetition is logic, not data |
| `reduce_complexity` | High cyclomatic/Halstead metrics | Break up complex functions |
| `review_structure` | Code structure diverges from corpus norms | Informational — review but don't necessarily change |
| `review_token_distribution` | Unusual token entropy | Usually noise — ignore unless extreme |
| `improve_compression` | Low information density | May indicate boilerplate — review for opportunities to simplify |

## Example workflow

```
1. Write code
2. Run tests → all pass
3. Run: eh evaluate src/mymodule.py --classify
4. Read output:
   - accept/marginal → done, move on
   - reject → read directives, apply obvious fixes
5. If you changed anything: run tests again
6. Done. Do not re-evaluate.
```
