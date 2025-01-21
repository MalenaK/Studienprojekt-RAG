import argparse

from models.infinity_reranker import rerank_top_k
from models.ollama_model import Model
from retrieval.database_helper import DatabaseHelper
from retrieval.document_handler import DocumentHandler
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from config.settings import config_embedding, config_model, top_k_retrieval, top_k_rerank
from langchain_core.messages import RemoveMessage

llm_model: Model = Model(model=config_model)
db_helper = DatabaseHelper(model=config_embedding)
doc_handler = DocumentHandler()

def setup(state: MessagesState):
    parser = argparse.ArgumentParser()

    parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
    parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")
    parser.add_argument("-d", "--pdf_dir", default="./data/data_basic", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()

    pdf_dir = args.pdf_dir
    doc_handler.set_pdf_dir(pdf_dir)

    collection_name = doc_handler.get_collection_name(file_path=pdf_dir)
    db_helper.set_collection_name(collection_name)
    
    if args.reset_all:
        db_helper.clear_database()
    
    if args.reset_collection:
        db_helper.clear_collection(collection_name)

    # Create (or update) the data store.
    documents = doc_handler.load_documents()
    chunks = doc_handler.split_documents(documents)
    db_helper.add_to_chroma(chunks)


def assert_setup(state: MessagesState):
    assert(state["messages"][-1] != None)
    
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    db = db_helper.get_db_for_collection()

    results = db.similarity_search_with_score(query, k=top_k_retrieval)
    results_reranked = rerank_top_k(query, results, k=top_k_rerank)
    serialized: str = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in results_reranked])

    return serialized, results_reranked

def generate(state: MessagesState):
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[0:top_k_rerank] #just take results from last retrieval

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    print("docs content", docs_content)
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]

    # Run
    response = llm_model.generate_answer_with_history(context_text=docs_content, conversation_messages=conversation_messages)
    return {"messages": [response]}

def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    response = llm_model.invoke_with_toolcall(tool = retrieve, messages=state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


def print_answer_to_user(state: MessagesState):
    print(state["messages"][-1].content)

def get_user_query(state: MessagesState):
    print("\nEnter 'exit' to exit")
    query_text = input("Prompt: ")
    return {"messages": [{"role": "user", "content": query_text}]}

def user_entered_exit(state: MessagesState):
    return state["messages"][-1].content == "exit"

def delete_messages(state: MessagesState):
    messages = state["messages"]
    return {"messages": [RemoveMessage(id=m.id) for m in messages]}

    



    