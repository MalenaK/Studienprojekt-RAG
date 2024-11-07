from main import *
from test_cases import *

#Maybe improve this by actually using 3 models and making it a democratic decision if an answer was correct or not

test_template = """
Question: 
Expected Response: {context}
Actual Response: {question}

Does the actual response match the expected Response regarding content? Only answer with "true" or "false". 
"""
counter: int = 0
collection_name = None

#Using sources is not necessary in comparison
def query_rag_no_sources(query_text) -> str:
    db = db_helper.get_collection(collection_name=collection_name)

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    answer: str = llm_model.generate_answer(context_text, query_text)


    return answer



def test_model(question: str, expected_answer: str) -> bool | None:
    global counter
    actual_answer = query_rag_no_sources(question)
    # Change template to evaluation mode
    llm_model.set_template(test_template)

    #Evaluate the response
    context = f"Question: {question}\nExpected Response: {expected_answer}"
    evaluation = llm_model.generate_answer(context, actual_answer)
    print(f"{"-"*50}\nTest Case Number: {counter}\nQuestion: {question}\nActual Answer: {actual_answer}\nExpected Answer: {expected_answer}\nEvaluation: {evaluation}\n{"-"*50}\n\n")

    #Track test cases number
    counter += 1
    llm_model.reset_template()

    #return if true or false
    evaluation = evaluation.lower()
    if evaluation == "true":
        return True
    elif evaluation == "false":
        return False
    #In case the question could not be answered, we return None, we count this as an undesirable case always
    #We many change and decide to track the undecided answers later
    else:
        return None



def test_loop():
    #Normal tests that should return true
    false_positives = 0
    for test in positive_test_cases:
        if test_model(test[0], test[1]) != True:
            false_positives += 1

    #Complement tests that should return
    false_negatives = 0
    for test in negative_test_cases:
        if test_model(test[0], test[1]) != False:
            false_negatives += 1

    num_test_cases = len(positive_test_cases) + len(negative_test_cases)
    num_correct_answers = num_test_cases - false_negatives - false_positives
    print(f"\n{"-"*100}\nTotal Accuracy: {100*(num_correct_answers/num_test_cases)} %\n"
          f"False Positive Percentage: {100*(false_positives/len(positive_test_cases))} %\n"
          f"False Negative Percentage: {100*(false_negatives/len(negative_test_cases))} %\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("-d", "--pdf_dir", default="./data", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()
    if args.reset:
        print("Clearing Database...")
        db_helper.clear_database()

    # Create (or update) the data store.
    update_data_store(args.pdf_dir)

    collection_name = doc_handler.get_collection_name(args.pdf_dir)

    test_loop()