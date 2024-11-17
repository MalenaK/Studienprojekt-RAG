# from langchain_community.embeddings.ollama import OllamaEmbeddings

# def get_embedding_function(model:str = "mxbai-embed-large"):
#     #llama3:70b parameter
#     embeddings = OllamaEmbeddings(model=model)
#     return embeddings

#from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# def get_embedding_function(model: str = "dunzhang/stella_en_1.5B_v5"):
#     model_name = model
#     model_kwargs = {'device': 'cpu'}
#     encode_kwargs = {'normalize_embeddings': True}
#     hf = HuggingFaceEmbeddings(
#         model_name=model_name,
#         model_kwargs=model_kwargs,
#         encode_kwargs=encode_kwargs
#     )
#     return hf


# from langchain.embeddings.base import Embeddings
# from sentence_transformers import SentenceTransformer
# from typing import List

# class SentenceTransformerEmbeddings(Embeddings):
#     def __init__(self, model_name: str):
#         self.model = SentenceTransformer(model_name, trust_remote_code=True).cuda()

#     def embed_documents(self, documents: List[str]) -> List[List[float]]:
#         return self.model.encode(documents)

#     def embed_query(self, query: str) -> List[float]:
#         return self.model.encode([query])[0]

from langchain.embeddings.base import Embeddings
from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

class SentenceTransformerEmbeddings(Embeddings):
    def __init__(self, model_name: str, use_gpu: bool = True):
        """
        Initialize the embedding model.

        Args:
            model_name (str): Name of the SentenceTransformer model.
            use_gpu (bool): Whether to use GPU if available.
        """
        #device = "cuda" if use_gpu and SentenceTransformer._has_cuda() else "cpu"
        self.model = SentenceTransformer(model_name, trust_remote_code=True).cuda()
        # self.model = SentenceTransformer(
        #     model_name,
        #     trust_remote_code=True,
        #     device="cpu",
        #     #config_kwargs={"use_memory_efficient_attention": False, "unpad_inputs": False}
        # )

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            documents (List[str]): List of text documents to embed.

        Returns:
            List[List[float]]: List of embeddings for each document.
        """
        if not documents:
            raise ValueError("The input document list is empty.")
        embeddings = self.model.encode(documents, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query.

        Args:
            query (str): Query string to embed.

        Returns:
            List[float]: Embedding for the query.
        """
        if not query:
            raise ValueError("The input query is empty.")
        embedding = self.model.encode([query], normalize_embeddings=True)[0]
        return embedding.tolist()
