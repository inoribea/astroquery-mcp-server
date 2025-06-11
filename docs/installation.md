# Installation Guide

## Prerequisites

### 1. Python Environment
- Python 3.8 or higher
- pip package manager

### 2. Install astroquery-cli
The server requires astroquery-cli to be installed and accessible:

```bash
pip install astroquery-cli
```

Verify installation:
```bash
astroquery-cli --help
```

### 3. Install MCP Server

#### From PyPI (when published)
```bash
pip install astroquery-mcp-server
```

#### From Source
```bash
git clone https://github.com/yourusername/astroquery-mcp-server.git
cd astroquery-mcp-server
pip install -e .
```

## Claude Desktop Setup

1. Locate your Claude Desktop configuration file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the server configuration:
```json
{
  "mcpServers": {
    "astroquery": {
      "command": "python",
      "args": ["-m", "astroquery_mcp"],
      "env": {
        "PATH": "/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

3. Restart Claude Desktop

## Verification

1. Start a new conversation in Claude Desktop
2. Ask: "What astronomical databases can you access?"
3. Claude should respond with information about available tools

## Troubleshooting

### Common Issues

1. **"astroquery-cli not found"**
   - Ensure astroquery-cli is installed: `pip install astroquery-cli`
   - Check PATH includes the installation directory

2. **"Permission denied"**
   - Ensure Python has execute permissions
   - Check file permissions on the server script

3. **"Server not responding"**
   - Restart Claude Desktop
   - Check the configuration file syntax
   - Verify all paths are correct
