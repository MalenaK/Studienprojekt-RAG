import os
from typing import List

from models.embedding import get_embedding_function
from langgraph.graph import MessagesState
from tests import test_cases
from config.settings import TEST_RESULT_NOEVAL_FOLDER
from rag_system.ragsystem import doc_handler, llm_model

"""
module rag_run_save_system
Provides helper functions to run the complex tests using run_and_safe.py.
It is important that you set test_cases_name here! See run_and_save_setup in this file.
"""
class RunAndSaveState(MessagesState):
    """
      Used by run_and_save to run the complex test cases. Note that you should write the test_cases manually into run_and_save_setup in this file.

      Attributes
      ----------
      path_to_testresults : str
          The path where test results will be saved.
      test_cases_list : List[str]
          A list of test case questions to be executed. Set in run_and_save.
      current_i : int
          The index of the current test case being executed.
      question : str
          The current test case question.
      """
    path_to_testresults: str
    test_cases_list: List[str]
    current_i: int
    question: str

def run_and_save_setup(state: RunAndSaveState) -> dict:
    """
    Sets up the environment for running test cases and saving results.
    Here you set the cases that shall be run. Also run run_and_save with the according flag.
    If test_cases_name = c4xx then use -d ../data/data_c4xx to run run_and_safe.py

    Parameters
    ----------
    state : RunAndSaveState
        The initial state of the run-and-save process.

    Returns
    -------
    dict
       A dictionary containing:
       - path_to_testresults: The path where test results will be saved.
       - test_cases_list: The list of test case questions.
       - current_i: The index of the current test case (initialized to 0).
    """
    test_folder = TEST_RESULT_NOEVAL_FOLDER
    os.makedirs(test_folder, exist_ok=True)

    data_name = doc_handler.get_pdf_dir().replace("/","").replace("\\", "").replace(" ","").replace(".","")
    model_name = llm_model.get_model()
    model_name = model_name.replace(':', '-')
    embedding_name = get_embedding_function().model
    test_cases_name = "c4xx" #to enter by developer!!
    file_name = f"{model_name}---{embedding_name}---{data_name}---{test_cases_name}.txt"

    relative_path = f"{test_folder}/{file_name}"

    with open(relative_path, 'w') as log_file:
        log_file.write("") #clear file

    test_cases_list = test_cases.test_cases_names_to_list[test_cases_name]

    return {"path_to_testresults": relative_path, "test_cases_list": test_cases_list, "current_i": 0}

def log(state: RunAndSaveState):
    """
    Logs the result of a test case to a log file.

    Parameters
    ----------
    state : RunAndSaveState
       The current state of the run-and-save process, including the question and messages.
    """
    message = f"Question: {state["question"]}\n{state["messages"][-1].content}\n{"-"*50}"
    with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def load_question(state: RunAndSaveState) -> dict:
    """
    Loads the next test case question and updates the state.

    Parameters
    ----------
    state : RunAndSaveState
        The current state of the run-and-save process.

    Returns
    -------
    dict
        A dictionary containing:
        - question: The next test case question.
        - current_i: The updated index of the current test case.
        - messages: The current test case question to be processed.
    """
    question = state["test_cases_list"][state["current_i"]]
    next_i = state["current_i"] + 1
    print(f"testing progress: question {next_i}/{len(state["test_cases_list"])}") #give user feedback on progess
    return { "question": question, "current_i": next_i, "messages": question}

def all_tests_done(state: RunAndSaveState) -> bool:
    """
    Checks whether all test cases have been executed.

    Parameters
    ----------
    state : RunAndSaveState
        The current state of the run-and-save process.

    Returns
    -------
    bool
        True if all test cases have been executed, False otherwise.
    """
    return state["current_i"] >= len(state["test_cases_list"])
    