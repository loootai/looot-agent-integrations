# looot agent integrations

Config snippets and a starter skill to add [looot](https://looot.ai) to open-source agent platforms. looot is one key and one prepaid balance for 4,200+ data API endpoints. The MCP server is `https://api.looot.ai/mcp` (streamable HTTP). It signs you in through the browser. For CI or a headless box, create an agent token at https://looot.ai (Settings, Agent tokens) and export it as `LOOOT_TOKEN`.

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

## Kimi Code

`~/.kimi-code/mcp.json`, or `.kimi-code/mcp.json` in a trusted project (`configs/kimi-code.mcp.json`). A `url` alone means HTTP. Sign in with `/mcp-config login looot`. With a token, add `"bearerTokenEnvVar": "LOOOT_TOKEN"` to the `looot` entry.

## Mistral Vibe

```
vibe mcp add looot --url https://api.looot.ai/mcp
```

That picks OAuth and opens the sign-in. Later sign-ins: `/mcp login looot`. The TOML form is `configs/vibe.config.toml` (`~/.vibe/config.toml`). With a token, set `[mcp_servers.auth]` to `type = "static"` and `api_key_env = "LOOOT_TOKEN"`.

## Qwen Code

```
qwen mcp add -s user --transport http looot https://api.looot.ai/mcp
```

Or merge `configs/qwen.settings.json` into `~/.qwen/settings.json`. Qwen reads `httpUrl` as Streamable HTTP and `url` as SSE, so keep `httpUrl`. Sign in from `/mcp`: pick looot, then Auth. With a token, add `"headers": { "Authorization": "Bearer ${LOOOT_TOKEN}" }`.

## Kiro

`~/.kiro/settings/mcp.json` or `.kiro/settings/mcp.json` (`configs/kiro.mcp.json`). Kiro starts the OAuth sign-in when it connects. `kiro-cli mcp add` only takes stdio servers, so edit the file or run `kiro-cli mcp import --file configs/kiro.mcp.json workspace`. A `${LOOOT_TOKEN}` header works only after you approve that variable in the "Mcp Approved Env Vars" setting.

## Antigravity

`~/.gemini/config/mcp_config.json`, or `.agents/mcp_config.json` in a workspace (`configs/antigravity.mcp_config.json`). Antigravity uses `serverUrl`. Authenticate under Customizations, Installed, MCP Servers.

## Auggie (Augment)

```
auggie mcp add looot --transport http --url https://api.looot.ai/mcp
```

Or merge `configs/auggie.settings.json` into `~/.augment/settings.json`. With a token: `-H "Authorization:Bearer ${LOOOT_TOKEN}"`.

## Command Code

```
cmd mcp add --transport http -s user looot https://api.looot.ai/mcp
cmd mcp auth looot
```

The JSON form is `configs/commandcode.mcp.json` (`.mcp.json` in a project or `~/.commandcode/mcp.json`). Command Code calls the field `transport`.

## Rovo Dev

`acli rovodev mcp` opens `~/.rovodev/mcp.json`. Merge `configs/rovodev.mcp.json` and put an agent token in the header. Rovo Dev's docs do not describe an OAuth sign-in for remote servers, so the snippet uses a token.

## MiMo Code

`~/.config/mimocode/mimocode.jsonc` or `.mimocode/mimocode.jsonc` (`configs/mimocode.jsonc`), then `mimo mcp auth looot`. MiMo Code is an OpenCode fork: the key is `mcp`, the type is `remote`, and a token header reads `"Bearer {env:LOOOT_TOKEN}"`.

## Pi

Pi has MCP built in since 0.99.0.

```
pi mcp add looot --url https://api.looot.ai/mcp
pi mcp login looot
```

Or merge `configs/pi.mcp.json` into `~/.pi/agent/mcp.json` (`.pi/mcp.json` per project). With a token: `--bearer-token-env-var LOOOT_TOKEN`.

## Jcode

`~/.jcode/mcp.json` or `.jcode/mcp.json` (`configs/jcode.mcp.json`), then `jcode mcp login looot`. Jcode also reads `.mcp.json` and `.claude/mcp.json`, so a Claude Code entry for looot already works there.

## Prime Agent

```
prime-agent mcp add looot --url https://api.looot.ai/mcp --oauth
```

Then `/mcp login looot`. The file form is `configs/prime-agent.settings.json` (`~/.prime/agent/settings.json`, user scope only). With a token, use `--bearer-token-env-var LOOOT_TOKEN` instead of `--oauth`.

## Trae

One click:

```
trae://trae.ai-ide/mcp-import?type=http&name=looot&config=eyJ1cmwiOiJodHRwczovL2FwaS5sb29vdC5haS9tY3AifQ%3D%3D
```

`config` is `{"url":"https://api.looot.ai/mcp"}` in base64. Or paste `configs/trae.mcp.json` into Settings, MCP, Raw Config, or `.trae/mcp.json` with Project MCP turned on.

## Qoder

```
qoder mcp add looot https://api.looot.ai/mcp -t http -s user
```

Or merge `configs/qoder.settings.json` into `~/.qoder/settings.json`. In the Qoder IDE: Settings, MCP, My Servers, Add.

## CodeBuddy

```
codebuddy mcp add --scope user --transport http looot https://api.looot.ai/mcp
```

Or `configs/codebuddy.mcp.json` as `~/.codebuddy/.mcp.json` or a project `.mcp.json`. CodeBuddy also installs the looot plugin: `/plugin marketplace add loootai/looot-plugin`. With a token: `--header "Authorization: Bearer ${LOOOT_TOKEN}"`.

## Droid (Factory)

```
droid mcp add looot https://api.looot.ai/mcp --type http
```

Then `/mcp`, pick looot, Authenticate. The file form is `configs/droid.mcp.json` (`~/.factory/mcp.json` or `.factory/mcp.json`).

## Claude Code, Cursor, VS Code, Windsurf

See https://github.com/loootai/looot-mcp and https://github.com/loootai/looot-plugin. Cursor users can also find looot at https://cursor.directory/plugins/looot.

## Not covered

Aider has no native MCP support. Frameworks that need code (LangChain, LlamaIndex, CrewAI, Agno, Vercel AI SDK, Mastra) take looot through their MCP clients or the SDKs: https://github.com/loootai/looot-js and https://github.com/loootai/looot-python.

MIT licensed.
