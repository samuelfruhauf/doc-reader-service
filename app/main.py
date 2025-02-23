import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import requests
from app.config import Config
from app.services.document_processor import DocumentProcessor
from app.services.s3_service import S3Service
from app.middleware.auth import require_api_token
from app.utils.error_handlers import handle_errors
from pydantic import BaseModel
from app.services.sqs_service import SQSService

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Ensure temp directory exists
os.makedirs(Config.TEMP_FILE_DIR, exist_ok=True)

class ProcessRequest(BaseModel):
    s3_bucket: str
    s3_key: str
    callback_url: str
    custom_data: dict = None

@app.post("/process")
async def process_request(request_data: ProcessRequest, auth: bool = Depends(require_api_token)):
    try:
        file_extension = os.path.splitext(request_data.s3_key)[1].lower().lstrip('.')
        if file_extension not in Config.SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_extension}")

        sqs_service = SQSService()
        message_id = sqs_service.send_message(request_data.dict())
        
        return {
            "message": "Request queued successfully",
            "message_id": message_id
        }
    
    except Exception as e:
        logger.error(f"Error queueing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/queue-status")
async def get_queue_status(auth: bool = Depends(require_api_token)):
    try:
        sqs_service = SQSService()
        attributes = sqs_service.get_queue_attributes()
        if attributes:
            return {
                "messages_available": int(attributes.get('ApproximateNumberOfMessages', 0)),
                "messages_in_flight": int(attributes.get('ApproximateNumberOfMessagesNotVisible', 0)),
                "messages_delayed": int(attributes.get('ApproximateNumberOfMessagesDelayed', 0))
            }
        raise HTTPException(status_code=500, detail="Could not fetch queue attributes")
    except Exception as e:
        logger.error(f"Error getting queue status: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    app.run(debug=False) 