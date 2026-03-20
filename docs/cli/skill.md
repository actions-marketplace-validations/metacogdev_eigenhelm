# eh skill

Install or print the eigenhelm agent skill file.

## Usage

```bash
eh skill                          # print to stdout
eh skill path/to/skill.md         # write to a specific file
eh skill --install                # write to .claude/skills/eigenhelm.md
eh skill --install --force        # overwrite existing
eh skill --install /path/to/dir   # write to <dir>/.claude/skills/eigenhelm.md
```

## What it does

Outputs the eigenhelm agent skill file — a structured workflow contract that teaches AI coding agents how to use eigenhelm correctly.

The skill file is bundled inside the eigenhelm package and versioned with each release.

## Options

| Flag | Description |
|------|-------------|
| `--install` | Write to `.claude/skills/eigenhelm.md` in the target directory (default: current directory) |
| `--force` | Overwrite existing skill file |

## Examples

### Install for Claude Code

```bash
eh skill --install
```

Creates `.claude/skills/eigenhelm.md` in the current directory.

### Print and pipe

```bash
eh skill | cat
eh skill > .cursor/skills/eigenhelm.md
```

### Install in a specific project

```bash
eh skill --install /path/to/my-project
```

## See also

- [Agent Skills integration guide](../integrations/agent-skills.md)
