from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function(model:str = "mxbai-embed-large"):
    #llama3:70b parameter
    embeddings = OllamaEmbeddings(model=model)
    return embeddings