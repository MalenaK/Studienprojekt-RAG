import os
from typing import List

from models.embedding import get_embedding_function
from langgraph.graph import MessagesState
from tests import test_cases
from config.settings import TEST_RESULT_NOEVAL_FOLDER
from rag_system.ragsystem import doc_handler, llm_model


class RunAndSaveState(MessagesState):
    path_to_testresults: str
    test_cases_list: List[str]
    current_i: int
    question: str

def run_and_save_setup(state: RunAndSaveState):
    test_folder = TEST_RESULT_NOEVAL_FOLDER
    os.makedirs(test_folder, exist_ok=True)

    data_name = doc_handler.get_pdf_dir().replace("/","").replace("\\", "").replace(" ","").replace(".","")
    model_name = llm_model.get_model()
    embedding_name = get_embedding_function().model
    test_cases_name = "c1xx" #to enter by developer!!
    file_name = f"{model_name}---{embedding_name}---{data_name}---{test_cases_name}.txt"

    relative_path = f"{test_folder}/{file_name}"

    with open(relative_path, 'w') as log_file:
        log_file.write("") #clear file

    test_cases_list = test_cases.test_cases_names_to_list[test_cases_name]

    return {"path_to_testresults": relative_path, "test_cases_list": test_cases_list, "current_i": 0}

def log(state: RunAndSaveState):
    message = f"Question: {state["question"]}\n{state["messages"][-1].content}\n{"-"*50}"
    print(message)
    with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
        log_file.write(message + '\n')

def load_question(state: RunAndSaveState):
    #todo: delete past history
    question = state["test_cases_list"][state["current_i"]]
    next_i = state["current_i"] + 1
    print(f"testing progess: question {next_i}/{len(state["test_cases_list"])}") #give user feedback on progess
    return { "question": question, "current_i": next_i, "messages": question}

def all_tests_done(state: RunAndSaveState):
    print("all tests done?", state["current_i"] >= len(state["test_cases_list"]))
    return state["current_i"] >= len(state["test_cases_list"])
    