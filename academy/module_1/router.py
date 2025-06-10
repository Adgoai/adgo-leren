from academy.module_0.basics import get_azure_chat_openai
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.messages import HumanMessage


llm = get_azure_chat_openai(model="o3-mini")

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

llm_with_tools = llm.bind_tools([multiply])

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

# View
print(graph.get_graph().draw_ascii())
graph.get_graph().draw_mermaid_png(output_file_path="graph_router.png")


if __name__ == "__main__":
    # Example usage
    messages = [HumanMessage(content="Hello, what is 2 multiplied by 12,3?")]
    messages = graph.invoke({"messages": messages})
    for m in messages['messages']:
        m.pretty_print()
    messages = [HumanMessage(content="Hello, Wat is de hoofdstad van Nederland?")]
    messages = graph.invoke({"messages": messages})
    for m in messages['messages']:
        m.pretty_print()