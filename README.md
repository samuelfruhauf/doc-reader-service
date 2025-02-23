# PDF Processor Service

A Flask-based service that processes PDF documents using document conversion and chunking capabilities.

## Features
- PDF processing with table structure recognition
- Document chunking
- S3 integration
- Callback notifications
- Authentication
- Structured logging

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

pdf-processor/
├── .gitignore
├── README.md
├── requirements.txt
├── config/
│   └── config.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── pdf_processor.py
│   │   └── s3_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   └── auth.py
│   └── middleware/
│       ├── __init__.py
│       └── auth_middleware.py
└── tests/
    └── __init__.py
