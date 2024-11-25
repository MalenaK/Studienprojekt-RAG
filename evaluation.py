import os
import sys

import numpy as np
from numpy.ma.core import negative
from pypika.enums import Boolean
from sympy import false

from main import *
from test_cases import *


import matplotlib.pyplot as plt
import seaborn as sns

#Maybe improve this by actually using 3 models and making it a democratic decision if an answer was correct or not

test_template = """
Question: 
Expected Response: {context}
Actual Response: {question}

Does the actual response match the expected Response regarding content? Only answer with "true", "no context" or "false". If the actual response states that it can not provide an answer due to missing context you must respond with "no context"".
"""
counter: int = 0


def log(message):
    # Write to the log file
    with open(f'./tests/{llm_model.get_model()}---{get_embedding_function().model}/testlog.txt', 'a') as log_file:
        log_file.write(message + '\n')

#Using sources is not necessary in comparison
def query_rag_no_sources(query_text) -> str:
    db = db_helper.get_db()

    #search in the db
    results = db.similarity_search_with_score(query_text, k=5)
    #print(f"Search Results: {results}")  # Debug: Print the results to check

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    answer: str = llm_model.generate_answer(context_text, query_text)


    return answer



def test_model(question: str, expected_answer: str) -> bool | str:
    global counter
    actual_answer = query_rag_no_sources(question)
    # Change template to evaluation mode
    llm_model.set_template(test_template)

    #Evaluate the response
    context = f"Question: {question}\nExpected Response: {expected_answer}"
    evaluation = llm_model.generate_answer(context, actual_answer)
    #print(f"{"-"*50}\nTest Case Number: {counter}\nQuestion: {question}\nActual Answer: {actual_answer}\nExpected Answer: {expected_answer}\nEvaluation: {evaluation}\n{"-"*50}\n\n")
    log(f"{'-' * 50}\nTest Case Number: {counter}\nQuestion: {question}\nActual Answer: {actual_answer}\nExpected Answer: {expected_answer}\nEvaluation: {evaluation}\n{'-' * 50}\n\n")

    #Track test cases number
    counter += 1
    llm_model.reset_template()

    evaluation = evaluation.lower()

    if evaluation == "true":
        return True
    elif evaluation == "false":
        return False
    #If there was insufficient context to answer the question  we return noc (no context)
    else:
        return "noc"


def plot_bar_chart(accuracy, false_positive_rate, false_negative_rate, no_context_rate, current_test):
    labels = ['Total Accuracy', 'False Positives', 'False Negatives', 'No Context']
    values = [accuracy, false_positive_rate, false_negative_rate, no_context_rate]
    colors = ['#4CAF50', '#FF5733', '#FFC300', '#3498db']

    plt.figure(figsize=(7, 6)) #tbd what size is good for putting into a report
    plt.bar(labels, values, color=colors)
    plt.title('Test Results Overview')
    plt.ylabel('Percentage (%)')
    plt.ylim(0, 100)

    # Annotate each bar with percentage values
    for i, v in enumerate(values):
        plt.text(i, v + 2, f"{v:.2f}%", ha='center')

    # Save the bar chart
    bar_chart_path = os.path.join(current_test, "bar_chart.png")
    plt.savefig(bar_chart_path)
    plt.close()

#Attention, in this confusion matrix we display no context just as a false prediction however we do state the total amount of no context entries separately as text!
def plot_confusion_matrix(false_positives, false_negatives, no_context_on_positive, no_context_on_negative, current_test):
    true_positives = len(positive_test_cases) - (false_positives+no_context_on_positive)
    true_negatives = len(negative_test_cases) - (false_negatives+no_context_on_negative)

    confusion_matrix = np.array([
        [true_positives, false_negatives],  # Positive cases
        [false_positives, true_negatives],  # Negative cases
    ])

    labels = ['Positive', 'Negative']

    plt.figure(figsize=(7, 6))
    sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix of Positives and Negatives')

    no_context_text = f"Total of No Context: {no_context_on_positive+ no_context_on_negative}\nNo Context on Positive Test: {no_context_on_positive}\nNo Context on Negative Test: {no_context_on_negative}"
    #Put text into lower right corner
    plt.figtext(0.95, -0.15, no_context_text, ha="right", fontsize=12, color="black")


    confusion_matrix_path = os.path.join(current_test, "confusion_matrix.png")
    plt.savefig(confusion_matrix_path, bbox_inches="tight")
    plt.close()


def test_loop():
    no_context_on_positive = 0
    no_context_on_negative = 0
    test_idx = 0 #Used to track the progress of the test
    #Normal tests that should return true
    false_positives = 0
    num_test_cases = len(positive_test_cases) + len(negative_test_cases)
    test_tracker = num_test_cases // 20
    test_folder = "./tests"
    os.makedirs(test_folder, exist_ok=True)

    current_test = f"{test_folder}/{llm_model.get_model()}---{get_embedding_function().model}" #always Language model followed by embedding seperated by ---
    os.makedirs(current_test, exist_ok=True)
    print("Starting tests...")
    for test in positive_test_cases:
        test_idx += 1
        if test_idx % test_tracker == 0:
            progress_percentage = (test_idx / num_test_cases) * 100
            progress_bar = '=' * (test_idx * 40 // num_test_cases) + ' ' * (40 - (test_idx * 40 // num_test_cases))
            print(f"Test Progress: [{progress_bar}] {progress_percentage:.2f}% ({test_idx}/{num_test_cases})")

        answer = test()

        if answer == "noc": #No context
            no_context_on_positive += 1
            continue

        if answer != True:
            false_positives += 1


    #Complement tests that should return
    false_negatives = 0
    for test in negative_test_cases:
        test_idx += 1
        if test_idx % test_tracker == 0:
            progress_percentage = (test_idx / num_test_cases) * 100
            progress_bar = '=' * (test_idx * 40 // num_test_cases) + ' ' * (40 - (test_idx * 40 // num_test_cases))
            print(f"Test Progress: [{progress_bar}] {progress_percentage:.2f}% ({test_idx}/{num_test_cases})")

        answer = test()

        if answer == "noc":
            no_context_on_negative += 1
            continue

        if answer == True:
            false_negatives += 1

    no_context = no_context_on_negative + no_context_on_positive
    num_correct_answers = num_test_cases - false_negatives - false_positives - no_context

    accuracy = 100 * (num_correct_answers / num_test_cases)
    false_positive_rate = 100*(false_positives/len(positive_test_cases))
    false_negative_rate = 100*(false_negatives/len(negative_test_cases))
    no_context_rate = 100*(no_context/num_test_cases)

    # print(f"\n{"-"*100}\nTotal Accuracy: {accuracy} %\n"
    #       f"False Positive Percentage: {false_positive_rate} %\n"
    #       f"False Negative Percentage: {false_negative_rate} %\n"
    #       f"No Context Percentage: {no_context_rate}")

    log(f"\n{'-' * 100}\nTotal Accuracy: {accuracy:.2f} %\n"
        f"False Positive Percentage: {false_positive_rate:.2f} %\n"
        f"False Negative Percentage: {false_negative_rate:.2f} %\n"
        f"No Context Percentage: {no_context_rate:.2f}")

    plot_bar_chart(accuracy=accuracy, false_positive_rate=false_positive_rate, false_negative_rate=false_negative_rate, no_context_rate=no_context_rate, current_test=current_test)
    plot_confusion_matrix(false_positives=false_positives, false_negatives=false_negatives, no_context_on_negative=no_context_on_negative, no_context_on_positive=no_context_on_positive, current_test=current_test)





if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    parser.add_argument("-d", "--pdf_dir", default="./data", help="Specify path to directory containing the pdfs.")

    args = parser.parse_args()
    if args.reset:
        print("Clearing Database...")
        db_helper.clear_database()

    test_dir = f'./tests/{llm_model.get_model()}---{get_embedding_function().model}'
    os.makedirs(test_dir, exist_ok=True)

    with open(f'./tests/{llm_model.get_model()}---{get_embedding_function().model}/testlog.txt', 'w') as f:  #Wipe old testlog
        f.write("")


    # Create (or update) the data store.
    update_data_store(args.pdf_dir)
    log("[START OF TEST]")
    test_loop()
    log("[END OF TEST]")

    print(f"Test is complete, see test folder: ./tests/{llm_model.get_model()}---{get_embedding_function().model}")
