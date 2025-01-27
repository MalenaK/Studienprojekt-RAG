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
from langchain_core.messages import RemoveMessage

"""
module evaluation_system
Provides helper functions to run the automated tests using evaluation.py.
"""

test_template = """
Question: {question}
Expected Response: {expected_answer}
Actual Response: {actual_answer}

Does the actual response match the expected Response regarding content? Only answer with "true", "no context" or "false". If the actual response states that it can not provide an answer due to missing context you must respond with "no context"".
"""
    
class EvalState(MessagesState):
    """
       Represents the state of the evaluation process.

       Attributes
       ----------
       question : str
           The current test case question.
       path_to_testresults : str
           The path where test results are saved.
       case_counter : int
           The number of test cases processed so far.
       expected_answer : str
           The expected answer for the current test case.
       evaluation : str
           The evaluation result for the current test case ("true", "false", or "noc").
       current_neg_i : int
           The index of the current negative test case being evaluated.
       current_pos_i : int
           The index of the current positive test case being evaluated.
       num_test_cases : int
           The total number of test cases.
       accuracy : int
           The accuracy percentage of the model.
       false_positive_rate : int
           The false positive rate percentage.
       false_negative_rate : int
           The false negative rate percentage.
       false_positives : int
           The count of false positive cases.
       false_negatives : int
           The count of false negative cases.
       no_context_rate : int
           The percentage of cases where the model provided no context.
       no_context_on_positive : int
           The count of "no context" responses for positive test cases.
       no_context_on_negative : int
           The count of "no context" responses for negative test cases.
    """
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


def evaluation_setup(state: EvalState) -> dict:
    """
    Sets up the environment for evaluation, including creating directories and initializing metrics.

    Parameters
    ----------
    state : EvalState
        The initial state of the evaluation process.

    Returns
    -------
    dict
        A dictionary with updated state values, including paths and metrics.
    """
    #make test result file
    test_folder = TEST_RESULT_FOLDER
    os.makedirs(test_folder, exist_ok=True)
    test_folder = f"{test_folder}/{llm_model.get_model()}---{get_embedding_function().model}" #always Language model followed by embedding seperated by ---
    # Illegal characters like : are replaced by -
    test_folder = test_folder.replace(':', '-')
    path_to_testresults = f"{test_folder}/testlog.txt"
    os.makedirs(test_folder, exist_ok=True)

    with open(path_to_testresults, 'w') as log_file:
        log_file.write("") #clear file

    return {"path_to_testresults": path_to_testresults, "current_pos_i": 0, "current_neg_i": 0, "case_counter": 0, "num_test_cases": len(positive_test_cases) + len(negative_test_cases),
            "accuracy": 0, "false_positive_rate":0, "false_negative_rate": 0, "false_positives": 0, "false_negatives":0, "no_context_rate":0, "no_context_on_positive":0, "no_context_on_negative":0}

def load_pos_question(state: EvalState) -> dict:
    """
    Loads the next positive test case question and updates the state.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with the next positive test case and expected answer.
    """
    question = positive_test_cases[state["current_pos_i"]][0]
    expected_answer = positive_test_cases[state["current_pos_i"]][1]
    next_i = state["current_pos_i"] + 1
    return {"question": question, "current_pos_i": next_i, "expected_answer": expected_answer, "messages": question}

def load_neg_question(state: EvalState) -> dict:
    """
    Loads the next negative test case question and updates the state.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with the next negative test case and expected answer.
        """
    question = negative_test_cases[state["current_neg_i"]][0]
    expected_answer = negative_test_cases[state["current_neg_i"]][1]
    next_i = state["current_neg_i"] + 1
    return {"question": question, "current_neg_i": next_i, "expected_answer": expected_answer, "messages": question}

def log(state: EvalState):
    """
    Logs the evaluation results for the current test case to a log.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.
    """
    print(f"Test Progress: {state["case_counter"]}/{state["num_test_cases"]} questions done.")
    message = f"{'-' * 50}\nTest Case Number: {state["case_counter"]}\nQuestion: {state["question"]}\nActual Answer: {state["messages"][-1].content}\nExpected Answer: {state["expected_answer"]}\nEvaluation: {state["evaluation"]}\n{'-' * 50}\n\n"
    #print(message)
    with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def evaluate(state: EvalState) -> dict:
    """
    Evaluates the model's response against the expected answer using a predefined template. See ollama_model.py.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with the evaluation result and incremented case counter.
    """
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
def update_stats_for_pos(state: EvalState) -> dict:
    """
    Updates statistics for positive test cases.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with adjusted statistics for positive cases.
    """
    no_context_on_pos = state["no_context_on_positive"]
    false_pos = state["false_positives"]
    if state["evaluation"] == "noc":
        no_context_on_pos += 1

    if state["evaluation"] == "false":
        false_pos += 1

    return {"no_context_on_positive": no_context_on_pos, "false_positives": false_pos}

#update stats for negative test cases
def update_stats_for_neg(state: EvalState) -> dict:
    """
    Updates statistics for negative test cases.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with adjusted statistics for negative cases.
    """
    no_context_on_neg = state["no_context_on_negative"]
    false_neg = state["false_negatives"]
    if state["evaluation"] == "noc":
        no_context_on_neg += 1

    if state["evaluation"] == "true":
        false_neg += 1

    return {"no_context_on_negative": no_context_on_neg, "false_negatives": false_neg}

def calc_stats(state: EvalState) -> dict:
    """
    Calculates overall evaluation metrics, including accuracy and error rates.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with calculated metrics.
    """
    no_context = state["no_context_on_negative"] + state["no_context_on_positive"]
    num_correct_answers = state["num_test_cases"] - state["false_negatives"] - state["false_positives"] - no_context

    accuracy = 100 * (num_correct_answers / state["num_test_cases"])
    false_positive_rate = 100*(state["false_positives"]/len(positive_test_cases))
    false_negative_rate = 100*(state["false_negatives"]/len(negative_test_cases))
    no_context_rate = 100*(no_context/state["num_test_cases"])

    return {"accuracy": accuracy, "false_negative_rate": false_negative_rate, "false_positive_rate": false_positive_rate, "no_context_rate": no_context_rate}

def plot_bar_chart(state: EvalState):
    """
    Generates a bar chart summarizing the evaluation results.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.
    """
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
    # Extract the directory part first since path_to_results points to a txt file -D
    test_results_dir = os.path.dirname(state["path_to_testresults"])
    bar_chart_path = os.path.join(test_results_dir, "bar_chart.png")

    # For additional safety use this
    os.makedirs(test_results_dir, exist_ok=True)

    plt.savefig(bar_chart_path)
    plt.close()

#Attention, in this confusion matrix we display no context just as a false prediction however we do state the total amount of no context entries separately as text!
def plot_confusion_matrix(state: EvalState):
    """
    Generates a confusion matrix summarizing the evaluation results.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.
    """
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

    #See comments for barchart
    test_results_dir = os.path.dirname(state["path_to_testresults"])
    confusion_matrix_path = os.path.join(test_results_dir, "confusion_matrix.png")

    os.makedirs(test_results_dir, exist_ok=True)

    plt.savefig(confusion_matrix_path, bbox_inches="tight")
    plt.close()

#method for conditional edge
def done_with_tests(state: EvalState) -> bool:
    """
    Checks whether all test cases have been evaluated.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    bool
        True if all test cases are done, False otherwise.
     """
    return (state["current_pos_i"] >= len(positive_test_cases)) and state["current_neg_i"] >= len(negative_test_cases)

#method for conditional edge
def done_with_pos(state: EvalState) -> bool:
    """
    Checks whether all positive test cases have been evaluated.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    bool
        True if all positive test cases are done, False otherwise.
    """
    return state["current_pos_i"] >= len(positive_test_cases)

def delete_messages(state: EvalState):
    """
    Deletes all messages from the state.

    Parameters
    ----------
    state : EvalState
        The current state of the evaluation process.

    Returns
    -------
    dict
        Updated state with messages removed.
    """
    messages = state["messages"]
    return {"messages": [RemoveMessage(id=m.id) for m in messages]}