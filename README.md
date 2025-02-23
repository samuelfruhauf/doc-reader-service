# Document Processing Service

A FastAPI-based service that processes various document types (PDF, TXT, RTF) using document conversion, chunking capabilities, and AWS services for reliable queue-based processing.

## Features
- Multi-format document processing:
  - PDF files with table structure recognition
  - Plain text (TXT) files
  - Rich Text Format (RTF) files
- Intelligent document chunking with hybrid approach
- AWS S3 integration for document storage
- AWS SQS integration for reliable queue processing
- Callback notifications for process completion
- Authentication with API tokens
- Comprehensive logging and monitoring
- Queue status monitoring
- Custom data passthrough support

## Architecture
The service uses a queue-based architecture:
1. API receives document processing requests
2. Documents are queued in AWS SQS
3. Worker processes pick up queue messages
4. Results are sent via callbacks with original custom data

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env`

## Configuration
Create a `.env` file with the following variables:

```
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=your_region
SQS_QUEUE_URL=your_queue_url
SQS_QUEUE_NAME=your_queue_name
```

## Running the Service
1. Start the FastAPI server: `uvicorn app.main:app --reload`
2. Start the worker: `python worker.py`

## API Endpoints

### Process Document

```
POST /process-document

{
    "s3_bucket": "your_bucket_name",
    "s3_key": "your_file_key",
    "callback_url": "your_callback_url",
    "custom_data": "your_custom_data"
}
```
