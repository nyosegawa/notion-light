"""Light Notion MCP descriptions - compressed for minimal context usage"""

from fastmcp import FastMCP

server = FastMCP("notion-light")


@server.tool(
    description="Search Notion workspace and connected sources by semantic query. See notion-best-practices skill for usage details."
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


@server.tool(
    description="Retrieve a Notion page or database by URL or ID. See notion-best-practices skill for usage details."
)
def notion_fetch(id: str, include_transcript: bool = False) -> str:
    return "mock"


@server.tool(
    description="Create one or more Notion pages in a database or standalone. See notion-best-practices skill for usage details."
)
def notion_create_pages(
    pages: list,
    parent_type: str = "",
    parent_id: str = "",
) -> str:
    return "mock"


@server.tool(
    description="Update a Notion page's properties or content. See notion-best-practices skill for usage details."
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


@server.tool(
    description="Create a new Notion database with specified property schema. See notion-best-practices skill for usage details."
)
def notion_create_database(
    properties: dict,
    parent_page_id: str = "",
    title: str = "",
) -> str:
    return "mock"


@server.tool(
    description="Update a Notion data source's properties, schema, or name. See notion-best-practices skill for usage details."
)
def notion_update_data_source(
    data_source_id: str,
    properties: dict = None,
    title: str = "",
    in_trash: bool = False,
) -> str:
    return "mock"


@server.tool(
    description="Query data from a Notion database using a view's filters and sorts. See notion-best-practices skill for usage details."
)
def notion_query_database_view(view_url: str) -> str:
    return "mock"


@server.tool(
    description="Add a comment to a Notion page. See notion-best-practices skill for usage details."
)
def notion_create_comment(page_id: str, rich_text: str) -> str:
    return "mock"


@server.tool(
    description="Get all comments of a Notion page. See notion-best-practices skill for usage details."
)
def notion_get_comments(page_id: str) -> str:
    return "mock"


@server.tool(
    description="Move Notion pages or databases to a new parent. See notion-best-practices skill for usage details."
)
def notion_move_pages(
    page_or_database_ids: list,
    new_parent_type: str = "page_id",
    new_parent_id: str = "",
) -> str:
    return "mock"


@server.tool(
    description="Duplicate a Notion page asynchronously. See notion-best-practices skill for usage details."
)
def notion_duplicate_page(page_id: str) -> str:
    return "mock"


@server.tool(
    description="List teams (teamspaces) in the Notion workspace. See notion-best-practices skill for usage details."
)
def notion_get_teams(query: str = "") -> str:
    return "mock"


@server.tool(
    description="List users in the Notion workspace. See notion-best-practices skill for usage details."
)
def notion_get_users(
    query: str = "",
    user_id: str = "",
    start_cursor: str = "",
    page_size: int = 100,
) -> str:
    return "mock"
