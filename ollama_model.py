"""
Model to interact with a local LLM.
This module is based on Ollama. It contains the model class which can be used to generate answers given some context.
To generate the answers you may use any Ollama model, see https://ollama.com/library?sort=popular for reference.
"""

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pandas.core.window.doc import template_returns


class Model:
    """
    Model class that can be used to generate answers.

    Attributes
    ----------
    template : str
        default string used to generate answers. It provides a template that is fed to the LLM.
    template_sheldon : str
        Trigger this easter egg template by entering the prompt "Bazinga". Template used to generate answers.
        It provides a template that is fed to the LLM.

    Methods
    -------
    generate_answer(self, prompt: str) -> str
        Generates answer based on prompt using model.


    """
    template: str = ""

    template_standard: str = """
    Answer the question based on the following context:
    {context}
    
    Add each relevant pdf and page source specified at the end of each information in the context to the relevant part of your answer. Do NOT copy sources from the information itself, which looks like [xx]!
    ---

    Question: {question}

    ---

    Answer: 
    """

    template_sheldon: str = """
    Pretend you are Sheldon from the Big Bang Theory and answer the following question based on the context but you must include at least 1 Bazinga in your answer but the more the better.
    Here is the context: 
    {context}

    Question: 
    {question}

    Answer: 
    """

    def __init__(self, model: str = "llama3"):
        """
        Constructs all necessary attributes for the model.

        Parameters
        ----------
        model: str, optional
            model that will be used for generating answers. Change the model using model parameter, see available models here https://ollama.com/library?sort=popular. Default is 'llama3' by Meta

        Returns
        -------
        None
        """
        self.model: OllamaLLM = OllamaLLM(model=model)
        self.set_template(self.template_standard)


    def generate_answer(self, context_text: str, query: str) -> str:
        """
        Generates answer from context retrieved by RAG and Query by user

        Parameters
        ----------
        context_text: str
            context that was found by RAG
        query: str
            user question used to query the RAG and Model

        Returns
        -------
        str
            Output of model, i.e. generated answer
        """
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(self.template)
        prompt: str = prompt_template.format(context=context_text, question=query)
        #print(f"prompting the LLM with: \n{prompt}") #disabled clutters testing
        answer: str = self.model.invoke(prompt)
        return answer
    
    def generate_answer_for_evaluation(self, question: str, expected_answer: str, actual_answer: str) -> str:
        """
        Generates answer from context retrieved by RAG and Query by user

        Parameters
        ----------
        context_text: str
            context that was found by RAG
        query: str
            user question used to query the RAG and Model

        Returns
        -------
        str
            Output of model, i.e. generated answer
        """
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(self.template)
        prompt: str = prompt_template.format(question=question, expected_answer=expected_answer, actual_answer=actual_answer)
        print(f"prompting the LLM with: \n{prompt}")
        answer: str = self.model.invoke(prompt)
        return answer

    def change_template(self, new_template: str) -> None:
        """
        Allows the caller to change the template the Ai uses to generate answers
        Parameters
        ----------
        new_template: str
            template that replaces the old one

        Returns
        -------
        None
        """
        self.template = new_template

    def get_model(self) -> str:
        return self.model.model

    def activate_sheldon_mode(self) -> str:
        self.template = self.template_sheldon
        return "🧠 Activating Sheldon Mode, BAZINGA ⚡"

    def set_template(self, template: str) -> None:
        self.template = template

    def reset_template(self):
        self.template = self.template_standard