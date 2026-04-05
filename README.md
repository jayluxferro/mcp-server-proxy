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
```

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
        "https://remote-server.com/mcp"
      ]
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
        "https://remote-server.com/mcp"
      ]
    }
  }
}
```

## How it works

The proxy uses FastMCP's `create_proxy()` to connect to the remote server as a client and re-expose all its tools, resources, and prompts over stdio. The transport is inferred from the URL:

- URLs ending in `/sse` use **SSE** transport
- All other `http://` / `https://` URLs use **Streamable HTTP** transport
