#Config Parameters
config_model = "llama3"
config_embedding = "mxbai-embed-large"

#Retrieve top k chunks for a query
#One Chunk is currently 1200, context limit is around 8000 tokens
top_k_retrieval = 20
# unused?
top_k_rerank = 5