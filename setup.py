#!/usr/bin/env python3
"""
项目设置脚本 - 快速创建完整的项目结构
"""

import os
import sys
from pathlib import Path


def create_project_structure():
    """创建完整的项目目录结构"""
    
    # 项目根目录
    project_root = Path("astroquery-mcp-server")
    
    # 创建目录结构
    directories = [
        project_root,
        project_root / "src" / "astroquery_mcp",
        project_root / "docs", 
        project_root / "examples",
        project_root / "tests",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # 文件内容映射
    files_content = {
        # README.md
        project_root / "README.md": """# Astroquery MCP Server

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
""",

        # pyproject.toml
        project_root / "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "astroquery-mcp-server"
version = "1.0.0"
description = "MCP server for astroquery-cli astronomical queries"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Astronomy",
]
keywords = ["astronomy", "mcp", "astroquery", "ai", "claude"]
requires-python = ">=3.8"
dependencies = [
    "mcp>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    "black",
    "flake8",
    "mypy",
]

[project.urls]
Homepage = "https://github.com/yourusername/astroquery-mcp-server"
Repository = "https://github.com/yourusername/astroquery-mcp-server"
Documentation = "https://github.com/yourusername/astroquery-mcp-server/docs"
"Bug Tracker" = "https://github.com/yourusername/astroquery-mcp-server/issues"

[project.scripts]
astroquery-mcp-server = "astroquery_mcp:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py38']

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
""",

        # requirements.txt
        project_root / "requirements.txt": """mcp>=1.0.0
""",

        # .gitignore
        project_root / ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# macOS
.DS_Store

# Logs
*.log
""",

        # LICENSE
        project_root / "LICENSE": """MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",

        # src/astroquery_mcp/__init__.py
        project_root / "src" / "astroquery_mcp" / "__init__.py": '''"""Astroquery MCP Server - Astronomical query server for Model Context Protocol."""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .server import AstroqueryMCPServer

__all__ = ["AstroqueryMCPServer"]
''',

        # src/astroquery_mcp/__main__.py
        project_root / "src" / "astroquery_mcp" / "__main__.py": '''"""Entry point for running the astroquery MCP server."""

import asyncio
from .server import main

if __name__ == "__main__":
    asyncio.run(main())
''',

        # examples/claude_desktop_config.json
        project_root / "examples" / "claude_desktop_config.json": """{
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
""",

        # tests/__init__.py
        project_root / "tests" / "__init__.py": "",
    }
    
    # 创建所有文件
    for file_path, content in files_content.items():
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created file: {file_path}")
    
    print(f"\n🎉 项目结构创建完成！")
    print(f"📁 项目位置: {project_root.absolute()}")
    print(f"\n📋 下一步操作:")
    print(f"1. cd {project_root}")
    print(f"2. 将核心服务器代码复制到 src/astroquery_mcp/server.py")
    print(f"3. 将测试代码复制到 tests/test_server.py")
    print(f"4. git init && git add . && git commit -m 'Initial commit'")
    print(f"5. 在GitHub上创建仓库并推送代码")
    
    return project_root


def main():
    """主函数"""
    print("🚀 开始创建 Astroquery MCP Server 项目...")
    
    try:
        project_path = create_project_structure()
        
        print(f"\n✅ 项目创建成功！")
        print(f"🎯 记住还需要:")
        print(f"   - 复制服务器代码到 src/astroquery_mcp/server.py")
        print(f"   - 复制测试代码到 tests/test_server.py") 
        print(f"   - 修改作者信息和GitHub用户名")
        print(f"   - 初始化Git仓库")
        
    except Exception as e:
        print(f"❌ 创建项目时出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
