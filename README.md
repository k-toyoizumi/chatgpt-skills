# ChatGPT Skills

Personal skills used by ChatGPT for repeatable workflows, project operations, research, development, and agentic tasks.

## Repository structure

```text
chatgpt-skills/
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

Each skill follows a standard `SKILL.md` format with YAML front matter:

```yaml
---
name: skill-name
description: When and why to use this skill.
metadata:
  short-description: Short human-readable summary
---
```

The body of each `SKILL.md` contains reusable operating instructions, workflows, and guardrails.

## Skills

### chatgpt-development-operations

Shared operating policy for long-running ChatGPT work such as:

- web development
- information retrieval and reporting
- automation
- research support
- agent development
- context / state design
- model and reasoning-effort routing
- incremental processing and validation
- cost-efficient workflows

Source: `skills/chatgpt-development-operations/SKILL.md`

## Conventions

- Keep reusable procedure in Skills.
- Keep project-specific current state in each project's own repository or state document.
- Keep long-lived user preferences and routing hints in ChatGPT Memory.
- Prefer small, focused Skills over one monolithic Skill as the library grows.
- Add references, examples, or scripts inside a skill directory only when they are required by that Skill.
