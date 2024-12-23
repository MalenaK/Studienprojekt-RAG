import os
from typing import List
from typing_extensions import Literal

import numpy as np
from models.embedding import get_embedding_function
from rag_system.ragsystem import RAGpipeline, State
import matplotlib.pyplot as plt
import seaborn as sns

test_template = """
Question: {question}
Expected Response: {expected_answer}
Actual Response: {actual_answer}

Does the actual response match the expected Response regarding content? Only answer with "true", "no context" or "false". If the actual response states that it can not provide an answer due to missing context you must respond with "no context"".
"""
    
class EvalState(State):
    path_to_testresults: str
    case_counter: int
    expected_answer: str
    evaluation: str
    current_neg_i: int
    current_pos_i: int

class Stats:
    num_test_cases: int = 0
    accuracy: int = 0
    false_positive_rate: int = 0
    false_negative_rate: int = 0
    false_positives: int = 0
    false_negatives: int = 0
    no_context_rate: int = 0
    no_context_on_positive: int = 0
    no_context_on_negative: int = 0

class RAGEvalPipeline(RAGpipeline):  
    def __init__(self, positive_test_cases, negative_test_cases):
        super().__init__()
        self.stats: Stats = Stats()
        self.positive_test_cases: List[str] = positive_test_cases
        self.negative_test_cases: List[str] = negative_test_cases

    def evaluation_setup(self, state: EvalState):
        self.stats.num_test_cases = len(self.positive_test_cases) + len(self.negative_test_cases)

        #make test result file
        test_folder = "./tests/test_results"
        os.makedirs(test_folder, exist_ok=True)

        test_folder = f"{test_folder}/{self.llm_model.get_model()}---{get_embedding_function().model}" #always Language model followed by embedding seperated by ---
        path_to_testresults = f"{test_folder}/testlog.txt"
        os.makedirs(test_folder, exist_ok=True)

        with open(path_to_testresults, 'w') as log_file:
            log_file.write("") #clear file

        return {"path_to_testresults": path_to_testresults, "current_pos_i": 0, "current_neg_i": 0, "case_counter": 0}
    
    def load_pos_question(self, state: EvalState):
        question = self.positive_test_cases[state["current_pos_i"]][0]
        expected_answer = self.positive_test_cases[state["current_pos_i"]][1]
        return {"question": question, "current_pos_i": state["current_pos_i"] + 1, "expected_answer": expected_answer}
    
    def load_neg_question(self, state: EvalState):
        question = self.negative_test_cases[state["current_neg_i"]][0]
        expected_answer = self.negative_test_cases[state["current_neg_i"]][1]
        return {"question": question, "current_neg_i": state["current_neg_i"] + 1, "expected_answer": expected_answer}

    def log(self, state: EvalState):
        print(f"Test Progress: {state["case_counter"]}/{len(self.positive_test_cases)+len(self.negative_test_cases)} questions done.")
        message = f"{'-' * 50}\nTest Case Number: {state["case_counter"]}\nQuestion: {state["question"]}\nActual Answer: {state["answer"]}\nExpected Answer: {state["expected_answer"]}\nEvaluation: {state["evaluation"]}\n{'-' * 50}\n\n"
        print(message)
        with open(state["path_to_testresults"], 'a', encoding='utf-8') as log_file:
            log_file.write(message + '\n')

    def evaluate(self, state: EvalState):
        # Change template to evaluation mode
        self.llm_model.set_template(test_template) #TODO: do this once?

        #Evaluate the response
        evaluation = self.llm_model.generate_answer_for_evaluation(question=state["question"], expected_answer=state["expected_answer"], actual_answer=state["answer"])

        self.llm_model.reset_template()

        evaluation = evaluation.lower()
        eval_result = ""
        if evaluation == "true":
            eval_result = "true"
        elif evaluation == "false":
            eval_result = "false"
        #If there was insufficient context to answer the question  we return noc (no context)
        else:
            eval_result =  "noc"

        return {"evaluation": eval_result, "case_counter": state["case_counter"] + 1}
    
    #update stats for positive test cases
    def update_stats_for_pos(self, state: EvalState):
        if state["evaluation"] == "noc":
            self.stats.no_context_on_positive += 1

        if state["evaluation"] == "false":
            self.stats.false_positives += 1

    #update stats for negative test cases
    def update_stats_for_neg(self, state: EvalState):
        if state["evaluation"] == "noc":
            self.stats.no_context_on_negative += 1

        if state["evaluation"] == "true":
            self.stats.false_negatives += 1
    
    def calc_stats(self, state: EvalState):
        no_context = self.stats.no_context_on_negative + self.stats.no_context_on_positive
        num_correct_answers = self.stats.num_test_cases - self.stats.false_negatives - self.stats.false_positives - no_context

        self.stats.accuracy = 100 * (num_correct_answers / self.stats.num_test_cases)
        self.stats.false_positive_rate = 100*(self.stats.false_positives/len(self.positive_test_cases))
        self.stats.false_negative_rate = 100*(self.stats.false_negatives/len(self.negative_test_cases))
        self.stats.no_context_rate = 100*(no_context/self.stats.num_test_cases)

    def plot_bar_chart(self, state: EvalState):
        labels = ['Total Accuracy', 'False Positives', 'False Negatives', 'No Context']
        values = [self.stats.accuracy, self.stats.false_positive_rate, self.stats.false_negative_rate, self.stats.no_context_rate]
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
    def plot_confusion_matrix(self, state: EvalState):
        true_positives = len(self.positive_test_cases) - (self.stats.false_positives + self.stats.no_context_on_positive)
        true_negatives = len(self.negative_test_cases) - (self.stats.false_negatives+self.stats.no_context_on_negative)

        confusion_matrix = np.array([
            [true_positives, self.stats.false_negatives],  # Positive cases
            [self.stats.false_positives, true_negatives],  # Negative cases
        ])

        labels = ['Positive', 'Negative']

        plt.figure(figsize=(7, 6))
        sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues",
                    xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.title('Confusion Matrix of Positives and Negatives')

        no_context_text = f"Total of No Context: {self.stats.no_context_on_positive + self.stats.no_context_on_negative}\nNo Context on Positive Test: {self.stats.no_context_on_positive}\nNo Context on Negative Test: {self.stats.no_context_on_negative}"
        #Put text into lower right corner
        plt.figtext(0.95, -0.15, no_context_text, ha="right", fontsize=12, color="black")


        confusion_matrix_path = os.path.join(state["path_to_testresults"], "confusion_matrix.png")
        plt.savefig(confusion_matrix_path, bbox_inches="tight")
        plt.close()

    #method for conditional edge
    def start_next_iteration_or_end(self, state: EvalState) -> Literal["calc_stats", "load_pos_question", "load_neg_question"]:
        if (state["current_pos_i"] >= len(self.positive_test_cases)) and state["current_neg_i"] >= len(self.negative_test_cases):
            return "calc_stats"
        if state["current_pos_i"] >= len(self.positive_test_cases):
            return "load_pos_question"
        return "load_neg_question"
    
    #method for conditional edge
    def done_with_pos(self, state: EvalState):
        return state["current_pos_i"] >= len(self.positive_test_cases)