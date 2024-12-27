import os
from typing_extensions import Literal

import numpy as np
from models.embedding import get_embedding_function
import matplotlib.pyplot as plt
import seaborn as sns
from config.settings import TEST_RESULT_FOLDER
from tests.test_cases import positive_test_cases, negative_test_cases
from langgraph.graph import MessagesState
from rag_system.ragsystem import llm_model


test_template = """
Question: {question}
Expected Response: {expected_answer}
Actual Response: {actual_answer}

Does the actual response match the expected Response regarding content? Only answer with "true", "no context" or "false". If the actual response states that it can not provide an answer due to missing context you must respond with "no context"".
"""
    
class EvalState(MessagesState):
    question: str
    path_to_testresults: str
    case_counter: int
    expected_answer: str
    evaluation: str
    current_neg_i: int
    current_pos_i: int
    num_test_cases: int
    accuracy: int
    false_positive_rate: int
    false_negative_rate: int
    false_positives: int
    false_negatives: int 
    no_context_rate: int 
    no_context_on_positive: int 
    no_context_on_negative: int 


def evaluation_setup(state: EvalState):
    #make test result file
    test_folder = TEST_RESULT_FOLDER
    os.makedirs(test_folder, exist_ok=True)

    test_folder = f"{test_folder}/{llm_model.get_model()}---{get_embedding_function().model}" #always Language model followed by embedding seperated by ---
    path_to_testresults = f"{test_folder}/testlog.txt"
    os.makedirs(test_folder, exist_ok=True)

    with open(path_to_testresults, 'w') as log_file:
        log_file.write("") #clear file

    return {"path_to_testresults": path_to_testresults, "current_pos_i": 0, "current_neg_i": 0, "case_counter": 0, "num_test_cases": len(positive_test_cases) + len(negative_test_cases),
            "accuracy": 0, "false_positive_rate":0, "false_negative_rate": 0, "false_positives": 0, "false_negatives":0, "no_context_rate":0, "no_context_on_positive":0, "no_context_on_negative":0}

def load_pos_question(state: EvalState):
    question = positive_test_cases[state["current_pos_i"]][0]
    expected_answer = positive_test_cases[state["current_pos_i"]][1]
    next_i = state["current_pos_i"] + 1
    return {"question": question, "current_pos_i": next_i, "expected_answer": expected_answer, "messages": question}

def load_neg_question(state: EvalState):
    question = negative_test_cases[state["current_neg_i"]][0]
    expected_answer = negative_test_cases[state["current_neg_i"]][1]
    next_i = state["current_neg_i"] + 1
    return {"question": question, "current_neg_i": next_i, "expected_answer": expected_answer, "messages": question}

def log(state: EvalState):
    print(f"Test Progress: {state["case_counter"]}/{state["num_test_cases"]} questions done.")
    message = f"{'-' * 50}\nTest Case Number: {state["case_counter"]}\nQuestion: {state["question"]}\nActual Answer: {state["messages"][-1].content}\nExpected Answer: {state["expected_answer"]}\nEvaluation: {state["evaluation"]}\n{'-' * 50}\n\n"
    print(message)
    with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def evaluate(state: EvalState):
    # Change template to evaluation mode
    llm_model.set_template(test_template) #TODO: do this once?

    #Evaluate the response
    evaluation = llm_model.generate_answer_for_evaluation(question=state["question"], expected_answer=state["expected_answer"], actual_answer=state["messages"][-1].content)
    evaluation = evaluation.content

    llm_model.reset_template()

    evaluation = evaluation.lower()
    eval_result = ""
    if evaluation == "true":
        eval_result = "true"
    elif evaluation == "false":
        eval_result = "false"
    #If there was insufficient context to answer the question  we return noc (no context)
    else:
        eval_result =  "noc"
    case_counter = state["case_counter"] + 1
    return {"evaluation": eval_result, "case_counter": case_counter}

#update stats for positive test cases
def update_stats_for_pos(state: EvalState):
    no_context_on_pos = state["no_context_on_positive"]
    false_pos = state["false_positives"]
    if state["evaluation"] == "noc":
        no_context_on_pos += 1

    if state["evaluation"] == "false":
        false_pos += 1

    return {"no_context_on_positive": no_context_on_pos, "false_positives": false_pos}

#update stats for negative test cases
def update_stats_for_neg(state: EvalState):
    no_context_on_neg = state["no_context_on_negative"]
    false_neg = state["false_negatives"]
    if state["evaluation"] == "noc":
        no_context_on_neg += 1

    if state["evaluation"] == "true":
        false_neg += 1

    return {"no_context_on_negative": no_context_on_neg, "false_negatives": false_neg}

def calc_stats(state: EvalState):
    no_context = state["no_context_on_negative"] + state["no_context_on_positive"]
    num_correct_answers = state["num_test_cases"] - state["false_negatives"] - state["false_positives"] - no_context

    accuracy = 100 * (num_correct_answers / state["num_test_cases"])
    false_positive_rate = 100*(state["false_positives"]/len(positive_test_cases))
    false_negative_rate = 100*(state["false_negatives"]/len(negative_test_cases))
    no_context_rate = 100*(no_context/state["num_test_cases"])

    return {"accuracy": accuracy, "false_negative_rate": false_negative_rate, "false_positive_rate": false_positive_rate, "no_context_rate": no_context_rate}

def plot_bar_chart(state: EvalState):
    labels = ['Total Accuracy', 'False Positives', 'False Negatives', 'No Context']
    values = state["accuracy"], state["false_positive_rate"], state["false_negative_rate"], state["no_context_rate"]
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
    bar_chart_path = os.path.join(state["p"], "bar_chart.png")
    plt.savefig(bar_chart_path)
    plt.close()

#Attention, in this confusion matrix we display no context just as a false prediction however we do state the total amount of no context entries separately as text!
def plot_confusion_matrix(state: EvalState):
    true_positives = len(positive_test_cases) - (state["false_positives"] + state["no_context_on_positive"])
    true_negatives = len(negative_test_cases) - (state["false_negatives"]+state["no_context_on_negative"])

    confusion_matrix = np.array([
        [true_positives, state["false_negatives"]],  # Positive cases
        [state["false_positives"], true_negatives],  # Negative cases
    ])

    labels = ['Positive', 'Negative']

    plt.figure(figsize=(7, 6))
    sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix of Positives and Negatives')

    no_context_text = f"Total of No Context: {state["no_context_on_positive"] + state["no_context_on_negative"]}\nNo Context on Positive Test: {state["no_context_on_positive"]}\nNo Context on Negative Test: {state["no_context_on_negative"]}"
    #Put text into lower right corner
    plt.figtext(0.95, -0.15, no_context_text, ha="right", fontsize=12, color="black")


    confusion_matrix_path = os.path.join(state["path_to_testresults"], "confusion_matrix.png")
    plt.savefig(confusion_matrix_path, bbox_inches="tight")
    plt.close()

#method for conditional edge
def done_with_tests(state: EvalState):
    return (state["current_pos_i"] >= len(positive_test_cases)) and state["current_neg_i"] >= len(negative_test_cases)

#method for conditional edge
def done_with_pos(state: EvalState):
    return state["current_pos_i"] >= len(positive_test_cases)