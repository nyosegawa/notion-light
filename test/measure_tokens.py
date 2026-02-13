"""Measure exact token counts for Original vs Light MCP tool definitions"""

import json
import subprocess
import sys
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")  # cl100k_base, same as Claude


def count_tokens(text: str) -> int:
    return len(enc.encode(text))


def get_tools_from_server(server_script: str) -> list[dict]:
    """Start MCP server and get tools/list response"""
    proc = subprocess.Popen(
        ["fastmcp", "run", server_script, "--transport", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Initialize
    init_msg = json.dumps(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "measure", "version": "0.1"},
            },
        }
    )
    proc.stdin.write(init_msg.encode() + b"\n")
    proc.stdin.flush()

    import time

    time.sleep(1)

    # List tools
    tools_msg = json.dumps(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    proc.stdin.write(tools_msg.encode() + b"\n")
    proc.stdin.flush()

    time.sleep(2)
    proc.terminate()

    stdout = proc.stdout.read().decode()
    # Parse the tools/list response (second JSON line)
    lines = [l.strip() for l in stdout.strip().split("\n") if l.strip()]
    for line in lines:
        data = json.loads(line)
        if data.get("id") == 2:
            return data["result"]["tools"]
    return []


def measure_server(name: str, script: str):
    """Measure token counts for a server"""
    tools = get_tools_from_server(script)

    print(f"\n{'='*60}")
    print(f"  {name} ({len(tools)} tools)")
    print(f"{'='*60}")

    total_desc = 0
    total_schema = 0
    total_all = 0
    results = []

    for tool in tools:
        tool_name = tool["name"]
        desc = tool.get("description", "")
        schema_str = json.dumps(tool.get("inputSchema", {}))

        desc_tokens = count_tokens(desc)
        schema_tokens = count_tokens(schema_str)
        tool_json_str = json.dumps(tool)
        all_tokens = count_tokens(tool_json_str)

        total_desc += desc_tokens
        total_schema += schema_tokens
        total_all += all_tokens

        results.append(
            {
                "name": tool_name,
                "desc_tokens": desc_tokens,
                "schema_tokens": schema_tokens,
                "all_tokens": all_tokens,
            }
        )

    # Print table
    print(f"\n{'Tool':<30} {'Desc':>8} {'Schema':>8} {'Total':>8}")
    print(f"{'-'*30} {'-'*8} {'-'*8} {'-'*8}")
    for r in results:
        print(
            f"{r['name']:<30} {r['desc_tokens']:>8} {r['schema_tokens']:>8} {r['all_tokens']:>8}"
        )
    print(f"{'-'*30} {'-'*8} {'-'*8} {'-'*8}")
    print(f"{'TOTAL':<30} {total_desc:>8} {total_schema:>8} {total_all:>8}")

    return {
        "total_desc": total_desc,
        "total_schema": total_schema,
        "total_all": total_all,
        "tools": results,
    }


if __name__ == "__main__":
    original = measure_server("Original (Fat) Notion MCP", "server_original.py:server")
    light = measure_server("Light Notion MCP", "server_light.py:server")

    print(f"\n{'='*60}")
    print(f"  COMPARISON")
    print(f"{'='*60}")

    desc_reduction = (1 - light["total_desc"] / original["total_desc"]) * 100
    all_reduction = (1 - light["total_all"] / original["total_all"]) * 100

    print(f"\nDescription tokens:  {original['total_desc']:>6} -> {light['total_desc']:>6}  ({desc_reduction:.1f}% reduction)")
    print(f"Schema tokens:       {original['total_schema']:>6} -> {light['total_schema']:>6}  (unchanged)")
    print(f"Total tool def:      {original['total_all']:>6} -> {light['total_all']:>6}  ({all_reduction:.1f}% reduction)")
    print(f"\nContext saved per session: {original['total_all'] - light['total_all']} tokens")
