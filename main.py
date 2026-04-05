"""MCP Proxy Server — translates HTTP/HTTPS MCP endpoints to stdio."""

from __future__ import annotations

import argparse
import sys

from fastmcp.server import create_proxy


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="mcp-server-proxy",
        description="Proxy a remote HTTP/HTTPS MCP server over stdio.",
    )
    parser.add_argument(
        "url",
        help="URL of the remote MCP server (http://, https://, or ending in /sse)",
    )
    parser.add_argument(
        "--name",
        default=None,
        help="Display name for this proxy server (default: derived from URL)",
    )
    args = parser.parse_args()

    url: str = args.url
    if not url.startswith(("http://", "https://")):
        print(f"Error: URL must start with http:// or https://, got: {url}", file=sys.stderr)
        sys.exit(1)

    name = args.name or f"proxy → {url}"
    proxy = create_proxy(url, name=name)
    proxy.run(transport="stdio")


if __name__ == "__main__":
    main()
