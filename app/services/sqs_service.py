import json
import boto3
import logging
from app.config import Config

logger = logging.getLogger(__name__)

class SQSService:
    def __init__(self):
        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )
        self.queue_url = Config.SQS_QUEUE_URL

    def send_message(self, message_body):
        try:
            logger.info(f"Queueing new job for file: {message_body.get('s3_key')} from bucket: {message_body.get('s3_bucket')}")
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            logger.info(f"Successfully queued job with message ID: {response['MessageId']}")
            return response['MessageId']
        except Exception as e:
            logger.error(f"Error sending message to SQS: {str(e)}", exc_info=True)
            raise

    def delete_message(self, receipt_handle):
        """
        Delete a message from the queue using its receipt handle.
        
        Args:
            receipt_handle (str): The receipt handle of the message to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            logger.info("Attempting to delete message from queue")
            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info("Successfully deleted message from queue")
            return True
        except Exception as e:
            logger.error(f"Error deleting message from SQS: {str(e)}", exc_info=True)
            return False

    def get_queue_attributes(self):
        """
        Get queue attributes including approximate message counts.
        
        Returns:
            dict: Queue attributes or None if there was an error
        """
        try:
            response = self.sqs_client.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=['All']
            )
            attributes = response['Attributes']
            logger.info(f"Queue stats: Messages Available: {attributes.get('ApproximateNumberOfMessages', 0)}, "
                       f"Messages In Flight: {attributes.get('ApproximateNumberOfMessagesNotVisible', 0)}")
            return attributes
        except Exception as e:
            logger.error(f"Error getting queue attributes: {str(e)}", exc_info=True)
            return None 