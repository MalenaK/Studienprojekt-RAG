import argparse
from typing import List, TypedDict
from models.infinity_reranker import rerank_top_k
from models.ollama_model import Model
from retrieval.database_helper import DatabaseHelper
from retrieval.document_handler import DocumentHandler
from langchain.schema.document import Document

from config.settings import config_embedding, config_model, top_k_retrieval

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

class RAGpipeline():
    def __init__(self):
        self.llm_model: Model = Model(model=config_model)
        self.db_helper = DatabaseHelper(model=config_embedding)
        self.doc_handler = DocumentHandler()
        self.collection_name = ""
        self.pdf_dir = ""
        self.args: argparse.Namespace

    def get_parser_args(self):
        parser = argparse.ArgumentParser()

        parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
        parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")
        parser.add_argument("-d", "--pdf_dir", default="./data/data_basic", help="Specify path to directory containing the pdfs.")

        self.args = parser.parse_args()

    def setup(self, state: State):
        self.get_parser_args()

        self.pdf_dir = self.args.pdf_dir
        self.collection_name = self.doc_handler.get_collection_name(file_path=self.pdf_dir)
        
        if self.args.reset_all:
            self.db_helper.clear_database()
        
        if self.args.reset_collection:
            self.db_helper.clear_collection(self.collection_name)

        # Create (or update) the data store.
        documents = self.doc_handler.load_documents(file_path=self.pdf_dir)
        chunks = self.doc_handler.split_documents(documents)
        self.db_helper.add_to_chroma(chunks, collection_name=self.doc_handler.get_collection_name(file_path=self.pdf_dir))

    def assert_setup(self, state: State):
        assert(state["question"] != None)
        

    def retrieve(self, state: State):
        db = self.db_helper.get_collection(collection_name=self.collection_name)

        #search in the db
        #First layer of filtering, computationally relatively inexpensive but higher inaccuracy
        #This layer should retrieve as many chunks as possible while keeping the second filtering layer in an acceptable time frame
        results:  list[tuple[Document, float]] = db.similarity_search_with_score(state["question"], k=top_k_retrieval)
        
        #We will use the reranker to make a second more fine but computationally expensive layer of filtering here
        #This layer should utilize the maximum context of our llm
        #Currently the rerank_top_k does not look at the document the text was taken from but only the content!
        results_reranked = rerank_top_k(state["question"], results)

        return {"context": results_reranked}

    def generate(self, state: State):
        context_text: str = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in state["context"]])
        answer: str = self.llm_model.generate_answer(context_text=context_text, query=state["question"])

        #Add sources to text
        sources = [doc.metadata.get("id", None) for doc, _score in state["context"]]
        formatted_answer = f"Answer: {answer}\n\nRAG Sources: {sources}"

        return { "answer": formatted_answer }
    
    def print_answer_to_user(self, state: State):
        print(state["answer"])

    def get_user_query(self, state: State):
        print("\nEnter 'exit' to exit")
        query_text = input("Prompt: ")
        return {"question": query_text }
    
    def user_entered_exit(self, state: State):
        return state["question"] == "exit"
    
    



    