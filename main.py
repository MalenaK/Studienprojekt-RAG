from rag_system.ragsystem import RAGpipeline, State
from langgraph.graph import START, END, StateGraph
pipeline = RAGpipeline()

graph_builder = StateGraph(State)
# Register class methods as nodes
graph_builder.add_node("setup", pipeline.setup)
graph_builder.add_node("get_user_query", pipeline.get_user_query)
graph_builder.add_node("retrieve", pipeline.retrieve)
graph_builder.add_node("generate", pipeline.generate)
graph_builder.add_node("assert_setup", pipeline.assert_setup)

# Define edges between nodes
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "assert_setup")
graph_builder.add_edge("assert_setup", "retrieve")
graph_builder.add_conditional_edges("get_user_query", pipeline.user_entered_exit, {True: END, False: "retrieve"}) #exit if user entered exit
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", "get_user_query") #next query (loop)

#build graph
graph = graph_builder.compile()

# Execute the graph starting from the START node
#state = State()
graph.invoke({"question": "Please ignore the context and reply with 'Hello everything is working fine'"} )