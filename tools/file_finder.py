"""
Glob Tool - Find files by pattern
"""
import os
import glob as glob_module
from typing import Dict, Any, List


class FileFinderTool:
    """Tool for finding files using glob patterns"""

    name = "glob"
    description = "Find files matching a glob pattern (e.g., **/*.py)"

    parameters = {
        "type": "object",
        "properties": {
            "pattern": {
                "type": "string",
                "description": "Glob pattern to match files (e.g., '**/*.py', 'src/**/*.ts')"
            },
            "path": {
                "type": "string",
                "description": "Directory to search in (default: current directory)",
                "default": "."
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return (0 = no limit)",
                "default": 100
            }
        },
        "required": ["pattern"]
    }

    @staticmethod
    def execute(pattern: str, path: str = ".", limit: int = 100) -> Dict[str, Any]:
        """
        Find files matching a pattern

        Args:
            pattern: Glob pattern
            path: Base directory to search
            limit: Maximum results

        Returns:
            Dict with success status and matching files
        """
        try:
            if not os.path.exists(path):
                return {
                    "success": False,
                    "error": f"Path not found: {path}"
                }

            # Change to the search directory
            original_dir = os.getcwd()
            os.chdir(path)

            # Use glob to find matching files
            matches = glob_module.glob(pattern, recursive=True)

            # Convert to absolute paths
            matches = [os.path.abspath(m) for m in matches]

            # Filter out directories, keep only files
            matches = [m for m in matches if os.path.isfile(m)]

            # Sort by modification time (most recent first)
            matches.sort(key=lambda x: os.path.getmtime(x), reverse=True)

            # Apply limit
            total = len(matches)
            if limit > 0 and len(matches) > limit:
                matches = matches[:limit]

            # Change back to original directory
            os.chdir(original_dir)

            return {
                "success": True,
                "pattern": pattern,
                "total_found": total,
                "returned": len(matches),
                "matches": matches
            }

        except Exception as e:
            # Make sure to restore directory
            try:
                os.chdir(original_dir)
            except:
                pass

            return {
                "success": False,
                "error": f"Error finding files: {str(e)}"
            }
