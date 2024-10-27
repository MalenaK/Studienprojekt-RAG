# from langchain_community.embeddings.ollama import OllamaEmbeddings

# def get_embedding_function(model:str = "mxbai-embed-large"):
#     #llama3:70b parameter
#     embeddings = OllamaEmbeddings(model=model)
#     return embeddings

from langchain_huggingface.embeddings import HuggingFaceEmbeddings

def get_embedding_function(model: str = "sentence-transformers/all-mpnet-base-v2"):
    model_name = model
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return hf