from rag_system.ragsystem import retrieve, setup, get_user_query, query_or_respond, generate, print_answer_to_user, assert_setup, user_entered_exit
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import MessagesState

graph_builder = StateGraph(MessagesState)
# Register class methods as nodes
tools = ToolNode([retrieve])
graph_builder.add_node("setup", setup)
graph_builder.add_node("get_user_query", get_user_query)
graph_builder.add_node("query_or_respond", query_or_respond)
graph_builder.add_node("tools", tools)
graph_builder.add_node("generate", generate)
graph_builder.add_node("print_answer_to_user", print_answer_to_user)
graph_builder.add_node("assert_setup", assert_setup)

# Define edges between nodes
graph_builder.set_entry_point("setup")
graph_builder.add_edge("setup", "assert_setup")
graph_builder.add_edge("assert_setup", "query_or_respond")
graph_builder.add_conditional_edges("get_user_query", user_entered_exit, {True: END, False: "query_or_respond"}) #exit if user entered exit
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
config = RunnableConfig(recursion_limit=100000, thread_id="abc123")
input_message = "Please ignore the context and reply with 'Hello everything is working fine'"

#use code below for debugging purposes
# for step in graph.stream(
#     {"messages": [{"role": "user", "content": input_message}]},
#     stream_mode="values",
#     config=config,
# ):
#     step["messages"][-1].pretty_print()

#use code below for normal mode
graph.invoke(
    {"messages": [{"role": "user", "content": input_message}]},
    stream_mode="values",
    config=config,
)