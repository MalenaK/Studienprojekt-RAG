import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

from spacy.lang.en import English

#from transformers import LlamaTokenizer

#PLEASE DO NOT DELETE THESE COMMENTS, I WILL USE THEM FOR THE REPORT!!!

#TODO CHECK IF USING TOKENIZER COULD IMPROVE THE RESULTS

class DocumentHandler:

    nlp = English()

    # def __init__(self, tokenizer: LlamaTokenizer = LlamaTokenizer.from_pretrained("meta-llama/Llama-3")):
    #     self.tokenizer = tokenizer

    def __init__(self):
        self.nlp.add_pipe("sentencizer")
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


    def sentencize(self, text):
        return list(self.nlp(text).sents)

    def chunk_sentences(self, sentences: list[str], slice_size: int) -> list[str]:
        array_chunks = [sentences[i:i + slice_size] for i in range(0, len(sentences), slice_size)]
        return [" ".join(array_chunks[i]) for i in range(0, len(array_chunks))]
    

    #def split_documents(self, documents: list[Document]) -> list[Document]:
    #    #TODO optimize values in recursiveCharacterText Splitter
    #    text_splitter = RecursiveCharacterTextSplitter(
    #        chunk_size=1200, #was 800
    #        chunk_overlap=120, #was 80
    #        length_function=len, # was len before, tokenizer may work better since len only uses characters but tokenizer uses tokens for llms
    #        separators=["\n\n", ".", " "], #semantic chunking, I found that these are common semantic seperators in papers
    #        #is_separator_regex=False,
    #    )
    #    tmp = text_splitter.split_documents(documents)
    #    print(tmp)
    #    return tmp

    # conda install -c conda-forge spacy
    # conda install -c conda-forge cupy
    # python -m spacy download en_core_web_sm

    def split_documents(self, documents: list[Document]) -> list[Document]:
        chunks = list()
        num_sentence_chunk_size = 10
    
        for page in documents:
            sentencized = [str(sentence) for sentence in self.sentencize(page.page_content)]
            pre_chunks = self.chunk_sentences(sentencized, num_sentence_chunk_size)
            for pre_chunk in pre_chunks:
                chunks.append(Document(page_content=pre_chunk,metadata={"source":page.metadata.get("source"),"page":page.metadata.get("page")}))
     
    
        print(chunks)
        return chunks # text_splitter.split_documents(documents)