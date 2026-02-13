# notion-light

A lightweight version of the [official Notion MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/notion) that compresses tool descriptions to single lines, saving ~1,500 tokens per session.

Best practices are separated into an [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) that loads automatically only when you actually use a tool.

[日本語版 README](./README-ja.md) | [Blog post](https://nyosegawa.github.io/posts/mcp-light/)

## Problem

MCP tool descriptions contain two types of information mixed together:

- **Decision info** — "Create Notion pages" (needed to choose the tool, 1 line)
- **Execution best practices** — "use data_source_id", "fetch first", "date format is..." (needed only when using the tool, hundreds of tokens)

The official Notion MCP server's 13 tools consume ~3,400 tokens just for tool definitions. notion-light reduces this to ~1,900 tokens (44% reduction) while preserving all best practices via an Agent Skill.

## Structure

```
notion-light/
├── mcp/
│   ├── server.py              # Light MCP server (FastMCP proxy)
│   └── pyproject.toml
├── skill/
│   └── notion-best-practices/
│       └── SKILL.md           # Best practices (auto-loaded on tool use)
└── test/
    ├── server_original.py     # Original descriptions (for comparison)
    ├── server_light.py        # Light descriptions (for comparison)
    ├── measure_tokens.py      # tiktoken measurement
    └── measure_json_size.py   # JSON payload measurement
```

## Setup

### 1. Install the Light MCP server

```bash
# Claude Code
claude mcp add notion-light -- fastmcp run /path/to/notion-light/mcp/server.py:server --transport stdio

# Or set NOTION_TOKEN and run directly
export NOTION_TOKEN=ntn_xxxxx
fastmcp run mcp/server.py:server --transport stdio
```

### 2. Install the best practices Skill

Copy the skill directory to your Claude Code skills location:

```bash
cp -r skill/notion-best-practices ~/.claude/skills/
```

The skill auto-activates when you use any Notion tool — no extra configuration needed.

### 3. Remove the original Notion MCP server

```bash
claude mcp remove notion  # or whatever name you used
```

## Verification Results

Measured with tiktoken (cl100k_base) on all 13 Notion MCP tools:

| Metric | Original | Light | Reduction |
| --- | --- | --- | --- |
| Description tokens | 1,725 | 285 | 83.5% |
| Total tool definition | 3,410 | 1,908 | 44.0% |
| JSON bytes | 18,367 | 11,565 | 37.0% |

Real-world measurement with [opencode](https://github.com/nicholasgriffintn/opencode) (no Tool Search): 16,796 → 15,410 tokens (-1,386 tokens).

## How it works

The Light server uses [FastMCP](https://github.com/jlowin/fastmcp)'s proxy pattern to wrap the original Notion MCP server, replacing only the `description` field of each tool:

```python
proxy_client = ProxyClient("npx @notionhq/notion-mcp-server")
server = FastMCP.as_proxy(proxy_client, name="notion-light")

for tool in server.list_tools():
    if tool.name in LIGHT_DESCRIPTIONS:
        tool.description = LIGHT_DESCRIPTIONS[tool.name]
```

Tool names, inputSchema, and execution logic are unchanged. It's a drop-in replacement.

## Create Light versions of other MCP servers

Use the [mcp-light-generator](https://github.com/nyosegawa/skills/blob/main/skills/mcp-light-generator/SKILL.md) skill to generate Light versions of any MCP server:

```
"Create a Light version of the GitHub MCP server"
```

Claude will analyze all tool descriptions, compress them to single lines, and generate both the Light MCP server and a best practices Skill.

## License

MIT
