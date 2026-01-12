import subprocess
import json
from typing import Optional, Dict

class NetworkScanTool:
    """
    Executes network scanning commands (e.g., nmap) to gather information about target hosts.
    This tool is designed for reconnaissance and active information gathering.
    """
    description = "Executes network scanning commands (e.g., nmap) to gather information about target hosts."
    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The network scanning command to execute (e.g., 'nmap -sV example.com', 'ping 192.168.1.1')."
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout for the command execution in seconds (default: 60).",
                "default": 60
            }
        },
        "required": ["command"]
    }

    @staticmethod
    def execute(command: str, timeout: int = 60) -> Dict:
        """
        Executes a network scanning command and returns its stdout, stderr, and exit code.
        """
        try:
            process = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": True,
                "command": command,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "exit_code": process.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "command": command,
                "error": f"Command timed out after {timeout} seconds.",
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "command": command,
                "error": str(e),
                "stdout": "",
                "stderr": "",
                "exit_code": -1
            }

if __name__ == '__main__':
    # Example usage for testing
    print("Testing NetworkScanTool...")
    # Example 1: Nmap scan (requires nmap to be installed)
    nmap_result = NetworkScanTool.execute(command="nmap -p 80,443 scanme.nmap.org")
    print(json.dumps(nmap_result, indent=2))

    # Example 2: Ping command
    ping_result = NetworkScanTool.execute(command="ping -c 4 google.com")
    print(json.dumps(ping_result, indent=2))

    # Example 3: Invalid command
    invalid_result = NetworkScanTool.execute(command="thisisnotacommand")
    print(json.dumps(invalid_result, indent=2))

    # Example 4: Timeout
    timeout_result = NetworkScanTool.execute(command="sleep 5", timeout=2)
    print(json.dumps(timeout_result, indent=2))
