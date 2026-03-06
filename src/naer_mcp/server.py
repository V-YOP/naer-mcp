"""
FastMCP server root file
"""

from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP("NAER MCP Server", version="0.1.0")

# use mount to seperate tools like Controller in MVC
from .example import mcp as example_mcp
mcp.mount(example_mcp, prefix='example', as_proxy=False)
