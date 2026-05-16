import os
import types
import requests
import hashlib

def get_sql_cipher_key(fetch_url: str, gateway_url: str, bundle_version: str):
    """
    Retrieves the SQL Cipher key.
    Uses the 'Bundle Only' recipe: SHA256(Salt + BundleVersion)
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

    # 2. Local "Raw Key" Generation (Most common BA JP method)
    try:
        if not bundle_version:
            return None

        # Many BA tools use Salt + BundleVersion (or vice-versa)
        salt = "BlueArchive" 
        
        # We'll try Salt + BundleVersion as it's the most standard 'recipe'
        seed = f"{salt}{bundle_version}".encode('utf-8')
        raw_hex = hashlib.sha256(seed).hexdigest()
        
        # Return as Raw Hex Key
        return f"0x{raw_hex}"
        
    except Exception as e:
        print(f"SQL Cipher Error: {e}")
        return None
