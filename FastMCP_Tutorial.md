# FastMCP 快速入门教程

## 什么是 FastMCP？

FastMCP 是一个用于构建 **MCP (Model Context Protocol)** 服务器和客户端的 Python 框架。MCP 是由 Anthropic 开发的开放协议，用于连接大型语言模型（如 Claude）与外部工具、数据和系统。

### 核心概念

- **MCP 服务器**: 提供工具、资源和提示的组件
- **工具 (Tools)**: LLM 可以调用的函数，用于执行特定任务
- **资源 (Resources)**: LLM 可以读取的数据源（文件、API 数据等）
- **提示 (Prompts)**: 可重用的提示模板

Human：注意——Prompt是给客户端用的，自己用的MCP按理说没必要使用Prompt？

### 为什么选择 FastMCP？

1. **简单易用**: Pythonic API，几行代码即可创建 MCP 服务器
2. **功能完整**: 支持所有 MCP 功能（工具、资源、提示）
3. **生产就绪**: 内置身份验证、监控、部署支持
4. **多传输模式**: 支持 stdio（本地）和 HTTP（远程）两种传输方式

## 安装 FastMCP

### 基础安装

```bash
# 使用 pip 安装
pip install fastmcp<3

# 使用 uv（推荐）
uv add fastmcp

# 验证安装
fastmcp version
```

### 版本说明

- FastMCP 3.0 正在开发中，建议固定到 v2 版本：`fastmcp<3`
- 生产环境建议固定具体版本：`fastmcp==2.14.5`

### 依赖管理

FastMCP 依赖 Cyclopts，如果担心许可证问题，可以安装特定版本：

```bash
pip install "cyclopts>=5.0.0a1"
```

## 创建你的第一个 MCP 服务器

### 1. 初始化服务器

创建一个新的 Python 文件 `my_server.py`：

```python
from fastmcp import FastMCP

# 创建 MCP 服务器实例
mcp = FastMCP("我的第一个 MCP 服务器", version="1.0.0")
```

### 2. 添加工具

工具是 LLM 可以调用的函数：

```python
@mcp.tool(name="greet", description="根据姓名问候某人")
def greet(name: str) -> str:
    """根据姓名问候某人

    Args:
        name: 要问候的人的姓名

    Returns:
        问候语
    """
    return f"你好, {name}!"

@mcp.tool(name="calculate", description="执行数学计算")
def calculate(expression: str) -> float:
    """计算数学表达式

    Args:
        expression: 数学表达式，如 "2 + 3 * 4"

    Returns:
        计算结果
    """
    try:
        return eval(expression)
    except Exception as e:
        return f"计算错误: {e}"
```

### 3. 添加资源

资源是 LLM 可以访问的数据：

```python
@mcp.resource("config://server-info")
def server_info() -> dict:
    """提供服务器信息

    Returns:
        服务器配置信息
    """
    return {
        "server_name": "我的 MCP 服务器",
        "version": "1.0.0",
        "author": "你的名字",
        "description": "示例 MCP 服务器"
    }

# 带参数的资源模板
@mcp.resource("data://user/{user_id}/profile")
def user_profile(user_id: str) -> dict:
    """获取用户资料

    Args:
        user_id: 用户 ID

    Returns:
        用户资料
    """
    # 这里可以从数据库或其他来源获取数据
    return {
        "user_id": user_id,
        "name": f"用户{user_id}",
        "email": f"user{user_id}@example.com",
        "created_at": "2024-01-01"
    }
```

### 4. 添加提示

提示是可重用的 LLM 提示模板：

```python
@mcp.prompt("greeting_template")
def greeting_template(user_name: str = "访客", language: str = "中文") -> str:
    """生成问候提示

    Args:
        user_name: 用户名
        language: 语言（中文/英文）

    Returns:
        问候提示
    """
    if language == "中文":
        return f"""你好 {user_name}！

我是你的 MCP 助手，我可以：
1. 使用工具帮你完成各种任务
2. 访问资源获取信息
3. 提供专门的提示模板

有什么我可以帮助你的吗？"""
    else:
        return f"""Hello {user_name}!

I'm your MCP assistant. I can:
1. Use tools to help you with various tasks
2. Access resources to get information
3. Provide specialized prompt templates

How can I assist you today?"""
```

### 5. 运行服务器

```python
if __name__ == "__main__":
    # 使用 stdio 传输（本地使用）
    mcp.run()

    # 或使用 HTTP 传输（远程访问）
    # mcp.run(transport="http", port=8000, host="0.0.0.0")
```

## 运行你的服务器

### 方式一：直接运行

```bash
python my_server.py
```

### 方式二：使用 FastMCP CLI

```bash
# 运行服务器
fastmcp run my_server.py:mcp

# 运行 HTTP 服务器
fastmcp run my_server.py:mcp --transport http --port 8000
```

### 方式三：作为模块运行

如果你的服务器在包中：

```bash
python -m my_package.my_server
```

## 连接客户端

### Claude Desktop 配置

在 Claude Desktop 的 MCP 设置中添加：

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "python",
      "args": ["my_server.py"],
      "env": {
        "PYTHONPATH": "/path/to/your/project"
      }
    }
  }
}
```

### HTTP 客户端访问

当使用 HTTP 传输时，可以通过以下端点访问：

- `GET /mcp` - MCP 协议端点
- 工具、资源、提示通过 MCP 协议提供

## 高级功能

### 1. 工具参数验证

FastMCP 自动使用类型提示进行参数验证：

```python
from typing import List, Optional
from pydantic import BaseModel

class UserData(BaseModel):
    name: str
    age: int
    email: Optional[str] = None

@mcp.tool(name="create_user", description="创建用户")
def create_user(user: UserData, tags: List[str] = None) -> dict:
    """创建新用户

    Args:
        user: 用户数据
        tags: 用户标签

    Returns:
        创建的用户信息
    """
    # 参数会自动验证和转换
    return {
        "id": "user_123",
        **user.dict(),
        "tags": tags or []
    }
```

### 2. 异步工具支持

```python
import asyncio

@mcp.tool(name="fetch_data", description="异步获取数据")
async def fetch_data(url: str) -> str:
    """从 URL 异步获取数据

    Args:
        url: 目标 URL

    Returns:
        获取的内容
    """
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 3. 错误处理

```python
@mcp.tool(name="safe_divide", description="安全除法")
def safe_divide(a: float, b: float) -> float:
    """执行除法运算，处理除零错误

    Args:
        a: 被除数
        b: 除数

    Returns:
        商

    Raises:
        ValueError: 当除数为零时
    """
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b
```

### 4. 服务器配置

```python
# 创建带配置的服务器
mcp = FastMCP(
    name="配置化服务器",
    version="1.0.0",
    description="这是一个配置化的 MCP 服务器",
    instructions="请礼貌地使用工具",

    # 控制重复组件的行为
    on_duplicate_tools="warn",  # warn/error/replace/ignore

    # 严格输入验证
    strict_input_validation=True,

    # 标签过滤
    include_tags={"public"},
    exclude_tags={"internal"}
)
```

## 项目结构建议

```
my-mcp-project/
├── src/
│   └── my_mcp_server/
│       ├── __init__.py
│       ├── server.py          # 主服务器文件
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── calculator.py  # 计算工具
│       │   ├── weather.py     # 天气工具
│       │   └── database.py    # 数据库工具
│       ├── resources/
│       │   ├── __init__.py
│       │   └── configs.py     # 资源配置
│       └── prompts/
│           ├── __init__.py
│           └── templates.py   # 提示模板
├── pyproject.toml            # 项目配置
├── requirements.txt          # 依赖列表
└── README.md                # 项目说明
```

## 部署选项

### 1. 本地部署（stdio）

```bash
# 最简单的方式
python my_server.py
```

### 2. HTTP 服务器

```bash
# 启动 HTTP 服务器
python my_server.py --transport http --port 8000

# 或使用 FastMCP CLI
fastmcp run my_server.py:mcp --transport http --port 8000
```

### 3. Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "my_server.py", "--transport", "http", "--port", "8000", "--host", "0.0.0.0"]
```

构建和运行：

```bash
docker build -t my-mcp-server .
docker run -p 8000:8000 my-mcp-server
```

### 4. 使用 Prefect Horizon（免费个人项目）

FastMCP 可以部署到 Prefect Horizon，提供托管服务：

1. 将代码推送到 GitHub
2. 在 Prefect Horizon 中创建部署
3. 获取托管 URL

## 最佳实践

### 1. 工具设计原则

- **单一职责**: 每个工具只做一件事
- **良好命名**: 使用动词+名词的命名方式
- **完整文档**: 为每个工具提供详细的文档字符串
- **错误处理**: 妥善处理可能出现的错误
- **类型提示**: 使用完整的类型提示

### 2. 安全性考虑

- **输入验证**: 始终验证用户输入
- **权限控制**: 根据需要使用标签过滤工具
- **敏感信息**: 不要将敏感信息硬编码在工具中
- **资源限制**: 对耗时的操作设置超时限制

### 3. 性能优化

- **异步操作**: 对 I/O 密集型操作使用异步工具
- **缓存结果**: 对频繁访问的资源进行缓存
- **连接池**: 对数据库和 API 连接使用连接池
- **懒加载**: 只在需要时加载资源

## 故障排除

### 常见问题

1. **工具未显示**
   - 检查工具是否已正确注册（@mcp.tool 装饰器）
   - 确认工具函数有正确的类型提示
   - 检查服务器是否已重新启动

2. **连接失败**
   - 确认传输模式（stdio/HTTP）正确
   - 检查端口是否被占用
   - 验证客户端配置是否正确

3. **依赖问题**
   - 确保所有依赖已安装：`pip install -r requirements.txt`
   - 检查 Python 版本兼容性（需要 Python 3.8+）

4. **权限问题**
   - 确保有足够的权限访问所需资源
   - 检查文件和目录权限

### 调试技巧

```python
# 启用调试日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 或在运行服务器时设置环境变量
# FASTMCP_LOG_LEVEL=DEBUG fastmcp run my_server.py:mcp
```

## 示例：完整天气查询服务器

```python
from fastmcp import FastMCP
from typing import Optional
import datetime

mcp = FastMCP("天气查询服务器", version="1.0.0")

@mcp.tool(name="get_weather", description="获取城市天气信息")
def get_weather(city: str, date: Optional[str] = None) -> dict:
    """获取指定城市的天气信息

    Args:
        city: 城市名称
        date: 日期（YYYY-MM-DD），默认为今天

    Returns:
        天气信息
    """
    # 这里可以调用天气 API
    # 示例数据
    return {
        "city": city,
        "date": date or datetime.datetime.now().strftime("%Y-%m-%d"),
        "temperature": "22°C",
        "condition": "晴天",
        "humidity": "65%",
        "wind_speed": "10 km/h"
    }

@mcp.resource("weather://cities/supported")
def supported_cities() -> list:
    """获取支持的城市列表

    Returns:
        支持的城市列表
    """
    return ["北京", "上海", "广州", "深圳", "杭州", "成都"]

@mcp.prompt("weather_assistant")
def weather_assistant(city: str = None) -> str:
    """天气助手提示模板

    Args:
        city: 城市名称

    Returns:
        助手提示
    """
    if city:
        return f"""你是一个天气助手，专门帮助用户查询 {city} 的天气信息。

你可以：
1. 查询当前天气
2. 查询未来天气
3. 提供天气建议

请礼貌、准确地回答用户的问题。"""
    else:
        return """你是一个天气助手，可以帮助用户查询各地天气信息。

你可以：
1. 查询任意城市的天气
2. 提供天气相关的建议
3. 解释天气术语

请先询问用户想查询哪个城市的天气。"""

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
```

## 下一步

### 学习资源

1. **官方文档**: https://gofastmcp.com/
2. **MCP 协议**: https://spec.modelcontextprotocol.io/
3. **示例项目**: 查看 FastMCP 的 GitHub 仓库

### 进阶主题

1. **自定义传输**: 实现自己的传输协议
2. **身份验证**: 添加 OAuth、API 密钥等认证
3. **监控指标**: 集成 Prometheus、OpenTelemetry
4. **插件系统**: 创建可插拔的工具模块
5. **测试框架**: 编写 MCP 服务器的单元测试

### 社区支持

- **GitHub Issues**: 报告问题和请求功能
- **Discord 社区**: 与其他开发者交流
- **Stack Overflow**: 使用 `fastmcp` 标签提问

---

**提示**: 这个教程涵盖了 FastMCP 的主要功能，但实际使用时请根据具体需求调整。FastMCP 的强大之处在于它的灵活性和可扩展性，不要害怕尝试新的用法和模式！

**开始构建**: 现在你已经掌握了 FastMCP 的基础知识，开始创建你自己的 MCP 服务器吧！从简单的工具开始，逐步添加更多功能，你会发现自己可以构建出非常强大的 AI 助手。