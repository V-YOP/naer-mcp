"""FastMCP server example.

This module provides a simple MCP server with example tools using FastMCP framework.
"""

from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP("NAER MCP Server", version="0.1.0")
mcp.mount

@mcp.tool(name="greet", description="根据姓名问候某人")
def greet(name: str) -> str:
    """根据姓名问候某人

    Args:
        name: 要问候的人的姓名

    Returns:
        问候语
    """
    return f"你好, {name}!"


@mcp.tool(name="add_numbers", description="将两个数字相加")
def add_numbers(a: float, b: float) -> float:
    """将两个数字相加

    Args:
        a: 第一个数字
        b: 第二个数字

    Returns:
        两个数字的和
    """
    return a + b


@mcp.tool(name="reverse_string", description="反转字符串")
def reverse_string(text: str) -> str:
    """反转字符串

    Args:
        text: 要反转的文本

    Returns:
        反转后的字符串
    """
    return text[::-1]


@mcp.tool(name="get_system_info", description="获取基本系统信息")
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


@mcp.prompt("greeting_prompt")
def greeting_prompt(name: str = "用户") -> str:
    """生成问候提示

    Args:
        name: 包含在问候中的姓名

    Returns:
        问候提示文本
    """
    return f"""你正在与 {name} 对话。
这是来自 NAER MCP 服务器的示例提示。
你可以使用可用的工具来帮助 {name} 完成各种任务。"""
