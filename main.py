"""MCP Proxy Server — translates HTTP/HTTPS MCP endpoints to stdio."""

from __future__ import annotations

import argparse
import os
import sys

from fastmcp.client.transports import SSETransport, StreamableHttpTransport
from fastmcp.mcp_config import infer_transport_type_from_url
from fastmcp.server import create_proxy


def _parse_header(value: str) -> tuple[str, str]:
    """Parse 'Key: Value' into (key, value). Exits on bad format."""
    if ": " not in value:
        print(f"Error: invalid header format {value!r}, expected 'Name: Value'", file=sys.stderr)
        sys.exit(1)
    name, _, val = value.partition(": ")
    return name.strip(), val.strip()


def _parse_env_header(value: str) -> tuple[str, str]:
    """Parse 'HeaderName=ENV_VAR' and resolve from environment. Exits on bad format or missing var."""
    if "=" not in value:
        print(f"Error: invalid env-header format {value!r}, expected 'Name=ENV_VAR'", file=sys.stderr)
        sys.exit(1)
    name, _, env_var = value.partition("=")
    name, env_var = name.strip(), env_var.strip()
    env_val = os.environ.get(env_var)
    if env_val is None:
        print(f"Error: environment variable {env_var!r} is not set (for header {name!r})", file=sys.stderr)
        sys.exit(1)
    return name, env_val


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
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        metavar="'Name: Value'",
        help="HTTP header to send with requests (repeatable)",
    )
    parser.add_argument(
        "--env-header",
        action="append",
        default=[],
        metavar="'Name=ENV_VAR'",
        help="HTTP header whose value is read from an environment variable (repeatable)",
    )
    args = parser.parse_args()

    url: str = args.url
    if not url.startswith(("http://", "https://")):
        print(f"Error: URL must start with http:// or https://, got: {url}", file=sys.stderr)
        sys.exit(1)

    # Build headers dict
    headers: dict[str, str] = {}
    for h in args.header:
        k, v = _parse_header(h)
        headers[k] = v
    for eh in args.env_header:
        k, v = _parse_env_header(eh)
        headers[k] = v

    # Create transport with headers
    transport_type = infer_transport_type_from_url(url)
    if transport_type == "sse":
        transport = SSETransport(url, headers=headers or None)
    else:
        transport = StreamableHttpTransport(url, headers=headers or None)

    name = args.name or f"proxy → {url}"
    proxy = create_proxy(transport, name=name)
    proxy.run(transport="stdio")


if __name__ == "__main__":
    main()
