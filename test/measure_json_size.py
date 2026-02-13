"""Compare the actual tools/list JSON payload size between Original and Light"""

import json
import subprocess
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")


def get_tools_response(server_script: str) -> dict:
    """Start MCP server and get raw tools/list response"""
    proc = subprocess.Popen(
        ["fastmcp", "run", server_script, "--transport", "stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

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

    tools_msg = json.dumps(
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    proc.stdin.write(tools_msg.encode() + b"\n")
    proc.stdin.flush()

    time.sleep(2)
    proc.terminate()

    stdout = proc.stdout.read().decode()
    lines = [l.strip() for l in stdout.strip().split("\n") if l.strip()]
    for line in lines:
        data = json.loads(line)
        if data.get("id") == 2:
            return data["result"]
    return {}


if __name__ == "__main__":
    print("Fetching Original tools/list response...")
    original = get_tools_response("server_original.py:server")

    print("Fetching Light tools/list response...")
    light = get_tools_response("server_light.py:server")

    # Serialize to JSON
    original_json = json.dumps(original, indent=2)
    light_json = json.dumps(light, indent=2)

    # Save to files for inspection
    with open("tools_list_original.json", "w") as f:
        f.write(original_json)
    with open("tools_list_light.json", "w") as f:
        f.write(light_json)

    # Token counts
    original_tokens = len(enc.encode(original_json))
    light_tokens = len(enc.encode(light_json))

    # Byte sizes
    original_bytes = len(original_json.encode())
    light_bytes = len(light_json.encode())

    print(f"\n{'='*60}")
    print(f"  tools/list Response Comparison")
    print(f"{'='*60}")
    print(f"\n{'Metric':<25} {'Original':>12} {'Light':>12} {'Reduction':>12}")
    print(f"{'-'*25} {'-'*12} {'-'*12} {'-'*12}")
    print(f"{'JSON bytes':<25} {original_bytes:>12,} {light_bytes:>12,} {(1-light_bytes/original_bytes)*100:>11.1f}%")
    print(f"{'Tokens (cl100k_base)':<25} {original_tokens:>12,} {light_tokens:>12,} {(1-light_tokens/original_tokens)*100:>11.1f}%")
    print(f"{'Tool count':<25} {len(original['tools']):>12} {len(light['tools']):>12} {'same':>12}")
    print(f"\nSaved files: tools_list_original.json, tools_list_light.json")

    # Per-tool description comparison
    print(f"\n{'='*60}")
    print(f"  Per-tool Description Comparison")
    print(f"{'='*60}")
    print(f"\n{'Tool':<30} {'Orig (tokens)':>14} {'Light (tokens)':>14} {'Reduction':>10}")
    print(f"{'-'*30} {'-'*14} {'-'*14} {'-'*10}")

    for orig_tool, light_tool in zip(original["tools"], light["tools"]):
        orig_desc_tokens = len(enc.encode(orig_tool.get("description", "")))
        light_desc_tokens = len(enc.encode(light_tool.get("description", "")))
        reduction = (1 - light_desc_tokens / orig_desc_tokens) * 100 if orig_desc_tokens > 0 else 0
        print(f"{orig_tool['name']:<30} {orig_desc_tokens:>14} {light_desc_tokens:>14} {reduction:>9.1f}%")
