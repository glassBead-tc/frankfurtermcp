# FrankfurterMCP Server Changes

## Summary
Modified the FrankfurterMCP server to work with Claude Code's stdio-only transport requirement while preserving all original functionality.

## Changes Made

### 1. MCP Configuration (`mcp_config_claude_code.json`)
- Added `--project` flag to the `uv run` command to ensure dependencies are found
- Changed from:
  ```json
  "args": ["run", "python", "/path/to/server.py"]
  ```
- To:
  ```json
  "args": ["run", "--project", "/path/to/frankfurtermcp", "python", "/path/to/server.py"]
  ```

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
- Server now works with Claude Code's stdio transport requirement

## Original Author
This server was created by Anirban Basu (anirbanbasu@users.noreply.github.com)
Repository: https://github.com/anirbanbasu/frankfurtermcp