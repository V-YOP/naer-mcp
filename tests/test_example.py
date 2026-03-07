"""Simple import test to verify the project structure."""

import pytest

@pytest.mark.asyncio
async def test_example():
    """Test that all modules can be imported."""
    from naer_mcp.example import greet, add_numbers, reverse_string

    # Test tool functions
    result = await greet.run({'name': 'Test'})
    result = result.structured_content['result']
    assert result == "你好, Test!", f"Expected 'Hello, Test!', got {result}"

    result = await add_numbers.run({'a': 2, 'b': 3})
    result = result.structured_content['result']
    assert result == 5.0, f"Expected 5.0, got {result}"

    result = await reverse_string.run({'text': "hello"})
    result = result.structured_content['result']
    assert result == "olleh", f"Expected 'olleh', got {result}"

