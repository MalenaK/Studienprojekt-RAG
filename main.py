#from transformers.models.pop2piano.convert_pop2piano_weights_to_hf import model

import argparse


from models.infinity_reranker import rerank_top_k

from langchain.schema.document import Document

from shared import llm_model, db_helper, doc_handler

from config import top_k_retrieval


#Use Cuda 12.4 https://developer.nvidia.com/cuda-12-4-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local

#TODO SEE DOCUMENT HANDLER
#TODO DOCUMENTATION/CLEAN UP



#handles querying the llm
# Should we rename this function? query_rag does not seem fitting as this in not the only thing we do
def query_rag(query_text, collection_name) -> str:
    db = db_helper.get_collection(collection_name=collection_name)

    #search in the db
    #First layer of filtering, computationally relatively inexpensive but higher inaccuracy
    #This layer should retrieve as many chunks as possible while keeping the second filtering layer in an acceptable time frame
    results:  list[tuple[Document, float]] = db.similarity_search_with_score(query_text, k=top_k_retrieval)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    
    #We will use the reranker to make a second more fine but computationally expensive layer of filtering here
    #This layer should utilize the maximum context of our llm
    #Currently the rerank_top_k does not look at the document the text was taken from but only the content!
    results_reranked = rerank_top_k(query_text, results)

    context_text = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in results_reranked])
    answer: str = llm_model.generate_answer(context_text, query_text)

    #Add sources to text
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_answer = f"Answer: {answer}\n\nRAG Sources: {sources}"
    return formatted_answer


def main():
    print(llm_model.generate_answer("There is no context", "Can you respond with '...Everything is working perfectly fine so far, getting the Database...'"))

    parser = argparse.ArgumentParser()

    # Check if the database should be cleared (using the --clear flag). We could use a different better approach here this /
    # is temporary
    parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
    parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")

    # flag for path to pdfs
    parser.add_argument("-d", "--pdf_dir", default="./data/data_basic", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()

    collection_name = doc_handler.get_collection_name(file_path=args.pdf_dir)
    if args.reset_all:
        db_helper.clear_database()
    
    if args.reset_collection:
        db_helper.clear_collection(collection_name)

    # Create (or update) the data store.
    doc_handler.update_data_store(args.pdf_dir, db_helper)

    print("Everything is operational, have fun :D")
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