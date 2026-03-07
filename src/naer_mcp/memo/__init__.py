"""Memo tools for NAER MCP server.

This module provides memo management tools including create, list, and retrieve operations.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fastmcp import FastMCP
from pydantic import BaseModel

# Create a FastMCP server instance for memo tools
mcp = FastMCP("Memo Tools", version="0.1.0")

# Data models
class Memo(BaseModel):
    """Memo data model."""
    id: str
    name: str
    description: str
    content: Optional[str] = None
    created_at: str
    updated_at: str

class MemoCreate(BaseModel):
    """Memo creation data model."""
    name: str
    description: str
    content: Optional[str] = None

# Storage configuration
DATA_DIR = Path(os.getcwd()) / "data"
MEMOS_FILE = DATA_DIR / "memos.json"

def _ensure_data_dir() -> None:
    """Ensure data directory exists."""
    DATA_DIR.mkdir(exist_ok=True)

def _load_memos() -> Dict[str, Memo]:
    """Load all memos from JSON file."""
    _ensure_data_dir()

    if not MEMOS_FILE.exists():
        return {}

    try:
        with open(MEMOS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert dict to Memo objects
        memos = {}
        for memo_id, memo_data in data.items():
            memos[memo_id] = Memo(**memo_data)
        return memos
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # If file is corrupted, return empty dict
        print(f"Warning: Failed to load memos from {MEMOS_FILE}: {e}")
        return {}

def _save_memos(memos: Dict[str, Memo]) -> None:
    """Save all memos to JSON file."""
    _ensure_data_dir()

    # Convert Memo objects to dict
    data = {memo_id: memo.model_dump() for memo_id, memo in memos.items()}

    with open(MEMOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@mcp.tool
def create_memo(name: str, description: str, content: Optional[str] = None) -> Dict:
    """创建新的备忘

    Args:
        name: 备忘名称
        description: 备忘简要描述
        content: 备忘详细内容（可选）

    Returns:
        包含创建的备忘信息和状态的字典
    """
    # Generate unique ID
    memo_id = str(uuid.uuid4())
    current_time = datetime.now().isoformat()

    # Create memo
    memo = Memo(
        id=memo_id,
        name=name,
        description=description,
        content=content,
        created_at=current_time,
        updated_at=current_time
    )

    # Load existing memos
    memos = _load_memos()

    # Add new memo
    memos[memo_id] = memo

    # Save to file
    _save_memos(memos)

    return {
        "status": "success",
        "message": "Memo created successfully",
        "memo": {
            "id": memo_id,
            "name": name,
            "description": description,
            "created_at": current_time
        }
    }

@mcp.tool
def list_memos() -> Dict:
    """列举所有备忘

    Returns:
        包含所有备忘列表的字典，每个备忘包含id、名称和简要描述
    """
    # Load memos
    memos = _load_memos()

    # Format response
    memo_list = []
    for memo in memos.values():
        memo_list.append({
            "id": memo.id,
            "name": memo.name,
            "description": memo.description
        })

    return {
        "status": "success",
        "count": len(memo_list),
        "memos": memo_list
    }

@mcp.tool
def get_memo(memo_id: str) -> Dict:
    """根据ID获取备忘详情

    Args:
        memo_id: 备忘的唯一ID

    Returns:
        包含备忘详情的字典，如果找不到则返回错误
    """
    # Load memos
    memos = _load_memos()

    # Find memo by ID
    if memo_id not in memos:
        return {
            "status": "error",
            "message": f"Memo with ID '{memo_id}' not found"
        }

    memo = memos[memo_id]

    return {
        "status": "success",
        "memo": memo.dict()
    }

@mcp.tool
def delete_memo(memo_id: str) -> Dict:
    """
    根据ID删除备忘。
    
    ⚠️执行之前，事先向用户确认！

    Args:
        memo_id: 备忘的唯一ID

    Returns:
        包含备忘详情的字典，如果找不到则返回错误
    """
    # Load memos
    memos = _load_memos()

    # Find memo by ID
    if memo_id not in memos:
        return {
            "status": "error",
            "message": f"Memo with ID '{memo_id}' not found"
        }

    del memos[memo_id]
    _save_memos(memos)

    return {
        "status": "success"
    }

@mcp.resource("memo://status")
def memo_status() -> Dict:
    """提供备忘工具状态信息的资源

    Returns:
        包含备忘工具状态的字典
    """
    memos = _load_memos()

    return {
        "tool_name": "Memo Tools",
        "version": "0.1.0",
        "memo_count": len(memos),
        "storage_path": str(MEMOS_FILE),
        "available_tools": ["create_memo", "list_memos", "get_memo"]
    }