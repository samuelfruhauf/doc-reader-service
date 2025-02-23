import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_TOKEN = os.getenv('API_TOKEN', 'your-default-secure-token')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    TEMP_FILE_DIR = os.getenv('TEMP_FILE_DIR', 'tmp')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    SUPPORTED_FILE_TYPES = [
        'pdf', 'txt', 'rtf'  # Removed image formats since we're not handling them
    ]
    SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
    SQS_QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'pdf-processor-queue') 