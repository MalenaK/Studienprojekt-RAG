from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.openai import OpenAIEmbeddings
import os
from config.settings import config_embedding
"""
embedding module

functions:
- get_embedding_function: Initializes and returns an embedding function based on the specified model. 
This module contains an Ollama implementation (recommended) and an example on how to use a commercial non-local embedding like OpenAi if needed. 
The latter is commented out but can be studied in the code. 
"""


def get_embedding_function(model:str = config_embedding) -> OllamaEmbeddings:
    """
    Returns an embedding function that is set in config/settings.py.
    The possible arguments can be found here: https://ollama.com/search?c=embedding.
    We recommend using: mxbai-embed-large, other options include bge-m3, nomic-embed-text.
    Parameters
    ----------
    model: str
        The name of the embedding model that shall be used.

    Returns
    -------
    OllamaEmbeddings
        The embedding function.
    """
    embeddings: OllamaEmbeddings = OllamaEmbeddings(model=model)
    return embeddings

#def get_embedding_function(model:str = config_embedding) -> OpenAIEmbeddings:
# """
# Returns an embedding function that is set in config/settings.py. Visit OpenAI's website for possible arguments.
# We recommend using text-embedding-3-small.
#
# Parameters
# ----------
# model: str
#     The name of the OpenAI embedding model to be used. This should be set in
#     the configuration or passed explicitly.
#
# Returns
# -------
# OpenAIEmbeddings
#     The embedding function initialized with the specified model and API key.
#
# Notes
# -----
# - Ensure that the `API_KEY` environment variable is set with a valid OpenAI API key.
# - For more information on available models, refer to the OpenAI API documentation.
# """
#    embeddings: OpenAIEmbeddings = OpenAIEmbeddings(openai_api_key=os.getenv('API_KEY'), model=model)
#    return embeddings