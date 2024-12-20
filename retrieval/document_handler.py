import os
import hashlib

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
#from transformers import LlamaTokenizer

#PLEASE DO NOT DELETE THESE COMMENTS, I WILL USE THEM FOR THE REPORT!!!

#TODO CHECK IF USING TOKENIZER COULD IMPROVE THE RESULTS

class DocumentHandler:

    # def __init__(self, tokenizer: LlamaTokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3")):
    #     self.tokenizer = tokenizer

    def __init__(self):
        pass


    #custom len function that uses words (tokens) instead of character amount
    #def token_length(self, text: str) -> int:
    #    return len(self.tokenizer.encode(text))

    def load_documents(self, file_path: str = "./data") -> list[Document]:
        # Ensure the directory exists before trying to load documents
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The specified directory does not exist: {file_path}")

        document_loader = PyPDFDirectoryLoader(file_path)
        return document_loader.load()

    # def split_documents(self, documents: list[Document]) -> list[Document]:
    #     #TODO optimize values in recursiveCharacterText Splitter
    #     text_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=1200, #was 800, increasing both chunk_size and chunk_overlap led to better results
    #         chunk_overlap=120, #was 80
    #         length_function=self.token_length, # was len before, tokenizer may work better since len only uses characters but tokenizer uses tokens for llms
    #         separators=["\n\n", ".", " "], #semantic chunking, I found that these are common semantic seperators in papers
    #         #is_separator_regex=False,
    #     )
    #     return text_splitter.split_documents(documents)

    #same as above, no tokenizer
    def split_documents(self, documents: list[Document]) -> list[Document]:
        #TODO optimize values in recursiveCharacterText Splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200, #was 800
            chunk_overlap=120, #was 80
            length_function=len, # was len before, tokenizer may work better since len only uses characters but tokenizer uses tokens for llms
            separators=["\n\n", ".", " "], #semantic chunking, I found that these are common semantic seperators in papers
            #is_separator_regex=False,
        )
        return text_splitter.split_documents(documents)
    
    #creates the name of the collection based on file names in dir + filepath
    def get_collection_name(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The specified directory does not exist: {file_path}")
        
        #compute hash of path + folder content to ensure uniqueness and meet criteria for collection name (< 63 character,...)
        #pdf_names: str = ''.join(sorted(os.listdir(file_path))).replace(' ','') #turn list into string
        abs_path = os.path.abspath(file_path)
        hash_object = hashlib.sha256(abs_path.encode('utf-8'))

        return hash_object.hexdigest()[:63]

        # Does this fit in here? I did not feel like adding another file just for one fun
    def update_data_store(self, pdf_dir, db_helper):
        # Create (or update) the data store.
        documents = self.load_documents(file_path=pdf_dir)
        chunks = self.split_documents(documents)
        db_helper.add_to_chroma(chunks, collection_name=self.get_collection_name(file_path=pdf_dir))

