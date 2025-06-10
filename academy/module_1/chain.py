from langchain_core.messages import HumanMessage, AIMessage
from rich import print # laat prints mooi zien in de terminal
from academy.module_0.basics import get_azure_chat_openai

messages = [AIMessage(content=f"So you said you were researching ocean mammals?", name="Model")]
messages.append(HumanMessage(content=f"Yes, that's right.", name="Lance"))
messages.append(AIMessage(content=f"Great, what would you like to learn about.", name="Model"))
messages.append(HumanMessage(content=f"I want to learn about the best place to see Orcas in the US.", name="Lance"))

llm = get_azure_chat_openai(model="o3-mini")

def part1():
    for m in messages:
        m.pretty_print()


def part2_3_4():
    result = llm.invoke(messages)
    type(result)
    print(type(result))
    print("---------------------------------------------")
    print(result)
    print("---------------------------------------------")
    print(result.response_metadata)


def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# hier wordt de tool gekoppeld .bind_tools
llm_with_tools = llm.bind_tools([multiply])

def part5_8_9():
    tool_call = llm_with_tools.invoke([HumanMessage(content=f"What is 2 multiplied by 3", name="Lance")])
    print(tool_call.tool_calls)

from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from typing import Annotated
from langgraph.graph.message import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def part12():
    # Initial state
    initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Model"),
                        HumanMessage(content="I'm looking for information on marine biology.", name="Lance")
                        ]

    # New message to add
    new_message = AIMessage(content="Sure, I can help with that. What specifically are you interested in?",
                            name="Model")

    # Test
    result = add_messages(initial_messages, new_message)
    print(result)


from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END


# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)
graph = builder.compile()

def part14_15_16():
    print(graph.get_graph().draw_ascii())
    graph.get_graph().draw_mermaid_png(output_file_path="graph_chain.png")

    messages = graph.invoke({"messages": HumanMessage(content="Hello!")})
    for m in messages['messages']:
        m.pretty_print()

    messages = graph.invoke({"messages": HumanMessage(content="Multiply 2 and 3")})
    for m in messages['messages']:
        m.pretty_print()


if __name__ == "__main__":
    teller = 4
    if teller == 1:
        part1()
    elif teller == 2:
        part2_3_4()
    elif teller == 3:
        part5_8_9()
    elif teller == 4:
        part12()
    elif teller == 5:
        part14_15_16()



