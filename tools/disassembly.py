import subprocess
import json
from typing import Dict, Optional, Literal

class DisassemblyTool:
    """
    Interacts with binary analysis tools (like 'strings', 'file', 'objdump', 'readelf')
    to extract information from binary files.
    """
    description = "Interacts with binary analysis tools to extract information such as strings, file format details, imported/exported symbols, or basic disassembled code from a specified binary file."
    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Absolute path to the binary file to analyze."
            },
            "operation": {
                "type": "string",
                "description": "The type of analysis to perform.",
                "enum": ["strings", "info", "symbols", "disassemble"]
            },
            "section": {
                "type": "string",
                "description": "Optional: For 'disassemble' operation, a specific section to disassemble (e.g., .text)."
            }
        },
        "required": ["file_path", "operation"]
    }

    @staticmethod
    def execute(file_path: str, operation: Literal["strings", "info", "symbols", "disassemble"],
                section: Optional[str] = None) -> Dict:
        """
        Executes the specified binary analysis operation.
        """
        try:
            command = []
            if operation == "strings":
                command = ["strings", file_path]
            elif operation == "info":
                # Try 'file' command first, then 'readelf'/'objdump' if more detail is needed
                command = ["file", file_path]
            elif operation == "symbols":
                # For Linux/ELF: readelf -s, For Windows/PE: objdump -x or specific PE tools
                command = ["readelf", "-s", file_path] # Assuming Linux for now
            elif operation == "disassemble":
                if not section:
                    # Default to .text section if not specified, or try to disassemble whole file
                    command = ["objdump", "-d", file_path] # Assuming Linux for now
                else:
                    command = ["objdump", "-d", "--section=", section, file_path]
            else:
                return {"success": False, "error": "Unknown disassembly operation."}

            if not command:
                 return {"success": False, "error": "No command formulated for the given operation."}

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120 # Increased timeout for potentially long binary ops
            )

            if process.returncode == 0:
                return {"success": True, "operation": operation, "file_path": file_path, "result": process.stdout}
            else:
                return {"success": False, "operation": operation, "file_path": file_path,
                        "error": process.stderr, "exit_code": process.returncode}

        except FileNotFoundError:
            return {"success": False, "operation": operation, "file_path": file_path,
                    "error": "Binary analysis tool not found (e.g., strings, file, readelf, objdump). Make sure they are installed and in PATH."}
        except subprocess.TimeoutExpired:
            return {"success": False, "operation": operation, "file_path": file_path,
                    "error": "Command timed out during binary analysis.", "stdout": process.stdout, "stderr": process.stderr}
        except Exception as e:
            return {"success": False, "operation": operation, "file_path": file_path, "error": str(e)}

if __name__ == '__main__':
    print("Testing DisassemblyTool...")
    # Note: These tests require 'strings', 'file', 'readelf', 'objdump' to be installed on a Linux-like system.
    # For Windows, you might need Cygwin/WSL or specific PE tools like 'dumpbin.exe'.

    # Create a dummy executable for testing (e.g., a simple C program compiled)
    # echo 'int main() { return 0; }' > test.c && gcc test.c -o test_bin

    dummy_bin_path = "./test_bin" # Replace with actual path to a binary for testing

    # Example 1: Extract strings
    print(json.dumps(DisassemblyTool.execute(file_path=dummy_bin_path, operation="strings"), indent=2))

    # Example 2: Get file info
    print(json.dumps(DisassemblyTool.execute(file_path=dummy_bin_path, operation="info"), indent=2))

    # Example 3: Get symbols (ELF specific)
    print(json.dumps(DisassemblyTool.execute(file_path=dummy_bin_path, operation="symbols"), indent=2))

    # Example 4: Disassemble .text section (ELF specific)
    print(json.dumps(DisassemblyTool.execute(file_path=dummy_bin_path, operation="disassemble", section=".text"), indent=2))

    # Example 5: Non-existent file
    print(json.dumps(DisassemblyTool.execute(file_path="/tmp/non_existent_binary", operation="info"), indent=2))
