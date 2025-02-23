import logging
import requests
from functools import wraps

logger = logging.getLogger(__name__)

def handle_errors(callback_url=None):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in function {f.__name__}: {str(e)}", exc_info=True)
                if callback_url:
                    try:
                        requests.post(callback_url, json={"error": str(e)})
                    except Exception as callback_error:
                        logger.error(f"Error sending callback: {str(callback_error)}", exc_info=True)
                raise
        return wrapped
    return decorator 