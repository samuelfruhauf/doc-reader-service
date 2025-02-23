import json
import logging
import os
from app.config import Config
from app.services.document_processor import DocumentProcessor
from app.services.s3_service import S3Service
from app.services.sqs_service import SQSService
import requests

logger = logging.getLogger(__name__)

def process_message(message_body):
    tmp_file = None
    try:
        data = json.loads(message_body)
        logger.info(f"Processing job for file {data['s3_key']} from bucket {data['s3_bucket']}")
        
        file_name = os.path.basename(data['s3_key'])
        tmp_file = os.path.join(Config.TEMP_FILE_DIR, file_name)

        s3_service = S3Service()
        logger.info(f"Downloading file from S3: {data['s3_bucket']}/{data['s3_key']}")
        s3_service.download_file(data['s3_bucket'], data['s3_key'], tmp_file)
        
        document_processor = DocumentProcessor()
        logger.info(f"Starting document processing for {data['s3_key']}")
        processed_data = document_processor.process_file(tmp_file)
        
        logger.info(f"Sending callback to {data['callback_url']}")
        callback_payload = {
            "data": processed_data,
            "custom_data": data.get('custom_data')
        }
        
        response = requests.post(data['callback_url'], json=callback_payload)
        logger.info(f"Callback response status: {response.status_code}")
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        if 'callback_url' in data:
            try:
                requests.post(data['callback_url'], json={"error": str(e)})
            except Exception as callback_error:
                logger.error(f"Error sending error callback: {str(callback_error)}")
    finally:
        if tmp_file and os.path.exists(tmp_file):
            os.remove(tmp_file)

def run_worker():
    sqs_service = SQSService()
    
    while True:
        try:
            logger.info("Polling for messages...")
            response = sqs_service.sqs_client.receive_message(
                QueueUrl=sqs_service.queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=20,
                AttributeNames=['All']
            )
            
            if 'Messages' in response:
                for message in response['Messages']:
                    message_id = message.get('MessageId', 'unknown')
                    logger.info(f"Processing message {message_id}")
                    
                    try:
                        process_message(message['Body'])
                        if sqs_service.delete_message(message['ReceiptHandle']):
                            logger.info(f"Successfully processed and deleted message {message_id}")
                        else:
                            logger.error(f"Failed to delete message {message_id}")
                    except Exception as e:
                        logger.error(f"Failed to process message {message_id}: {str(e)}", exc_info=True)
            else:
                logger.debug("No messages available in queue")
                
        except Exception as e:
            logger.error(f"Worker error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    run_worker() 