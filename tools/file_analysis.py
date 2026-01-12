import subprocess
import json
import hashlib
import os
from typing import Dict, Optional, Literal

class FileAnalysisTool:
    """
    Analyzes file properties, extracts metadata, computes cryptographic hashes,
    and extracts printable strings from a given file.
    """
    description = "Analyzes file properties, extracts metadata, computes cryptographic hashes, and extracts printable strings from a given file."
    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Absolute path to the file to analyze."
            },
            "operation": {
                "type": "string",
                "description": "The type of analysis to perform.",
                "enum": ["info", "hashes", "strings"]
            },
            "hash_type": {
                "type": "string",
                "description": "Optional: For 'hashes' operation, the type of hash to compute ('md5', 'sha1', 'sha256', 'all'). Default is 'all'.",
                "enum": ["md5", "sha1", "sha256", "all"],
                "default": "all"
            }
        },
        "required": ["file_path", "operation"]
    }

    @staticmethod
    def execute(file_path: str, operation: Literal["info", "hashes", "strings"], 
                hash_type: Literal["md5", "sha1", "sha256", "all"] = "all") -> Dict:
        """
        Executes the specified file analysis operation.
        """
        try:
            if operation == "info":
                # Using 'file' command for basic info (Linux/macOS)
                # For Windows, more complex logic or external tool might be needed
                process = subprocess.run(["file", file_path], capture_output=True, text=True, timeout=10)
                return {"success": True, "operation": operation, "file_path": file_path, "result": process.stdout.strip()}
            
            elif operation == "hashes":
                hashes = {}
                with open(file_path, "rb") as f:
                    bytes_content = f.read()
                    if hash_type == "md5" or hash_type == "all":
                        hashes["md5"] = hashlib.md5(bytes_content).hexdigest()
                    if hash_type == "sha1" or hash_type == "all":
                        hashes["sha1"] = hashlib.sha1(bytes_content).hexdigest()
                    if hash_type == "sha256" or hash_type == "all":
                        hashes["sha256"] = hashlib.sha256(bytes_content).hexdigest()
                return {"success": True, "operation": operation, "file_path": file_path, "result": hashes}
            
            elif operation == "strings":
                # Using 'strings' command (Linux/macOS)
                process = subprocess.run(["strings", file_path], capture_output=True, text=True, timeout=60)
                return {"success": True, "operation": operation, "file_path": file_path, "result": process.stdout.splitlines()}
            
            else:
                return {"success": False, "error": "Unknown file analysis operation."}

        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {file_path}. Ensure 'file' and 'strings' commands are installed and in PATH on Linux/macOS. For Windows, these tools may not be available or require WSL/Cygwin."}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": f"Command failed: {e.cmd}, {e.stderr}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

if __name__ == '__main__':
    print("Testing FileAnalysisTool...")

    dummy_file_path = "./test_file.txt"
    try:
        # Create the dummy file BEFORE any calls to execute
        with open(dummy_file_path, "w") as f:
            f.write("This is a test file with some strings.\n")
            f.write("And some more data. Password: mysecret123\n")

        # Example 1: Get file info
        # This will likely fail on Windows if 'file' command is not installed
        print(json.dumps(FileAnalysisTool.execute(file_path=dummy_file_path, operation="info"), indent=2))

        # Example 2: Get all hashes
        print(json.dumps(FileAnalysisTool.execute(file_path=dummy_file_path, operation="hashes"), indent=2))

        # Example 3: Get SHA256 hash
        print(json.dumps(FileAnalysisTool.execute(file_path=dummy_file_path, operation="hashes", hash_type="sha256"), indent=2))

        # Example 4: Extract strings
        # This will likely fail on Windows if 'strings' command is not installed
        print(json.dumps(FileAnalysisTool.execute(file_path=dummy_file_path, operation="strings"), indent=2))

    finally:
        # Clean up dummy file using os.remove for cross-platform compatibility
        if os.path.exists(dummy_file_path):
            os.remove(dummy_file_path)
