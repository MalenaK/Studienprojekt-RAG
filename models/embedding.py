from langchain_community.embeddings.ollama import OllamaEmbeddings
from config.settings import config_embedding
#bge-m3
#nomic-embed-text
#mxbai-embed-large
def get_embedding_function(model:str = config_embedding):
    #llama3:70b parameter
    embeddings = OllamaEmbeddings(model=model)
    return embeddings