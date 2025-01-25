#Config Parameters
#possible options include
#llama3.1 <-- recommended
#deepseek-r1:14b does not support tools yet so N/A
#deepseek-r1:7b does not support tools yet so N/A
config_model = "llama3.1"

#possible options include
#bge-m3
#nomic-embed-text
#mxbai-embed-large <-- recommended
config_embedding = "mxbai-embed-large"

#Retrieve top k chunks for a query
#One Chunk is currently 1200, context limit is around 8000 tokens
top_k_retrieval = 20
top_k_rerank = 5

TEST_FOLDER = "./tests"
TEST_RESULT_FOLDER = f"{TEST_FOLDER}/test_results"
TEST_RESULT_NOEVAL_FOLDER = f"{TEST_RESULT_FOLDER}/complex_testcases"

CHROMA_FOLDER = "./chroma"