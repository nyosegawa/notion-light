"""Notion Light MCP Server: description を1行に圧縮した軽量版"""

from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient

LIGHT_DESCRIPTIONS = {
    "notion-search": (
        "Search Notion workspace and connected sources by semantic query. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-fetch": (
        "Retrieve a Notion page or database by URL or ID. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-create-pages": (
        "Create one or more Notion pages in a database or standalone. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-update-page": (
        "Update a Notion page's properties or content. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-create-database": (
        "Create a new Notion database with specified property schema. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-create-comment": (
        "Add a comment to a Notion page. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-get-comments": (
        "Get all comments of a Notion page. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-move-pages": (
        "Move Notion pages or databases to a new parent. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-update-data-source": (
        "Update a Notion data source's properties, schema, or name. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-query-database-view": (
        "Query data from a Notion database using a view's filters and sorts. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-duplicate-page": (
        "Duplicate a Notion page asynchronously. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-get-teams": (
        "List teams (teamspaces) in the Notion workspace. "
        "See notion-best-practices skill for usage details."
    ),
    "notion-get-users": (
        "List users in the Notion workspace. "
        "See notion-best-practices skill for usage details."
    ),
}

proxy_client = ProxyClient("npx @notionhq/notion-mcp-server")
server = FastMCP.as_proxy(proxy_client, name="notion-light")

for tool in server.list_tools():
    if tool.name in LIGHT_DESCRIPTIONS:
        tool.description = LIGHT_DESCRIPTIONS[tool.name]
