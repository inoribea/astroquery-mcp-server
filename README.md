# Astroquery MCP Server

A Model Context Protocol (MCP) server that provides access to astronomical data through the astroquery-cli tool, enabling AI assistants to perform professional astronomical queries.

## 🌟 Features

- **Complete astroquery-cli integration**: Access all astronomical databases (SIMBAD, Gaia, VizieR, MAST, NED, IRSA, ALMA)
- **Dynamic command discovery**: Automatically detects available commands and subcommands
- **Zero maintenance**: Updates automatically when astroquery-cli is updated
- **Async execution**: Supports long-running queries with timeout protection
- **Rich output formatting**: Preserves all output formatting and error information

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- astroquery-cli installed and accessible in PATH

### Installation
```bash
# Install astroquery-cli if not already installed
pip install astroquery-cli

# Install the MCP server
pip install -e .
```

### Claude Desktop Configuration
Add to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

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

## 📚 Usage Examples

Once connected, you can ask Claude to perform astronomical queries:

- "Query SIMBAD for information about the Andromeda Galaxy M31"
- "Search for stars in Gaia catalog near coordinates RA=12h30m, Dec=+41°16'"
- "Cross-match my observation data with the 2MASS catalog"
- "Get ALMA archive data for NGC 1068"

## 🛠️ Available Tools

The server provides these MCP tools:

- `astroquery_simbad`: Query the SIMBAD astronomical database
- `astroquery_gaia`: Search the Gaia star catalog
- `astroquery_vizier`: Query VizieR catalog service
- `astroquery_mast`: Access MAST (Mikulski Archive for Space Telescopes)
- `astroquery_ned`: Query NASA/IPAC Extragalactic Database
- `astroquery_irsa`: Access IRSA (Infrared Science Archive)
- `astroquery_alma`: Query ALMA (Atacama Large Millimeter Array) archive
- `astroquery_execute`: Execute any astroquery-cli command directly

## 🔧 Development

### Local Development Setup
```bash
git clone https://github.com/yourusername/astroquery-mcp-server.git
cd astroquery-mcp-server
pip install -e .
```

### Running the Server
```bash
python -m astroquery_mcp
```

## 📖 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Guide](docs/usage.md)
- [Examples](docs/examples.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [astroquery-cli](https://github.com/inoribea/astroquery-cli) - The underlying astronomical query tool
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol that makes this integration possible

## ⭐ Support

If you find this project useful, please consider giving it a star on GitHub!
