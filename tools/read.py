"""
Read Tool - Read files from the filesystem
"""
import os
from typing import Dict, Any, Optional


class ReadTool:
    """Tool for reading files with line numbers (like cat -n)"""

    name = "read"
    description = "Read a file from the filesystem with line numbers"

    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Absolute path to the file to read"
            },
            "offset": {
                "type": "integer",
                "description": "Line number to start reading from (optional)",
                "default": 0
            },
            "limit": {
                "type": "integer",
                "description": "Number of lines to read (optional, 0 = all)",
                "default": 0
            }
        },
        "required": ["file_path"]
    }

    @staticmethod
    def execute(file_path: str, offset: int = 0, limit: int = 0) -> Dict[str, Any]:
        """
        Read a file and return its contents with line numbers

        Args:
            file_path: Path to the file
            offset: Starting line number (0-indexed)
            limit: Maximum number of lines to read (0 = all)

        Returns:
            Dict with success status and content or error message
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }

            if not os.path.isfile(file_path):
                return {
                    "success": False,
                    "error": f"Not a file: {file_path}"
                }

            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Apply offset and limit
            start = offset
            end = len(lines) if limit == 0 else min(start + limit, len(lines))
            selected_lines = lines[start:end]

            # Format with line numbers (1-indexed for display)
            formatted_lines = []
            for i, line in enumerate(selected_lines, start=start + 1):
                # Remove trailing newline for display, add line number
                formatted_lines.append(f"{i:6d}\t{line.rstrip()}")

            content = "\n".join(formatted_lines)

            return {
                "success": True,
                "file_path": file_path,
                "total_lines": len(lines),
                "lines_read": len(selected_lines),
                "content": content
            }

        except PermissionError:
            return {
                "success": False,
                "error": f"Permission denied: {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading file: {str(e)}"
            }
