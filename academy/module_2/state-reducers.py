from typing_extensions import TypedDict
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from rich import print

def default_overwriting():
    class State(TypedDict):
        foo: int

    def node_1(state):
        print("---Node 1---")
        return {"foo": state['foo'] + 1}

    # Build graph
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    # Add
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())

    response = graph.invoke({"foo" : 1})
    print("---------------------------------------------")
    print(response)

def branching():
    class State(TypedDict):
        foo: int

    def node_1(state):
        print("---Node 1---")
        return {"foo": state['foo'] + 1}

    def node_2(state):
        print("---Node 2---")
        return {"foo": state['foo'] + 1}

    def node_3(state):
        print("---Node 3---")
        return {"foo": state['foo'] + 1}

    # Build graph
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    # Add
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())

    from langgraph.errors import InvalidUpdateError
    try:
        response = graph.invoke({"foo": 1})
        print("---------------------------------------------")
        print(response)
    except InvalidUpdateError as e:
        print(f"InvalidUpdateError occurred: {e}")

from operator import add
from typing import Annotated

def Reducers():

    class State(TypedDict):
        foo: Annotated[list[int], add]

    def node_1(state):
        print("---Node 1---")
        return {"foo": [state['foo'][0] + 1]}

    # Build graph
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    # Add
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())

    response = graph.invoke({"foo": [1]})
    print("---------------------------------------------")
    print(response)

def reducers_branch():
    class State(TypedDict):
        foo: Annotated[list[int], add]
    def node_1(state):
        print("---Node 1---")
        return {"foo": [state['foo'][-1] + 1]}

    def node_2(state):
        print("---Node 2---")
        return {"foo": [state['foo'][-1] + 1]}

    def node_3(state):
        print("---Node 3---")
        return {"foo": [state['foo'][-1] + 1]}

    # Build graph
    builder = StateGraph(State)
    builder.add_node("node_1", node_1)
    builder.add_node("node_2", node_2)
    builder.add_node("node_3", node_3)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", "node_2")
    builder.add_edge("node_1", "node_3")
    builder.add_edge("node_2", END)
    builder.add_edge("node_3", END)

    # Add
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())
    response = graph.invoke({"foo": [1]})
    print("---------------------------------------------")
    print(response)

    print("---------------------------------------------")
    print("Testing with None value:")
    try:
        graph.invoke({"foo": None})
    except TypeError as e:
        print(f"TypeError occurred: {e}")

def custom_reducer():
    def reduce_list(left: list | None, right: list | None) -> list:
        """Safely combine two lists, handling cases where either or both inputs might be None.

        Args:
            left (list | None): The first list to combine, or None.
            right (list | None): The second list to combine, or None.

        Returns:
            list: A new list containing all elements from both input lists.
                   If an input is None, it's treated as an empty list.
        """
        if not left:
            left = []
        if not right:
            right = []
        return left + right

    class DefaultState(TypedDict):
        foo: Annotated[list[int], add]

    class CustomReducerState(TypedDict):
        foo: Annotated[list[int], reduce_list]

    def node_1(state):
        print("---Node 1---")
        return {"foo": [2]}

    # Build graph
    builder = StateGraph(DefaultState)
    builder.add_node("node_1", node_1)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    # Add
    graph = builder.compile()
    print(graph.get_graph().draw_ascii())

    try:
        print(graph.invoke({"foo": None}))
    except TypeError as e:
        print(f"TypeError occurred: {e}")

    print("---------------------------------------------")

    print("Testing with custom reducer:")

    builder = StateGraph(CustomReducerState)
    builder.add_node("node_1", node_1)

    # Logic
    builder.add_edge(START, "node_1")
    builder.add_edge("node_1", END)

    # Add
    graph = builder.compile()

    # View
    display(Image(graph.get_graph().draw_mermaid_png()))

    try:
        print(graph.invoke({"foo": None}))
    except TypeError as e:
        print(f"TypeError occurred: {e}")


from typing import Annotated
from langgraph.graph import MessagesState
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, RemoveMessage
from langgraph.graph.message import add_messages

def messages():
    # Define a custom TypedDict that includes a list of messages with add_messages reducer
    class CustomMessagesState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]
        added_key_1: str
        added_key_2: str
        # etc

    # Use MessagesState, which includes the messages key with add_messages reducer
    class ExtendedMessagesState(MessagesState):
        # Add any keys needed beyond messages, which is pre-built
        added_key_1: str
        added_key_2: str
        # etc

    # Initial state
    initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Model"),
                        HumanMessage(content="I'm looking for information on marine biology.", name="Lance")
                        ]

    # New message to add
    new_message = AIMessage(content="Sure, I can help with that. What specifically are you interested in?",
                            name="Model")

    # Test
    add_messages(initial_messages, new_message)
    print("---------------------------------------------")
    print("Initial messages:", initial_messages)

    # Initial state
    initial_messages = [AIMessage(content="Hello! How can I assist you?", name="Model", id="1"),
                        HumanMessage(content="I'm looking for information on marine biology.", name="Lance", id="2")
                        ]

    # New message to add
    new_message = HumanMessage(content="I'm looking for information on whales, specifically", name="Lance", id="2")

    # Test
    add_messages(initial_messages, new_message)
    print("---------------------------------------------")
    print("Initial messages with IDs:", initial_messages)

    # Message list
    messages = [AIMessage("Hi.", name="Bot", id="1")]
    messages.append(HumanMessage("Hi.", name="Lance", id="2"))
    messages.append(AIMessage("So you said you were researching ocean mammals?", name="Bot", id="3"))
    messages.append(
        HumanMessage("Yes, I know about whales. But what others should I learn about?", name="Lance", id="4"))

    # Isolate messages to delete
    delete_messages = [RemoveMessage(id=m.id) for m in messages[:-2]]
    print("---------------------------------------------")
    print("Messages to be deleted:", delete_messages)
    print("---------------------------------------------")
    print("Messages before deletion:", messages)

    add_messages(messages, delete_messages)
    print("---------------------------------------------")
    print("Messages after deletion:", messages)


if __name__ == "__main__":
    teller = 6
    if teller == 1:
        default_overwriting()
    elif teller == 2:
        branching()
    elif teller == 3:
        Reducers()
    elif teller == 4:
        reducers_branch()
    elif teller == 5:
        custom_reducer()
    elif teller == 6:
        messages()
