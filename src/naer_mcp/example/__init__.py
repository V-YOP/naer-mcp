"""FastMCP server example.

This module provides a simple MCP server with example tools using FastMCP framework.
"""

from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP("示例", version="0.1.0")

@mcp.tool
def greet(name: str) -> str:
    """根据姓名问候某人

    Args:
        name: 要问候的人的姓名

    Returns:
        问候语
    """
    return f"你好, {name}!"


@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """将两个数字相加

    Args:
        a: 第一个数字
        b: 第二个数字

    Returns:
        两个数字的和
    """
    return a + b


@mcp.tool
def reverse_string(text: str) -> str:
    """反转字符串

    Args:
        text: 要反转的文本

    Returns:
        反转后的字符串
    """
    return text[::-1]


@mcp.tool
def get_system_info() -> dict:
    """获取基本系统信息

    Returns:
        包含系统信息的字典
    """
    import platform
    import sys

    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "system": platform.system(),
        "processor": platform.processor(),
    }


@mcp.resource("example://config")
def example_config() -> dict:
    """提供配置信息的示例资源

    Returns:
        配置字典
    """
    return {
        "server_name": "NAER MCP 服务器",
        "version": "0.1.0",
        "tools": ["greet", "add_numbers", "reverse_string", "get_system_info"],
        "description": "包含实用工具的示例 MCP 服务器",
    }
