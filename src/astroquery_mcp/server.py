#!/usr/bin/env python3
"""
Astroquery-CLI MCP Server
将整个astroquery-cli项目包装为MCP服务
"""

import asyncio
import json
import os # Added import for os module
import shutil # Added import for shutil module
import subprocess
import sys
from typing import Any, Dict, List, Optional
from pathlib import Path

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class AstroqueryMCPServer:
    def __init__(self):
        self.server = Server("astroquery-cli")
        self.astroquery_cli_path = self._find_astroquery_cli()
        self._setup_handlers()
        
    def _find_astroquery_cli(self) -> str:
        """查找aqc可执行文件路径"""
        # 尝试使用 shutil.which 来查找可执行文件
        aqc_path = shutil.which("aqc")
        
        if aqc_path:
            try:
                # 验证找到的路径是否确实是可执行文件
                result = subprocess.run([aqc_path, "--help"], 
                                      capture_output=True, text=True, timeout=5, env=os.environ)
                if result.returncode == 0:
                    return aqc_path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass # 如果找到的路径不可用，继续抛出错误
                
        # 如果 shutil.which 找不到，或者找到的路径不可用，则尝试硬编码路径
        hardcoded_path = str(Path.home() / ".local/bin/aqc")
        try:
            result = subprocess.run([hardcoded_path, "--help"], 
                                  capture_output=True, text=True, timeout=5, env=os.environ)
            if result.returncode == 0:
                return hardcoded_path
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
                
        raise RuntimeError(f"Cannot find aqc executable. Tried PATH and {hardcoded_path}")
    
    def _get_available_commands(self) -> Dict[str, Dict]:
        """动态获取所有可用的aqc命令和子命令"""
        try:
            # 明确传递 env=os.environ 来继承当前进程的PATH
            result = subprocess.run([self.astroquery_cli_path, "--help"], 
                                  capture_output=True, text=True, timeout=10, env=os.environ)
            
            commands = {}
            
            # 解析help输出，提取命令信息
            lines = result.stdout.split('\n')
            in_commands_section = False
            
            for line in lines:
                if 'Commands:' in line or 'Available commands:' in line:
                    in_commands_section = True
                    continue
                    
                if in_commands_section and line.strip():
                    if line.startswith('  ') and not line.startswith('    '):
                        # 这是一个命令行
                        parts = line.strip().split(None, 1)
                        if len(parts) >= 1:
                            cmd = parts[0]
                            description = parts[1] if len(parts) > 1 else "No description available"
                            commands[cmd] = {
                                "description": description,
                                "subcommands": self._get_subcommands(cmd)
                            }
                            
            return commands
            
        except Exception as e:
            print(f"Error getting commands: {e}", file=sys.stderr)
            return {}
    
    def _get_subcommands(self, command: str) -> Dict[str, str]:
        """获取特定命令的子命令"""
        try:
            # 明确传递 env=os.environ 来继承当前进程的PATH
            result = subprocess.run([self.astroquery_cli_path, command, "--help"], 
                                  capture_output=True, text=True, timeout=10, env=os.environ)
            
            subcommands = {}
            lines = result.stdout.split('\n')
            in_commands_section = False
            
            for line in lines:
                if 'Commands:' in line or 'Available commands:' in line:
                    in_commands_section = True
                    continue
                    
                if in_commands_section and line.strip():
                    if line.startswith('  ') and not line.startswith('    '):
                        parts = line.strip().split(None, 1)
                        if len(parts) >= 1:
                            subcmd = parts[0]
                            description = parts[1] if len(parts) > 1 else "No description available"
                            subcommands[subcmd] = description
                            
            return subcommands
            
        except Exception:
            return {}
    
    def _setup_handlers(self):
        """设置MCP处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """动态生成工具列表"""
            tools = []
            commands = self._get_available_commands()
            
            # 为每个主命令创建一个工具
            for cmd, cmd_info in commands.items():
                tools.append(Tool(
                    name=f"astroquery_{cmd}",
                    description=f"Execute aqc {cmd} command: {cmd_info['description']}",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "subcommand": {
                                "type": "string",
                                "description": f"Subcommand for {cmd}",
                                "enum": list(cmd_info['subcommands'].keys()) if cmd_info['subcommands'] else []
                            },
                            "arguments": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Additional arguments for the command"
                            },
                            "options": {
                                "type": "object",
                                "description": "Command options as key-value pairs",
                                "additionalProperties": {"type": "string"}
                            }
                        },
                        "required": []
                    }
                ))
            
            # 添加一个通用执行工具
            tools.append(Tool(
                name="astroquery_execute",
                description="Execute any aqc command with full control",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Full command to execute (without 'aqc' prefix)"
                        },
                        "timeout": {
                            "type": "number",
                            "description": "Command timeout in seconds (default: 30)",
                            "default": 30
                        }
                    },
                    "required": ["command"]
                }
            ))
            
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """处理工具调用"""
            try:
                if name == "astroquery_execute":
                    return await self._execute_generic_command(arguments)
                elif name.startswith("astroquery_"):
                    cmd = name.replace("astroquery_", "")
                    return await self._execute_specific_command(cmd, arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
                    
            except Exception as e:
                return [TextContent(
                    type="text", 
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    async def _execute_generic_command(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """执行通用命令"""
        command = arguments.get("command", "")
        timeout = arguments.get("timeout", 30)
        
        if not command:
            return [TextContent(type="text", text="No command provided")]
        
        # 构建完整命令
        full_command = [self.astroquery_cli_path] + command.split()
        
        try:
            result = await asyncio.create_subprocess_exec(
                *full_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ # 明确传递环境变量
            )
            
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=timeout)
            
            output_text = f"Command: {' '.join(full_command)}\n\n"
            
            if stdout:
                output_text += f"Output:\n{stdout.decode('utf-8')}\n\n"
            
            if stderr:
                output_text += f"Errors:\n{stderr.decode('utf-8')}\n\n"
                
            output_text += f"Return code: {result.returncode}"
            
            return [TextContent(type="text", text=output_text)]
            
        except asyncio.TimeoutError:
            return [TextContent(type="text", text=f"Command timed out after {timeout} seconds")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error executing command: {str(e)}")]
    
    async def _execute_specific_command(self, cmd: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """执行特定的astroquery命令"""
        subcommand = arguments.get("subcommand", "")
        args = arguments.get("arguments", [])
        options = arguments.get("options", {})
        
        # 构建命令
        command_parts = [self.astroquery_cli_path, cmd]
        
        if subcommand:
            command_parts.append(subcommand)
        
        # 添加选项
        for key, value in options.items():
            if key.startswith("--"):
                command_parts.extend([key, str(value)])
            else:
                command_parts.extend([f"--{key}", str(value)])
        
        # 添加参数
        command_parts.extend(str(arg) for arg in args)
        
        try:
            result = await asyncio.create_subprocess_exec(
                *command_parts,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=os.environ # 明确传递环境变量
            )
            
            stdout, stderr = await asyncio.wait_for(result.communicate(), timeout=30)
            
            output_text = f"Command: {' '.join(command_parts)}\n\n"
            
            if stdout:
                output_text += f"Output:\n{stdout.decode('utf-8')}\n\n"
            
            if stderr:
                output_text += f"Errors:\n{stderr.decode('utf-8')}\n\n"
                
            output_text += f"Return code: {result.returncode}"
            
            return [TextContent(type="text", text=output_text)]
            
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def run(self):
        """运行MCP服务器"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream, 
                write_stream, 
                InitializationOptions(
                    server_name="astroquery-cli",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None
                    )
                )
            )


async def main():
    """主函数"""
    try:
        server = AstroqueryMCPServer()
        await server.run()
    except Exception as e:
        print(f"Failed to start server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
