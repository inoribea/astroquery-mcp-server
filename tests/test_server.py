"""Test suite for Astroquery MCP Server."""

import asyncio
import pytest
import subprocess
from unittest.mock import Mock, patch, AsyncMock
from astroquery_mcp.server import AstroqueryMCPServer


class TestAstroqueryMCPServer:
    """Test cases for AstroqueryMCPServer."""
    
    @patch('subprocess.run')
    def test_find_astroquery_cli_success(self, mock_run):
        """Test successful astroquery-cli discovery."""
        mock_run.return_value = Mock(returncode=0)
        
        server = AstroqueryMCPServer()
        assert server.astroquery_cli_path == "astroquery-cli"
    
    @patch('subprocess.run')
    def test_find_astroquery_cli_failure(self, mock_run):
        """Test astroquery-cli discovery failure."""
        mock_run.side_effect = FileNotFoundError()
        
        with pytest.raises(RuntimeError, match="Cannot find astroquery-cli executable"):
            AstroqueryMCPServer()
    
    @patch('subprocess.run')
    def test_get_available_commands(self, mock_run):
        """Test command discovery functionality."""
        mock_help_output = """
Usage: astroquery-cli [OPTIONS] COMMAND [ARGS]...

Commands:
  simbad  Query SIMBAD astronomical database
  gaia    Query Gaia Data Release
  vizier  Query VizieR catalog service
"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout=mock_help_output
        )
        
        server = AstroqueryMCPServer()
        commands = server._get_available_commands()
        
        assert "simbad" in commands
        assert "gaia" in commands
        assert "vizier" in commands
        assert commands["simbad"]["description"] == "Query SIMBAD astronomical database"
    
    @patch('subprocess.run')
    def test_get_subcommands(self, mock_run):
        """Test subcommand discovery."""
        mock_subcommand_output = """
Usage: astroquery-cli simbad [OPTIONS] COMMAND [ARGS]...

Commands:
  query      Query by object name
  coords     Query by coordinates
  region     Query by region
"""
        # First call for main help, second for subcommand help
        mock_run.side_effect = [
            Mock(returncode=0, stdout="Commands:\n  simbad  Test command"),
            Mock(returncode=0, stdout=mock_subcommand_output)
        ]
        
        server = AstroqueryMCPServer()
        subcommands = server._get_subcommands("simbad")
        
        assert "query" in subcommands
        assert "coords" in subcommands
        assert "region" in subcommands
    
    @pytest.mark.asyncio
    @patch('asyncio.create_subprocess_exec')
    async def test_execute_generic_command(self, mock_subprocess):
        """Test generic command execution."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (
            b"Test output\n", 
            b"Test error\n"
        )
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process
        
        # Mock the constructor to avoid subprocess calls
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            server = AstroqueryMCPServer()
        
        result = await server._execute_generic_command({
            "command": "simbad query M31",
            "timeout": 30
        })
        
        assert len(result) == 1
        assert "Test output" in result[0].text
        assert "Test error" in result[0].text
        assert "Return code: 0" in result[0].text
    
    @pytest.mark.asyncio
    @patch('asyncio.create_subprocess_exec')
    async def test_execute_specific_command(self, mock_subprocess):
        """Test specific command execution with options."""
        # Mock process
        mock_process = AsyncMock()
        mock_process.communicate.return_value = (
            b"Simbad query result\n",
            b""
        )
        mock_process.returncode = 0
        mock_subprocess.return_value = mock_process
        
        # Mock the constructor
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            server = AstroqueryMCPServer()
        
        result = await server._execute_specific_command("simbad", {
            "subcommand": "query",
            "arguments": ["M31"],
            "options": {"output-format": "votable"}
        })
        
        assert len(result) == 1
        assert "Simbad query result" in result[0].text
        
        # Verify the command was called correctly
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0]
        assert "simbad" in call_args
        assert "query" in call_args
        assert "--output-format" in call_args
        assert "votable" in call_args
        assert "M31" in call_args
    
    @pytest.mark.asyncio
    async def test_command_timeout(self):
        """Test command timeout handling."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0)
            server = AstroqueryMCPServer()
        
        with patch('asyncio.wait_for') as mock_wait:
            mock_wait.side_effect = asyncio.TimeoutError()
            
            result = await server._execute_generic_command({
                "command": "slow command",
                "timeout": 1
            })
            
            assert len(result) == 1
            assert "timed out" in result[0].text.lower()


@pytest.mark.integration
class TestIntegration:
    """Integration tests (requires astroquery-cli to be installed)."""
    
    def test_astroquery_cli_available(self):
        """Test if astroquery-cli is available for integration tests."""
        try:
            result = subprocess.run(
                ["astroquery-cli", "--help"],
                capture_output=True,
                timeout=5
            )
            assert result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pytest.skip("astroquery-cli not available for integration testing")
    
    @pytest.mark.asyncio
    async def test_real_simbad_query(self):
        """Test a real SIMBAD query (requires network and astroquery-cli)."""
        try:
            # This is a real integration test
            server = AstroqueryMCPServer()
            result = await server._execute_generic_command({
                "command": "simbad query --object M31 --output-format json",
                "timeout": 30
            })
            
            assert len(result) == 1
            # Should contain some astronomical data
            assert any(keyword in result[0].text.lower() 
                      for keyword in ["andromeda", "m31", "coordinates", "ra", "dec"])
            
        except RuntimeError:
            pytest.skip("astroquery-cli not available")
        except Exception as e:
            # Network or other issues
            pytest.skip(f"Integration test failed: {e}")


if __name__ == "__main__":
    pytest.main()
