import argparse
import os
from typing import List

from models.embedding import get_embedding_function
from rag_system.ragsystem import RAGpipeline, State
from tests import test_cases


class RunAndSaveState(State):
    path_to_testresults: str
    test_cases_list: List[str]
    current_i: int

class RAGRunSavePipeline(RAGpipeline):
    #additional setup for running run and save
    #normal setup method needs to be executed beforehand

    #overwrite get_parser_args from RAGpipeline to parse additional args
    def get_parser_args(self):
        print("inside parser args")
        parser = argparse.ArgumentParser()

        parser.add_argument("-ra", "--reset_all", action="store_true", help="Reset the whole database.")
        parser.add_argument("-rc", "--reset_collection", action="store_true", help="Reset the collection specified in pdf_dir.")
        parser.add_argument("-d", "--pdf_dir", default="./data/data_basic", help="Specify path to directory containing the pdfs.")
        parser.add_argument("-tc", "--test_cases_name", required=True, help="Specify name of test cases list.")

        self.args = parser.parse_args()

    def run_and_save_setup(self, state: RunAndSaveState):
        print("inside run and save setup")
        test_folder = "./tests/test_results/complex_testcases"
        os.makedirs(test_folder, exist_ok=True)

        data_name = self.pdf_dir.replace("/","").replace("\\", "").replace(" ","").replace(".","")
        model_name = self.llm_model.get_model()
        embedding_name = get_embedding_function().model
        test_cases_name = self.args.test_cases_name
        file_name = f"{model_name}---{embedding_name}---{data_name}---{test_cases_name}.txt"

        relative_path = f"{test_folder}/{file_name}"

        with open(relative_path, 'w') as log_file:
            log_file.write("") #clear file

        test_cases_list = test_cases.test_cases_names_to_list[test_cases_name]

        return {"path_to_testresults": relative_path, "test_cases_list": test_cases_list, "current_i": 0}
    
    def log(self, state: RunAndSaveState):
        print("inside log")
        message = f"Question: {state["question"]}\n{state["answer"]}\n{"-"*50}"
        print(message)
        with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
            log_file.write(message + '\n')

    def load_question(self, state: RunAndSaveState):
        print("inside load question")
        question = state["test_cases_list"][state["current_i"]]
        next_i = state["current_i"] + 1
        print(f"testing progess: question {next_i}/{len(state["test_cases_list"])}") #give user feedback on progess
        return { "question": question, "current_i": next_i}
    
    def all_tests_done(self, state: RunAndSaveState):
        print("all tests done?", state["current_i"] >= len(state["test_cases_list"]))
        return state["current_i"] >= len(state["test_cases_list"])
        