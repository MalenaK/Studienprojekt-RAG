from main import *
from test_cases import *

#Maybe improve this by actually using 3 models and making it a democratic decision if an answer was correct or not

test_template = """
Question: {question}
Expected Response: {expected_answer}
Actual Response: {actual_answer}

Does the actual response match the expected Response regarding content? Only answer with "true" or "false". 
Just use one of these two words (true/false) and do not elaborate.
"""
counter: int = 0

#use regular chat llm as evaluation llm no 1
evaluation_llm1: Model = Model(model="llama3")
evaluation_llm2: Model = Model(model="phi3:mini")
evalutaion_llm3: Model = Model(model="mistral")

evaluation_llms = [evaluation_llm1, evaluation_llm2, evalutaion_llm3]

#Using sources is not necessary in comparison
def query_rag_no_sources(query_text) -> str:
    db = db_helper.get_db()

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    answer: str = llm_model.generate_answer(context_text, query_text)


    return answer

def query_judging_model(evalutaion_llm: Model, expected_answer: str, actual_answer: str, question: str):
    evalutaion_llm.set_template(test_template)

    evaluation = evalutaion_llm.generate_answer_for_evaluation(question, expected_answer, actual_answer)

    print("\nmodel evaluation: \n", evaluation)

    evalutaion_llm.reset_template()

    evaluation = evaluation.replace(" ", "").lower()
    if evaluation == "true":
        return True
    elif evaluation == "false":
        return False
    #In case the question could not be answered, we return None, we count this as an undesirable case always
    #We many change and decide to track the undecided answers later
    else:
        return None


def test_model(question: str, expected_answer: str) -> bool | None:
    global counter
    actual_answer = query_rag_no_sources(question)

    eval_false_answers = 0
    eval_true_answers = 0

    for evaluation_llm in evaluation_llms:
        #print("\n####model name####\n",evaluation_llm.get_model())
        result = query_judging_model(evalutaion_llm=evaluation_llm, actual_answer=actual_answer, expected_answer=expected_answer, question=question)
        #print("corresponding result: ", result)
        if result == True:
            eval_true_answers += 1
        elif result == False:
            eval_false_answers += 1
        #else None was returned, answer is not counted

    evaluation = None #None in case of tie
    if eval_true_answers > eval_false_answers:
        evaluation = True
    elif eval_true_answers < eval_false_answers:
        evaluation = False

    print(f"{"-"*50}\nTest Case Number: {counter}\nQuestion: {question}\nActual Answer: {actual_answer}\nExpected Answer: {expected_answer}\nEvaluation: {evaluation}\nNumber of true evaluations:{eval_true_answers}, Number of false evaluations:{eval_false_answers}\n{"-"*50}\n\n")

    #Track test cases number
    counter += 1

    return evaluation

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

    test_loop()