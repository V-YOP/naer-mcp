完全来自 Vibe Coding，纯粹供自用（NAER是我的名字，没有其他意思）！倒也可以算是个 FastMCP 的示例项目吧。

# NAER MCP

一个基于 FastMCP 框架的 MCP (Model Context Protocol) 工具集合。

## 概述

NAER MCP 是一个使用 FastMCP 框架构建的 MCP 服务器，提供了一系列有用的工具、资源和提示，可以与 Claude Desktop 等 MCP 客户端集成。

## 功能特性

- **工具集**: 提供多个实用工具（问候、数学计算、字符串处理、系统信息等）
- **资源**: 提供配置信息等资源
- **提示**: 提供可重用的提示模板
- **多传输支持**: 支持 stdio 和 HTTP 两种传输模式
- **Docker 支持**: 提供完整的 Docker 容器化部署方案
- **易于扩展**: 模块化设计，方便添加自定义工具

## 项目结构

```
naer-mcp/
├── src/
│   └── naer_mcp/
│       ├── __init__.py
│       ├── __main__.py      # 主入口点
│       └── server.py        # MCP 服务器实现
├── examples/
│   └── client.py           # 示例客户端
├── config/
│   └── example_config.yaml # 配置示例
├── tests/                  # 测试目录
├── docker/                 # Docker 相关文件
├── pyproject.toml         # Python 项目配置
├── requirements.txt       # 依赖列表
├── Dockerfile            # Docker 构建文件
├── docker-compose.yml    # Docker Compose 配置
└── README.md            # 本文档
```

## 快速开始

### 1. 本地运行

```bash
# 克隆项目
git clone <repository-url>
cd naer-mcp

# 安装依赖
pip install -r requirements.txt

# 运行服务器（stdio 模式）
python -m naer_mcp

# 或使用 HTTP 模式
python -m naer_mcp --transport http --port 8000
```

### 2. 使用 Docker

```bash
# 构建镜像
docker build -t naer-mcp .

# 运行容器（HTTP 模式）
docker run -p 8000:8000 naer-mcp \
  python -m naer_mcp --transport http --port 8000 --host 0.0.0.0
```

### 3. 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 可用工具

服务器提供以下工具：

1. **greet** - 问候某人
   ```python
   @mcp.tool(name="greet", description="Greet someone by name")
   def greet(name: str) -> str:
       return f"Hello, {name}!"
   ```

2. **add_numbers** - 数字相加
   ```python
   @mcp.tool(name="add_numbers", description="Add two numbers")
   def add_numbers(a: float, b: float) -> float:
       return a + b
   ```

3. **reverse_string** - 反转字符串
   ```python
   @mcp.tool(name="reverse_string", description="Reverse a string")
   def reverse_string(text: str) -> str:
       return text[::-1]
   ```

4. **get_system_info** - 获取系统信息
   ```python
   @mcp.tool(name="get_system_info", description="Get basic system information")
   def get_system_info() -> dict:
       import platform
       import sys
       return {
           "python_version": sys.version,
           "platform": platform.platform(),
           "system": platform.system(),
           "processor": platform.processor(),
       }
   ```

## 扩展和自定义

参照`src/naer_mcp/server.py`和`src/naer_mcp/example/__init__.py`，以及`FastMCP_Tutorial.md`。

## 开发指南

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black src/
flake8 src/
mypy src/
```

### 添加测试

在 `tests/` 目录中添加测试文件：

```python
# tests/test_example.py
def test_greet():
    from naer_mcp.example import greet
    assert greet("Alice") == "Hello, Alice!"
```

## Docker 部署

### 构建选项

```bash
# 开发模式（挂载本地代码）
docker-compose up -d

# 生产模式（构建优化镜像）
docker build --target production -t naer-mcp:prod .
```

### 镜像加速（中国用户）

在国内环境构建 Docker 镜像时，可以通过取消注释 Dockerfile 中的以下行来使用国内镜像源加速依赖下载：

```dockerfile
# Optional: Use Chinese mirror for faster downloads in China
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

取消注释后重新构建镜像：

```bash
docker build --no-cache -t naer-mcp .
```

### 环境变量

- `PYTHONPATH` - Python 模块搜索路径
- `PYTHONUNBUFFERED` - 取消输出缓冲
- `TRANSPORT` - 传输模式（stdio/http）
- `PORT` - HTTP 端口（默认 8000）
- `HOST` - HTTP 主机（默认 0.0.0.0）

### 健康检查

容器包含健康检查，可通过以下方式验证：

```bash
# 检查容器健康状态
docker inspect --format='{{.State.Health.Status}}' naer-mcp-server

# 手动健康检查
curl http://localhost:8000/health
```

## 故障排除

### 常见问题

1. **导入错误**: 确保 `PYTHONPATH` 包含 `src/` 目录
2. **端口冲突**: 检查端口 8000 是否被占用
3. **依赖问题**: 使用 `pip install -r requirements.txt` 重新安装依赖
4. **Docker 构建失败**: 清理 Docker 缓存 `docker system prune -a`

### 日志查看

```bash
# 本地运行
python -m naer_mcp --transport http 2>&1 | tee server.log

# Docker 容器
docker-compose logs -f naer-mcp

# 详细日志
docker logs --tail 100 -f naer-mcp-server
```

## 许可证

MIT License

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 支持

如有问题或建议，请通过以下方式联系：

- 创建 GitHub Issue
- 查看 [FastMCP 文档](https://gofastmcp.com/)

---

**提示**: 这是一个示例项目，请根据实际需求进行修改和扩展。FastMCP 框架提供了丰富的功能，可以创建复杂的 MCP 服务器以满足各种需求。