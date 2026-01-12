import requests
import json
from typing import Dict, Any, Optional

class WebExploitTool:
    """
    Interacts with web applications by sending HTTP requests and parsing responses.
    Useful for web reconnaissance, vulnerability testing, and simulating web interactions.
    """
    description = "Performs HTTP requests (GET, POST, etc.) to interact with web applications and retrieve content."
    parameters = {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The target URL."
            },
            "method": {
                "type": "string",
                "description": "HTTP method (GET, POST, PUT, DELETE, etc.). Defaults to GET.",
                "enum": ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
                "default": "GET"
            },
            "headers": {
                "type": "object",
                "description": "JSON string of HTTP headers.",
                "additionalProperties": {"type": "string"}
            },
            "params": {
                "type": "object",
                "description": "JSON string of URL parameters (for GET requests).",
                "additionalProperties": {"type": "string"}
            },
            "data": {
                "type": "object",
                "description": "JSON string of request body data (for POST/PUT requests, form-encoded).",
                "additionalProperties": {"type": "string"}
            },
            "json": {
                "type": "object",
                "description": "JSON string of request body data (for POST/PUT requests, JSON-encoded).",
                "additionalProperties": {"type": "string"}
            },
            "timeout": {
                "type": "integer",
                "description": "Timeout for the request in seconds (default: 30).",
                "default": 30
            },
            "verify_ssl": {
                "type": "boolean",
                "description": "Whether to verify SSL certificates (default: True).",
                "default": True
            }
        },
        "required": ["url"]
    }

    @staticmethod
    def execute(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, 
                params: Optional[Dict[str, str]] = None, data: Optional[Dict[str, str]] = None,
                json_data: Optional[Dict[str, Any]] = None, timeout: int = 30, verify_ssl: bool = True) -> Dict:
        """
        Sends an HTTP request to the specified URL and returns the response details.
        """
        try:
            response = requests.request(
                method.upper(),
                url,
                headers=headers,
                params=params,
                data=data,
                json=json_data, # Renamed to json_data to avoid conflict with method parameter
                timeout=timeout,
                verify=verify_ssl
            )
            return {
                "success": True,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "content": response.text,
                "elapsed_time": response.elapsed.total_seconds()
            }
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": f"Request to {url} timed out after {timeout} seconds."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"An unexpected error occurred: {str(e)}"
            }

if __name__ == '__main__':
    print("Testing WebExploitTool...")

    # Example 1: Simple GET request
    get_result = WebExploitTool.execute(url="https://httpbin.org/get", params={"key": "value"})
    print(json.dumps(get_result, indent=2))

    # Example 2: POST request with JSON data
    post_result = WebExploitTool.execute(
        url="https://httpbin.org/post", 
        method="POST", 
        json_data={
            "user": "hacker", 
            "password": "secure_pass"
            },
        headers={
            "Content-Type": "application/json",
            "User-Agent": "HacxGPT-Agent"
        }
    )
    print(json.dumps(post_result, indent=2))

    # Example 3: Invalid URL
    invalid_url_result = WebExploitTool.execute(url="http://invalid.url.local")
    print(json.dumps(invalid_url_result, indent=2))

    # Example 4: Timeout test
    timeout_test = WebExploitTool.execute(url="http://google.com:81", timeout=1)
    print(json.dumps(timeout_test, indent=2))
