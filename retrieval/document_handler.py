import os
import hashlib
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

class DocumentHandler:
    """A helper class for managing the access to the directory where the PDFs for the external knowledge base are stored."""
    def __init__(self):
        self.pdf_dir = ""

    def load_documents(self) -> list[Document]:
        """
        Loads the pdf documents from pdf_dir.

        Raises
        ----------
        Exception
            This indicates an error in the logical flow of your program. The pdf_dir is not defined, so the handler does not know where to look.
        FileNotFoundError
            This indicates that you specified a directory that does not exist. Reference the pdf_dir relative to where you launched main.py

        Returns
        ----------
        List[Document]
            The list of documents that have been loaded.
        """
        if not self.pdf_dir:
            raise Exception("no pdf dir set before loading documents. This is an error in your RAG application, please fix.")
        if not os.path.exists(self.pdf_dir):
            raise FileNotFoundError(f"The specified directory does not exist: {self.pdf_dir}")

        document_loader = PyPDFDirectoryLoader(self.pdf_dir)
        return document_loader.load()
    
    def set_pdf_dir(self, pdf_dir: str) -> None:
        """
        Loads the pdf documents from pdf_dir.

        Parameters
        ----------
        pdf_dir
            path to the pdf directory. Reference the pdf_dir relative to where you launched main.py

        Raises
        ----------
        FileNotFoundError
            This indicates that you specified a directory that does not exist. Reference the pdf_dir relative to where you launched main.py

        """
        if not os.path.exists(pdf_dir):
            raise FileNotFoundError(f"The specified directory does not exist: {pdf_dir}")
        
        self.pdf_dir = pdf_dir

    def get_pdf_dir(self):
        """
        Returns
        ----------
        pdf_dir: str
            The path to the directory where all the PDFs for the external knowledge base lie.

        """
        return self.pdf_dir

    def split_documents(self, documents: list[Document]) -> list[Document]:
        """
        Splits the documents into chunks using the RecursiveTextSplitter.

        Parameters
        ----------
        documents: list[Document]
            documents to be split into chunks.

        Returns
        ----------
        list[Document]
            documents split into chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200, #was 800
            chunk_overlap=120, #was 80
            length_function=len, # was len before, tokenizer may work better since len only uses characters but tokenizer uses tokens for llms
            separators=["\n\n", ".", " "], #semantic chunking, I found that these are common semantic seperators in papers
        )
        return text_splitter.split_documents(documents)
    
    #creates the name of the collection based on file names in dir + filepath
    def get_collection_name(self, file_path: str) -> str:
        """
        creates the name of the collection based on filepath. The collection name is created using a hashfunction to its uniqueness and maximum length.

        Parameters
        ----------
        file_path: str
            path to pdf directory.

        Raises
        ----------
        FileNotFoundError
            This indicates that you specified a directory that does not exist. Reference the pdf_dir relative to where you launched main.py
            
        Returns
        ----------
        str
            collection name
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The specified directory does not exist: {file_path}")
        
        #compute hash of folder path content to ensure uniqueness and meet criteria for collection name (< 63 character,...)
        abs_path = os.path.abspath(file_path)
        hash_object = hashlib.sha256(abs_path.encode('utf-8'))

        return hash_object.hexdigest()[:63]

