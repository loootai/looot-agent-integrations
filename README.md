# looot agent integrations

Config snippets and a starter skill to add [looot](https://looot.ai) to open-source agent platforms. looot is one key and one prepaid balance for 2,500+ data API endpoints. The MCP server is `https://api.looot.ai/mcp` (streamable HTTP). It signs you in through the browser. For CI or a headless box, create an agent token at https://looot.ai (Settings, Agent tokens) and export it as `LOOOT_TOKEN`.

Every snippet is in `configs/` and is checked by `python3 scripts/validate.py` (JSON, TOML, YAML parse, skill frontmatter, no secrets). Merge a snippet into your existing config. Do not overwrite your other servers.

## OpenCode

`opencode.json` (project) or the global config:

```json
{ "$schema": "https://opencode.ai/config.json",
  "mcp": { "looot": { "type": "remote", "url": "https://api.looot.ai/mcp", "enabled": true } } }
```

Then `opencode mcp auth looot`. With a token instead, see `configs/opencode.token.json`.

## Hermes Agent (Nous Research)

MCP, in `~/.hermes/config.yaml` (`configs/hermes.config.yaml`):

```yaml
mcp_servers:
  looot:
    url: "https://api.looot.ai/mcp"
    headers:
      Authorization: "Bearer ${LOOOT_TOKEN}"
```

Skills: `hermes skills tap add loootai/looot-skills`, then `hermes skills install loootai/looot-skills/skills/looot`.

## OpenClaw

MCP: `openclaw mcp set looot '{"url":"https://api.looot.ai/mcp","transport":"streamable-http"}'` (`configs/openclaw.mcp.json`).
Skill: copy `skills/looot-quickstart` into your OpenClaw skills folder. Its frontmatter carries `metadata.openclaw` (env `LOOOT_TOKEN`). Publishing it to ClawHub needs a GitHub login, see the plan file.

## Goose

One click with browser sign-in:

```
goose://extension?url=https%3A%2F%2Fapi.looot.ai%2Fmcp&type=streamable_http&id=looot&name=looot&description=2500%2B%20data%20API%20endpoints
```

Or merge `configs/goose.config.yaml` into `~/.config/goose/config.yaml`.

## Cline

Add to `cline_mcp_settings.json`, then run Authorize OAuth for `looot`:

```json
{ "mcpServers": { "looot": { "type": "streamableHttp", "url": "https://api.looot.ai/mcp", "disabled": false } } }
```

## Roo Code

`.roo/mcp.json` or global `mcp_settings.json` (`configs/roo.mcp.json`).

## Kilo Code

`kilo.jsonc` (`configs/kilo.jsonc`). The marketplace entry is in `kilo-marketplace/mcps/looot/MCP.yaml`.

## Continue

Save `configs/continue.looot.yaml` as `.continue/mcpServers/looot.yaml`.

## Zed

`settings.json`, key `context_servers` (`configs/zed.settings.json`). Omit headers to get the OAuth prompt.

## Codex CLI

```
codex mcp add looot --url https://api.looot.ai/mcp
codex mcp login looot
```

Or `configs/codex.config.toml`. With a token, `configs/codex.token.config.toml` sets `bearer_token_env_var = "LOOOT_TOKEN"`.

## Gemini CLI

`gemini mcp add --transport http looot https://api.looot.ai/mcp`. The extension manifest lives in https://github.com/loootai/looot-mcp.

## Crush

`configs/crush.json` into your Crush config.

## Amp

Amp recommends loading MCP servers from a skill, so the tools load only when a task needs them. `amp/skills/looot` holds a `SKILL.md` and an `mcp.json` that points at `https://api.looot.ai/mcp`. Copy that folder to `.agents/skills/looot` in a project or `~/.config/agents/skills/looot` for every project, or run `amp skill add https://github.com/loootai/looot-agent-integrations`. The first looot call opens the sign-in page in your browser.

Without the skill, add the server directly:

```
amp mcp add looot https://api.looot.ai/mcp
```

Or merge `configs/amp.settings.json` (`amp.mcpServers`) into your Amp settings. With a token instead of browser sign-in, add `"headers": { "Authorization": "Bearer ${LOOOT_TOKEN}" }` to the `looot` entry.

## Claude Code, Cursor, VS Code, Windsurf

See https://github.com/loootai/looot-mcp and https://github.com/loootai/looot-plugin.

## Not covered

Aider has no native MCP support. Frameworks that need code (LangChain, LlamaIndex, CrewAI, Agno, Vercel AI SDK, Mastra) take looot through their MCP clients or the SDKs: https://github.com/loootai/looot-js and https://github.com/loootai/looot-python.

MIT licensed.
