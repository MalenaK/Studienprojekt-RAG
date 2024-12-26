import argparse
from models.infinity_reranker import rerank_top_k
from models.ollama_model import Model
from retrieval.database_helper import DatabaseHelper
from retrieval.document_handler import DocumentHandler
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from config.settings import config_embedding, config_model, top_k_retrieval

# class State(TypedDict):
#     question: str
#     context: List[Document]
#     answer: str
#     messages: List[str]

# db_helper = DatabaseHelper(model=config_model)
# @tool(response_format="content_and_artifact")
# def retrieve(query: str):
#     """Retrieve information related to a query."""
#     print("\n##########retrieving##############\n")
#     db = db_helper.get_collection(collection_name="13036544b45fd5c71237c5d6f3683d3dd5186bd9e09e0c502500b6bbfd2cea8:")

#     results = db.similarity_search_with_score(query, k=top_k_retrieval)
#     results_reranked = rerank_top_k(query, results)
#     serialized: str = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in results_reranked])

#     return serialized, results_reranked

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

    def setup(self, state: MessagesState):
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


    def assert_setup(self, state: MessagesState):
        assert(state["messages"][-1] != None)
        
    @tool(response_format="content_and_artifact")
    def retrieve(self, query: str):
        """Retrieve information related to a query."""
        db = self.db_helper.get_collection(collection_name=self.collection_name)

        results = db.similarity_search_with_score(query, k=top_k_retrieval)
        results_reranked = rerank_top_k(query, results)
        serialized: str = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in results_reranked])

        return serialized, results_reranked

    def generate(self, state: MessagesState):
        recent_tool_messages = []
        for message in reversed(state["messages"]):
            if message.type == "tool":
                recent_tool_messages.append(message)
            else:
                break
        tool_messages = recent_tool_messages[::-1]
        context_text = "\n\n".join(doc.content for doc in tool_messages)

        conversation_messages = [
            message
            for message in state["messages"]
            if message.type in ("human", "system")
            or (message.type == "ai" and not message.tool_calls)
        ]
        
        answer: str = self.llm_model.generate_answer_with_history(context_text=context_text, conversation_messages=conversation_messages)

        #Add sources to text
        sources = [doc.metadata.get("id", None) for doc, _score in state["context"]]
        formatted_answer = f"Answer: {answer}\n\nRAG Sources: {sources}"

        return { "messages": {"role": "ai", "content": formatted_answer} }
    
    def query_or_respond(self, state: MessagesState):
        """Generate tool call for retrieval or respond."""
        # self.llm_model.bind_tools([self.retrieve])
        response = self.llm_model.generate_answer_with_history(context_text="no context", conversation_messages=state["messages"])
        # MessagesState appends messages to state instead of overwriting
        return {"messages": [response]}
    
    def print_answer_to_user(self, state: MessagesState):
        # print(state["messages"][-1])
        print("")

    def get_user_query(self, state: MessagesState):
        print("\nEnter 'exit' to exit")
        query_text = input("Prompt: ")
        return {"messages": [{"role": "user", "content": query_text}]}
    
    def user_entered_exit(self, state: MessagesState):
        return state["messages"][-1].content == "exit"
    
    



    