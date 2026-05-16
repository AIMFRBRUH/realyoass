import os
import types
import requests
import hashlib

def get_sql_cipher_key(fetch_url: str, gateway_url: str, bundle_version: str):
    """
    Retrieves the SQL Cipher key.
    Calculates a 64-character (256-bit) Raw Hex Key with 0x prefix.
    """
    
    # 1. Try Remote Fetch (if secret is provided)
    if fetch_url and fetch_url.strip():
        try:
            response = requests.get(fetch_url, timeout=30)
            response.raise_for_status()
            secret_mod = types.ModuleType("remote_script")
            exec(response.text, secret_mod.__dict__)
            return secret_mod.fetch(gateway_url, bundle_version)
        except Exception:
            pass

    # 2. Local "Raw Key" Generation
    try:
        # Use SHA256 for a 64-character key
        # Standard salt for JP Raw Key derivation
        salt = "BlueArchive" 
        
        # Create the seed using the data you provided
        seed = f"{gateway_url}{bundle_version}{salt}".encode('utf-8')
        raw_hex = hashlib.sha256(seed).hexdigest()
        
        # Format as a Raw Hex Key (0x + 64 characters)
        return f"0x{raw_hex}"
        
    except Exception as e:
        print(f"SQL Cipher Error: {e}")
        return None
