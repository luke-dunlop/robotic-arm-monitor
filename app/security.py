import secrets
from fastapi import Header, HTTPException

from app.config import settings

def verify_api_key(x_api_key: str = Header(...)):
    if not secrets.compare_digest(x_api_key, settings.api_key): # use secrets.compare_digest rather than ==. Its constant-time, which avoids leaking the key length/contents through reponse time differences (a timing attack).
        raise HTTPException(status_code=401, detail="Invalid API key")