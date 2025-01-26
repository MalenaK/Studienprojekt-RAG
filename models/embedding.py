from langchain_community.embeddings.ollama import OllamaEmbeddings
from config.settings import config_embedding
#bge-m3
#nomic-embed-text
#mxbai-embed-large
def get_embedding_function(model:str = config_embedding):
    #llama3:70b parameter
    embeddings = OllamaEmbeddings(model=model)
    return embeddings

#def get_embedding_function(model:str = "text-embedding-3-large"):
#    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("API_KEY"), model="text-embedding-3-large")
#    return embeddings