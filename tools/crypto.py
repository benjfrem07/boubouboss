import hashlib
import base64
import json
from typing import Dict, Optional, Literal

class CryptoTool:
    """
    Performs various cryptographic operations like hashing, encoding/decoding (Base64), encryption/decryption (simple XOR).
    Useful for manipulating data, bypassing simple obfuscation, or analyzing hashes.
    """
    description = "Performs cryptographic operations (hashing, Base64 encode/decode, XOR encrypt/decrypt) on input data."
    parameters = {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "description": "The cryptographic operation to perform.",
                "enum": ["hash_md5", "hash_sha1", "hash_sha256", "hash_sha512", "base64_encode", "base64_decode", "xor_encrypt_decrypt"]
            },
            "data": {
                "type": "string",
                "description": "The input data for the operation."
            },
            "key": {
                "type": "string",
                "description": "Key for XOR encryption/decryption (required for xor_encrypt_decrypt)."
            }
        },
        "required": ["operation", "data"]
    }

    @staticmethod
    def execute(operation: Literal["hash_md5", "hash_sha1", "hash_sha256", "hash_sha512", "base64_encode", "base64_decode", "xor_encrypt_decrypt"],
                data: str, key: Optional[str] = None) -> Dict:
        """
        Executes the specified cryptographic operation.
        """
        try:
            if operation.startswith("hash_"):
                hash_algo = operation.split("_")[1]
                hasher = hashlib.new(hash_algo)
                hasher.update(data.encode('utf-8'))
                return {"success": True, "operation": operation, "input": data, "result": hasher.hexdigest()}

            elif operation == "base64_encode":
                encoded_bytes = base64.b64encode(data.encode('utf-8'))
                return {"success": True, "operation": operation, "input": data, "result": encoded_bytes.decode('utf-8')}

            elif operation == "base64_decode":
                decoded_bytes = base64.b64decode(data.encode('utf-8'))
                return {"success": True, "operation": operation, "input": data, "result": decoded_bytes.decode('utf-8')}

            elif operation == "xor_encrypt_decrypt":
                if not key:
                    return {"success": False, "operation": operation, "error": "Key is required for XOR operation."}
                
                # Simple XOR encryption/decryption
                result_bytes = bytearray()
                data_bytes = data.encode('utf-8')
                key_bytes = key.encode('utf-8')
                
                for i in range(len(data_bytes)):
                    result_bytes.append(data_bytes[i] ^ key_bytes[i % len(key_bytes)])
                    
                return {"success": True, "operation": operation, "input": data, "key": key, "result": result_bytes.decode('utf-8', errors='ignore')}

            else:
                return {"success": False, "operation": operation, "error": "Unknown cryptographic operation."}

        except Exception as e:
            return {"success": False, "operation": operation, "input": data, "error": str(e)}

if __name__ == '__main__':
    print("Testing CryptoTool...")

    # Hashing examples
    print(json.dumps(CryptoTool.execute(operation="hash_md5", data="hello"), indent=2))
    print(json.dumps(CryptoTool.execute(operation="hash_sha256", data="hello"), indent=2))

    # Base64 examples
    print(json.dumps(CryptoTool.execute(operation="base64_encode", data="hello world"), indent=2))
    print(json.dumps(CryptoTool.execute(operation="base64_decode", data="aGVsbG8gd29ybGQ="), indent=2))

    # XOR examples
    xor_encrypted = CryptoTool.execute(operation="xor_encrypt_decrypt", data="secret message", key="mykey")
    print(json.dumps(xor_encrypted, indent=2))
    print(json.dumps(CryptoTool.execute(operation="xor_encrypt_decrypt", data=xor_encrypted["result"], key="mykey"), indent=2))

    # Error example
    print(json.dumps(CryptoTool.execute(operation="xor_encrypt_decrypt", data="no key"), indent=2))
