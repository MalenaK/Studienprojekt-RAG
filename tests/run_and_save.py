from rag_system.rag_run_save_system import RAGRunSavePipeline, RunAndSaveState
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.config import RunnableConfig

pipeline = RAGRunSavePipeline()

graph_builder = StateGraph(RunAndSaveState)
# Register class methods as nodes
graph_builder.add_node("setup", pipeline.setup)
graph_builder.add_node("run_and_save_setup", pipeline.run_and_save_setup)
graph_builder.add_node("load_question", pipeline.load_question)
graph_builder.add_node("retrieve", pipeline.retrieve)
graph_builder.add_node("generate", pipeline.generate)
graph_builder.add_node("log", pipeline.log)

#add edges
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "run_and_save_setup")
graph_builder.add_edge("run_and_save_setup", "load_question")
graph_builder.add_edge("load_question", "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", "log")
graph_builder.add_conditional_edges("log", pipeline.all_tests_done, {True: END, False: "load_question"}) #end or load next question

graph = graph_builder.compile()
config = RunnableConfig(recursion_limit=100)
graph.invoke(input={"question": "Let's get started"}, config=config)