"""
Edit Tool - Perform exact string replacements in files
"""
import os
from typing import Dict, Any


class EditTool:
    """Tool for editing files with exact string replacement"""

    name = "edit"
    description = "Replace exact strings in files"

    parameters = {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Absolute path to the file to edit"
            },
            "old_string": {
                "type": "string",
                "description": "Exact string to find and replace"
            },
            "new_string": {
                "type": "string",
                "description": "String to replace with"
            },
            "replace_all": {
                "type": "boolean",
                "description": "Replace all occurrences (default: False, only first)",
                "default": False
            }
        },
        "required": ["file_path", "old_string", "new_string"]
    }

    @staticmethod
    def execute(file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> Dict[str, Any]:
        """
        Replace text in a file

        Args:
            file_path: Path to the file
            old_string: Text to find
            new_string: Text to replace with
            replace_all: Replace all occurrences or just first

        Returns:
            Dict with success status and info or error message
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }

            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Check if old_string exists
            if old_string not in content:
                return {
                    "success": False,
                    "error": f"String not found in file: {old_string[:50]}..."
                }

            # Count occurrences
            count = content.count(old_string)

            # Perform replacement
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = count
            else:
                # Replace only first occurrence
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1

                # Check if the replacement would be unique
                if count > 1:
                    return {
                        "success": False,
                        "error": f"String appears {count} times in file. Use replace_all=true or provide a more unique string."
                    }

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return {
                "success": True,
                "file_path": file_path,
                "replacements": replacements,
                "message": f"Successfully replaced {replacements} occurrence(s)"
            }

        except PermissionError:
            return {
                "success": False,
                "error": f"Permission denied: {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error editing file: {str(e)}"
            }
