from numpy.ma.core import negative
from pypika.enums import Boolean
from sympy import false

from main import *
from test_cases import *

#Maybe improve this by actually using 3 models and making it a democratic decision if an answer was correct or not

test_template = """
Question: 
Expected Response: {context}
Actual Response: {question}

Does the actual response match the expected Response regarding content? Only answer with "true" or "false". 
"""
global counter
counter: int = 0


#Using sources is not necessary in comparison
def query_rag_no_sources(query_text) -> str:
    db = db_helper.get_db()

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





positive_test_cases = [test_case_1] #...
negative_test_cases = [test_case_1_complement]

def test_loop():
    #Normal tests that should return true
    false_positives = 0
    for test in positive_test_cases:
        if test() != True:
            false_positives += 1

    #Complement tests that should return
    false_negatives = 0
    for test in negative_test_cases:
        if test() != False:
            false_negatives += 1

    print(f"\n{"-"*100}\nTotal Accuracy: {100*((false_negatives+false_positives)/counter)} %\n"
          f"False Positive Percentage: {100*(false_positives/len(positive_test_cases))} %\n"
          f"False Negative Percentage: {100*(false_negatives/len(negative_test_cases))} %\n")



if __name__ == "__main__":
    test_loop()