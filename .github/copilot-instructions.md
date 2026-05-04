# AgentSpec Copilot Instructions

This repository is an AgentSpec runtime for GitHub Copilot. Treat `.github/` as the operating system for the workspace: grounding, routing, skills, agents, knowledge bases, and SDD workflow artifacts all live there.

## Mandatory Grounding

**Before any operational response, read `.github/config/grounding.md`.** It is the single normative source for execution rules, including the required response block, permissions policy, response language, token budget strategy, skill priority, SDD lifecycle, and security gates.

Use `AGENTS.md` as descriptive runtime documentation for inventory, repository structure, examples, and build delegation patterns.

Do not duplicate operational rules outside `grounding.md`. If there is a conflict, follow `.github/config/grounding.md`.

## Git Commit Trailer

Always include this trailer in commit messages:

```
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```
