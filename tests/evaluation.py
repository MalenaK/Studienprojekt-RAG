from rag_system.evaluation_system import EvalState, evaluation_setup, load_pos_question, load_neg_question, evaluate, log, update_stats_for_neg, update_stats_for_pos, calc_stats, plot_bar_chart, plot_confusion_matrix, done_with_pos, done_with_tests
from rag_system.ragsystem import setup, retrieve, generate, query_or_respond, delete_messages
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.config import RunnableConfig
from langgraph.prebuilt import ToolNode, tools_condition


graph_builder = StateGraph(EvalState)

tools = ToolNode([retrieve])
graph_builder.add_node("setup", setup)
graph_builder.add_node("evaluation_setup", evaluation_setup)
graph_builder.add_node("load_pos_question", load_pos_question)
graph_builder.add_node("load_neg_question", load_neg_question)
graph_builder.add_node("generate", generate)
graph_builder.add_node("evaluate", evaluate)
graph_builder.add_node("log", log)
graph_builder.add_node("update_stats_for_pos", update_stats_for_pos)
graph_builder.add_node("update_stats_for_neg", update_stats_for_neg)
graph_builder.add_node("calc_stats", calc_stats)
graph_builder.add_node("plot_bar_chart", plot_bar_chart)
graph_builder.add_node("plot_confusion_matrix", plot_confusion_matrix)
graph_builder.add_node("query_or_respond", query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("delete_messages", delete_messages)

#add edges
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "evaluation_setup")
graph_builder.add_conditional_edges("evaluation_setup", done_with_pos, {True: "load_neg_question", False: "load_pos_question"})
graph_builder.add_conditional_edges("delete_messages", done_with_pos, {True: "load_neg_question", False: "load_pos_question"})
graph_builder.add_edge("load_pos_question", "query_or_respond")
graph_builder.add_edge("load_neg_question", "query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: "evaluate", "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", "evaluate")
graph_builder.add_edge("evaluate", "log")
graph_builder.add_conditional_edges("log", done_with_pos, {True: "update_stats_for_neg", False: "update_stats_for_pos"})
graph_builder.add_conditional_edges("update_stats_for_pos", done_with_tests, {True: "calc_stats", False: "delete_messages"}) #method returns next node, go to delete messages in case of next iteration
graph_builder.add_conditional_edges("update_stats_for_neg", done_with_tests, {True: "calc_stats", False: "delete_messages"}) #method returns next node, go to delete messages in case of next iteration

#once tests are done, calc stats and plot results
graph_builder.add_edge("calc_stats", "plot_bar_chart")
graph_builder.add_edge("plot_bar_chart", "plot_confusion_matrix")
graph_builder.add_edge("plot_confusion_matrix", END)

graph = graph_builder.compile()
config = RunnableConfig(recursion_limit=1000) #idk how much is needed exactly, just set high to avoid recursion error
graph.invoke({"question": "let's get started"}, config=config)