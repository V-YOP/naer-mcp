"""Simple import test to verify the project structure."""

def test_imports():
    """Test that all modules can be imported."""
    try:
        import naer_mcp
        import naer_mcp
        from naer_mcp.example.example import mcp, greet, add_numbers, reverse_string

        print("✓ All imports successful")
        print(f"  - naer_mcp version: {naer_mcp.__version__}")
        print(f"  - Server name: {mcp.name}")

        # Test tool functions
        result = greet("Test")
        assert result == "Hello, Test!", f"Expected 'Hello, Test!', got {result}"
        print("✓ greet() function works")

        result = add_numbers(2, 3)
        assert result == 5.0, f"Expected 5.0, got {result}"
        print("✓ add_numbers() function works")

        result = reverse_string("hello")
        assert result == "olleh", f"Expected 'olleh', got {result}"
        print("✓ reverse_string() function works")

        return True

    except Exception as e:
        print(f"✗ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    exit(0 if success else 1)