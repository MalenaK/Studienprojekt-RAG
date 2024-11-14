#from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

import argparse

from ollama_model import Model

from database_helper import DatabaseHelper

from document_handler import DocumentHandler

from embedding import get_embedding_function



#Use Cuda 12.4 https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

#TODO SEE DOCUMENT HANDLER
#TODO DOCUMENTATION/CLEAN UP


#Config Parameters
config_model = "llama3"
config_embedding = "mxbai-embed-large"

#Instantiate Required Objects
llm_model: Model = Model(model=config_model)  # Idk why it says that we are getting None here in pycharm, it returns an object
db_helper = DatabaseHelper(model=config_embedding)
doc_handler = DocumentHandler()


#handles querying the llm
def query_rag(query_text, collection_name) -> str:
    db = db_helper.get_collection(collection_name=collection_name)

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    answer: str = llm_model.generate_answer(context_text, query_text)

    #Add sources to text
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_answer = f"Answer: {answer}\nSources: {sources}"
    return formatted_answer

def update_data_store(pdf_dir):
    # Create (or update) the data store.
    documents = doc_handler.load_documents(file_path=pdf_dir)
    chunks = doc_handler.split_documents(documents)
    db_helper.add_to_chroma(chunks, collection_name=doc_handler.get_collection_name(file_path=pdf_dir))

def main():
    print(llm_model.generate_answer("There is no context", "Can you respond with 'Hello, everything is working fine!'"))

    parser = argparse.ArgumentParser()

    # Check if the database should be cleared (using the --clear flag). We could use a different better approach here this /
    # is temporary
    parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
    parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")

    # flag for path to pdfs
    parser.add_argument("-d", "--pdf_dir", default="./data", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()

    collection_name = doc_handler.get_collection_name(file_path=args.pdf_dir)
    if args.reset_all:
        db_helper.clear_database()
    
    if args.reset_collection:
        db_helper.clear_collection(collection_name)

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
        print(query_rag(query_text, collection_name))

if __name__ == "__main__":
    main()