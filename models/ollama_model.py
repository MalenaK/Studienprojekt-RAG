"""
module ollama_model
Module to interact with a local LLM.

This module is based on Ollama. It contains the model class which can be used to generate answers given some context.
To generate the answers you may use any Ollama model, see https://ollama.com/library?sort=popular for reference.
"""

from typing import List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

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
     generate_answer_with_history(context_text: str, conversation_messages: List[str]) -> str
        Generates an answer based on the context and a history of conversation messages.
    invoke_with_toolcall(tool, messages) -> str
        Invokes the model with a tool and a list of messages.
    generate_answer_for_evaluation(question: str, expected_answer: str, actual_answer: str) -> str
        Generates an answer for evaluation purposes based on a question, expected answer, and actual answer.
        Only to be used by evaluation.py!
    change_template(new_template: str) -> None
        Changes the template used for generating answers.
    get_model() -> str
        Returns the name of the currently used model.
    activate_sheldon_mode() -> str
        Activates Easter Egg Sheldon mode, setting the template to the `template_sheldon`. BAZINGA!
    set_template(template: str) -> None
        Sets a specific template for generating answers.
    reset_template() -> None
        Resets the template to the default `template_standard`.
    """
    template: str = ""

    template_standard: str = """
        You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer 
        the question. If you don't know the answer, say that you 
        don't know. When provided with additional context,  please 
        add each relevant pdf and page source specified at the end of 
        each information in the context to the relevant part of your answer.
        Do NOT copy sources from the information itself, which looks like [xx]!
        Context:
        {context}
        """
    template_sheldon: str = """
    Pretend you are Sheldon from the Big Bang Theory and answer the following question based on the context but you must include at least 1 Bazinga in your answer but the more the better.
    Here is the context: 
    {context}

    Question: 
    {question}

    Answer: 
    """

    def __init__(self, model: str):
        """
        Initializes the `Model` class with the specified model. The model can be set in config/settings.py

        Parameters
        ----------
        model : str
            The name of the Ollama model to use for generating answers.
            See available models at https://ollama.com/library?sort=popular.
            We recommend  'llama3.1'.
        """
        self.model: ChatOllama = ChatOllama(model=model)
        self.set_template(self.template_standard)

    def generate_answer_with_history(self, context_text: str, conversation_messages: List[str]) -> str:
        """
        Generates an answer based on the context and conversation history.

        Parameters
        ----------
        context_text : str
            The context to provide to the model.
        conversation_messages : List[str]
            A list of previous conversation messages.

        Returns
        -------
        str
        The generated answer.
        """
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(self.template)
        system_message_content: str = prompt_template.format(context=context_text)
        prompt = [SystemMessage(system_message_content)] + conversation_messages

        # print(f"prompting the LLM with: \n{prompt}") #disabled clutters testing
        answer: str = self.model.invoke(prompt)
        return answer
    
    def invoke_with_toolcall(self, tool, messages):
        """
        Invokes the model with a tool and a list of messages.

        Parameters
        ----------
        tool : ?
            The tool to bind and use with the model.
        messages : ?
            A list of messages to provide as input to the model.

        Returns
        -------
        ?
            The generated output after invoking the tool.
        """
        bound_model = self.model.bind_tools([tool])
        return bound_model.invoke(messages)
    
    def generate_answer_for_evaluation(self, question: str, expected_answer: str, actual_answer: str) -> str:
        """
        Generates an answer for evaluation purposes. Used by evaluation.py

        Parameters
        ----------
        question : str
            The question provided for the evaluation.
        expected_answer : str
            The expected answer for comparison.
        actual_answer : str
            The actual answer generated for evaluation.

        Returns
        -------
        str
            The generated answer for evaluation.
        """
        prompt_template: ChatPromptTemplate = ChatPromptTemplate.from_template(self.template)
        prompt: str = prompt_template.format(question=question, expected_answer=expected_answer, actual_answer=actual_answer)
        #print(f"prompting the LLM with: \n{prompt}")
        answer: str = self.model.invoke(prompt)
        return answer

    def change_template(self, new_template: str) -> None:
        """
        Changes the template used for generating answers.

        Parameters
        ----------
        new_template : str
            The new template to use.
        """
        self.template = new_template

    def get_model(self) -> str:
        """
        Retrieves the name of the currently used language  model.

        Returns
        -------
        str
            The name of the model.
        """
        return self.model.model

    def activate_sheldon_mode(self) -> str:
        """
        Activates the easter egg. BAZINGA!
        Returns
        -------
        BAAZZZIINGA!
        """
        self.template = self.template_sheldon
        return "🧠 Activating Sheldon Mode, BAZINGA ⚡"

    def set_template(self, template: str) -> None:
        """
        Sets a specific template for generating answers.

        Parameters
        ----------
        template : str
            The template to use.
        """
        self.template = template

    def reset_template(self):
        """
        Resets the template to the default `template_standard`.
        """
        self.template = self.template_standard