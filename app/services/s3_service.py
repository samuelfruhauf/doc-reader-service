import boto3
import logging
from app.config import Config

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_KEY,
            region_name=Config.AWS_REGION
        )

    def download_file(self, bucket, key, local_path):
        try:
            logger.info(f"Downloading file from S3: {bucket}/{key}")
            self.s3_client.download_file(bucket, key, local_path)
        except Exception as e:
            logger.error(f"Error downloading from S3: {str(e)}", exc_info=True)
            raise 