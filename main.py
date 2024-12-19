from ragsystem import RAGpipeline, State
from langgraph.graph import START, StateGraph
pipeline = RAGpipeline()

graph_builder = StateGraph(State)
# Register class methods as nodes
graph_builder.add_node("setup", pipeline.setup)
graph_builder.add_node("retrieve", pipeline.retrieve)
graph_builder.add_node("generate", pipeline.generate)

# Define edges between nodes
graph_builder.add_edge(START, "setup")
graph_builder.add_edge("setup", "retrieve")
graph_builder.add_edge("retrieve", "generate")

#build graph
graph = graph_builder.compile()

result = graph.invoke({"question": "What is Task Decomposition?"})

print(f'Context: {result["context"]}\n\n')
print(f'Answer: {result["answer"]}')