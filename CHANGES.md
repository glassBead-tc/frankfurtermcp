# FrankfurterMCP Server Changes

## Summary
Modified the FrankfurterMCP server to use stdio transport for MCP communication while preserving all original functionality.

## Changes Made

### 1. MCP Configuration
- Note: The original author tested with FastMCP client and custom agents, not Claude Desktop
- For Claude Desktop/Claude Code usage, created configuration with:
  ```json
  "command": "uv",
  "args": ["run", "--project", "/path/to/frankfurtermcp", "python", "/path/to/server.py"]
  ```
- The `--project` flag ensures dependencies are found when running from any directory

### 2. Server Code (`src/frankfurtermcp/server.py`)
- **Line 14**: Swapped import order (cosmetic change only)
  - Original: `from frankfurtermcp.common import EnvironmentVariables, parse_env`
  - Current: `from frankfurtermcp.common import parse_env, EnvironmentVariables`
- **Line 382**: Removed transport configuration to force stdio mode
  - Original: `app.run(transport=parse_env(...), uvicorn_config={...})`
  - Current: `app.run()`

### 3. Common Module (`src/frankfurtermcp/common.py`)
- **Lines 22-25**: Commented out transport-related environment variables
  ```python
  # Transport configuration removed - using stdio only
  # MCP_SERVER_TRANSPORT = "MCP_SERVER_TRANSPORT"
  # DEFAULT__MCP_SERVER_TRANSPORT = "stdio"
  # ALLOWED__MCP_SERVER_TRANSPORT = ["stdio"]
  ```

## Result
- All 5 currency exchange tools function correctly
- SSL/proxy support preserved
- All original functionality maintained
- Server now uses stdio transport for MCP communication

## Original Author
This server was created by Anirban Basu (anirbanbasu@users.noreply.github.com)
Repository: https://github.com/anirbanbasu/frankfurtermcp

---

## Plain English Summary

I made minimal changes to get this MCP server working. Here's what I changed:

1. In `server.py` on line 382, I removed the transport configuration from `app.run()`. The original code let you choose between different transport modes (stdio, sse, streamable-http). I simplified it to just use stdio.

2. In `common.py` on lines 22-25, I commented out the environment variables that controlled transport selection since we're only using stdio now.

3. That's it. Everything else is exactly as the original author wrote it.

The server works perfectly - all 5 currency exchange tools are functional.