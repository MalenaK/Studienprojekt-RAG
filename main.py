from rag_system.ragsystem import RAGpipeline, retrieve
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import MessagesState


pipeline = RAGpipeline()

graph_builder = StateGraph(MessagesState)
# Register class methods as nodes
tools = ToolNode([retrieve])
graph_builder.add_node("setup", pipeline.setup)
graph_builder.add_node("get_user_query", pipeline.get_user_query)
graph_builder.add_node("query_or_respond", pipeline.query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("generate", pipeline.generate)
graph_builder.add_node("print_answer_to_user", pipeline.print_answer_to_user)
graph_builder.add_node("assert_setup", pipeline.assert_setup)

# Define edges between nodes
graph_builder.set_entry_point("setup")
graph_builder.add_edge("setup", "assert_setup")
graph_builder.add_edge("assert_setup", "query_or_respond")
graph_builder.add_conditional_edges("get_user_query", pipeline.user_entered_exit, {True: END, False: "query_or_respond"}) #exit if user entered exit
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: "print_answer_to_user", "tools": "tools"},
)
#graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", "print_answer_to_user")
graph_builder.add_edge("print_answer_to_user", "get_user_query") #next query (loop)

#build graph
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Execute the graph starting from the START node
#graph.invoke({"question": "Please ignore the context and reply with 'Hello everything is working fine'"} )
config = RunnableConfig(recursion_limit=100000, thread_id="abc123")
input_message = "Please ignore the context and reply with 'Hello everything is working fine'"

# graph.invoke(
#     {"messages": [{"role": "user", "content": input_message}]},
#     stream_mode="values",
#     config=config,
# )
for step in graph.stream(
    {"messages": [{"role": "user", "content": input_message}]},
    stream_mode="values",
    config=config,
):
    step["messages"][-1].pretty_print()