from rag_system.rag_run_save_system import RunAndSaveState, run_and_save_setup, load_question, log, all_tests_done
from rag_system.ragsystem import setup, retrieve, generate, query_or_respond, delete_messages
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.config import RunnableConfig
from langgraph.prebuilt import ToolNode, tools_condition


graph_builder = StateGraph(RunAndSaveState)

tools = ToolNode([retrieve])
# Register class methods as nodes
graph_builder.add_node("setup", setup)
graph_builder.add_node("run_and_save_setup", run_and_save_setup)
graph_builder.add_node("load_question", load_question)
graph_builder.add_node("generate", generate)
graph_builder.add_node("log", log)
graph_builder.add_node("query_or_respond", query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("delete_messages", delete_messages)


#add edges
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "run_and_save_setup")
graph_builder.add_edge("run_and_save_setup", "load_question")
graph_builder.add_edge("delete_messages", "load_question")
graph_builder.add_edge("load_question", "query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: "log", "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", "log")
graph_builder.add_conditional_edges("log", all_tests_done, {True: END, False: "delete_messages"}) #end or load next question

graph = graph_builder.compile()
config = RunnableConfig(recursion_limit=100)
graph.invoke(input={"question": "Let's get started"}, config=config)