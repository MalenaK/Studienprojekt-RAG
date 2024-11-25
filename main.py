#from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

import argparse

from oauthlib.uri_validate import query

from infinity_reranker import rerank_top_k
from ollama_model import Model

from database_helper import DatabaseHelper

from document_handler import DocumentHandler

from embedding import get_embedding_function

import infinity_reranker



#Use Cuda 12.4 https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

#TODO SEE DOCUMENT HANDLER
#TODO DOCUMENTATION/CLEAN UP


#Config Parameters
config_model = "llama3"
config_embedding = "mxbai-embed-large"

#Retrieve top k chunks for a query
#One Chunk is currently 1200, context limit is around 8000 tokens
top_k_retrieval = 24
top_k_rerank = 7


#Instantiate Required Objects
llm_model: Model = Model(model=config_model)  # Idk why it says that we are getting None here in pycharm, it returns an object
db_helper = DatabaseHelper(model=config_embedding)
doc_handler = DocumentHandler()


#handles querying the llm
def query_rag(query_text) -> str:
    db = db_helper.get_db()

    #search in the db
    #First layer of filtering, computationally relatively inexpensive but higher inaccuracy
    #This layer should retrieve as many chunks as possible while keeping the second filtering layer in an acceptable time frame
    results = db.similarity_search_with_score(query_text, k=top_k_retrieval)
    #print(f"Search Results: {results}")  # Debug: Print the results to check


    #We will use the reranker to make a second more fine but computationally expensive layer of filtering here
    #This layer should utilize the maximum context of our llm
    results_reranked = rerank_top_k(results, query_text)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results_reranked])

    answer: str = llm_model.generate_answer(context_text, query_text)

    #Add sources to text
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_answer = f"Answer: {answer}\nSources: {sources}"
    return formatted_answer

def update_data_store(pdf_dir):
    # Create (or update) the data store.
    documents = doc_handler.load_documents(file_path=pdf_dir)
    chunks = doc_handler.split_documents(documents)
    db_helper.add_to_chroma(chunks)

def main():
    print(llm_model.generate_answer("There is no context", "Can you respond with 'Hello, everything is working fine!'"))

    parser = argparse.ArgumentParser()

    # Check if the database should be cleared (using the --clear flag). We could use a different better approach here this /
    # is temporary
    parser.add_argument("--reset", action="store_true", help="Reset the database.")

    # flag for path to pdfs
    parser.add_argument("-d", "--pdf_dir", default="./data", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()
    if args.reset:
        print("Clearing Database...")
        db_helper.clear_database()


    # Create (or update) the data store.
    update_data_store(args.pdf_dir)

    #Main Loop
    while True:
        print("\nEnter 'exit' to exit")
        query_text = input("Prompt: ")
        if query_text == 'exit':
            break
        elif query_text == 'Bazinga':  # easter egg
            print("🧠 Switching to Sheldon Mode... Bazinga!")
            llm_model.activate_sheldon_mode()
        print(query_rag(query_text))

if __name__ == "__main__":
    main()