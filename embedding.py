from langchain_community.embeddings.ollama import OllamaEmbeddings

def get_embedding_function(model:str = "llama3"):
    #llama3:70b parameter
    embeddings = OllamaEmbeddings(model=model)
    return embeddings