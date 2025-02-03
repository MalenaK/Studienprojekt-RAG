"""
 infinity_reranker module
Implements a reranker using https://github.com/michaelfeil/infinity?tab=readme-ov-file#reranking.
The reranker model must be set within the module itself, see comments in infinity_reranker.py.

functions:
- __rerank: Asynchronously reranks a list of documents based on a query. Used internally should not be called outside this module.
- rerank_top_k: Returns the top-k most relevant documents according to reranker from a given list.
"""

import os, sys #To supress the info spam infinity reranker
import torch
import logging

device = "cuda" if torch.cuda.is_available() else "cpu"
if device == "cuda":
    print(f"Using GPU: {device}\nEverything is operating as expected, initializing the rest of the system...")
else:
    print(f"Warning using device: {device}\nNot using cuda will have slower performance!")


# Set the logging level to WARNING to suppress INFO and DEBUG messages else the terminal will have too much spam
logging.basicConfig(level=logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("infinity_emb").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("numexpr").setLevel(logging.WARNING)
logging.getLogger("datasets").setLevel(logging.WARNING)
logging.getLogger("torch").setLevel(logging.WARNING)

#Disable all logs optionally, not recommended!
# even from external libraries if the problem arises once again, finding the libraries that spammed was not so fun
#logging.disable(logging.WARNING)



import asyncio
from infinity_emb import AsyncEngineArray, EngineArgs, AsyncEmbeddingEngine




from langchain.schema.document import Document

#Running this script for the first time should be done in administrator mode and will take quite some time
#Due to having to download the models from huggingface

#Use GPU to speed up the process , make sure you have a compatible cuda version I have Cuda 12.4 installed
#https://developer.nvidia.com/cuda-downloads

#Setting up this server does take some time, ideally it should run in its own docker or similiar, initialization has
#Big effect on initialization of main






#for different models see https://github.com/michaelfeil/infinity?tab=readme-ov-file#reranking
#very fast but lower performance -> mixedbread-ai/mxbai-rerank-xsmall-v1
#current recommended -> BAAI/bge-reranker-base
#Depending on hardware you may also try BAAI/bge-reranker-large

#I had to modify this to not use the array it didn't work for us for some reason?
engine_args: EngineArgs = EngineArgs(model_name_or_path="BAAI/bge-reranker-base", engine="torch", device=device)
engine: AsyncEmbeddingEngine = AsyncEmbeddingEngine.from_args(engine_args)


async def __rerank(query: str, docs: [], engine: AsyncEmbeddingEngine) -> list:
    """
       Asynchronously reranks documents based on their relevance to the query. This function is used by
       rerank_top_k internally.

       Parameters
       ----------
       query: str
           The user query to base the ranking on.
       docs: list[str]
           documents to be reranked.
       engine: AsyncEmbeddingEngine
           The Infinity embedding engine used for reranking.

       Returns
       -------
       list
           A list of ranked documents with relevance scores.
       """
    async with engine:
        ranking, usage = await engine.rerank(query=query, docs=docs)
    await engine.astart()
    ranking, usage = await engine.rerank(query=query, docs=docs)
    await engine.astop()
    return ranking

def rerank_top_k(query: str, docs: list[tuple[Document, float]], k=7) -> list[tuple[Document, float]]:
    """
    Reranks documents based on relevance to a query and returns the top-k results.

    Parameters
    ----------
    query: str
        The user query to base the ranking on.
    docs: list[tuple[Document, float]]
        A list of tuples, where each tuple contains a `Document` object and its initial relevance score.
    k: int, optional
        The number of top documents to return (default is 7).

    Returns
    -------
    list[tuple[Document, float]]
        A list of the top-k most relevant documents, sorted by relevance.
    """
    doc_texts = [doc[0].page_content for doc in docs]

    reranked_docs = asyncio.run(__rerank(query, doc_texts, engine))

    #All indices sorted based on relevance
    #Here the relevance score can also be given back if needed
    reranked_indices = [ idx.index for idx in reranked_docs]

    #Sort docs list based on relevance
    reshuffled_list = [docs[i] for i in reranked_indices]
    return reshuffled_list[:k]

if __name__ == "__main__":
    print(f"OUTPUT: {rerank_top_k("", [], 1)}")
