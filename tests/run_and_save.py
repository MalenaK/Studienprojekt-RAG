"""
Automated Test Execution and Logging for the RAG System

This script sets up and runs an automated process for executing and logging test cases.
It uses LangGraph to construct a state-based workflow. 

Usage:
    Set correct test cases in rag_run_save_system.py, then
    python -m test.run_and_save -d [directory to data]
"""

# Import required modules
from rag_system.rag_run_save_system import RunAndSaveState, run_and_save_setup, load_question, log, all_tests_done
from rag_system.ragsystem import setup, retrieve, generate, query_or_respond, delete_messages
from langgraph.graph import START, END, StateGraph
from langchain_core.runnables.config import RunnableConfig
from langgraph.prebuilt import ToolNode, tools_condition

# Create a state graph for managing the test execution workflow
graph_builder = StateGraph(RunAndSaveState)

# Add retrieve as an available tool 
tools = ToolNode([retrieve])

# Add nodes to the graph (each node represents a processing step), second parameter is a method
graph_builder.add_node("setup", setup)
graph_builder.add_node("run_and_save_setup", run_and_save_setup)
graph_builder.add_node("load_question", load_question)
graph_builder.add_node("generate", generate)
graph_builder.add_node("log", log)
graph_builder.add_node("query_or_respond", query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("delete_messages", delete_messages)


# Define transitions between nodes
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "run_and_save_setup")
graph_builder.add_edge("run_and_save_setup", "load_question")
graph_builder.add_edge("delete_messages", "load_question")

# Query processing
graph_builder.add_edge("load_question", "query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: "log", "tools": "tools"}, # Decide whether to use tools or log directly
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", "log")

# Logging and deciding whether to continue testing
graph_builder.add_conditional_edges("log", all_tests_done, {True: END, False: "delete_messages"})

# Compile the graph
graph = graph_builder.compile()

# Configure execution settings
config = RunnableConfig(recursion_limit=100)

# Run the test execution process
graph.invoke(input={"question": "Let's get started"}, config=config)