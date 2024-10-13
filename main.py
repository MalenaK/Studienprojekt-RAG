#from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

import argparse

from ollama_model import Model

from database_helper import DatabaseHelper

from document_handler import DocumentHandler

from embedding import get_embedding_function



#Use Cuda 12.4 https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

#TODO SEE DOCUMENT HANDLER
#TODO DOCUMENTATION/CLEAN UP
#

#Instantiate Required Objects
llm_model: Model = Model()  # Idk why it says that we are getting None here in pycharm, it returns an object
db_helper = DatabaseHelper(model=llm_model.get_model())
doc_handler = DocumentHandler()


#handles querying the llm
def query_rag(query_text) -> str:
    db = db_helper.get_db()

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    answer: str = llm_model.generate_answer(context_text, query_text)

    #Add sources to text
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_answer = f"Answer: {answer}\nSources: {sources}"
    return formatted_answer

def main():
    llm_model: Model = Model() #Idk why it says that we are getting None here in pycharm, it returns an object

    print(llm_model.generate_answer("There is no context", "Can you respond with 'Hello, everything is working fine!'"))

    # Check if the database should be cleared (using the --clear flag). We could use a different better approach here this /
    # is temporary
    # -----------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("Clearing Database...")
        db_helper.clear_database()
    #--------------------------------------

    # Create (or update) the data store.
    documents = doc_handler.load_documents()
    chunks = doc_handler.split_documents(documents)
    db_helper.add_to_chroma(chunks)

    #Main Loop
    print("Enter 'exit' to exit")
    while True:
        query_text = input("Prompt: ")
        if query_text == 'exit':
            break
        elif query_text == 'Bazinga':  # easter egg
            print("🧠 Switching to Sheldon Mode... Bazinga!")
            llm_model.activate_sheldon_mode()
        print(query_rag(query_text))

if __name__ == "__main__":
    main()