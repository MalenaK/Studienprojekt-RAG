#Config Parameters
config_model = "llama3.1"
config_embedding = "mxbai-embed-large"

#Retrieve top k chunks for a query
#One Chunk is currently 1200, context limit is around 8000 tokens
top_k_retrieval = 20
top_k_rerank = 5

TEST_FOLDER = "./tests"
TEST_RESULT_FOLDER = f"{TEST_FOLDER}/test_results"
TEST_RESULT_NOEVAL_FOLDER = f"{TEST_RESULT_FOLDER}/complex_testcases"

CHROMA_FOLDER = "./chroma"