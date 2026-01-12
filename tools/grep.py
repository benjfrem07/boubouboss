"""
Grep Tool - Search for patterns in files
"""
import os
import re
from typing import Dict, Any, List
import glob as glob_module


class GrepTool:
    """Tool for searching text patterns in files (like ripgrep)"""

    name = "grep"
    description = "Search for text patterns in files"

    parameters = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Regex pattern to search for"
            },
            "path": {
                "type": "string",
                "description": "File or directory to search in (default: current directory)",
                "default": "."
            },
            "glob": {
                "type": "string",
                "description": "Glob pattern to filter files (e.g., '*.py')",
                "default": None
            },
            "case_insensitive": {
                "type": "boolean",
                "description": "Case insensitive search",
                "default": False
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of matches to return (0 = no limit)",
                "default": 50
            }
        },
        "required": ["pattern"]
    }

    @staticmethod
    def execute(pattern: str, path: str = ".", glob: str = None, case_insensitive: bool = False, limit: int = 50) -> Dict[str, Any]:
        """
        Search for pattern in files

        Args:
            pattern: Regex pattern to search
            path: File or directory to search
            glob: Optional glob pattern to filter files
            case_insensitive: Case insensitive search
            limit: Maximum results

        Returns:
            Dict with success status and matches
        """
        try:
            # Compile regex
            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            # Get list of files to search
            files_to_search = []

            if os.path.isfile(path):
                files_to_search = [path]
            elif os.path.isdir(path):
                # Find all files in directory
                if glob:
                    pattern_path = os.path.join(path, "**", glob)
                    files_to_search = glob_module.glob(pattern_path, recursive=True)
                else:
                    # Search all files
                    for root, dirs, files in os.walk(path):
                        # Skip common ignore patterns
                        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv', 'venv']]
                        for file in files:
                            files_to_search.append(os.path.join(root, file))

                # Keep only files
                files_to_search = [f for f in files_to_search if os.path.isfile(f)]
            else:
                return {
                    "success": False,
                    "error": f"Path not found: {path}"
                }

            # Search in files
            matches = []
            files_with_matches = 0

            for file_path in files_to_search:
                if limit > 0 and len(matches) >= limit:
                    break

                try:
                    # Try to read as text file
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_matches = []
                        for line_num, line in enumerate(f, 1):
                            if regex.search(line):
                                file_matches.append({
                                    "line": line_num,
                                    "content": line.rstrip()
                                })

                                if limit > 0 and len(matches) + len(file_matches) >= limit:
                                    break

                        if file_matches:
                            files_with_matches += 1
                            matches.extend([{
                                "file": file_path,
                                **match
                            } for match in file_matches])

                except (UnicodeDecodeError, PermissionError):
                    # Skip binary files or files without permission
                    continue

            return {
                "success": True,
                "pattern": pattern,
                "files_searched": len(files_to_search),
                "files_with_matches": files_with_matches,
                "total_matches": len(matches),
                "matches": matches[:limit] if limit > 0 else matches
            }

        except re.error as e:
            return {
                "success": False,
                "error": f"Invalid regex pattern: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error searching files: {str(e)}"
            }
