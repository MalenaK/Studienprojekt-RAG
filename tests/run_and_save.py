# run specified test cases and safe output to file

import argparse
import os
from retrieval.database_helper import DatabaseHelper
from models.embedding import get_embedding_function
from models.infinity_reranker import rerank_top_k
from models.ollama_model import Model
import main as mainFile
import tests.test_cases as test_cases

class simple_test_suite:
    db_helper: DatabaseHelper
    llm_model: Model
    path_to_testresults: str
    collection_name: str

def query_rag(query_text, test_suite) -> str:

    db = test_suite.db_helper.get_collection(collection_name=test_suite.collection_name)

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    results_reranked = rerank_top_k(query_text, results)
    # Page count starts at 0.
    # Add sources to context
    context_text = "\n\n-Block-\n\n".join([doc.page_content + "\nSource of info in this block: " + doc.metadata.get("id", None) for doc, _score in results_reranked])
    answer: str = test_suite.llm_model.generate_answer(context_text, query_text)

    #Add sources to text
    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_answer = f"Answer: {answer}\n\nRAG Sources: {sources}"
    return formatted_answer

def log(message: str, test_suite: simple_test_suite):
    with open(test_suite.path_to_testresults, 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')
    
def test_loop(test_cases, test_suite: simple_test_suite):
    #loop over all elements in list, ask question
    for test_case in test_cases:
        answer: str = query_rag(query_text=test_case, test_suite=test_suite)
        message = f"Question: {test_case}\n{answer}\n{"-"*50}"
        log(message=message, test_suite=test_suite)

def create_resultfile(test_suite, data_path, test_cases_name) -> str:
    test_folder = "./testresults/complex_testcases"
    os.makedirs(test_folder, exist_ok=True)

    data_name = data_path.replace("/","").replace("\\", "").replace(" ","").replace(".","")
    model_name = test_suite.llm_model.get_model()
    embedding_name = get_embedding_function().model
    file_name = f"{model_name}---{embedding_name}---{data_name}---{test_cases_name}.txt"

    relative_path = f"{test_folder}/{file_name}"

    with open(relative_path, 'w') as log_file:
        log_file.write("") #clear file

    return relative_path

def set_up_testsuite(data_path, test_cases_name) -> simple_test_suite:
    test_suite = simple_test_suite()
    test_suite.db_helper = mainFile.db_helper
    test_suite.llm_model = mainFile.llm_model
    test_suite.collection_name = mainFile.doc_handler.get_collection_name(file_path=data_path)
    test_suite.path_to_testresults = create_resultfile(test_suite, data_path, test_cases_name)
    return test_suite

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
    parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")
    parser.add_argument("-d", "--pdf_dir", default="./data/data_basic/", help="Specify path to directory containing the pdfs.")
    parser.add_argument("-tc", "--test_cases_name", required=True, help="Specify name of test cases list.")
    args = parser.parse_args()

    test_suite = set_up_testsuite(data_path=args.pdf_dir, test_cases_name=args.test_cases_name)

    if args.reset_all:
        test_suite.db_helper.clear_database()
    
    if args.reset_collection:
        test_suite.db_helper.clear_collection(test_suite.collection_name)
    # Create (or update) the data store.
    
    mainFile.update_data_store(args.pdf_dir)

    test_cases_list = test_cases.test_cases_names_to_list[args.test_cases_name]

    test_loop(test_cases=test_cases_list, test_suite=test_suite)
