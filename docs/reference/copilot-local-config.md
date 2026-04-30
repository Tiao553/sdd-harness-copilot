# Copilot Local Configuration

This repository includes a local VS Code/GitHub Copilot MCP setup ported from the Antigravity `.gemini` configuration in `Tiao553/sdd-for-antigravity`.

## Files

| File | Purpose |
|---|---|
| `.vscode/mcp.json` | Workspace MCP servers for Copilot Chat and agent mode in VS Code |
| `.github/config/security-settings.json` | Exact copy of the Antigravity `.gemini/settings.json` permission policy |
| `.github/copilot-instructions.md` | AgentSpec grounding, routing, and local execution policy |
| `.env.example` | Optional environment variables for local MCP servers |

## MCP Servers

| Server | Package | Purpose |
|---|---|---|
| `context7` | `@upstash/context7-mcp@latest` | Current documentation lookup |
| `sequential-thinking` | `@modelcontextprotocol/server-sequential-thinking` | Structured reasoning support |
| `github` | `@modelcontextprotocol/server-github` | GitHub repository, issue, PR, and code search tools |

## Local Setup

1. Copy `.env.example` to `.env`.
2. Set `GITHUB_PERSONAL_ACCESS_TOKEN` if you want the GitHub MCP server.
3. In VS Code, run `MCP: Open Workspace Folder MCP Configuration` to inspect `.vscode/mcp.json`.
4. Run `MCP: List Servers` and start the servers you want.

The `github` server reads `GITHUB_PERSONAL_ACCESS_TOKEN` from `.env` through the workspace MCP configuration.

## Safety Policy

The Antigravity permission policy is copied to `.github/config/security-settings.json` and enforced by `.github/config/grounding.md`.

VS Code/Copilot does not natively consume Antigravity's `autoExecution`, `reviewPolicy`, `planningPolicy`, or `permissions` keys from `.vscode/settings.json`, so AgentSpec forces the policy through grounding:

- `alwaysAllow`: safe inspection and local validation.
- `alwaysAsk`: state-changing operations that require explicit approval.
- `alwaysDeny`: destructive or high-risk operations that must be refused unless the user explicitly scopes and confirms them.
