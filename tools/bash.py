"""
Bash Tool - Execute shell commands
"""
import subprocess
import os
from typing import Dict, Any


class BashTool:
    """Tool for executing bash/shell commands"""

    name = "bash"
    description = "Execute shell commands in the system"

    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The shell command to execute"
            },
            "cwd": {
                "type": "string",
                "description": "Working directory (optional, defaults to current)",
                "default": None
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout in seconds (default: 120)",
                "default": 120
            }
        },
        "required": ["command"]
    }

    @staticmethod
    def execute(command: str, cwd: str = None, timeout: int = 120) -> Dict[str, Any]:
        """
        Execute a shell command

        Args:
            command: Command to execute
            cwd: Working directory
            timeout: Timeout in seconds

        Returns:
            Dict with success status, output, and error
        """
        try:
            # Determine shell based on OS
            if os.name == 'nt':  # Windows
                shell_cmd = ['cmd', '/c', command]
                use_shell = False
            else:  # Unix/Linux/Mac
                shell_cmd = command
                use_shell = True

            # Execute command
            result = subprocess.run(
                shell_cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=use_shell
            )

            return {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
                "command": command
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Working directory not found: {cwd}",
                "command": command
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error executing command: {str(e)}",
                "command": command
            }
