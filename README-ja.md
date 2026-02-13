# notion-light

[公式 Notion MCP サーバー](https://github.com/modelcontextprotocol/servers/tree/main/src/notion)の軽量版です。ツールのdescriptionを1行に圧縮し、1セッションあたり約1,500トークンを節約します。

ベストプラクティスは[Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)として分離し、ツールを実際に使う瞬間にだけ自動ロードされます。

[English README](./README.md) | [ブログ記事](https://nyosegawa.github.io/posts/mcp-light/)

## 問題

MCPのツール定義には2種類の情報が混在しています。

- 判断用情報 — 「Notionにページを作成する」（ツール選択に必要、1行で済む）
- 実行時ベストプラクティス — 「data_source_idを使え」「先にfetchしろ」「日付形式は...」（ツール使用時まで不要、数百トークン）

公式Notion MCPサーバーの13ツールはツール定義だけで約3,400トークンを消費します。notion-lightはこれを約1,900トークンに削減（44%削減）しつつ、Agent Skill経由でベストプラクティスを保持します。

## 構成

```
notion-light/
├── mcp/
│   ├── server.py              # Light版MCPサーバー（FastMCPプロキシ）
│   └── pyproject.toml
├── skill/
│   └── notion-best-practices/
│       └── SKILL.md           # ベストプラクティス（ツール使用時に自動ロード）
└── test/
    ├── server_original.py     # 元のdescription（比較用）
    ├── server_light.py        # Light版description（比較用）
    ├── measure_tokens.py      # tiktoken計測
    └── measure_json_size.py   # JSONペイロード計測
```

## セットアップ

### 1. Light版MCPサーバーをインストール

```bash
# Claude Code
claude mcp add notion-light -- fastmcp run /path/to/notion-light/mcp/server.py:server --transport stdio

# または NOTION_TOKEN を設定して直接実行
export NOTION_TOKEN=ntn_xxxxx
fastmcp run mcp/server.py:server --transport stdio
```

### 2. ベストプラクティスSkillをインストール

```bash
cp -r skill/notion-best-practices ~/.claude/skills/
```

Notionツールを使うと自動的にSkillが発火します。追加の設定は不要です。

### 3. 元のNotion MCPサーバーを削除

```bash
claude mcp remove notion  # 登録名に合わせて変更
```

## 検証結果

tiktoken（cl100k_base）で全13ツールを計測:

| 指標 | Original | Light | 削減率 |
| --- | --- | --- | --- |
| description合計 | 1,725 tokens | 285 tokens | 83.5% |
| ツール定義全体 | 3,410 tokens | 1,908 tokens | 44.0% |
| JSON bytes | 18,367 bytes | 11,565 bytes | 37.0% |

[opencode](https://github.com/nicholasgriffintn/opencode)（Tool Searchなし）での実測: 16,796 → 15,410 tokens（-1,386 tokens）

## 仕組み

[FastMCP](https://github.com/jlowin/fastmcp)のプロキシパターンで元サーバーを丸ごとラップし、`description` フィールドだけを差し替えます。

```python
proxy_client = ProxyClient("npx @notionhq/notion-mcp-server")
server = FastMCP.as_proxy(proxy_client, name="notion-light")

for tool in server.list_tools():
    if tool.name in LIGHT_DESCRIPTIONS:
        tool.description = LIGHT_DESCRIPTIONS[tool.name]
```

ツール名、inputSchema、実行ロジックは元サーバーそのまま。差し替えるだけで動きます。

## 他のMCPサーバーのLight版を作る

[mcp-light-generator](https://github.com/nyosegawa/skills/blob/main/skills/mcp-light-generator/SKILL.md) スキルを使えば、任意のMCPサーバーのLight版を生成できます。

```
「GitHub MCPのLight版を作って」
```

Claudeが全ツールのdescriptionを分析し、Light版MCPサーバーとベストプラクティスSkillの両方を生成します。

## ライセンス

MIT
