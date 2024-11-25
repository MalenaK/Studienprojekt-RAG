#refer to https://github.com/michaelfeil/infinity?tab=readme-ov-file#reranking

import asyncio
from infinity_emb import AsyncEngineArray, EngineArgs, AsyncEmbeddingEngine
import torch

from langchain.schema.document import Document

#Running this script for the first time should be done in administrator mode and will take quite some time
#Due to having to download the models from huggingface

#Use GPU to speed up the process , make sure you have a compatible cuda version I have Cuda 12.4 installed
#https://developer.nvidia.com/cuda-downloads

#Setting up this server does take some time, ideally it should run in its own docker or similiar, initialization has
#Big effect on initialization of main

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


#for different models see https://github.com/michaelfeil/infinity?tab=readme-ov-file#reranking
#very fast but lower performance -> mixedbread-ai/mxbai-rerank-xsmall-v1
#current -> BAAI/bge-reranker-base

#I had to modify this to not use the array it didn't work for us for some reason
engine_args = EngineArgs(model_name_or_path="BAAI/bge-reranker-base", engine="torch", device=device)
engine = AsyncEmbeddingEngine.from_args(engine_args)

async def __rerank(query: str, docs: [], engine: AsyncEmbeddingEngine):

    async with engine:
        ranking, usage = await engine.rerank(query=query, docs=docs)
        print(list(zip(ranking, docs)))
    await engine.astart()
    ranking, usage = await engine.rerank(query=query, docs=docs)
    await engine.astop()
    return ranking

def rerank_top_k(query: str, docs: list[tuple[Document, float]], k=7):
    
    reranked_docs = asyncio.run(__rerank(query, docs, engine))
    #All indices sorted based on relevance
    #Here the relevance score can also be given back if needed
    reranked_indices = [ i.index for i in reranked_docs]

    #print(f"a: {reranked_docs[0]}\n Type: {type(reranked_docs)}")
    #print(reranked_indices)

    return reranked_indices

    #reshuffle docs
    #reshuffled_list = list(map(lambda i: docs[i], reranked_indices))
    #print(reshuffled_list)

    #return reshuffled_list[:k]

if __name__ == "__main__":
    print(f"OUTPUT: {rerank_top_k("", [], 1)}")
