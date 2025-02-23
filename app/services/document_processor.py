import os
import logging
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableFormerMode
)
from docling.chunking import HybridChunker
from app.config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def __init__(self):
        # Configure pipeline options for PDF files
        pdf_pipeline_options = PdfPipelineOptions(do_table_structure=True)
        pdf_pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

        # Configure format options
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options),
            }
        )
        self.chunker = HybridChunker(tokenizer="BAAI/bge-small-en-v1.5")

    def process_file(self, file_path):
        try:
            file_extension = self._get_file_extension(file_path)
            if file_extension not in Config.SUPPORTED_FILE_TYPES:
                raise ValueError(f"Unsupported file type: {file_extension}")

            logger.info(f"Processing file: {file_path}")
            result = self.converter.convert(file_path)
            chunks = self.chunker.chunk(result.document)
            
            return self._format_chunks(chunks, file_path)
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            raise

    def _get_file_extension(self, file_path):
        return os.path.splitext(file_path)[1].lower().lstrip('.')

    def _format_chunks(self, chunks, file_path):
        data = []
        for i, chunk in enumerate(chunks):
            chunk_data = {
                "file_name": os.path.basename(file_path),
                "chunk_index": i,
                "text": chunk.text
            }

            # Handle page information if available
            if chunk.meta and getattr(chunk.meta, "doc_items", None):
                chunk_data["pages"] = sorted(self._extract_pages(chunk))

            # Handle headings if available
            if chunk.meta and getattr(chunk.meta, "headings", None):
                chunk_data["headings"] = chunk.meta.headings

            data.append(chunk_data)
        return data

    def _extract_pages(self, chunk):
        pages = set()
        if chunk.meta and getattr(chunk.meta, "doc_items", None):
            for doc_item in chunk.meta.doc_items:
                if getattr(doc_item, "prov", None):
                    for p in doc_item.prov:
                        if getattr(p, "page_no", None) is not None:
                            pages.add(p.page_no)
        return pages 