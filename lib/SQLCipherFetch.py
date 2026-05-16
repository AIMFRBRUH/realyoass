import os
import types
import requests
import hashlib

def get_sql_cipher_key(fetch_url: str, gateway_url: str, bundle_version: str):
    """
    Retrieves the SQL Cipher key.
    Attempting the 'Pure' recipe: SHA256(BundleVersion)
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

    # 2. Local "Raw Key" Generation (Pure Version)
    try:
        if not bundle_version:
            return None

        # Just the bundle version, no salts.
        seed = bundle_version.encode('utf-8')
        raw_hex = hashlib.sha256(seed).hexdigest()
        
        # Return as Raw Hex Key
        return f"0x{raw_hex}"
        
    except Exception as e:
        print(f"SQL Cipher Error: {e}")
        return None
