"""Main entry point for NAER MCP server."""

from .server import mcp

if __name__ == "__main__":
    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="NAER MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode (stdio or http)",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for HTTP transport"
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP transport"
    )

    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="http", port=args.port, host=args.host)
    else:
        mcp.run()