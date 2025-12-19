import tempfile
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    async def process_file(self, file_path: str, file_type: str) -> List[str]:
        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type == "csv":
            loader = CSVLoader(file_path)
        else:
            loader = TextLoader(file_path)
        
        docs = loader.load()
        split_docs = self.text_splitter.split_documents(docs)
        return [doc.page_content for doc in split_docs]

document_processor = DocumentProcessor()
