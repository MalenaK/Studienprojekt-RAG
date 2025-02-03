# Config Parameters

# Specifies the Ollama model to be used
# Possible options include:
#   llama3.1 <-- recommended
#   deepseek-r1:14b does not support tools yet so N/A
#   deepseek-r1:7b does not support tools yet so N/A
config_model = "llama3.1"

# Specifies the embedding model to be used
# Possible options include
#   mxbai-embed-large <-- recommended
#   bge-m3
#   nomic-embed-text
config_embedding = "mxbai-embed-large"

# Number of chunks retrieved for a query
top_k_retrieval = 20
# Number of chunks after reranking
top_k_rerank = 5

# Relative path to where test results are stored
TEST_FOLDER = "./tests"
TEST_RESULT_FOLDER = f"{TEST_FOLDER}/test_results"
TEST_RESULT_NOEVAL_FOLDER = f"{TEST_RESULT_FOLDER}/complex_testcases"

# Relative path to the Chroma vector database 
CHROMA_FOLDER = "./chroma"