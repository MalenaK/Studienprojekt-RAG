from rag_system.evaluation_system import EvalState, RAGEvalPipeline
from langgraph.graph import START, END, StateGraph
from tests.test_cases import positive_test_cases, negative_test_cases
from langchain_core.runnables.config import RunnableConfig


pipeline = RAGEvalPipeline(positive_test_cases=positive_test_cases, negative_test_cases=negative_test_cases)

graph_builder = StateGraph(EvalState)

graph_builder.add_node("setup", pipeline.setup)
graph_builder.add_node("evaluation_setup", pipeline.evaluation_setup)
graph_builder.add_node("load_pos_question", pipeline.load_pos_question)
graph_builder.add_node("load_neg_question", pipeline.load_neg_question)
graph_builder.add_node("retrieve", pipeline.retrieve)
graph_builder.add_node("generate", pipeline.generate)
graph_builder.add_node("evaluate", pipeline.evaluate)
graph_builder.add_node("log", pipeline.log)
graph_builder.add_node("update_stats_for_pos", pipeline.update_stats_for_pos)
graph_builder.add_node("update_stats_for_neg", pipeline.update_stats_for_neg)
graph_builder.add_node("calc_stats", pipeline.calc_stats)
graph_builder.add_node("plot_bar_chart", pipeline.plot_bar_chart)
graph_builder.add_node("plot_confusion_matrix", pipeline.plot_confusion_matrix)

graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "evaluation_setup")
graph_builder.add_conditional_edges("evaluation_setup", pipeline.done_with_pos, {True: "load_neg_question", False: "load_pos_question"})
graph_builder.add_edge("load_pos_question", "retrieve")
graph_builder.add_edge("load_neg_question", "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", "evaluate")
graph_builder.add_edge("evaluate", "log")
graph_builder.add_conditional_edges("log", pipeline.done_with_pos, {True: "update_stats_for_neg", False: "update_stats_for_pos"})
graph_builder.add_conditional_edges("update_stats_for_pos", pipeline.start_next_iteration_or_end) #method returns next node
graph_builder.add_conditional_edges("update_stats_for_neg", pipeline.start_next_iteration_or_end) #method returns next node
graph_builder.add_edge("calc_stats", "plot_bar_chart")
graph_builder.add_edge("plot_bar_chart", "plot_confusion_matrix")
graph_builder.add_edge("plot_confusion_matrix", END)

graph = graph_builder.compile()
config = RunnableConfig(recursion_limit=1000) #idk how much is needed exactly, just set high to avoid recursion error
graph.invoke({"question": "let's get started"}, config=config)