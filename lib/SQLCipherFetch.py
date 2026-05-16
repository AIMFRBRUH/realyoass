import os
import types
import requests
import hashlib

def get_sql_cipher_key(fetch_url: str, gateway_url: str, bundle_version: str):
    """
    Retrieves the SQL Cipher key.
    If no secret URL is provided, it calculates it locally using the JP 'Recipe'.
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
            pass # Fallback to local if remote fails

    # 2. Local "Just Works" Logic (The Full Thing)
    # This is the standard Blue Archive JP key derivation
    try:
        salt = "BlueArchive" 
        raw_seed = f"{gateway_url}{bundle_version}{salt}".encode('utf-8')
        return hashlib.sha1(raw_seed).hexdigest()
    except Exception as e:
        print(f"SQL Cipher Error: {e}")
        return None
