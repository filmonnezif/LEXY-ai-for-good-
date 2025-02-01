from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
import tempfile
from dotenv import load_dotenv
import os
load_dotenv()


def extract_text_from_document(file_content):
    # Create a temporary file to store the uploaded content
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        file_path = temp_file.name

    # Initialize the loader with the temp file
    loader = AzureAIDocumentIntelligenceLoader(
        api_endpoint=os.getenv("DOCAPI"),
        api_key=os.getenv("DOCKEY"),
        file_path=file_path,
        api_model="prebuilt-layout"
    )
    
    # Extract text
    documents = loader.load()
    
    # Get the extracted text
    extracted_tex = " ".join([doc.page_content for doc in documents])
    
    return extracted_tex
