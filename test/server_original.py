"""Original (fat) Notion MCP descriptions - for comparison testing"""

from fastmcp import FastMCP

server = FastMCP("notion-original")


# --- notion-search ---
@server.tool(
    description='''Perform a search over:
- "internal": Semantic search over Notion workspace and connected sources (Slack, Google Drive, Github, Jira, Microsoft Teams, Sharepoint, OneDrive, Linear). Supports filtering by creation date and creator.
- "user": Search for users by name or email.

Auto-selects AI search (with connected sources) or workspace search (workspace-only, faster) based on user's access to Notion AI. Use content_search_mode to override.
Use "fetch" tool for full page/database contents after getting search results.
To search within a database: First fetch the database to get the data source URL (collection://...) from <data-source url="..."> tags, then use that as data_source_url. For multi-source databases, match by view ID (?v=...) in URL or search all sources separately.
Don't combine database URL/ID with collection:// prefix for data_source_url. Don't use database URL as page_url.'''
)
def notion_search(
    query: str,
    query_type: str = "internal",
    data_source_url: str = "",
    page_url: str = "",
    teamspace_id: str = "",
    content_search_mode: str = "",
) -> str:
    return "mock"


# --- notion-fetch ---
@server.tool(
    description='''Retrieves details about a Notion entity (page or database) by URL or ID.
Provide URL or ID in id parameter. Make multiple calls to fetch multiple entities.
Pages use enhanced Markdown format. For the complete specification, fetch the MCP resource at notion://docs/enhanced-markdown-spec.
Databases return all data sources (collections). Each data source has a unique ID shown in <data-source url="collection://..."> tags. Use this data source ID with update_data_source and query_data_sources tools. Multi-source databases (e.g., with linked sources) will show multiple data sources.'''
)
def notion_fetch(id: str, include_transcript: bool = False) -> str:
    return "mock"


# --- notion-create-pages ---
@server.tool(
    description='''Creates one or more Notion pages, with the specified properties and content.
All pages created with a single call to this tool will have the same parent. The parent can be a Notion page ("page_id") or data source ("data_source_id"). If the parent is omitted, the pages are created as standalone, workspace-level private pages.
If you have a database URL, ALWAYS pass it to the "fetch" tool first to get the schema and URLs of each data source under the database. You can't use the "database_id" parent type if the database has more than one data source, so you'll need to identify which "data_source_id" to use.
If you know the pages should be created under a data source, do NOT use the database ID or URL under the "page_id" parameter; "page_id" is only for regular, non-database pages.
Notion page content is a string in Notion-flavored Markdown format. Don't include the page title at the top of the page's content. Only include it under "properties".
IMPORTANT: For the complete Markdown specification, always first fetch the MCP resource at notion://docs/enhanced-markdown-spec. Do NOT guess or hallucinate Markdown syntax.
When creating pages in a database: Use the correct property names from the data source schema. Always include a title property.
For pages outside of a database: The only allowed property is "title".
IMPORTANT: Some property types require expanded formats:
- Date properties: Split into "date:{property}:start", "date:{property}:end" (optional), and "date:{property}:is_datetime" (0 or 1)
- Place properties: Split into "place:{property}:name", "place:{property}:address", "place:{property}:latitude", "place:{property}:longitude", and "place:{property}:google_place_id" (optional)
- Number properties: Use JavaScript numbers (not strings)
- Checkbox properties: Use "__YES__" for checked, "__NO__" for unchecked
Special property naming: Properties named "id" or "url" (case insensitive) must be prefixed with "userDefined:" (e.g., "userDefined:URL", "userDefined:id")'''
)
def notion_create_pages(
    pages: list,
    parent_type: str = "",
    parent_id: str = "",
) -> str:
    return "mock"


# --- notion-update-page ---
@server.tool(
    description='''Update a Notion page's properties or content.
For pages in a database: ALWAYS use the "fetch" tool first to get the data source schema and the exact property names. Provide a non-null value to update a property's value. Omitted properties are left unchanged.
IMPORTANT: Some property types require expanded formats:
- Date properties: Split into "date:{property}:start", "date:{property}:end" (optional), and "date:{property}:is_datetime" (0 or 1)
- Place properties: Split into "place:{property}:name", "place:{property}:address", "place:{property}:latitude", "place:{property}:longitude", and "place:{property}:google_place_id" (optional)
- Number properties: Use JavaScript numbers (not strings)
- Checkbox properties: Use "__YES__" for checked, "__NO__" for unchecked
Special property naming: Properties named "id" or "url" (case insensitive) must be prefixed with "userDefined:".
For pages outside of a database: The only allowed property is "title".
Notion page content is a string in Notion-flavored Markdown format.
IMPORTANT: For the complete Markdown specification, first fetch the MCP resource at notion://docs/enhanced-markdown-spec. Do NOT guess or hallucinate Markdown syntax.
Before updating a page's content with this tool, use the "fetch" tool first to get the existing content.
When using "replace_content" or "replace_content_range", the operation will check if any child pages or databases would be deleted. If so, it will fail with an error listing the affected items.
To preserve child pages/databases, include them in new_str using <page url="..."> or <database url="..."> tags.
CRITICAL: To intentionally delete child content: if the call failed with validation and requires allow_deleting_content to be true, DO NOT automatically assume the content should be deleted. ALWAYS show the list of pages to be deleted and ask for user confirmation before proceeding.'''
)
def notion_update_page(
    page_id: str,
    command: str = "update_properties",
    properties: dict = None,
    new_str: str = "",
    selection_with_ellipsis: str = "",
    allow_deleting_content: bool = False,
) -> str:
    return "mock"


# --- notion-create-database ---
@server.tool(
    description='''Creates a new Notion database with the specified properties schema.
If no title property provided, "Name" is auto-added. Returns Markdown with schema, SQLite definition, and data source ID in <data-source> tag for use with update_data_source and query_data_sources tools.
Property types: title (required), rich_text, number, select, multi_select, date, people, checkbox, url, email, phone_number, formula, relation, rollup.'''
)
def notion_create_database(
    properties: dict,
    parent_page_id: str = "",
    title: str = "",
) -> str:
    return "mock"


# --- notion-update-data-source ---
@server.tool(
    description='''Update a Notion data source's properties, name, or other attributes. Returns Markdown showing updated structure and schema.
Accepts a data source ID (collection ID from fetch response's <data-source> tag) or a single-source database ID. Multi-source databases require the specific data source ID.
Property types: title (required), rich_text, number, select, multi_select, date, people, checkbox, url, email, phone_number, formula, relation, rollup, unique_id.
Use null to remove a property. Provide only name to rename a property.
Cannot delete/create title properties. Max one unique_id property. Cannot update synced databases.
Use "fetch" first to see current schema and get the data source ID from <data-source url="collection://..."> tags.
Trashing requires in_trash: true (confirm with user, requires Notion UI to undo).'''
)
def notion_update_data_source(
    data_source_id: str,
    properties: dict = None,
    title: str = "",
    in_trash: bool = False,
) -> str:
    return "mock"


# --- notion-query-database-view ---
@server.tool(
    description='''Query data from a Notion database view.
Executes a database view's existing filters, sorts, and column selections to return matching pages.
Prerequisites: Use the "fetch" tool first to get the database and its view URLs.
View URLs are found in database responses, typically in the format: https://www.notion.so/workspace/db-id?v=view-id'''
)
def notion_query_database_view(view_url: str) -> str:
    return "mock"


# --- notion-create-comment ---
@server.tool(
    description="Add a comment to a page"
)
def notion_create_comment(page_id: str, rich_text: str) -> str:
    return "mock"


# --- notion-get-comments ---
@server.tool(description="Get all comments of a page")
def notion_get_comments(page_id: str) -> str:
    return "mock"


# --- notion-move-pages ---
@server.tool(
    description='''Move one or more Notion pages or databases to a new parent.'''
)
def notion_move_pages(
    page_or_database_ids: list,
    new_parent_type: str = "page_id",
    new_parent_id: str = "",
) -> str:
    return "mock"


# --- notion-duplicate-page ---
@server.tool(
    description='''Duplicate a Notion page. The page must be within the current workspace, and you must have permission to access it. The duplication completes asynchronously, so do not rely on the new page identified by the returned ID or URL to be populated immediately. Let the user know that the duplication is in progress and that they can check back later using the fetch tool or by clicking the returned URL and viewing it in the Notion app.'''
)
def notion_duplicate_page(page_id: str) -> str:
    return "mock"


# --- notion-get-teams ---
@server.tool(
    description='''Retrieves a list of teams (teamspaces) in the current workspace. Shows which teams exist, user membership status, IDs, names, and roles. Teams are returned split by membership status and limited to a maximum of 10 results.'''
)
def notion_get_teams(query: str = "") -> str:
    return "mock"


# --- notion-get-users ---
@server.tool(
    description='''Retrieves a list of users in the current workspace. Shows workspace members and guests with their IDs, names, emails (if available), and types (person or bot).
Supports cursor-based pagination to iterate through all users in the workspace.'''
)
def notion_get_users(
    query: str = "",
    user_id: str = "",
    start_cursor: str = "",
    page_size: int = 100,
) -> str:
    return "mock"
