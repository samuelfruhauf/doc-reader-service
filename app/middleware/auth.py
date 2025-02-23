from functools import wraps
from flask import request, jsonify
from app.config import Config
from fastapi import HTTPException, Request

def require_api_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token.replace('Bearer ', '') != Config.API_TOKEN:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated 

async def require_api_token(request: Request):
    token = request.headers.get('Authorization')
    if not token or token.replace('Bearer ', '') != Config.API_TOKEN:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return True 