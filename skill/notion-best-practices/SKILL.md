---
name: notion-best-practices
description: Best practices for Notion MCP tools. Auto-loaded when using notion-light MCP server. Contains parameter formats, recommended workflows, and error prevention tips for all Notion MCP tools. Use when user works with Notion MCP tools, says "Notion best practices", or when notion-light MCP description references this skill.
---

# Notion Best Practices

Notion MCP ツールを正しく使うためのベストプラクティス集。

## 共通ルール

### コンテンツ形式
- ページコンテンツは **Notion-flavored Markdown** 形式
- 完全な仕様は MCP リソース `notion://docs/enhanced-markdown-spec` を fetch して確認する
- Markdown 構文を推測しない。必ず仕様を参照する

### プロパティの特殊形式
以下のプロパティ型は展開形式が必要:

| プロパティ型 | 形式 | 例 |
|---|---|---|
| Date | `date:{property}:start`, `date:{property}:end`(任意), `date:{property}:is_datetime`(0 or 1) | `"date:Due Date:start": "2024-12-25"` |
| Place | `place:{property}:name`, `place:{property}:address`, `place:{property}:latitude`, `place:{property}:longitude`, `place:{property}:google_place_id`(任意) | `"place:office:name": "HQ"` |
| Number | JavaScript の数値型を使う（文字列不可） | `"priority": 5` |
| Checkbox | `__YES__` / `__NO__` を使う | `"Is Complete": "__YES__"` |

### 特殊プロパティ名
- "id" や "url" という名前のプロパティは `userDefined:` プレフィックスが必要
- 例: `"userDefined:URL"`, `"userDefined:id"`

### データソースとデータベースの区別
- データベースは複数のデータソース（コレクション）を持てる
- `<data-source url="collection://...">` タグからデータソース ID を取得する
- 複数データソースがある場合、`database_id` は使えない — `data_source_id` を使う

---

## notion-search

ワークスペースとconnected sources（Slack, Google Drive, GitHub, Jira, Microsoft Teams, SharePoint, OneDrive, Linear）を横断検索する。

### 検索タイプ
- `"internal"`: ワークスペース + connected sources のセマンティック検索
- `"user"`: ユーザー名・メールでの検索

### ベストプラクティス
- 1回の呼び出しにつき1つの質問にする。複数検索は別々の呼び出しで
- 検索結果から完全なページ内容が必要なら `fetch` ツールを使う
- データベース内検索: 先に `fetch` でデータベースを取得し、`<data-source url="...">` から data_source_url を得て検索
- 複数データソースのデータベースは、view ID (`?v=...`) で照合するか、各ソースを個別検索
- database URL/ID に `collection://` プレフィックスを付けない
- database URL を page_url パラメータに使わない
- `content_search_mode` で AI search / workspace search を切り替え可能
- フィルタ: `created_date_range`（作成日範囲）、`created_by_user_ids`（作成者）が使用可能

---

## notion-fetch

URL または ID でページ・データベースの詳細を取得する。

### ベストプラクティス
- notion.so URL、Notion Sites URL (`*.notion.site`)、生 UUID のいずれも受け付ける
- ページはenhanced Markdown形式で返る
- データベースは全データソース（コレクション）を返す。各データソースの ID は `<data-source url="collection://...">` タグに含まれる
- create-pages や update-page の前に必ず fetch して、スキーマやプロパティ名を確認する

---

## notion-create-pages

1回の呼び出しで1つ以上のページを作成する。

### Parent の選び方
1. **page_id**: 通常のページの下に作成
2. **data_source_id**: データソース（コレクション）の下に作成（推奨）
3. **database_id**: 単一データソースのデータベースでのみ使用可
4. **省略**: ワークスペースレベルのプライベートページとして作成

### ベストプラクティス
- database URL がある場合、**必ず先に `fetch`** してスキーマとデータソース URL を取得する
- 複数データソースのデータベースでは `database_id` は使えない — `data_source_id` を使う
- ページの下に作る場合、database ID/URL を `page_id` パラメータに入れない
- コンテンツにページタイトルを含めない（properties の title で指定する）
- データベース内ページ: スキーマに合ったプロパティ名を使い、title プロパティを必ず含める（"title" 以外の名前の場合もある）
- データベース外ページ: 使えるプロパティは `title` のみ

---

## notion-update-page

ページのプロパティまたはコンテンツを更新する。

### コマンド
| コマンド | 用途 |
|---|---|
| `update_properties` | プロパティ値の更新 |
| `replace_content` | コンテンツ全体の置換 |
| `replace_content_range` | 特定範囲のコンテンツ置換 |
| `insert_content_after` | 特定位置の後にコンテンツ挿入 |

### ベストプラクティス
- **更新前に必ず `fetch`** でページの現在内容を取得する
- `selection_with_ellipsis`: 先頭約10文字 + `...` + 末尾約10文字で一意に特定する
- 一意に特定できない場合はスニペットを長くする
- `replace_content` / `replace_content_range` は子ページ・データベースの削除チェックを行う
- 子ページを保持するには `<page url="...">` / `<database url="...">` タグで含める
- **CRITICAL**: `allow_deleting_content` が必要なエラーが出ても、自動で削除しない。必ずユーザーに削除対象を提示して確認を取る
- プロパティの値を消すには `null` を設定

---

## notion-create-database

新しいデータベースを作成する。

### ベストプラクティス
- title プロパティを指定しない場合、"Name" が自動追加される
- 利用可能なプロパティ型: title, rich_text, number, select, multi_select, date, people, checkbox, url, email, phone_number, formula, relation, rollup, unique_id, status, place
- 返り値にスキーマ、SQLite定義、`<data-source>` タグ内のデータソース ID が含まれる
- parent を省略するとワークスペースレベルのプライベートページとして作成

---

## notion-update-data-source

データソースのプロパティ、スキーマ、名前を更新する。

### ベストプラクティス
- データソース ID（`<data-source>` タグから取得）または単一データソースのデータベース ID を受け付ける
- 複数データソースのデータベースでは個別のデータソース ID が必要
- プロパティを削除: `null` を設定
- プロパティ名を変更: `{"name": "New Name"}` のみ指定
- title プロパティの削除・作成はできない
- unique_id プロパティは最大1つ
- synced databases は更新できない
- **先に `fetch`** で現在のスキーマを確認する
- `in_trash: true` でデータソースをゴミ箱に移動（Notion UI でしか元に戻せない。ユーザー確認必須）

---

## notion-query-database-view

データベースビューのフィルタ・ソート・カラム選択を使ってデータを取得する。

### ベストプラクティス
- 先に `fetch` でデータベースとビュー URL を取得する
- ビュー URL の形式: `https://www.notion.so/workspace/db-id?v=view-id`
- ビューに設定済みのフィルタ・ソートがそのまま適用される

---

## notion-move-pages

ページまたはデータベースを新しい親に移動する。

### ベストプラクティス
- 1回の呼び出しで最大100件の移動が可能
- 移動先: page_id, database_id, data_source_id, workspace
- workspace への移動はプライベートページとして追加される（稀に使用）
- データベース配下のデータソースは個別移動できない

---

## notion-duplicate-page

ページを複製する。

### ベストプラクティス
- 複製は非同期で完了する
- 返される ID/URL のページはすぐには内容が反映されない
- ユーザーに「複製は進行中で、後から確認できる」と伝える
- `fetch` ツールまたは Notion アプリの URL で確認を促す

---

## notion-create-comment

ページにコメントを追加する。

### ベストプラクティス
- parent に `page_id` を指定する
- コメント内容は rich_text 配列で指定する
- 対応する rich_text タイプ: text, mention (user, date, page, database, template_mention, custom_emoji), equation

---

## notion-get-comments

ページの全コメントを取得する。

### ベストプラクティス
- `page_id` でページを指定する

---

## notion-get-teams

ワークスペースのチーム（teamspaces）一覧を取得する。

### ベストプラクティス
- `query` パラメータでチーム名フィルタ（大小文字無視）
- メンバーシップ状態別に返される
- 各タイプ最大10件

---

## notion-get-users

ワークスペースのユーザー一覧を取得する。

### ベストプラクティス
- `query` でユーザー名・メールフィルタ（大小文字無視）
- `user_id: "self"` で現在のユーザーを取得
- カーソルベースのページネーション対応（`start_cursor`, `page_size`）
- 1ページ最大100件
