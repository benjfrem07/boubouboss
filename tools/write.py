"""
Write Tool - Write files to the filesystem
"""
import os
from typing import Dict, Any


class WriteTool:
    """Tool for writing/creating files"""

    name = "write"
    description = "Write content to a file (creates or overwrites)"

    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Absolute path to the file to write"
            },
            "content": {
                "type": "string",
                "description": "Content to write to the file"
            }
        },
        "required": ["file_path", "content"]
    }

    @staticmethod
    def execute(file_path: str, content: str) -> Dict[str, Any]:
        """
        Write content to a file

        Args:
            file_path: Path to the file
            content: Content to write

        Returns:
            Dict with success status and info or error message
        """
        try:
            # Create directories if they don't exist
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            # Write the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Get file info
            file_size = os.path.getsize(file_path)
            line_count = content.count('\n') + (1 if content and not content.endswith('\n') else 0)

            return {
                "success": True,
                "file_path": file_path,
                "bytes_written": file_size,
                "lines_written": line_count,
                "message": f"Successfully wrote {line_count} lines to {file_path}"
            }

        except PermissionError:
            return {
                "success": False,
                "error": f"Permission denied: {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error writing file: {str(e)}"
            }
