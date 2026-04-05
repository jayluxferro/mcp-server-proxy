# mcp-server-proxy

Proxy a remote HTTP/HTTPS MCP server over stdio. This lets any MCP client that speaks stdio connect to remote MCP servers running over HTTP.

Supports both **Streamable HTTP** and **SSE** transports, auto-detected from the URL.

## Install

```bash
uv sync
```

## Usage

```bash
# Streamable HTTP
uv run mcp-server-proxy http://remote-server:8000/mcp

# SSE (auto-detected when URL ends in /sse)
uv run mcp-server-proxy https://remote-server:8000/sse

# Custom display name
uv run mcp-server-proxy --name "My API" http://example.com/mcp

# With auth header (value visible in process args)
uv run mcp-server-proxy --header "Authorization: Bearer tok_123" http://example.com/mcp

# With auth from environment variable (recommended for secrets)
export MCP_TOKEN="Bearer tok_123"
uv run mcp-server-proxy --env-header "Authorization=MCP_TOKEN" http://example.com/mcp

# Multiple headers
uv run mcp-server-proxy \
  --env-header "Authorization=MCP_TOKEN" \
  --header "X-Custom: value" \
  http://example.com/mcp
```

### Headers

| Flag | Format | Description |
|------|--------|-------------|
| `--header` | `"Name: Value"` | Pass a literal header value |
| `--env-header` | `"Name=ENV_VAR"` | Read the header value from an environment variable |

Use `--env-header` for secrets like API keys and tokens — values passed via `--header` are visible in the process argument list.

## Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "my-remote-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/mcp-server-proxy",
        "mcp-server-proxy",
        "--name", "My Remote Server",
        "--env-header", "Authorization=MCP_TOKEN",
        "https://remote-server.com/mcp"
      ],
      "env": {
        "MCP_TOKEN": "Bearer tok_123"
      }
    }
  }
}
```

## Claude Code

Add to your Claude Code config (`.claude/settings.json` or `~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "my-remote-server": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/mcp-server-proxy",
        "mcp-server-proxy",
        "--name", "My Remote Server",
        "--env-header", "Authorization=MCP_TOKEN",
        "https://remote-server.com/mcp"
      ],
      "env": {
        "MCP_TOKEN": "Bearer tok_123"
      }
    }
  }
}
```

## Codex

Add to your Codex config (`~/.codex/config.toml`):

```toml
[mcp_servers.my-remote-server]
command = "uv"
args = [
  "run",
  "--directory", "/path/to/mcp-server-proxy",
  "mcp-server-proxy",
  "--name", "My Remote Server",
  "--env-header", "Authorization=MCP_TOKEN",
  "https://remote-server.com/mcp",
]

[mcp_servers.my-remote-server.env]
MCP_TOKEN = "Bearer tok_123"
```

## How it works

The proxy uses FastMCP's `create_proxy()` to connect to the remote server as a client and re-expose all its tools, resources, and prompts over stdio. The transport is inferred from the URL:

- URLs ending in `/sse` use **SSE** transport
- All other `http://` / `https://` URLs use **Streamable HTTP** transport
